"""Measure coarse Ricci curvature and heat-return dimensions on evolving networks."""
import argparse
import gzip
import json
from math import lcm
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import linear_sum_assignment
from scipy.sparse import csr_matrix, diags, eye
from scipy.sparse.csgraph import connected_components

parser=argparse.ArgumentParser()
parser.add_argument("results",type=Path)
parser.add_argument("--kind",choices=["forest","architecture","calibration","all"],default="all")
args=parser.parse_args()
out=args.results
rng=np.random.default_rng(82712)
times=np.array([2,4,8,16,32,64,128])


def read_data(path):
    if path.is_file():
        return json.loads(path.read_text())
    with gzip.open(str(path)+".gz","rt") as handle:
        return json.load(handle)


def lattice(L,dim):
    grid=np.arange(L**dim).reshape((L,)*dim)
    return np.vstack([np.column_stack((grid.ravel(),np.roll(grid,-1,axis).ravel())) for axis in range(dim)])


def curvature(n,edges):
    if not len(edges):
        return np.nan,np.nan,np.nan,np.nan
    adjacent=[set() for _ in range(n)]
    for i,j in edges:
        adjacent[i].add(j)
        adjacent[j].add(i)
    sample=rng.choice(len(edges),size=min(60,len(edges)),replace=False)
    values=[]
    for i,j in edges[sample]:
        a,b=adjacent[i],adjacent[j]
        count=lcm(len(a),len(b))
        # Lazy walk with idleness 1/2; repeat each atom by its exact integer weight.
        left=sorted(a)+[i]
        right=sorted(b)+[j]
        cost=np.asarray([[0 if x==y else 1 if y in adjacent[x] else
                          2 if adjacent[x]&adjacent[y] else 3 for y in right] for x in left])
        m=cost.repeat([count//len(a)]*len(a)+[count],axis=0)
        m=m.repeat([count//len(b)]*len(b)+[count],axis=1)
        row,col=linear_sum_assignment(m)
        values.append(1-m[row,col].sum()/(2*count))
    a=np.asarray(values)
    return a.mean(),np.mean(a< -1e-10),np.mean(abs(a)<=1e-10),np.mean(a>1e-10)


def measures(n,edges):
    if not len(edges):
        return [0,1]+[np.nan]*(4+2*len(times)-1)
    i,j=edges.T
    row=np.r_[i,j]; col=np.r_[j,i]
    A=csr_matrix((np.ones(len(row)),(row,col)),shape=(n,n))
    c,labels=connected_components(A,directed=False)
    counts=np.bincount(labels,minlength=c)
    subset=np.flatnonzero(labels==counts.argmax())
    B=A[subset][:,subset]
    D=diags(np.asarray(B.sum(axis=1)).ravel()**-.5)
    transition=(eye(len(subset),format="csr")+D@B@D)*.5
    if len(subset)<=500:
        eig=np.linalg.eigvalsh(transition.toarray())
        heat=np.mean(eig[:,None]**times,axis=0)
    else:
        z=rng.choice([-1.,1.],size=(len(subset),24))
        evolved=z.copy()
        heat=[]
        next_sample=0
        for t in range(1,times[-1]+1):
            evolved=transition@evolved
            if t==times[next_sample]:
                heat.append(np.mean(z*evolved))
                next_sample+=1
        heat=np.array(heat)
    dimension=-2*np.diff(np.log(heat))/np.log(2)
    dimension=np.where(heat[1:]*len(subset)>=4,dimension,np.nan)
    return [len(edges),len(subset),*curvature(n,edges),*heat,*dimension]


metric_cols=["edges","largest","kappa","negative","zero","positive"]
metric_cols += [f"heat_{t}" for t in times]+[f"dimension_{t}" for t in times[:-1]]


def forest():
    rows=[]
    for geometry in [0,1,-1,"cliques","torus","regular"]:
        filename=out/f"snapshots_{geometry}.json"
        if not filename.is_file() and not Path(str(filename)+".gz").is_file():
            continue
        runs={}
        for snap in read_data(filename):
            L,seed,t,tr=(snap[k] for k in ["L","seed","t","treatment"])
            key=(L,seed,tr)
            labels=np.asarray(snap["labels"])
            traits=np.asarray(snap["strategies"])
            if t==0:
                substrate=np.array(snap["edges"])
                runs[key]=(substrate,labels.copy())
            edges,initial=runs[key]
            if t not in [0,60,260]:
                continue
            i,j=edges.T
            occupied=(labels[i]>=0)&(labels[j]>=0)
            def gates(a):
                return occupied & ((a[i]==a[j])|(abs(traits[a[i]]-traits[a[j]])<=.01+1e-12))
            shuffled=labels.copy()
            shuffled[labels>=0]=rng.permutation(shuffled[labels>=0])
            count=np.count_nonzero(gates(labels))
            reference=np.zeros(len(edges),dtype=bool)
            reference[rng.choice(np.flatnonzero(occupied),size=count,replace=False)]=True
            for mode,open_edges in [
                ("observed",gates(labels)),
                ("shuffled",gates(shuffled)),
                ("frozen_initial",gates(initial)),
                ("occupied_substrate",occupied),
                ("matched_edge_count",reference),
            ]:
                rows.append((geometry,L,seed,t,tr,mode,snap["density"],snap["balance"],
                             *measures(L*L,edges[open_edges])))
    base=["geometry","L","seed","t","treatment","mode","density","balance"]
    pd.DataFrame(rows,columns=base+metric_cols).to_csv(out/"forest_geometry.csv",index=False)


def architecture():
    rows=[]
    for L,env,mode,seed,t,traits in read_data(out/"architectures.json"):
        trait=np.array(traits)
        edges=lattice(L,3)
        i,j=edges.T
        orientation=np.repeat([1,2,4],L**3)
        active=((trait[i]&orientation)>0)&((trait[j]&orientation)>0)
        rows.append((L,env,mode,seed,t,*measures(L**3,edges[active])))
    pd.DataFrame(rows,columns=["L","env","mode","seed","t"]+metric_cols).to_csv(out/"architecture_geometry.csv",index=False)


def gasket(level):
    edges=[]
    def add(x,y,r):
        if r==1:
            a,b,c=(x,y),(x+r,y),(x,y+r)
            edges.extend([(a,b),(b,c),(a,c)])
        else:
            add(x,y,r//2)
            add(x+r//2,y,r//2)
            add(x,y+r//2,r//2)
    add(0,0,2**level)
    nodes={n for e in edges for n in e}
    lookup={a:i for i,a in enumerate(sorted(nodes))}
    return len(nodes),np.array([(lookup[a],lookup[b]) for a,b in edges])


def calibrate():
    rows=[]
    for d,L in [(1,256),(2,24),(3,12)]:
        edges=lattice(L,d)
        rows.append((f"torus_{d}D",d,len(np.unique(edges)),*measures(L**d,edges)))
    n,edges=gasket(6)
    rows.append(("sierpinski",2*np.log(3)/np.log(5),n,*measures(n,edges)))
    pd.DataFrame(rows,columns=["model","theory","N"]+metric_cols).to_csv(out/"calibration.csv",index=False)


if args.kind in ["forest","all"]:
    forest()
if args.kind in ["architecture","all"]:
    architecture()
if args.kind in ["calibration","all"]:
    calibrate()
