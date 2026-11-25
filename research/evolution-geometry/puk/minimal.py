"""One heritable bit, two local energy reservoirs, nearest-neighbour competition."""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

p=argparse.ArgumentParser()
p.add_argument("output",type=Path)
p.add_argument("--interfaces",action="store_true")
args=p.parse_args()
out=args.output
out.mkdir(exist_ok=True,parents=True)
network_samples=[]


def run(L,env,mode,start,total,beta,periodic,steps=480):
    rng=np.random.default_rng(153903+L)
    seeds=12
    shape=(seeds,L,L)
    gate=rng.random(shape)<start
    fixed=gate.copy()
    reserve=np.full(shape,.35*total)
    local_stock=np.full(shape,.65*total)
    x,y=np.indices((L,L))
    hot={"uniform":np.ones_like(x,dtype=bool),"x":x<L//3,"y":y<L//3,"repeated":x%12<4}[env]
    a=np.where(hot,.5,.03)
    trajectories=[]
    for t in range(steps+1):
        if t in [0,40,120,240,360,480] or (L==24 and env=="x" and (mode in ["selection","neutral","frozen"]) and t>=240 and t%2==0):
            for i in range(seeds):
                budget=np.sum(reserve[i]+local_stock[i])-total*L*L
                assert abs(budget)<1e-8
                current=fixed[i] if mode=="frozen" else gate[i]
                edges=current&np.roll(current,-1,0)
                if not periodic:
                    edges[-1,:]=False
                if mode=="decoupled":
                    edges=np.ones_like(edges)
                    if not periodic:
                        edges[-1,:]=False
                trajectories.append((L,env,mode,start,total,beta,periodic,i+1,t,gate[i].mean(),edges.mean(),
                                     reserve[i].mean(),np.mean((reserve[i]-np.roll(reserve[i],-1,0))**2),
                                     reserve[i][hot].mean(),reserve[i][~hot].mean() if np.any(~hot) else np.nan,budget))
        if t in [0,steps] and L in [12,24,40] and env=="x" and start==.5 and total==2 and beta==14 and periodic:
            bits=fixed if mode=="frozen" else np.ones_like(gate) if mode=="decoupled" else gate
            for seed in range(seeds):
                network_samples.append([L,mode,seed+1,t,bits[seed].ravel().astype(int).tolist()])
        if t==steps: break
        delta=a*local_stock-.13*reserve
        reserve+=delta
        local_stock-=delta
        for axis in [1,2]:
            if axis==1:
                conductive=gate&np.roll(gate,-1,axis)
                if mode=="decoupled":
                    conductive=np.ones(shape,dtype=bool)
                elif mode=="frozen":
                    conductive=fixed&np.roll(fixed,-1,axis)
            else:
                conductive=np.ones(shape,dtype=bool)
            flux=.16*conductive*(np.roll(reserve,-1,axis)-reserve)
            if not periodic:
                end=[slice(None)]*3
                end[axis]=-1
                flux[tuple(end)]=0.
            reserve+=flux-np.roll(flux,1,axis)
        source=rng.integers(4,size=shape)
        for axis in [1,2]:
            if not periodic:
                sl=[slice(None)]*3
                for sign in [-1,1]:
                    sl[axis]=0 if sign==1 else -1
                    boundary=source[tuple(sl)]==2*(axis-1)+(sign==1)
                    source[tuple(sl)][boundary]=4
        chance=rng.random(shape)
        mutates=rng.random(shape)<.003
        children=gate.copy()
        for code,(axis,sign) in enumerate([(1,-1),(1,1),(2,-1),(2,1)]):
            payoff=np.roll(reserve,sign,axis)-reserve
            velocity=.12 if mode=="neutral" else .24/(1+np.exp(-beta*payoff))
            copying=(source==code)&(chance<velocity)
            children[copying]=np.roll(gate,sign,axis)[copying]
        gate=children^mutates if mode!="no_mutation" else children
    return trajectories


rows=[]
if args.interfaces:
    for L in [12,24,36,48]:
        for env in ["x","repeated"]:
            for mode in ["selection","neutral"]:
                rows.extend(run(L,env,mode,.5,2.,14,True))
else:
    for L in [12,24,40]:
        for mode in ["selection","neutral","no_mutation","frozen","decoupled"]:
            for env in ["x","uniform"]:
                rows.extend(run(L,env,mode,.5,2.,14,True))
    for periodic in [True,False]:
        for start in [.15,.85]:
            for env in ["x","y"]:
                rows.extend(run(24,env,"selection",start,2.,14,periodic))
    for total in [.5,1.,4.,8.]:
        for beta in [14.,28/total]:
            rows.extend(run(24,"x","selection",.5,total,beta,True))
cols=["L","env","mode","start","energy_density","beta","periodic","seed","t","open","edge_x",
      "reserve","roughness","reserve_hot","reserve_cold","balance"]
name="interfaces.csv" if args.interfaces else "minimal.csv"
pd.DataFrame(rows,columns=cols).drop_duplicates().to_csv(out/name,index=False)
if args.interfaces:
    raise SystemExit
(out/"minimal_networks.json").write_text(json.dumps(network_samples,separators=(",",":")))

# An exact two-node limiting case for the same local reservoirs.
x=np.array([.5,.03])
b=.13
rows=[]
for total in [.5,2,8]:
    y0=x*total/(x+b)
    target=2*total/np.sum(1+b/x)
    for D in [0.,.02,.16]:
        e=np.full(2,total*.35)
        q=np.full(2,total*.65)
        for _ in range(30000):
            delta=x*q-b*e
            e+=delta
            q-=delta
            e+=D*(e[::-1]-e)
        predicted=y0 if D==0 else np.full(2,target)
        assert np.max(abs(e-predicted))<1e-9
        rows.append((total,D,*e,*predicted))
pd.DataFrame(rows,columns=["total","diffusion","hot","cold","predicted_hot","predicted_cold"]).to_csv(out/"two_sites.csv",index=False)
