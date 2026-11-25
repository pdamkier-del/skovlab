"""Competing degree-matched transport motifs with no curvature term in fitness."""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import linear_sum_assignment
from scipy.sparse.csgraph import shortest_path

p=argparse.ArgumentParser()
p.add_argument("output",type=Path)
out=p.parse_args().output
out.mkdir(exist_ok=True,parents=True)
N=16


def matrices(variant):
    A=np.zeros((N,N))
    def edge(i,j):
        A[i,j]=A[j,i]=1
    if variant=="cluster":
        for a in range(0,N,4):
            for i in range(a,a+4):
                for j in range(i+1,a+4):
                    if (i,j)!=(a,a+1):
                        edge(i,j)
            edge(a+1,(a+4)%N)
    else:
        for i in range(N):
            edge(i,(i+1)%N)
        # A fixed, reproducible long matching inside the same finite module.
        for i,j in [(0,8),(1,6),(2,10),(3,13),(4,12),(5,14),(7,15),(9,11)]:
            edge(i,j)
    assert np.all(A.sum(axis=1)==3)
    return A


def curvature(A):
    distance=shortest_path(A,directed=False,unweighted=True)
    results=[]
    for a,b in zip(*np.triu(A,1).nonzero()):
        left=[a]*3+list(A[a].nonzero()[0])
        right=[b]*3+list(A[b].nonzero()[0])
        cost=distance[np.ix_(left,right)]
        i,j=linear_sum_assignment(cost)
        results.append(1-cost[i,j].mean())
    return np.mean(results)


A0,A1=matrices("cluster"),matrices("open")
rho=[curvature(A) for A in (A0,A1)]
ring=np.roll(np.eye(N),1,axis=0)+np.roll(np.eye(N),-1,axis=0)
K=np.array([3*np.eye(N)-A for A in (A0,A1)])
Kr=2*np.eye(N)-ring
movement=.12
circulation=.09


def rates(donor,receiver):
    pump=np.full(N,.04)
    pump[donor]=.54
    upkeep=np.full(N,.10)
    upkeep[receiver]=.23
    return pump,upkeep


def steady(donor,receiver):
    a,b=rates(donor,receiver)
    solutions=[]
    for L in K:
        G=np.block([[-movement*L-np.diag(b),np.diag(a)],
                    [np.diag(b),-circulation*Kr-np.diag(a)]])
        assert np.max(abs(G.sum(axis=0)))<1e-12
        final=G.copy()
        final[-1]=1
        initial=np.zeros(2*N)
        initial[-1]=2*N
        z=np.linalg.solve(final,initial)
        assert np.all(z>0) and np.max(abs(G@z))<1e-12
        solutions.append(z)
    return np.array(solutions)


positions=[]
for donor in range(N):
    for receiver in range(N):
        if donor==receiver:
            continue
        z=steady(donor,receiver)
        positions.append((donor,receiver,z[0,receiver],z[1,receiver],z[0,receiver]-z[1,receiver],
                         rho[0],rho[1]))
cols=["donor","receiver","cluster_reserve","open_reserve","difference","kappa_cluster","kappa_open"]
table=pd.DataFrame(positions,columns=cols)
table.to_csv(out/"motif_equilibria.csv",index=False)


def population(donor,receiver,mode,wait):
    rng=np.random.default_rng(185752)
    runs,L=20,10
    shape=(runs,L,L)
    graph=(rng.random(shape)>.5).astype(int)
    initial=graph.copy()
    e=np.full((*shape,N),.7)
    q=np.full((*shape,N),1.3)
    eq=steady(donor,receiver)
    a,b=rates(donor,receiver)
    rows=[]
    iterations=300 if wait==0 else 85
    for t in range(iterations+1):
        budget=np.max(abs((e+q).sum(axis=-1)-2*N))
        assert budget<1e-8
        if t in [0,20,50,85,150,300]:
            for r in range(runs):
                mask=graph[r]==0
                rows.append((donor,receiver,mode,wait,r+1,t,mask.mean(),budget,
                             e[r,...,receiver][mask].mean() if mask.any() else np.nan,
                             e[r,...,receiver][~mask].mean() if (~mask).any() else np.nan))
        if t==iterations:
            break
        if not wait:
            index=initial if mode=="frozen" else graph
            local=eq[index,receiver]
            if mode=="decoupled":
                local=np.full(shape,eq[0,receiver])
        else:
            index=initial if mode=="frozen" else graph
            if mode=="decoupled":
                index=np.zeros_like(index)
            for _ in range(wait):
                delta=a*q-b*e
                flow=np.where(index[...,None]==0,e@K[0],e@K[1])
                next_q=q-delta-circulation*(q@Kr)
                e=e+delta-movement*flow
                q=next_q
            local=e[...,receiver]
        source=rng.integers(4,size=shape)
        chance=rng.random(shape)
        children=graph.copy()
        for k,(axis,sign) in enumerate([(1,-1),(1,1),(2,-1),(2,1)]):
            gap=np.roll(local,sign,axis)-local
            probability=.22/(1+np.exp(-36*gap)) if mode!="neutral" else .11
            copy=(source==k)&(chance<probability)
            children[copy]=np.roll(graph,sign,axis)[copy]
        graph=children^(rng.random(shape)<.004) if mode!="no_mutation" else children
    return rows


rows=[]
# Invasion tests chosen by whether the exact local model predicts opposite signs.
witness=table.query("donor==0")
receivers=[int(witness.loc[witness.difference.idxmax(),"receiver"]),
           int(witness.loc[witness.difference.idxmin(),"receiver"])]
assert witness.difference.min()<0<witness.difference.max()
for receiver in receivers:
    for mode in ["selection","neutral","decoupled","frozen","no_mutation"]:
        for wait in [0,12]:
            rows.extend(population(0,receiver,mode,wait))
cols=["donor","receiver","mode","relaxation_steps","seed","t","cluster_share","balance",
      "mean_cluster_reserve","mean_open_reserve"]
pd.DataFrame(rows,columns=cols).to_csv(out/"motif_population.csv",index=False)
