"""Independent component connection and exact curvature for the C06 isotropic branch."""
import argparse,json
from pathlib import Path
import sympy as s
from itertools import permutations
# Exact n0=4,D0=0,kappa=1 massless harmonic solution: v=e^-3t, a=e^-t.
t=s.symbols('t',real=True);g=s.diag(-s.exp(-6*t),s.exp(-2*t),s.exp(-2*t),s.exp(-2*t));inv=g.inv()
G=[s.zeros(4) for _ in range(4)] # G[mu][r,nu]
G[0][0,0]=-3
for i in [1,2,3]:G[0][i,i]=-1;G[i][i,0]=-1;G[i][0,i]=-s.exp(4*t)
G[1][0,2]+=s.exp(4*t);G[2][0,1]-=s.exp(4*t)
G[0][1,2]+=1;G[2][1,0]-=1
G[0][2,1]-=1;G[1][2,0]+=1
R={}
for mu in range(4):
 for nu in range(4):
  R[mu,nu]=(s.diff(G[nu],t) if mu==0 else s.zeros(4))-(s.diff(G[mu],t) if nu==0 else s.zeros(4))+G[mu]*G[nu]-G[nu]*G[mu]
ric=s.Matrix(4,4,lambda sigma,nu:sum(R[rho,nu][rho,sigma] for rho in range(4)))
scalar=s.simplify(s.trace(inv*ric));kretsch=0
for r in range(4):
 for sigma in range(4):
  for mu in range(4):
   for nu in range(4):
    lower=g[r,r]*R[mu,nu][r,sigma]
    kretsch+=inv[r,r]*inv[sigma,sigma]*inv[mu,mu]*inv[nu,nu]*lower**2
assert scalar==0
assert s.simplify(kretsch-128*s.exp(12*t))==0
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
 result={'full_R':str(scalar),'full_K':str(s.simplify(kretsch)),'full_Ricci_coordinate_components':str(ric),'sympy':s.__version__,'classification':'Exact symbolic contraction from independently specified connection components; no numerical engine imports.'}
 args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n');print(result)

