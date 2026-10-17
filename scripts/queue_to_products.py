#!/usr/bin/env python3
"""Convert a Findora daily publishing queue to permanent catalogue records.
Usage: python scripts/queue_to_products.py queue.json incoming.json
Never creates affiliate URLs or product photographs.
"""
import json,sys
from pathlib import Path
if len(sys.argv)!=3: raise SystemExit('Usage: queue_to_products.py queue.json incoming.json')
raw=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
if not isinstance(raw,dict) or not isinstance(raw.get('publications'),list):
    raise SystemExit('Queue must contain a publications array')
rows=[]
for i,p in enumerate(raw['publications'],1):
    if not isinstance(p,dict): raise SystemExit(f'Invalid publication {i}')
    link=p.get('profit_link') or p.get('affiliate_url') or p.get('link') or p.get('product_url')
    title=p.get('product_name') or p.get('title') or p.get('name')
    if not link or not title:
        raise SystemExit(f'Publication {i}: missing product title or link; no silent omission')
    image=p.get('product_image_url') or p.get('image_url') or ''
    rows.append({'title':title,'url':link,'image':image,
                 'category':p.get('category') or 'Other',
                 'date':p.get('date') or raw.get('date') or ''})
Path(sys.argv[2]).write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(f'CONVERTED={len(rows)}')
