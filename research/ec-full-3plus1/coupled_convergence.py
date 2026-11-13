"""Optional heavier weak-field refinement experiment (about 2 minutes locally)."""
import argparse,json,time
from pathlib import Path
import numpy as np
from ecd import Grid,rk4,diagnostics
from initial_data import solve_constraints


def run():
    states=[];runs=[]
    for n in [9,17,33]:
        start=time.monotonic();grid=Grid(n);state,report=solve_constraints(grid)
        for _ in range(2):state=rk4(grid,state,.005)
        ix=np.rint((np.array([-1.,0.,1.])+4)/grid.dx).astype(int);nodes=np.ix_(ix,ix,ix)
        states.append(tuple(x[nodes].copy() for x in state));d=diagnostics(grid,state)
        runs.append({'n':n,'initial':report,'seconds':time.monotonic()-start,
                     'hamiltonian_common_max':float(np.max(np.abs(d['hamiltonian'][nodes]))),
                     'gauge_common_max':float(np.max(np.abs(d['harmonic'][nodes])))})
    errors=[[float(np.linalg.norm(a-b)) for a,b in zip(states[i],states[i+1])] for i in range(2)]
    ratios=np.array(errors[0])/errors[1]
    success=bool(np.all((ratios>3)&(ratios<8)) and runs[2]['hamiltonian_common_max']<.5*runs[1]['hamiltonian_common_max'])
    return {'success':success,'parameters':{'half_width':4,'duration':.01,'dt':.005,'seed':'seed_spinor defaults, no additional spin twist','mass':.1,'kappa':1},
            'common_nodes':'Cartesian product of {-1,0,1} in each axis; exact shared grid nodes',
            'runs':runs,'common_node_state_differences':errors,'refinement_ratios':ratios.tolist(),
            'scope':'Short weak-field convergence evidence on 27 shared nodes, not a global-norm convergence or strong-collapse theorem.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path);args=p.parse_args();report=run()
    if args.output:args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2));raise SystemExit(0 if report['success'] else 1)
