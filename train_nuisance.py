"""Train nuisance-aware AdaptCLIP with retrieved train-only normal references.

Collapse fix (docs/results.md §2b.4), all opt-in so v0 / ablation runs stay reproducible:
  --bg-target normal   background cells target the normal anchor only
  --bg-target pseudo   background cells target the normal anchor unless frozen-CLIP zero-shot (hand prompts, projected
                       patch tokens, 4-layer mean) assigns a nuisance anchor with probability >= --pseudo-conf
  --freeze-nuisance    nuisance anchors use the hand-prompt embeddings (no learnable context); only normal/defect anchors learn
  --prior hand         L_prior pulls learned anchors toward the hand-prompt embeddings instead of the random-context init
"""
import argparse,csv,json,random,os
from pathlib import Path
import numpy as np
from PIL import Image
import torch
from torch import nn
from torch.nn import functional as F
from torch.utils.data import Dataset,DataLoader,WeightedRandomSampler
import adaptcliplib
from adaptcliplib.adaptclip import tokenize
from nuisance_model import NuisanceHead,explanation_loss,NuisanceHeadV2,explanation_loss_v2,ortho_loss
from tools import get_transform,setup_seed
from tqdm import tqdm

NAMES=['intact concrete surface','crack on concrete','rust stain on concrete','spalling on concrete','efflorescence on concrete','damaged concrete surface','water stain on concrete','shadow on concrete','moss on concrete','patch repair on concrete','graffiti on concrete','formwork texture on concrete','dirt on concrete']
# Anchor sets: 'full' = 13 anchors; 'no-nuisance' drops the seven nuisance anchors (aggregate form of prediction P2);
# 'v2' drops graffiti (absent from CODEBRIM) -> 12 anchors.
ANCHOR_SETS={'full':NAMES,'no-nuisance':NAMES[:6],'v2':[n for n in NAMES if not n.startswith('graffiti')]}
TEMPLATES=['a photo of {}','a close-up photo of {} on a bridge','{} on a concrete wall','an inspection image showing {}']
CLASSES=['Crack','Corrosion','Spalling','Efflorescence']
N_FIXED=6  # anchors 0..5 (normal, 4 defect types, generic defect) always learn; 6.. are nuisances

def alternatives(i,name):
 return [name,'exposed corroded rebar'] if i==2 else [name]

class Anchors(nn.Module):
 def __init__(self,clip,names=NAMES,freeze_nuisance=False):
  super().__init__(); self.names=list(names); n=len(self.names); self.freeze_nuisance=freeze_nuisance; self.ctx=nn.Parameter(torch.randn(n,12,768)*.02)
  texts=[]; groups=[]; plain=[]; plain_groups=[]
  for i,name in enumerate(self.names):
   for alternative in alternatives(i,name):
    for template in TEMPLATES:
     texts.append(' '.join(['X']*12)+' '+template.format(alternative)+'.'); groups.append(i)
     plain.append(template.format(alternative)+'.'); plain_groups.append(i)
  device=next(clip.parameters()).device
  ids=tokenize(texts); emb=clip.token_embedding(ids.to(device)).detach()
  self.register_buffer('ids',ids); self.register_buffer('prefix',emb[:,:1]); self.register_buffer('suffix',emb[:,13:]); self.register_buffer('groups',torch.tensor(groups))
  # Hand-prompt embeddings (template ensemble, no learnable context): used as frozen nuisance anchors, L_prior target and zero-shot pseudo-labeller.
  with torch.no_grad():
   h=F.normalize(clip.encode_text(tokenize(plain).to(device)).float(),dim=-1); pg=torch.tensor(plain_groups,device=device)
   hand=F.normalize(torch.stack([h[pg==i].mean(0) for i in range(n)]),dim=-1)
  self.register_buffer('hand',hand,persistent=False)  # recomputed at load time, so old checkpoints still load
 def forward(self,clip):
  context=self.ctx[self.groups]; inp=torch.cat([self.prefix,context.to(self.prefix.dtype),self.suffix],1)
  f=clip.encode_text_learn(inp,self.ids).float(); f=F.normalize(f,dim=-1)
  learned=F.normalize(torch.stack([f[self.groups==i].mean(0) for i in range(len(self.names))]),dim=-1)
  if self.freeze_nuisance and len(self.names)>N_FIXED: learned=torch.cat([learned[:N_FIXED],self.hand[N_FIXED:]],0)
  return learned

