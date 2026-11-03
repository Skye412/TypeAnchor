"""Qualitative check: what do the nuisance anchors suppress on normal validation images?

Region of interest R per normal image = pixels flagged by the no-nuisance ablation but not by nuisance-v0,
both at their own TPR-0.8 thresholds (runs/compare_fp.json). nuisance-v0 is re-run on the selected images to
obtain pi (13 anchors, 37x37); R is pooled to the grid and the argmax anchor inside R is histogrammed.
Outputs under runs/qualitative/: attribution.json / .md (all normal images) and contact sheets for the
top-N images by |R| : image | ablation binary | v0 binary | v0 argmax anchor (R outlined) | v0 nuisance mass.
"""
import argparse,csv,json
from pathlib import Path
import numpy as np
import torch,torch.nn.functional as F
from PIL import Image
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import adaptcliplib
from train_nuisance import Anchors,Bridge,NAMES
from nuisance_model import NuisanceHead
from tools import get_transform,setup_seed
SHORT=['normal','crack','corrosion','spalling','efflorescence','generic defect','water stain','shadow','moss','patch repair','graffiti','formwork','dirt']
COLORS=['#d9d9d9','#e41a1c','#ff7f00','#984ea3','#4daf4a','#000000','#377eb8','#636363','#a6d854','#f781bf','#ffff33','#a65628','#8c510a']

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--v0',default='runs/nuisance-v0/val-epoch20'); ap.add_argument('--abl',default='runs/ablation-no-nuisance/val-epoch20'); ap.add_argument('--checkpoint',default='runs/nuisance-v0/epoch_20.pth')
 ap.add_argument('--data',default='/home/skye/data/Skye/databases/Bridge512_balance_CODEBRIM'); ap.add_argument('--top',type=int,default=24); ap.add_argument('--out',default='runs/qualitative'); a=ap.parse_args(); setup_seed(10)
 cmp=json.loads(Path('runs/compare_fp.json').read_text()); thr_v0=cmp[a.v0]['tpr0.8']['threshold']; thr_abl=cmp[a.abl]['tpr0.8']['threshold']
 out=Path(a.out); (out/'sheets').mkdir(parents=True,exist_ok=True)
 rows=[r for r in csv.DictReader((Path(a.v0)/'predictions.csv').open()) if r['label']=='0']
 device='cuda'; clip,_=adaptcliplib.load('ViT-L/14@336px',device=device); clip.visual.DAPM_replace(DPAM_layer=20); clip.eval()
 trans,_=get_transform(518); train=Bridge(a.data,'train',trans); val=Bridge(a.data,'val',trans); normals=[r for r in train.rows if r['category']=='normal']; valrows={r['sample']:r for r in val.rows}
 bank=torch.load('runs/nuisance-v0/normal_globals.pt',map_location=device,weights_only=True)
 ck=torch.load(a.checkpoint,map_location='cpu',weights_only=True); names=ck['config'].get('anchors',NAMES)
 head=NuisanceHead(n_anchors=len(names)).to(device).eval(); head.load_state_dict(ck['head']); anchors=Anchors(clip,names,freeze_nuisance=ck['config'].get('freeze_nuisance',False)).to(device).eval(); anchors.load_state_dict(ck['anchors'])
 hist=np.zeros(13); hist_all=np.zeros(13); per=[]; cache={}
 with torch.inference_mode():
  text=anchors(clip)
  for r in rows:
   s=r['sample']; m0=np.load(Path(a.v0)/'maps'/(s+'.npy')); m1=np.load(Path(a.abl)/'maps'/(s+'.npy'))
   R=(m1>=thr_abl)&(m0<thr_v0); Rg=F.adaptive_avg_pool2d(torch.from_numpy(R.astype(np.float32))[None,None],37)[0,0].numpy()>=.25
   img=trans(Image.open(val.root/valrows[s]['image_path']).convert('RGB')).unsqueeze(0).to(device)
   g,q=clip.encode_image(img,[6,12,18,24],proj_use=False,DPAM_layer=20); q=[x[:,1:].float() for x in q]; sim=F.normalize(g.float(),dim=-1)@bank.T; ids=sim[0].topk(4).indices.tolist(); feats=[]
   for idx in ids:
    if idx not in cache:
     ref=trans(Image.open(train.root/normals[idx]['image_path']).convert('RGB')).unsqueeze(0).to(device); _,rf=clip.encode_image(ref,[6,12,18,24],proj_use=False,DPAM_layer=20); cache[idx]=[z[:,1:].half().cpu() for z in rf]
    feats.append(cache[idx])
   refs=[torch.cat([x[l] for x in feats],0).unsqueeze(0).to(device).float() for l in range(4)]
   res=head(q,refs,text); pi=res['pi'][0].cpu().numpy(); am=pi.argmax(0)
   hist_all+=np.bincount(am.ravel(),minlength=13)
   if Rg.any(): hist+=np.bincount(am[Rg],minlength=13)
   per.append({'sample':s,'R_area':float(R.mean()),'R_cells':int(Rg.sum()),'abl_area':float((m1>=thr_abl).mean()),'v0_area':float((m0>=thr_v0).mean()),'top_anchor_in_R':SHORT[int(np.bincount(am[Rg],minlength=13).argmax())] if Rg.any() else None,'am':am,'pi_nuis':pi[6:].sum(0),'R':R})
  per.sort(key=lambda d:-d['R_area'])
  # ---- contact sheets ----
  cmap=ListedColormap(COLORS)
  tag=Path(a.v0).parent.name
  for d in per[:a.top]:
   s=d['sample']; im=np.asarray(Image.open(val.root/valrows[s]['image_path']).convert('RGB').resize((518,518)))
   m0=np.load(Path(a.v0)/'maps'/(s+'.npy')); m1=np.load(Path(a.abl)/'maps'/(s+'.npy'))
   fig,ax=plt.subplots(1,5,figsize=(22,4.8))
   ax[0].imshow(im); ax[0].set_title(s[-30:],fontsize=8)
   ax[1].imshow(im); ax[1].imshow(m1,cmap='jet',alpha=.5,vmin=0,vmax=1); ax[1].contour(m1>=thr_abl,levels=[.5],colors='w',linewidths=.8); ax[1].set_title('no-nuisance binary (thr %.2f, area %.1f%%)'%(thr_abl,100*d['abl_area']),fontsize=8)
   ax[2].imshow(im); ax[2].imshow(m0,cmap='jet',alpha=.5,vmin=0,vmax=1); ax[2].contour(m0>=thr_v0,levels=[.5],colors='w',linewidths=.8); ax[2].set_title(tag+' binary (thr %.2f, area %.1f%%)'%(thr_v0,100*d['v0_area']),fontsize=8)
   amu=np.kron(d['am'],np.ones((14,14),int))[:518,:518]; ax[3].imshow(im); ax[3].imshow(amu,cmap=cmap,vmin=-.5,vmax=12.5,alpha=.55,interpolation='nearest'); ax[3].contour(d['R'],levels=[.5],colors='k',linewidths=1.2); ax[3].set_title(tag+' argmax anchor; R outlined -> %s'%d['top_anchor_in_R'],fontsize=8)
   ax[4].imshow(im); ax[4].imshow(np.kron(d['pi_nuis'],np.ones((14,14)))[:518,:518],cmap='magma',alpha=.6,vmin=0,vmax=1); ax[4].set_title(tag+' nuisance mass (sum of 7)',fontsize=8)
   for x in ax: x.axis('off')
   handles=[plt.Rectangle((0,0),1,1,color=COLORS[i]) for i in range(13)]; fig.legend(handles,SHORT,loc='lower center',ncol=13,fontsize=7,frameon=False)
   fig.tight_layout(rect=(0,.06,1,1)); fig.savefig(out/'sheets'/('%03d_%s.png'%(per.index(d),s)),dpi=90); plt.close(fig)
 # ---- attribution tables ----
 tot=hist.sum(); tot_all=hist_all.sum()
 rep={'thresholds':{'v0_tpr0.8':thr_v0,'abl_tpr0.8':thr_abl},'normal_images':len(rows),'images_with_R':int(sum(1 for d in per if d['R_cells']>0)),'R_cells_total':int(tot),
      'argmax_anchor_in_R':{SHORT[i]:{'cells':int(hist[i]),'share':float(hist[i]/max(tot,1))} for i in range(13)},
      'argmax_anchor_all_normal_cells':{SHORT[i]:float(hist_all[i]/tot_all) for i in range(13)},
      'top_images':[{k:v for k,v in d.items() if k not in('am','pi_nuis','R')} for d in per[:a.top]]}
 (out/'attribution.json').write_text(json.dumps(rep,indent=2))
 lines=['## 被干扰锚点抑制的区域 R 归到了哪个锚点（正常验证图 %d 张，含 R 的 %d 张，R 共 %d 格）'%(len(rows),rep['images_with_R'],tot),'','| 锚点 | R 内 argmax 占比 | 全部正常图格子占比 |','|---|---|---|']
 for i in np.argsort(-hist): lines.append('| %s | %.1f%% | %.1f%% |'%(SHORT[i],100*hist[i]/max(tot,1),100*hist_all[i]/tot_all))
 nuis=hist[6:].sum()/max(tot,1); lines+=['',"R 内归入 7 个干扰锚点的比例 %.1f%%，归入正常锚点 %.1f%%，归入缺陷类/类无关 %.1f%%"%(100*nuis,100*hist[0]/max(tot,1),100*hist[1:6].sum()/max(tot,1))]
 (out/'attribution.md').write_text('\n'.join(lines)+'\n',encoding='utf-8'); print('\n'.join(lines)); print('QUALITATIVE_DONE')
if __name__=='__main__': main()
