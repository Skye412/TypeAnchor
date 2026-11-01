"""Train nuisance-aware AdaptCLIP with retrieved train-only normal references."""
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
from nuisance_model import NuisanceHead,explanation_loss
from tools import get_transform,setup_seed
from tqdm import tqdm

NAMES=['intact concrete surface','crack on concrete','rust stain on concrete','spalling on concrete','efflorescence on concrete','damaged concrete surface','water stain on concrete','shadow on concrete','moss on concrete','patch repair on concrete','graffiti on concrete','formwork texture on concrete','dirt on concrete']
# Anchor sets: 'full' = 13 anchors; 'no-nuisance' drops the seven nuisance anchors (aggregate form of prediction P2).
ANCHOR_SETS={'full':NAMES,'no-nuisance':NAMES[:6]}
TEMPLATES=['a photo of {}','a close-up photo of {} on a bridge','{} on a concrete wall','an inspection image showing {}']
CLASSES=['Crack','Corrosion','Spalling','Efflorescence']
class Anchors(nn.Module):
 def __init__(self,clip,names=NAMES):
  super().__init__(); self.names=list(names); n=len(self.names); self.ctx=nn.Parameter(torch.randn(n,12,768)*.02)
  texts=[]; groups=[]
  for i,name in enumerate(self.names):
   for alternative in ([name,'exposed corroded rebar'] if i==2 else [name]):
    for template in TEMPLATES: texts.append(' '.join(['X']*12)+' '+template.format(alternative)+'.'); groups.append(i)
  ids=tokenize(texts); emb=clip.token_embedding(ids.to(next(clip.parameters()).device)).detach()
  self.register_buffer('ids',ids); self.register_buffer('prefix',emb[:,:1]); self.register_buffer('suffix',emb[:,13:]); self.register_buffer('groups',torch.tensor(groups))
 def forward(self,clip):
  context=self.ctx[self.groups]; inp=torch.cat([self.prefix,context.to(self.prefix.dtype),self.suffix],1)
  f=clip.encode_text_learn(inp,self.ids).float(); f=F.normalize(f,dim=-1)
  return F.normalize(torch.stack([f[self.groups==i].mean(0) for i in range(len(self.names))]),dim=-1)
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

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--data',default='/home/skye/data/Skye/databases/Bridge512_balance_CODEBRIM'); ap.add_argument('--out',default='runs/nuisance-v0'); ap.add_argument('--epochs',type=int,default=20); ap.add_argument('--seed',type=int,default=10)
 ap.add_argument('--anchor-set',choices=sorted(ANCHOR_SETS),default='full'); ap.add_argument('--bank',default=None,help='cached normal global vectors; default <out>/normal_globals.pt')
 args=ap.parse_args()
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
 head=NuisanceHead(n_anchors=len(names)).to(device); anchors=Anchors(clip,names).to(device)
 with torch.no_grad(): prior=anchors(clip).detach()
 visual_opt=torch.optim.AdamW(head.parameters(),lr=.001); text_opt=torch.optim.AdamW(anchors.parameters(),lr=.001)
 weights=torch.tensor([1/(sum(r['category']==c for r in train.rows)) for c in ('normal','annotated')]); sampleweights=torch.tensor([weights[int(r['category']=='annotated')] for r in train.rows]); sampler=WeightedRandomSampler(sampleweights,len(train),replacement=True,generator=torch.Generator().manual_seed(args.seed))
 loader=DataLoader(train,batch_size=1,sampler=sampler,num_workers=4,pin_memory=True)
 for epoch in range(1,args.epochs+1):
  visual=epoch%2==1; head.train(); anchors.train(); opt=visual_opt if visual else text_opt; opt.zero_grad(set_to_none=True); losses=[]
  for step,(img,masks,label,parent,_) in enumerate(tqdm(loader,desc=f'epoch {epoch}/{args.epochs}')):
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
   text=anchors(clip) if not visual else anchors(clip).detach()
   output=head(q,ref,text); union=masks.amax(1,keepdim=True)
   loss=binary_loss(output['residual'],union)+F.cross_entropy(output['image_logits'],label)+explanation_loss(output['pi'],masks)+.5*binary_loss(output['generic'],union)+(1-F.cosine_similarity(text,prior,dim=-1)).sum()
   (loss/8).backward(); losses.append(loss.item())
   if (step+1)%8==0 or step+1==len(loader): opt.step(); opt.zero_grad(set_to_none=True)
  torch.save({'epoch':epoch,'head':head.state_dict(),'anchors':anchors.state_dict(),'config':config,'loss':sum(losses)/len(losses)},out/f'epoch_{epoch}.pth')
  print(f'epoch {epoch}/{args.epochs} loss={sum(losses)/len(losses):.6f}',flush=True)
if __name__=='__main__': main()
