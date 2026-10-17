#!/usr/bin/env python3
"""Regression tests: preserve catalogue, deduplicate, and reject bad inputs."""
import json,subprocess,sys,tempfile
from pathlib import Path
source=Path(__file__).resolve().parents[1]/'scripts'/'append_products.py'
with tempfile.TemporaryDirectory() as d:
    root=Path(d)
    (root/'scripts').mkdir()
    (root/'scripts'/'append_products.py').write_text(source.read_text(encoding='utf-8'),encoding='utf-8')
    base=[{'id':'old','title':'Historic product','url':'https://example.com/old','date':'2026-10-15','category':'Beauty','image':''}]
    (root/'products.json').write_text(json.dumps(base),encoding='utf-8')
    incoming=[{'title':'Historic product','url':'https://example.com/old'},{'title':'New find','url':'https://example.com/new','category':'Jewellery','date':'2026-10-17'}]
    (root/'incoming.json').write_text(json.dumps(incoming),encoding='utf-8')
    cmd=[sys.executable,str(root/'scripts'/'append_products.py'),str(root/'incoming.json')]
    first=subprocess.run(cmd,capture_output=True,text=True)
    assert first.returncode==0,first.stderr
    data=json.loads((root/'products.json').read_text(encoding='utf-8'))
    assert len(data)==2 and data[0]==base[0] and data[1]['title']=='New find'
    second=subprocess.run(cmd,capture_output=True,text=True)
    assert second.returncode==0 and 'ADDED=0' in second.stdout
    assert len(json.loads((root/'products.json').read_text(encoding='utf-8')))==2
    (root/'bad.json').write_text(json.dumps([{'title':'Bad','url':'javascript:alert(1)'}]),encoding='utf-8')
    bad=subprocess.run([sys.executable,str(root/'scripts'/'append_products.py'),str(root/'bad.json')],capture_output=True,text=True)
    assert bad.returncode!=0
    assert len(json.loads((root/'products.json').read_text(encoding='utf-8')))==2
    print('PASS: preserve, append, deduplicate, reject invalid URL')
