"""AnomalyDINO-style normalized patch nearest-neighbor audit maps."""
import json, random
from pathlib import Path
import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image
from scipy.ndimage import gaussian_filter
from torchvision import transforms
from tqdm import tqdm
root=Path(__file__).resolve().parent
out=root/'runs/audit/anomalydino'; maps=out/'maps'; maps.mkdir(parents=True,exist_ok=True)
meta=json.loads((root/'data_views/val/meta.json').read_text())
refs=meta['train']['structural defects']; queries=meta['test']['structural defects']
selected=random.Random(10).sample(refs,16)
(out/'references.json').write_text(json.dumps([x['img_path'] for x in selected],indent=2))
model=torch.hub.load('/home/skye/.cache/torch/hub/facebookresearch_dinov2_main','dinov2_vitb14',source='local',pretrained=True).cuda().eval()
transform=transforms.Compose([transforms.Resize((518,518),interpolation=transforms.InterpolationMode.BICUBIC,antialias=True),transforms.ToTensor(),transforms.Normalize((.485,.456,.406),(.229,.224,.225))])
def features(path):
 x=transform(Image.open(path).convert('RGB')).unsqueeze(0).cuda()
 with torch.inference_mode(): return F.normalize(model.get_intermediate_layers(x)[0][0].float(),dim=-1)
ref=torch.cat([features(x['img_path']) for x in tqdm(selected,desc='references')])
for q in tqdm(queries,desc='validation'):
 f=features(q['img_path']); dist=[]
 for chunk in f.split(256): dist.append((1-chunk@ref.T).amin(1))
 grid=torch.cat(dist).reshape(37,37).cpu().numpy()
 import cv2
 score=gaussian_filter(cv2.resize(grid,(512,512),interpolation=cv2.INTER_LINEAR),sigma=4).astype(np.float32)
 if not np.isfinite(score).all(): raise ValueError(q['img_path'])
 np.save(maps/(Path(q['img_path']).stem+'.npy'),score)