class AnchorsV2(nn.Module):
 """Symmetric, norm-bounded anchors: t_a = normalize(hand_a + eps * delta_a / max(1, |delta_a|)).
 Every anchor (normal, defects, nuisances) gets the same freedom; cos(t_a, hand_a) >= 1/sqrt(1+eps^2) (0.894 at eps=0.5).
 No text-encoder forward per step."""
 def __init__(self,clip,names,eps=.5):
  super().__init__(); self.names=list(names); self.eps=eps
  base=Anchors(clip,names); self.register_buffer('hand',base.hand.clone()); del base
  self.delta=nn.Parameter(torch.zeros(len(self.names),self.hand.shape[1]))
 def forward(self,clip=None):
  d=self.delta; d=d/d.norm(dim=-1,keepdim=True).clamp_min(1.)
  return F.normalize(self.hand+self.eps*d,dim=-1)

class Bridge(Dataset):
 def __init__(self,root,split,transform):
  self.root=Path(root)/split; self.transform=transform
  with (Path(root)/(split+'_manifest.csv')).open() as f:self.rows=list(csv.DictReader(f))
 def __len__(self):return len(self.rows)
 def __getitem__(self,i):
  r=self.rows[i]; im=self.transform(Image.open(self.root/r['image_path']).convert('RGB')); masks=[]
  for c in CLASSES:
   p=self.root/'multiclass_annotations'/'masks'/(r['sample']+'__'+c+'.png')
   masks.append(torch.from_numpy((np.asarray(Image.open(p).convert('L').resize((518,518),Image.Resampling.NEAREST))>0).copy()).float() if r['category']=='annotated' else torch.zeros(518,518))
  return im,torch.stack(masks),int(r['category']=='annotated'),r['parent_id'],i

def binary_loss(p,y):
 p=p.clamp(1e-6,1-1e-6); focal=-(y*(1-p)**2*p.log()+(1-y)*p**2*(1-p).log()).mean(); dice=1-(2*(p*y).sum()+1)/(p.sum()+y.sum()+1); return focal+dice

@torch.no_grad()
def zero_shot_sims(q,clip,cand):
 """4-layer mean cosine between projected patch tokens and candidate text embeddings. q: list of [1,N,1024]; cand [k,768] -> [N,k]."""
 return torch.stack([F.normalize((t[0].to(clip.visual.proj.dtype)@clip.visual.proj).float(),dim=-1)@cand.T for t in q]).mean(0)

@torch.no_grad()
def pseudo_background(q,clip,hand,conf,bias=None,grid=37,scale=100.):
 """Zero-shot background target per cell: 0 (normal) or a nuisance anchor index >= N_FIXED.
 Raw CLIP similarities carry a strong class bias ('dirt' wins ~55% of normal cells at conf 0.6), so `bias` (per-class mean
 similarity over training-normal cells) is subtracted before the softmax; with centering, conf 0.5 fires on ~8% of cells.
 Returns (target [1,grid,grid] long, probs [N,k])."""
 idx=torch.tensor([0]+list(range(N_FIXED,hand.shape[0])),device=hand.device); cand=hand[idx]
 sims=zero_shot_sims(q,clip,cand)
 if bias is not None: sims=sims-bias
 prob=(scale*sims).softmax(-1); best=prob.argmax(-1); p=prob.gather(1,best[:,None])[:,0]
 target=torch.where((best>0)&(p>=conf),idx[best],torch.zeros_like(best))
 return target.view(1,grid,grid),prob

@torch.no_grad()
def zero_shot_grid(q,clip,hand,bias=None,grid=37,scale=100.):
 """Centered zero-shot distribution over [normal + nuisances] for every cell -> [1,k,grid,grid]."""
 idx=torch.tensor([0]+list(range(N_FIXED,hand.shape[0])),device=hand.device); sims=zero_shot_sims(q,clip,hand[idx])
 if bias is not None: sims=sims-bias
 return (scale*sims).softmax(-1).T.reshape(1,len(idx),grid,grid)

