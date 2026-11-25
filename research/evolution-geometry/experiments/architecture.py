"""Natural selection among inherited local conductance masks, with site-local reservoirs."""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

parser=argparse.ArgumentParser()
parser.add_argument("results",type=Path)
out=parser.parse_args().results
out.mkdir(exist_ok=True,parents=True)

axes=[1,2,3]
bits=[1,2,4]
codes=np.array([0,1,1,2,1,2,2,3])
sides=[(axis,sign) for axis in axes for sign in [-1,1]]
rows=[]
networks=[]
for L in [10,16]:
    for environment in ["uniform","layered","patches"]:
        for start in ["balanced","line_biased","space_biased"]:
            for mode in ["selection","neutral","decoupled"]:
                runs=12
                rng=np.random.default_rng(81249)
                probabilities={"balanced":[1/9]*6+[1/3],
                               "line_biased":[.27,.27,.27,.05,.05,.05,.04],
                               "space_biased":[.025,.025,.025,.025,.025,.025,.85]}[start]
                # Distribute initial weight uniformly among permutations of each rank.
                if start=="balanced":
                    probabilities=[1/9,1/9,1/9,1/9,1/9,1/9,1/3]
                options=[1,2,4,3,5,6,7]
                traits=rng.choice(options,size=(runs,L,L,L),p=probabilities).astype(np.uint8)
                E=np.full(traits.shape,.7)
                Q=np.full(traits.shape,1.3)
                heat=np.indices((L,L,L))
                x,y,z=heat/L
                phase=rng.uniform(0,2*np.pi,size=(runs,1,1,1))
                total0=(E+Q).sum(axis=(1,2,3))
                for t in range(801):
                    if t in [0,40,120,300,600,800]:
                        for index in range(runs):
                            ranks=codes[traits[index]]
                            shares=[float(np.mean(ranks==d)) for d in [1,2,3]]
                            open_fraction=np.mean([np.mean(((traits[index]&bit)>0)&
                                                       ((np.roll(traits[index],-1,i)&bit)>0))
                                                    for i,bit in enumerate(bits)])
                            axis_shares=[float(np.mean((traits[index]&bit)>0)) for bit in bits]
                            es=float(E[index].std())
                            balance=float((E[index]+Q[index]).sum()-total0[index])
                            assert abs(balance)<1e-8
                            rows.append((L,environment,start,mode,index+1,t,*shares,*axis_shares,
                                         open_fraction,es,balance))
                            if index<4 and t in [0,300,800] and start=="balanced":
                                networks.append((L,environment,mode,index+1,t,traits[index].ravel().tolist()))
                    if t==800:
                        break
                    # Local season redistributes Q_i to E_i. Its form contains no trait reward.
                    theta=2*np.pi*t/27+phase
                    if environment=="uniform":
                        pump=.14+.08*np.cos(theta)
                    elif environment=="layered":
                        pump=.14+.08*np.cos(theta+2*np.pi*x)
                    else:
                        pump=.14+.08*np.cos(theta+2*np.pi*(x+y+z)) * np.cos(2*np.pi*y)
                    paid=pump*Q
                    returned=.13*E
                    E+=paid-returned
                    Q+=returned-paid
                    net=np.zeros_like(E)
                    for axis,bit in zip(axes,bits):
                        candidate=np.roll(traits,-1,axis)
                        gate=np.ones_like(E) if mode=="decoupled" else ((traits&bit)>0)&((candidate&bit)>0)
                        flux=.11*gate*(np.roll(E,-1,axis)-E)
                        net+=flux-np.roll(flux,1,axis)
                    E+=net
                    # All types compete along the same six birth edges.
                    direction=rng.integers(6,size=E.shape)
                    candidate=np.empty_like(traits)
                    neighbour_E=np.empty_like(E)
                    for digit,(axis,step) in enumerate(sides):
                        active=direction==digit
                        candidate[active]=np.roll(traits,step,axis)[active]
                        neighbour_E[active]=np.roll(E,step,axis)[active]
                    advantage=neighbour_E-E
                    replacement=.20/(1+np.exp(-6*advantage)) if mode!="neutral" else .1
                    traits=np.where(rng.random(E.shape)<replacement,candidate,traits)
                    # Symmetric graph-bit mutations on nonempty subsets.
                    mutation=rng.random(E.shape)<.003
                    flip=rng.choice(bits,size=E.shape).astype(np.uint8)
                    new=traits^flip
                    traits=np.where(mutation&(new>0),new,traits)
cols=["L","env","start","mode","seed","t","rank1","rank2","rank3","axis_x","axis_y","axis_z","edges",
      "reserve_sd","balance"]
pd.DataFrame(rows,columns=cols).to_csv(out/"architecture.csv",index=False)
(out/"architectures.json").write_text(json.dumps(networks,separators=(",",":")))
