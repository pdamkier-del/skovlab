"""Exact stationary time reversal of a minimal four-module evolutionary model."""
import argparse
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

p=argparse.ArgumentParser()
p.add_argument("output",type=Path)
out=p.parse_args().output
routings=pd.read_csv(out/"motif_equilibria.csv").query("donor==0").set_index("receiver")
hi=int(routings.difference.idxmax())
lo=int(routings.difference.idxmin())
n=4
configurations=np.array(list(product([0,1],repeat=n)))
lookup={tuple(a):i for i,a in enumerate(configurations)}


def model(layout,mu,mode):
    energy=routings.loc[layout,["cluster_reserve","open_reserve"]].to_numpy()
    generator=np.zeros((2**n,2**n))
    for index,g in enumerate(configurations):
        z=energy[np.arange(n),g] if mode=="selection" else energy[:,0]
        for i in range(n):
            h=g.copy()
            h[i]=1-h[i]
            target=lookup[tuple(h)]
            rate=mu
            for j in [(i-1)%n,(i+1)%n]:
                if g[j]!=g[i]:
                    rate+=.2 if mode=="neutral" else .4/(1+np.exp(-36*(z[j]-z[i])))
            generator[index,target]=rate
    generator-=np.diag(generator.sum(axis=1))
    observation=np.eye(2**n)+.1*generator
    assert observation.min()>=0
    invariant=generator.T.copy()
    invariant[-1]=1
    target=np.zeros(len(configurations))
    target[-1]=1
    pi=np.linalg.solve(invariant,target)
    traffic=pi[:,None]*observation
    active=traffic>0
    full=np.sum(traffic[active]*np.log(traffic[active]/traffic.T[active]))
    count=configurations.sum(axis=1)
    coarse=np.zeros((n+1,n+1))
    np.add.at(coarse,(count[:,None],count[None,:]),traffic)
    observed=coarse>0
    pair=np.sum(coarse[observed]*np.log(coarse[observed]/coarse.T[observed]))
    assert full>=pair-1e-12
    cycle_max=0.
    for pattern in configurations:
        k=lookup[tuple(pattern)]
        for i in range(n):
            for j in range(i+1,n):
                l,m=pattern.copy(),pattern.copy()
                l[i]^=1
                m[j]^=1
                both=l.copy()
                both[j]^=1
                cycle=[k,lookup[tuple(l)],lookup[tuple(both)],lookup[tuple(m)],k]
                a,b=cycle[:-1],cycle[1:]
                affinity=np.sum(np.log(observation[a,b]/observation[b,a]))
                cycle_max=max(cycle_max,abs(affinity))
    exact_words=[]
    for length in [3,4,5]:
        symbols=np.array(list(product(range(n+1),repeat=length)))
        probs=pi*(symbols[:,0,None]==count)
        for k in range(1,length):
            probs=(probs@observation)*(symbols[:,k,None]==count)
        f=probs.sum(axis=1)
        rev=np.ravel_multi_index(symbols[:,::-1].T,[n+1]*length)
        positive=f>0
        exact_words.append(np.dot(f[positive],np.log(f[positive]/f[rev[positive]])))
    return full,pair,pi,cycle_max,*exact_words


rows=[]
for name,layout in [("same_plus",[hi]*4),("same_minus",[lo]*4),("alternating",[hi,lo,hi,lo]),
                    ("mixed",[hi,hi,hi,lo])]:
    for mutation in [.001,.01,.05]:
        for mode in ["selection","neutral","decoupled"]:
            full,pair,pi,cycle,*sequence=model(layout,mutation,mode)
            if mode=="neutral":
                assert abs(full)<1e-12
            rows.append((name,mutation,mode,full,pair,pi@configurations.sum(axis=1)/n,cycle,*sequence))
cols=["layout","mutation","mode","full_KL","count_KL","open_share","max_cycle_affinity","D3","D4","D5"]
pd.DataFrame(rows,columns=cols).to_csv(out/"markov.csv",index=False)
