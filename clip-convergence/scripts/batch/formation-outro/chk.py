import json,sys; r=json.load(sys.stdin)
def walk(o):
    if isinstance(o,dict):
        if o.get('severity') in ('error','warning'): yield o
        for v in o.values(): yield from walk(v)
    elif isinstance(o,list):
        for v in o: yield from walk(v)
seen={}
for f in walk(r):
    k=(f['severity'], f.get('rule') or f.get('id') or f.get('code') or f.get('message','')[:60]); seen[k]=seen.get(k,0)+1
print(seen)
errs=[f for f in walk(r) if f['severity']=='error']
for e in errs[:5]: print(json.dumps(e, ensure_ascii=False)[:600])
