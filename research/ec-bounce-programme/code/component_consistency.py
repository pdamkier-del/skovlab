"""Algebraic audit of the printed equal-time component generator (Eq.33).
The covariance interpretation is conditional: renormalized/subtracted currents
are not themselves occupation matrices. This does not refute a full 2PI theory.
"""
import json
from pathlib import Path
import numpy as np
import sympy as s

def main():
 x,y,z,X,Y,B,c,k,m=s.symbols('x y z X Y B c k m',real=True)
 printed=s.Matrix([-2*k*y+c*(B*y-z*Y/4),2*k*x-2*m*z-c*(B*x-z*X/4),2*m*y])
 defect=s.factor(2*(s.Matrix([x,y,z]).dot(printed)))
 required=c*(x*Y-y*X)/4
 completed=printed+s.Matrix([0,0,required]);assert s.simplify(2*s.Matrix([x,y,z]).dot(completed))==0
 assert s.simplify(defect-c*z*(y*X-x*Y)/2)==0
 # Full admissible Bloch matrices, two momenta for each helicity, trace one.
 f=np.array([[[.2,.1,-.4],[.1,-.25,-.3]],[[.2,-.1,.4],[.1,.25,.3]]]);weights=np.array([1e-4,2e-4]);mom=np.array([.01,.04]);mass=.1;coefficient=.75
 F=np.einsum('j,hja->ha',weights,f);F3tot=F[:,2].sum();P=np.zeros_like(f);C=np.zeros_like(f)
 for h in range(2):
  hh=1 if h==0 else -1;Xh,Yh,Zh=F[h];Bh=F3tot-Zh/4
  for j,p in enumerate(mom):
   xx,yy,zz=f[h,j];P[h,j]=[-2*hh*p*yy+coefficient*(Bh*yy-zz*Yh/4),2*hh*p*xx-2*mass*zz-coefficient*(Bh*xx-zz*Xh/4),2*mass*yy]
   C[h,j]=P[h,j]+[0,0,coefficient*(xx*Yh-yy*Xh)/4]
 defects=2*np.sum(f*P,axis=-1);resid=2*np.sum(f*C,axis=-1)
 assert np.max(abs(defects))>1e-7 and np.max(abs(resid))<1e-15
 vals=np.stack([(1-np.linalg.norm(f,axis=-1))/2,(1+np.linalg.norm(f,axis=-1))/2],axis=-1)
 assert vals.min()>0 and vals.max()<1
 result={'primary_source':'https://arxiv.org/html/1512.06074v1','equation':'33b-33d as printed, real mass; c=6 pi G_N xi^2/a^2, B=sum_h F3h-F3h/4','Bloch_length_squared_derivative':str(defect),'component_required_for_cross_product_completion':str(required),'admissible_full_covariance_eigenvalue_range':[float(vals.min()),float(vals.max())],'printed_generator_length_derivative':defects.tolist(),'cross_product_completion_residual':resid.tolist(),'classification':'The printed components cannot be used as an exact isospectral Hartree-Fock generator for a full equal-time covariance in general. If f denotes vacuum-subtracted/approximated currents, reference-source terms and approximation errors must be derived before interpreting it as a Pauli state.','limitation':'The completion is an algebraic consistency condition, not a validated replacement for the full renormalized 2PI equations. No published bounce is declared disproven.'}
 (Path(__file__).resolve().parents[1]/'results/07_component_consistency.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS component identity; nonzero printed full-covariance norm defect:',np.max(abs(defects)))
if __name__=='__main__':main()
