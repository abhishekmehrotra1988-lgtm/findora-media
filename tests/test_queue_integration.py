#!/usr/bin/env python3
"""Test queue conversion and catalogue append without modifying production data."""
import json,subprocess,sys,tempfile
from pathlib import Path
root=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as d:
    t=Path(d)
    (t/'scripts').mkdir()
    for name in ['queue_to_products.py','append_products.py']:
        (t/'scripts'/name).write_text((root/'scripts'/name).read_text(encoding='utf-8'),encoding='utf-8')
    old=[{'id':'historic','title':'Existing','url':'https://example.com/old','date':'2026-10-15','category':'Beauty','image':''}]
    (t/'products.json').write_text(json.dumps(old),encoding='utf-8')
    queue={'date':'2026-10-17','publications':[{'format':'REELS','product_name':'New jewellery','link':'https://example.com/new','category':'Jewellery','product_image_url':'https://example.com/photo.jpg'},{'format':'IMAGE','product_name':'Existing','link':'https://example.com/old'}]}
    (t/'queue.json').write_text(json.dumps(queue),encoding='utf-8')
    subprocess.run([sys.executable,str(t/'scripts'/'queue_to_products.py'),str(t/'queue.json'),str(t/'incoming.json')],check=True)
    subprocess.run([sys.executable,str(t/'scripts'/'append_products.py'),str(t/'incoming.json')],check=True)
    result=json.loads((t/'products.json').read_text(encoding='utf-8'))
    assert len(result)==2 and result[0]==old[0]
    assert result[1]['image']=='https://example.com/photo.jpg'
    subprocess.run([sys.executable,str(t/'scripts'/'append_products.py'),str(t/'incoming.json')],check=True)
    assert len(json.loads((t/'products.json').read_text(encoding='utf-8')))==2
    print('PASS: queue conversion, product image, append-only preservation, deduplication')
