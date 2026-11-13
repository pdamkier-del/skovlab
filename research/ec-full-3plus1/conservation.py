"""Independent finite-difference divergence of the full effective stress."""
import argparse,json
from pathlib import Path
import numpy as np
from ecd import Grid,rk4,derivatives,matter
from initial_data import solve_constraints


def measure(n=9):
    grid=Grid(n);state,_=solve_constraints(grid);snap=[];h=.005
    for step in range(3):
        dg,_=derivatives(grid,state[0],state[1]);src=matter(state[0],dg,state[2],grid.grad(state[2]))
        inv=src['frame']['inv'];T=inv@src['stress']@inv
        snap.append((T,src['frame']['connection']))
        if step<2:state=rk4(grid,state,h)
    T,con=snap[1];dt=(snap[2][0]-snap[0][0])/(2*h);ds=grid.grad(T)
    div=dt[...,0,:]+np.einsum('...iin->...n',ds[..., :,1:,:])+np.einsum('...mml,...ln->...n',con,T)+np.einsum('...nml,...ml->...n',con,T)
    nodes=np.rint((np.array([-1.,0.,1.])+4)/grid.dx).astype(int);common=np.ix_(nodes,nodes,nodes)
    return {'n':n,'stress_divergence_L2_common':float(np.sqrt(np.mean(div[common]**2))),'stress_divergence_max_common':float(np.max(np.abs(div[common])))}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--n',type=int,nargs='+',default=[9,17,33]);parser.add_argument('--output',type=Path);args=parser.parse_args()
    records=[measure(n) for n in args.n]
    report={'records':records,'scope':'Finite-difference covariant divergence of complete effective stress at t=.005; no global energy integral imposed.'}
    if args.output:args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
