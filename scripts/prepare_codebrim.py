"""Prepare metadata views without modifying or copying the source dataset."""
import argparse, json, hashlib
from pathlib import Path
from PIL import Image
import numpy as np
p=argparse.ArgumentParser()
p.add_argument('--source',required=True)
p.add_argument('--output',default='data_views')
a=p.parse_args(); source=Path(a.source); out=Path(a.output)
records={}; counts={}
for split in ['train','val','test']:
    meta=json.loads((source/split/'meta.json').read_text(encoding='utf-8-sig'))
    populated=[v for v in meta.values() if isinstance(v,dict) and any(v.values())]
    rows=next(iter(populated[0].values()))
    records[split]=[]
    for original in rows:
        item=dict(original)
        item['img_path']=str(source/split/item['img_path'])
        if item['anomaly']:
            mask_path=source/split/item['mask_path']
            rgb=np.asarray(Image.open(mask_path).convert('RGB'))
            valid=np.zeros(rgb.shape[:2],bool)
            for color in [(255,0,0),(0,255,0),(0,0,255),(255,255,0)]:
                valid |= np.all(rgb==color,axis=-1)
            if np.any(np.any(rgb!=0,axis=-1)&~valid):
                raise ValueError(f'Unknown palette: {mask_path}')
            dest=(out/split/'masks_union'/mask_path.name).resolve()
            dest.parent.mkdir(parents=True,exist_ok=True)
            Image.fromarray(valid.astype('uint8')*255).save(dest)
            item['mask_path']=str(dest)
        records[split].append(item)
    counts[split]={'total':len(rows),'normal':sum(x['anomaly']==0 for x in rows)}
normals=[x for x in records['train'] if x['anomaly']==0]
for split,rows in records.items():
    d=out/split; d.mkdir(parents=True,exist_ok=True)
    (d/'meta.json').write_text(json.dumps({'train':{'structural defects':normals},'test':{'structural defects':rows}},indent=2))
    for label,value in [('normal',0),('anomaly',1)]:
        (d/(label+'.txt')).write_text(''.join(Path(x['img_path']).name+'\n' for x in rows if x['anomaly']==value))
    images=d/'images'; images.mkdir(exist_ok=True)
    for x in rows:
        link=images/Path(x['img_path']).name
        if not link.exists(): link.symlink_to(x['img_path'])
(out/'summary.json').write_text(json.dumps(counts,indent=2)); print(counts)
