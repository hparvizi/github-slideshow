"""Q fixes: leakage-free matrix, common play-wide sigma, full threshold grid, 20000-draw permutation. python3 -I"""
import random, math, statistics as st, importlib.util, io, contextlib
spec=importlib.util.spec_from_file_location('t','loo_complexity_test.py'); t=importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(t)
F=t.F; names=list(F)
# common sigma: always play-wide sigma of all other fields (comparable coverage/width)
def predict(target,key,field):
    others=[f for f in F if f!=field and F[f][target] is not None]
    peers=[f for f in others if F[f][key]==F[field][key]]
    use=peers if len(peers)>=2 else others
    mu,_=t.lstats([F[f][target] for f in use]); _,sd=t.lstats([F[f][target] for f in others])
    return math.exp(mu),sd,len(use),''
t.predict=predict
def run(tg,key,efr=False):
    s,_=t.score_run(tg,key,efr); return s
# leakage-free matrix: only measured p_i (C5), direct DST test (C1 Cavendish), geological stacking descriptions (C2)
LF={'Breagh':'. . . . O','Kilmar':'. I . . .','Trent':'. I . . .','Cavendish':'O I . . .'}
def set_classes(M,a=0.5,b=1.5):
    for f in names:
        sc=sum(t.W[c] for c in M.get(f,'. . . . .').split()); F[f]['cx']='simple' if sc<a else ('moderate' if sc<b else 'complex')
def table(label):
    print(label,{c:[f for f in names if F[f]['cx']==c] for c in('simple','moderate','complex')})
    for tg,lab,e in [('tau','tau',False),('euw','EUR/well',False),('rfe','RF_eff',False)]:
        a=run(tg,'g',e);b=run(tg,'cx',e)
        print(f"  {lab:9s} strat {a['med_abs_err']*100:5.1f}% in {a['inside']}/{a['n']} w{a['width']:.1f}x | class {b['med_abs_err']*100:5.1f}% in {b['inside']}/{b['n']} w{b['width']:.1f}x")
def perm(tg,N=20000,seed=7):
    obs=run(tg,'cx')['med_abs_err']; lab=[F[f]['cx'] for f in names]; random.seed(seed); c=0
    for _ in range(N):
        random.shuffle(lab)
        for f,l in zip(names,lab): F[f]['cx']=l
        if run(tg,'cx')['med_abs_err']<=obs: c+=1
    for f,l in zip(names,saved): F[f]['cx']=l
    return c/N
print('=== ORIGINAL matrix, common play-wide sigma ==='); set_classes(t.M); table('classes'); saved=[F[f]['cx'] for f in names]
print('perm P (20000, seed 7):',{tg:perm(tg) for tg in('tau','euw','rfe')})
print('=== threshold grid, original matrix (tau/euw/rfe class medAE; strat euw 41.8) ===')
for a,b in [(0.5,1.5),(0.5,2.0),(1.0,2.0),(1.0,1.5),(0.5,1.0)]:
    set_classes(t.M,a,b); print(a,b,[round(run(tg,'cx')['med_abs_err'],3) for tg in('tau','euw','rfe')],{c:sum(F[f]['cx']==c for f in names) for c in('simple','moderate','complex')})
print('Cavendish moderate (threshold 1.6):'); set_classes(t.M,0.5,1.6); print([round(run(tg,'cx')['med_abs_err'],3) for tg in('tau','euw','rfe')])
print('=== LEAKAGE-FREE matrix ==='); set_classes(LF); table('classes'); saved=[F[f]['cx'] for f in names]
print('perm P:',{tg:perm(tg) for tg in('tau','euw','rfe')})
for a,b in [(0.5,1.5),(0.5,1.0),(1.0,1.5)]:
    set_classes(LF,a,b); print('LF grid',a,b,[round(run(tg,'cx')['med_abs_err'],3) for tg in('tau','euw','rfe')],{c:sum(F[f]['cx']==c for f in names) for c in('simple','moderate','complex')})