@torch.no_grad()
def zero_shot_bias(clip,hand,train,normal,transform,device,n=200,seed=0):
 """Per-class mean zero-shot similarity over cells of n random training normals (class-prior correction)."""
 idx=torch.tensor([0]+list(range(N_FIXED,hand.shape[0])),device=hand.device); cand=hand[idx]; acc=torch.zeros(len(idx),device=device); cnt=0
 rng=random.Random(seed)
 for r in tqdm(rng.sample(normal,min(n,len(normal))),desc='zero-shot bias'):
  x=transform(Image.open(train.root/r['image_path']).convert('RGB')).unsqueeze(0).to(device); _,q=clip.encode_image(x,[6,12,18,24],proj_use=False,DPAM_layer=20)
  s=zero_shot_sims([t[:,1:] for t in q],clip,cand); acc+=s.sum(0); cnt+=s.shape[0]
 return acc/cnt

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--data',default='/home/skye/data/Skye/databases/Bridge512_balance_CODEBRIM'); ap.add_argument('--out',default='runs/nuisance-v0'); ap.add_argument('--epochs',type=int,default=20); ap.add_argument('--seed',type=int,default=10)
 ap.add_argument('--anchor-set',choices=sorted(ANCHOR_SETS),default='full'); ap.add_argument('--bank',default=None,help='cached normal global vectors; default <out>/normal_globals.pt')
 ap.add_argument('--bg-target',choices=['loose','normal','pseudo'],default='loose'); ap.add_argument('--pseudo-conf',type=float,default=.5); ap.add_argument('--no-pseudo-center',action='store_true',help='disable class-prior centering of zero-shot similarities'); ap.add_argument('--freeze-nuisance',action='store_true'); ap.add_argument('--prior',choices=['init','hand'],default='init')
 ap.add_argument('--max-steps',type=int,default=0,help='smoke test: stop each epoch after this many steps')
 ap.add_argument('--arch',choices=['v0','v2'],default='v0'); ap.add_argument('--eps',type=float,default=.5); ap.add_argument('--tau-res',type=float,default=.25); ap.add_argument('--beta',type=float,default=.5); ap.add_argument('--lambda-ortho',type=float,default=.1); ap.add_argument('--lambda-type',type=float,default=1.); ap.add_argument('--res-warmup',type=int,default=2,help='epochs before the residual condition of the stratified target is enabled'); ap.add_argument('--res-cap',type=float,default=.3)
 args=ap.parse_args()
 if args.arch=='v2' and args.bg_target=='loose': args.bg_target='pseudo'   # v2 always uses the stratified target with centered zero-shot
 names=ANCHOR_SETS[args.anchor_set]; config=dict(vars(args),anchors=names)
 setup_seed(args.seed); out=Path(args.out); out.mkdir(parents=True,exist_ok=True); (out/'config.json').write_text(json.dumps(config,indent=2))
 device='cuda'; clip,_=adaptcliplib.load('ViT-L/14@336px',device=device); clip.visual.DAPM_replace(DPAM_layer=20); clip.eval()
 for p in clip.parameters():p.requires_grad_(False)
 transform,_=get_transform(518); train=Bridge(args.data,'train',transform); normal=[r for r in train.rows if r['category']=='normal']
 # Cached global vectors for retrieval; only selected training normals enter the bank.
 cache=Path(args.bank) if args.bank else out/'normal_globals.pt'
 if cache.exists(): bank=torch.load(cache,map_location=device,weights_only=True)
 else:
  bank=[]
  for r in tqdm(normal,desc='normal bank'):
   x=transform(Image.open(train.root/r['image_path']).convert('RGB')).unsqueeze(0).to(device)
   with torch.no_grad(): g,_=clip.encode_image(x,[6,12,18,24],proj_use=False,DPAM_layer=20)
   bank.append(F.normalize(g.float(),dim=-1).cpu())
  bank=torch.cat(bank); torch.save(bank,cache); bank=bank.to(device)
 if args.arch=='v2': head=NuisanceHeadV2(n_anchors=len(names)).to(device); anchors=AnchorsV2(clip,names,eps=args.eps).to(device)
 else: head=NuisanceHead(n_anchors=len(names)).to(device); anchors=Anchors(clip,names,freeze_nuisance=args.freeze_nuisance).to(device)
 with torch.no_grad(): prior=(anchors.hand if args.prior=='hand' else anchors(clip)).detach().clone()
 learn_rows=N_FIXED if (args.freeze_nuisance and len(names)>N_FIXED) else len(names)
 bias=None
 if args.bg_target in ('pseudo',) and not args.no_pseudo_center:
  bias=zero_shot_bias(clip,anchors.hand,train,normal,transform,device); torch.save(bias.cpu(),out/'zs_bias.pt'); print('zero-shot bias',[round(float(b),4) for b in bias],flush=True)
 visual_opt=torch.optim.AdamW(head.parameters(),lr=.001); text_opt=torch.optim.AdamW(anchors.parameters(),lr=.001)
 weights=torch.tensor([1/(sum(r['category']==c for r in train.rows)) for c in ('normal','annotated')]); sampleweights=torch.tensor([weights[int(r['category']=='annotated')] for r in train.rows]); sampler=WeightedRandomSampler(sampleweights,len(train),replacement=True,generator=torch.Generator().manual_seed(args.seed))
 loader=DataLoader(train,batch_size=1,sampler=sampler,num_workers=4,pin_memory=True)
 for epoch in range(1,args.epochs+1):
  visual=epoch%2==1; head.train(); anchors.train(); opt=visual_opt if visual else text_opt; opt.zero_grad(set_to_none=True); losses=[]; pseudo_hist=torch.zeros(len(names)); bg_cells=0; strat={'defect_cells':0,'clean_cells':0,'suspicious_cells':0}
  for step,(img,masks,label,parent,_) in enumerate(tqdm(loader,desc=f'epoch {epoch}/{args.epochs}')):
   if args.max_steps and step>=args.max_steps: break
   img=img.to(device); masks=masks.to(device); label=label.to(device)
   with torch.no_grad():
    global_feat,q=clip.encode_image(img,[6,12,18,24],proj_use=False,DPAM_layer=20); q=[x[:,1:].float() for x in q]; sim=F.normalize(global_feat.float(),dim=-1)@bank.T
    excluded=torch.tensor([r['parent_id']==parent[0] for r in normal],device=device); sim[:,excluded]=-float('inf')
    if random.random()<.05: inds=torch.nonzero(~excluded).flatten()[torch.randperm(int((~excluded).sum()),device=device)[:4]]
    else: inds=sim[0].topk(4).indices
    refs=[]
    for idx in inds.tolist():
     refimg=transform(Image.open(train.root/normal[idx]['image_path']).convert('RGB')).unsqueeze(0).to(device); _,rf=clip.encode_image(refimg,[6,12,18,24],proj_use=False,DPAM_layer=20); refs.append([v[:,1:].float() for v in rf])
    ref=[torch.stack([x[l][0] for x in refs],0).unsqueeze(0) for l in range(4)]
    bg=None; zs=None
    if args.arch=='v2': zs=zero_shot_grid(q,clip,anchors.hand,bias=bias)
    elif args.bg_target=='normal': bg=torch.zeros(1,37,37,dtype=torch.long,device=device)
    elif args.bg_target=='pseudo':
     bg,_=pseudo_background(q,clip,anchors.hand,args.pseudo_conf,bias=bias)
     cell_bg=F.adaptive_avg_pool2d(masks.amax(1,keepdim=True),37)[0,0]<.25; pseudo_hist+=torch.bincount(bg[0][cell_bg],minlength=len(names)).cpu(); bg_cells+=int(cell_bg.sum())
   text=anchors(clip) if not visual else anchors(clip).detach()
   output=head(q,ref,text); union=masks.amax(1,keepdim=True)
   if args.arch=='v2':
    l_exp,st=explanation_loss_v2(output['pi'],masks,output['res_weights'],zs_prob=zs,tau_res=args.tau_res,tau_conf=args.pseudo_conf,beta=args.beta,use_res=epoch>args.res_warmup,res_cap=args.res_cap)
    for k in strat: strat[k]+=st[k]
    l_type=sum(binary_loss(output['typed'][:,c:c+1],masks[:,c:c+1]) for c in range(4))/4
    loss=binary_loss(output['residual'],union)+F.cross_entropy(output['image_logits'],label)+l_exp+.5*binary_loss(output['generic'],union)+args.lambda_type*l_type+args.lambda_ortho*ortho_loss(text,anchors.hand)
   else:
    loss=binary_loss(output['residual'],union)+F.cross_entropy(output['image_logits'],label)+explanation_loss(output['pi'],masks,bg_target=bg)+.5*binary_loss(output['generic'],union)+(1-F.cosine_similarity(text[:learn_rows],prior[:learn_rows],dim=-1)).sum()
   (loss/8).backward(); losses.append(loss.item())
   if (step+1)%8==0 or step+1==len(loader): opt.step(); opt.zero_grad(set_to_none=True)
  stats={'epoch':epoch,'loss':sum(losses)/len(losses)}
  if args.bg_target=='pseudo' and bg_cells: stats['pseudo_share']={names[i].split(' on ')[0]:round(float(pseudo_hist[i]/bg_cells),4) for i in range(len(names)) if pseudo_hist[i]>0}
  if args.arch=='v2':
   tot=max(1,sum(strat.values())); stats['strata']={k:round(v/tot,4) for k,v in strat.items()}
   with torch.no_grad(): t=anchors(clip); stats['anchor_cos_to_hand']=[round(float(x),3) for x in F.cosine_similarity(t,anchors.hand,dim=-1)]; stats['gamma']=[round(float(x),3) for x in head.gamma_logit.sigmoid()]
  torch.save({'epoch':epoch,'head':head.state_dict(),'anchors':anchors.state_dict(),'config':config,'loss':stats['loss']},out/f'epoch_{epoch}.pth')
  with (out/'train_log.jsonl').open('a') as f: f.write(json.dumps(stats)+'\n')
  print(f'epoch {epoch}/{args.epochs} loss={stats["loss"]:.6f} '+json.dumps({k:v for k,v in stats.items() if k not in ('epoch','loss')}),flush=True)
if __name__=='__main__': main()
