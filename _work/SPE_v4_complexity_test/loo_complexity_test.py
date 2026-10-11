"""Complexity-class vs stratigraphic-group leave-one-field-out test. Inputs: SPE v3 Tables 9-14, 22 (see protocol file)."""
import math, json, statistics as st

# Table 22: group, q_ref, EUR_tech, EUR_w (clean 12 only), tau.  Table 9: RF_eff (credible only).
F = {
 'Breagh':    dict(g='Dinantian',     q=112, eur=319, euw=29,   tau=7.8,  rfe=0.40),
 'Kilmar':    dict(g='Namurian',      q=34,  eur=66,  euw=22,   tau=5.4,  rfe=0.25),
 'Trent':     dict(g='StackedNamWA',  q=50,  eur=132, euw=None, tau=7.2,  rfe=None),
 'Cavendish': dict(g='StackedNamWA',  q=66,  eur=101, euw=34,   tau=4.2,  rfe=0.61),
 'Chiswick':  dict(g='WestphAB',      q=89,  eur=314, euw=52,   tau=9.7,  rfe=0.51),
 'Kew':       dict(g='WestphAB',      q=26,  eur=43,  euw=43,   tau=4.6,  rfe=0.56),
 'Murdoch':   dict(g='WestphB',       q=141, eur=518, euw=52,   tau=10.1, rfe=0.98),
 'McAdam':    dict(g='WestphB',       q=95,  eur=150, euw=75,   tau=4.3,  rfe=0.84),
 'Schooner':  dict(g='WestphCD',      q=123, eur=313, euw=26,   tau=7.0,  rfe=0.53),
 'Boulton':   dict(g='WestphCD',      q=86,  eur=348, euw=70,   tau=11.1, rfe=None),
 'Ketch':     dict(g='WestphCD',      q=126, eur=253, euw=28,   tau=5.5,  rfe=None),
 'MurdochK':  dict(g='WestphCD',      q=139, eur=282, euw=282,  tau=5.6,  rfe=None),
 'Rita':      dict(g='WestphCD',      q=56,  eur=51,  euw=51,   tau=2.5,  rfe=None),
}
# Challenge matrix (O observed 1, I inferred 0.5, . open 0). Evidence in matrix_evidence.md
M = {
 #            C1 C2 C3 C4 C5
 'Breagh':   '. I . I O',
 'Kilmar':   'I I O . .',
 'Trent':    '. I . . .',
 'Cavendish':'O I . . .',
 'Chiswick': '. . . I .',
 'Kew':      '. . . I .',
 'Murdoch':  '. . . . .',
 'McAdam':   '. . . . .',
 'Schooner': '. . . . .',
 'Boulton':  '. . . . .',
 'Ketch':    '. . . . .',
 'MurdochK': '. . . . .',
 'Rita':     '. . . I .',
}
W = {'O':1.0,'I':0.5,'.':0.0}
score = {k: sum(W[c] for c in v.split()) for k,v in M.items()}
def cls(s): return 'simple' if s<0.5 else ('moderate' if s<1.5 else 'complex')
for k in F: F[k]['cx']=cls(score[k]); F[k]['score']=score[k]

Z=1.2816
def lstats(vals):
    l=[math.log(v) for v in vals]
    return st.mean(l), (st.stdev(l) if len(l)>1 else float('nan'))

def predict(target, key, field):
    others=[f for f in F if f!=field and F[f][target] is not None]
    peers=[f for f in others if F[f][key]==F[field][key]]
    use = peers if len(peers)>=2 else others
    mu,sd=lstats([F[f][target] for f in use])
    _,sd_all=lstats([F[f][target] for f in others])
    sig = sd if len(use)>=3 else sd_all
    return math.exp(mu), sig, len(use), ('peers' if use is peers else 'play')

def score_run(target, key, eur_from_tau=False):
    rows=[]
    fields=[f for f in F if F[f][target] is not None]
    for f in fields:
        p,sig,n,src=predict(target,key,f)
        a=F[f][target]
        if eur_from_tau:
            pe=0.365*F[f]['q']*p; ae=F[f]['eur']
            # lognormal scale carries over multiplicatively
            p,a=pe,ae
        lo,hi=p*math.exp(-Z*sig),p*math.exp(Z*sig)
        rows.append(dict(f=f,pred=p,act=a,err=(p-a)/a,inside=lo<=a<=hi,width=hi/lo,n=n,src=src))
    ae=[abs(r['err']) for r in rows]
    bias=math.exp(st.mean([math.log(r['pred']/r['act']) for r in rows]))-1
    return dict(n=len(rows),med_abs_err=st.median(ae),bias=bias,
                inside=sum(r['inside'] for r in rows),
                width=st.median([r['width'] for r in rows]),
                err_min=min(r['err'] for r in rows),err_max=max(r['err'] for r in rows)),rows

out={}
print('Class assignments:')
for k in F: print(f"  {k:10s} score {F[k]['score']:.1f} -> {F[k]['cx']:8s} | strat {F[k]['g']}")
tests=[('tau','tau',False),('tau','EUR_field(0.365 q tau)',True),('euw','EUR_per_well',False),('rfe','RF_eff',False)]
for tgt,label,efr in tests:
    for key,name in [('g','stratigraphic'),('cx','complexity')]:
        s,rows=score_run(tgt,key,efr)
        out[(label,name)]=(s,rows)
        print(f"{label:24s} {name:14s} n={s['n']:2d} medAE={s['med_abs_err']*100:5.1f}% bias={s['bias']*100:+6.1f}% inside={s['inside']}/{s['n']} width(med)={s['width']:.1f}x err[{s['err_min']*100:+.0f}%,{s['err_max']*100:+.0f}%]")
# per-field detail
json.dump({f"{a}|{b}":{'summary':v[0],'rows':v[1]} for (a,b),v in out.items()},open('loo_results.json','w'),indent=1,default=str)
# same-peer-set check: how many fields have identical peer sets under both groupings
same=0
for f in F:
    a={g for g in F if g!=f and F[g]['g']==F[f]['g']}; b={g for g in F if g!=f and F[g]['cx']==F[f]['cx']}
    same+= (a==b)
print('fields with identical peer sets under both groupings:',same,'of',len(F))
