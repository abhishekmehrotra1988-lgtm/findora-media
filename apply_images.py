#!/usr/bin/env python3
import json,pathlib
root=pathlib.Path(__file__).resolve().parent
catalog=root/'products.json'
products=json.loads(catalog.read_text(encoding='utf-8'))
images=json.loads((root/'image-map.json').read_text(encoding='utf-8'))
matched=0
for product in products:
    path=images.get(product.get('url'))
    if path:
        assert (root/path).is_file(),path
        product['image']=path
        product['image_kind']='ILLUSTRATIVE_CAMPAIGN_CREATIVE'
        matched+=1
assert matched==16,f'Expected 16 matched products, found {matched}'
catalog.write_text(json.dumps(products,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'Updated {matched} product images; catalogue has {len(products)} products')
