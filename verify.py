import os,re
ROOT='.'
bad=0; checked=0
for dp,_,fs in os.walk(ROOT):
    for fn in fs:
        if not fn.endswith('.html'): continue
        p=os.path.join(dp,fn)
        html=open(p).read()
        base=os.path.dirname(p)
        # collect href/src (skip http, mailto, #, javascript)
        refs=re.findall(r'(?:href|src)="([^"]+)"',html)
        for r in refs:
            if r.startswith(('http','mailto:','tel:','#','javascript:','data:')): continue
            target=os.path.normpath(os.path.join(base,r))
            checked+=1
            if not os.path.exists(target):
                print('BROKEN',p,'->',r); bad+=1
print(f'checked {checked} refs, {bad} broken')
# gallery images referenced in JS (built dynamically) exist?
missing=[i for i in range(1,25) if not os.path.exists(f'img/gallery/g{i:02d}.webp')]
print('gallery missing:',missing)
