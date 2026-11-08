"""Second fully supervised reference baseline: DeepLabV3 with a ResNet-50 backbone (torchvision, ImageNet-1k weights from the
local torch hub cache), trained on the same CODEBRIM tiles and the same four independent class masks as SegFormer-B2
(train_segformer.py: Tiles, loss_fn, evaluate and augmentation are imported unchanged; multi-label sigmoid, BCE + Dice).
Run in the MixerCSeg conda env:
  python train_deeplab.py --out runs/deeplabv3-r50 [--epochs 40]
  python train_deeplab.py --out runs/deeplabv3-r50 --eval-only --split test --eval-out runs/deeplabv3-r50/test-epoch40
"""
import argparse,json,random
from pathlib import Path
import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision.models.segmentation import deeplabv3_resnet50
from torchvision.models import ResNet50_Weights
from train_segformer import Tiles,loss_fn,evaluate

class DeepLabR50(nn.Module):
 def __init__(self,pretrained=True):
  super().__init__()
  self.net=deeplabv3_resnet50(weights=None,weights_backbone=ResNet50_Weights.IMAGENET1K_V2 if pretrained else None,num_classes=4,aux_loss=False)
 def forward(self,x): return self.net(x)['out']

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--data',default='/home/skye/data/Skye/databases/Bridge512_balance_CODEBRIM'); ap.add_argument('--out',default='runs/deeplabv3-r50'); ap.add_argument('--epochs',type=int,default=40); ap.add_argument('--bs',type=int,default=8); ap.add_argument('--lr',type=float,default=1e-4); ap.add_argument('--seed',type=int,default=10)
 ap.add_argument('--eval-only',action='store_true'); ap.add_argument('--split',default='val'); ap.add_argument('--eval-data',default=None); ap.add_argument('--eval-out',default=None)
 a=ap.parse_args(); random.seed(a.seed); np.random.seed(a.seed); torch.manual_seed(a.seed); device='cuda'; out=Path(a.out); out.mkdir(parents=True,exist_ok=True)
 if a.eval_only:
  model=DeepLabR50(pretrained=False).to(device); ck=torch.load(out/'last.pth',map_location='cpu'); model.load_state_dict(ck['model'])
  evaluate(model,a.eval_data or a.data,a.split,a.eval_out or out/f'{a.split}-epoch{ck["epoch"]}',device,str(out/'last.pth')); return
 model=DeepLabR50().to(device); (out/'config.json').write_text(json.dumps(vars(a),indent=2))
 ds=Tiles(a.data,'train',True); dl=DataLoader(ds,batch_size=a.bs,shuffle=True,num_workers=6,drop_last=True,pin_memory=True)
 opt=torch.optim.AdamW([{'params':model.net.backbone.parameters(),'lr':a.lr},{'params':model.net.classifier.parameters(),'lr':a.lr*10}],weight_decay=.01)
 total=a.epochs*len(dl); warm=min(1500,total//10); step=0; scaler=torch.cuda.amp.GradScaler()
 for ep in range(1,a.epochs+1):
  model.train(); losses=[]
  for x,y,_ in dl:
   f=(step+1)/warm if step<warm else (1-(step-warm)/max(1,total-warm))**1.0
   for g,base in zip(opt.param_groups,(a.lr,a.lr*10)): g['lr']=base*max(f,1e-3)
   with torch.cuda.amp.autocast(): loss=loss_fn(model(x.to(device,non_blocking=True)).float(),y.to(device,non_blocking=True))
   opt.zero_grad(set_to_none=True); scaler.scale(loss).backward(); scaler.step(opt); scaler.update(); losses.append(loss.item()); step+=1
  torch.save({'model':model.state_dict(),'epoch':ep,'config':vars(a)},out/'last.pth')
  with (out/'train_log.jsonl').open('a') as fh: fh.write(json.dumps({'epoch':ep,'loss':float(np.mean(losses)),'steps':step})+'\n')
  print(f'epoch {ep}/{a.epochs} loss={np.mean(losses):.4f} steps={step}',flush=True)
 evaluate(model,a.data,'val',out/f'val-epoch{ep}',device,str(out/'last.pth'))
if __name__=='__main__': main()
