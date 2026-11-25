"""Periodic cell problem for the axial diffusivity of a frozen inherited graph."""
import argparse
import gzip
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix, diags
from scipy.sparse.csgraph import connected_components
from scipy.sparse.linalg import spsolve

p=argparse.ArgumentParser()
p.add_argument("output",type=Path)
out=p.parse_args().output
source=out/"minimal_networks.json"
with (source.open() if source.is_file() else gzip.open(str(source)+".gz","rt")) as file:
    samples=json.load(file)


def homogenize(bits):
    L=bits.shape[0]
    cells=np.arange(L*L).reshape(L,L)
    x_edge=bits & np.roll(bits,-1,0)
    start=np.r_[cells[x_edge],cells.ravel()]
    end=np.r_[np.roll(cells,-1,0)[x_edge],np.roll(cells,-1,1).ravel()]
    step=np.zeros((len(start),2))
    step[:x_edge.sum(),0]=1
    step[x_edge.sum():,1]=1
    row=np.r_[start,end]
    col=np.r_[end,start]
    A=csr_matrix((np.ones(len(row)),(row,col)),shape=(L*L,L*L))
    number,groups=connected_components(A,directed=False)
    first_index=np.unique(groups,return_index=True)[1]
    K=diags(np.asarray(A.sum(axis=1)).ravel())-A
    rhs=np.zeros((L*L,2))
    np.add.at(rhs,start,step)
    np.add.at(rhs,end,-step)
    keep=np.ones(L*L,dtype=bool)
    keep[first_index]=False
    corrector=np.zeros_like(rhs)
    corrector[keep]=spsolve(K[keep][:,keep],rhs[keep])
    increment=step+corrector[end]-corrector[start]
    D=increment.T@increment/(L*L)
    assert D[0,0]<=x_edge.mean()+1e-10
    assert np.isclose(D[1,1],1) and abs(D[0,1])<1e-10
    return D[0,0],D[1,1],number


assert np.allclose(homogenize(np.ones((8,8),dtype=bool))[:2],[1,1])
assert np.allclose(homogenize(np.zeros((8,8),dtype=bool))[:2],[0,1])
rows=[]
for L,mode,seed,t,flat in samples:
    rows.append((L,mode,seed,t,*homogenize(np.array(flat,dtype=bool).reshape(L,L))))
pd.DataFrame(rows,columns=["L","mode","seed","t","D_x","D_y","components"]).to_csv(out/"conductance.csv",index=False)
