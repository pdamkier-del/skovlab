"""Natural selection among inherited local conductance masks, with site-local reservoirs."""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

parser=argparse.ArgumentParser()
parser.add_argument("results",type=Path)
stage=parser.add_mutually_exclusive_group()
stage.add_argument("--focused",action="store_true")
stage.add_argument("--replicate",action="store_true")
args=parser.parse_args()
out=args.results
out.mkdir(exist_ok=True,parents=True)

axes=[1,2,3]
bits=[1,2,4]
codes=np.array([0,1,1,2,1,2,2,3])
sides=[(axis,sign) for axis in axes for sign in [-1,1]]
rows=[]
networks=[]
stationarity=[]
environments=["strong_layers","strong_islands"] if args.focused else ["uniform","layered","patches"]
starts=["balanced"] if args.focused else ["balanced","line_biased","space_biased"]
sizes=[10,16]
modes=["selection","neutral","decoupled"]
if args.replicate:
    environments=["strong_layers","rotated_layers"]
    starts=["line_biased","space_biased"]
    sizes=[16]
    modes=["selection","neutral"]
for L in sizes:
    for environment in environments:
        for start in starts:
            for mode in modes:
                runs=12
                rng=np.random.default_rng(17071 if args.replicate else 81249)
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
                    if args.focused and t>=400 and t%2==0:
                        means=E.mean(axis=(1,2,3))
                        roughness=np.mean((E-np.roll(E,1,1))**2,axis=(1,2,3))
                        for j in range(runs):
                            stationarity.append((L,environment,mode,j+1,t,means[j],roughness[j]))
                    if t==800:
                        break
                    # Local season redistributes Q_i to E_i. Its form contains no trait reward.
                    theta=2*np.pi*t/27+phase
                    if environment=="uniform":
                        pump=.14+.08*np.cos(theta)
                    elif environment=="layered":
                        pump=.14+.08*np.cos(theta+2*np.pi*x)
                    elif environment=="patches":
                        pump=.14+.08*np.cos(theta+2*np.pi*(x+y+z)) * np.cos(2*np.pi*y)
                    elif environment in ["strong_layers","rotated_layers"]:
                        coordinate=x if environment=="strong_layers" else y
                        pump=.03+.47*(coordinate<.35)
                    else:
                        pump=.03+.47*((x-.5)**2+(y-.5)**2+(z-.5)**2<.27**2)
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
                    contrast=18 if args.focused or args.replicate else 6
                    replacement=.20/(1+np.exp(-contrast*advantage)) if mode!="neutral" else .1
                    traits=np.where(rng.random(E.shape)<replacement,candidate,traits)
                    # Symmetric graph-bit mutations on nonempty subsets.
                    mutation=rng.random(E.shape)<.003
                    flip=rng.choice(bits,size=E.shape).astype(np.uint8)
                    new=traits^flip
                    traits=np.where(mutation&(new>0),new,traits)
cols=["L","env","start","mode","seed","t","rank1","rank2","rank3","axis_x","axis_y","axis_z","edges",
      "reserve_sd","balance"]
suffix="_focused" if args.focused else "_replicate" if args.replicate else ""
pd.DataFrame(rows,columns=cols).to_csv(out/f"architecture{suffix}.csv",index=False)
if networks:
    (out/f"architectures{suffix}.json").write_text(json.dumps(networks,separators=(",",":")))
if args.focused:
    pd.DataFrame(stationarity,columns=["L","env","mode","seed","t","reserve","roughness"]
                 ).to_csv(out/"architecture_time.csv",index=False)
