#!/usr/bin/env python3
"""Append Findora product records without replacing earlier entries.
Usage: python scripts/append_products.py incoming.json
Incoming JSON: array of {title,url,category,date,image?}.
"""
import json,sys,re,os,tempfile
from pathlib import Path
from urllib.parse import urlparse
ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'products.json'
def valid_url(s):
    try:
        u=urlparse(s)
        return u.scheme=='https' and bool(u.netloc) and not u.username and not u.password
    except (ValueError,TypeError): return False
def main():
    if len(sys.argv)!=2: raise SystemExit('Usage: append_products.py incoming.json')
    incoming=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
    if not isinstance(incoming,list): raise SystemExit('Expected a JSON array')
    existing=json.loads(DEST.read_text(encoding='utf-8'))
    if not isinstance(existing,list): raise SystemExit('Existing catalogue invalid')
    seen={p.get('url','').strip() for p in existing}
    added=0
    for item in incoming:
        if not isinstance(item,dict): raise SystemExit('Invalid product record')
        title=item.get('title','').strip()
        url=item.get('url','').strip()
        if not title or not valid_url(url): raise SystemExit('Missing title or invalid HTTPS product URL')
        image=item.get('image','')
        if image and not valid_url(image): raise SystemExit('Invalid image URL')
        if url in seen: continue
        row={'id':item.get('id') or 'findora-'+str(len(existing)+1),
             'title':title,'url':url,'date':item.get('date',''),
             'category':item.get('category','Other'),'image':image}
        existing.append(row);seen.add(url);added+=1
    if added:
        fd,tmp=tempfile.mkstemp(dir=ROOT,prefix='.findora-',suffix='.json')
        try:
            with os.fdopen(fd,'w',encoding='utf-8') as f:
                json.dump(existing,f,indent=2,ensure_ascii=False);f.write('\n')
            os.replace(tmp,DEST)
        finally:
            if os.path.exists(tmp): os.unlink(tmp)
    print(f'ADDED={added} TOTAL={len(existing)}')
if __name__=='__main__':main()
