import random, statistics as st, importlib.util, io, contextlib, math, itertools
spec=importlib.util.spec_from_file_location('t','loo_complexity_test.py'); t=importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(t)
F=t.F
def medae(target,key,efr=False): return t.score_run(target,key,efr)[0]['med_abs_err']
base={tg:medae(tg,'cx',e) for tg,e in [('tau',False),('euw',False),('rfe',False)]}
strat={tg:medae(tg,'g',e) for tg,e in [('tau',False),('euw',False),('rfe',False)]}
print('observed complexity medAE',base,'\nstrat medAE',strat)
# permutation: shuffle class labels preserving class sizes
labels=[F[f]['cx'] for f in F]; names=list(F)
random.seed(1); N=4000; cnt={k:0 for k in base}
for _ in range(N):
    random.shuffle(labels)
    for f,l in zip(names,labels): F[f]['cx']=l
    for tg in base:
        if medae(tg,'cx')<=base[tg]: cnt[tg]+=1
print('permutation P(random classes do as well or better):',{k:v/N for k,v in cnt.items()})
# restore, then threshold sensitivity
for f in names: F[f]['cx']=t.cls(t.score[f])
print('threshold sensitivity (simple<a, complex>=b) -> medAE tau / euw / rfe')
for a,b in [(0.5,1.5),(0.5,2.0),(1.0,2.0),(0.25,1.0),(0.5,1.0)]:
    for f in names: F[f]['cx']='simple' if t.score[f]<a else ('moderate' if t.score[f]<b else 'complex')
    print(a,b,[round(medae(tg,'cx'),3) for tg in ('tau','euw','rfe')],{c:sum(1 for f in names if F[f]['cx']==c) for c in('simple','moderate','complex')})
# leave out Murdoch K (single-well 282 bcf) from euw
for f in names: F[f]['cx']=t.cls(t.score[f])
mk=F.pop('MurdochK')
print('euw without Murdoch K: complexity',round(medae('euw','cx'),3),'strat',round(medae('euw','g'),3))
