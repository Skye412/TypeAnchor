"""Reconstruct independent 4-class masks from selected 512 CODEBRIM crops."""
import argparse,csv,json
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np
CLASSES={"Crack":"Crack","Spalling":"Spalling","Corrosion":"Corrosion","Efflorescence":"Efflorescence","Exposed Bars":"Corrosion","Exposed Rebars":"Corrosion","exposed bars":"Corrosion","crack":"Crack","spalling":"Spalling","corrosion":"Corrosion","efflorescence":"Efflorescence"}
ap=argparse.ArgumentParser(); ap.add_argument('--source',required=True); ap.add_argument('--selected',required=True); ap.add_argument('--output',required=True); a=ap.parse_args()
source=Path(a.source); out=Path(a.output); out.mkdir(parents=True,exist_ok=True)
summary={}; global_counts={c:0 for c in set(CLASSES.values())}; overlaps=0; total=0
for split in ('train','val','test'):
 rows=list(csv.DictReader((Path(a.selected)/(split+'_manifest.csv')).open(encoding='utf-8')))
 dest=out/split; (dest/'masks').mkdir(parents=True,exist_ok=True)
 meta=[]
 for r in rows:
  item=dict(r); sample=r['sample']; source_sample=r['source_sample']; x,y=int(r['crop_x']),int(r['crop_y'])
  image_path=source/'annotated'/(source_sample+'.jpg')
  json_path=source/'annotated'/(source_sample+'.json')
  if r['category']!='annotated':
   item['class_masks']={}; meta.append(item); continue
  if not json_path.exists(): raise FileNotFoundError(json_path)
  obj=json.loads(json_path.read_text(encoding='utf-8'))
  w,h=obj['imageWidth'],obj['imageHeight']
  masks={c:Image.new('L',(w,h),0) for c in ('Crack','Spalling','Corrosion','Efflorescence')}
  for sh in obj.get('shapes',[]):
   c=CLASSES.get(str(sh.get('label','')).strip())
   if c is None: raise ValueError(f'Unknown annotation label: {sh.get("label")} in {json_path}')
   pts=[tuple(map(float,p)) for p in sh.get('points',[])]
   d=ImageDraw.Draw(masks[c]); typ=sh.get('shape_type','polygon')
   if typ in ('polygon','rectangle') and len(pts)>=2:
    if typ=='rectangle' and len(pts)==2: d.rectangle([pts[0],pts[1]],fill=255)
    else: d.polygon(pts,fill=255)
   elif typ in ('line','linestrip') and len(pts)>=2: d.line(pts,fill=255,width=3,joint='curve')
  crop_masks={}; arrs=[]
  for c,m in masks.items():
   crop=m.crop((x,y,x+512,y+512)); p=dest/'masks'/f'{sample}__{c}.png'; crop.save(p); crop_masks[c]=str(p); z=np.asarray(crop)>0; global_counts[c]+=int(z.sum()); arrs.append(z)
  union=np.logical_or.reduce(arrs); overlaps += int(np.sum(np.stack(arrs,axis=0).sum(0)>1)); total += int(union.sum()); item['class_masks']=crop_masks; meta.append(item)
 (dest/'meta_multiclass.json').write_text(json.dumps({'samples':meta,'classes':['Crack','Corrosion','Spalling','Efflorescence'],'mask_semantics':'independent binary masks reconstructed from LabelMe JSON; Exposed Bars merged into Corrosion'},indent=2))
 summary[split]={'images':len(rows),'annotated':sum(r['category']=='annotated' for r in rows)}
(out/'reconstruction_summary.json').write_text(json.dumps({'splits':summary,'class_pixels':global_counts,'overlap_pixels':overlaps,'union_pixels':total,'overlap_fraction_of_union':overlaps/max(total,1),'label_map':CLASSES},indent=2))
print(json.dumps({'splits':summary,'class_pixels':global_counts,'overlap_pixels':overlaps,'union_pixels':total},indent=2))
