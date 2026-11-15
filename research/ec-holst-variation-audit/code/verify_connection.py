"""Independent 24-component connection variation, gamma source, and elimination."""
import json,itertools
from pathlib import Path
import numpy as np
from geometry import ETA,E,torsion,contortion,contractions

def main():
 basis=[]
 for mu in range(4):
  for a in range(4):
   for b in range(a+1,4):
    C=np.zeros((4,4,4));C[a,mu,b]=1;C[b,mu,a]=-1;basis.append(C)
 basis=np.array(basis);n=24
 # Direct affine quadratic Hessians, not a supplied irreducible Lagrangian.
 vals=np.array([contractions(C)[:2] for C in basis]);H=np.zeros((2,n,n))
 for i in range(n):
  H[:,i,i]=2*vals[i]
  for j in range(i):
   z=np.array(contractions(basis[i]+basis[j])[:2])-vals[i]-vals[j];H[:,i,j]=H[:,j,i]=z
 # R' derivative term integrate by parts against f(x).
 derivative=np.zeros((4,n))
 for mu in range(4):
  for j,C in enumerate(basis):
   dC=np.zeros((4,4,4,4));dC[mu]=C;derivative[mu,j]=contractions(np.zeros_like(C),dC)[1]
 I=np.eye(2);Z=np.zeros((2,2));sigma=np.array([[[0,1],[1,0]],[[0,-1j],[1j,0]],[[1,0],[0,-1]]],complex)
 gamma=np.array([np.block([[Z,I],[I,Z]])]+[np.block([[Z,s],[-s,Z]]) for s in sigma]);g5=-1j*gamma[0]@gamma[1]@gamma[2]@gamma[3]
 rng=np.random.default_rng(610);records=[]
 for f,Jscale in itertools.product([0.,.03,-.4,2.],[0.,.1]):
  M2=1.7;df=rng.normal(size=4)*.1;psi=rng.normal(size=(3,4))+1j*rng.normal(size=(3,4));bar=psi.conj()@gamma[0]
  A=np.einsum('fi,aij,fj->a',bar,np.array([g5@g for g in gamma]),psi).real
  spin=np.zeros(n)
  for j,C in enumerate(basis):
   om=np.array([-sum(C[a,mu,b]*(gamma[a]@gamma[b]-gamma[b]@gamma[a])/8 for a in range(4) for b in range(4)) for mu in range(4)])
   spin[j]=sum((.5j*np.einsum('fi,ij,fj->',bar,gamma[mu]@om[mu]+om[mu]@gamma[mu],psi)).real for mu in range(4))
  J=rng.normal(size=4)*Jscale;trace_basis=np.array([[sum(ETA[a]*(C[a,b,a]-C[a,a,b]) for a in range(4)) for C in basis] for b in range(4)]);hess=M2/2*H[0]+f*H[1];linear=-df@derivative+spin+J@trace_basis;x=np.linalg.solve(hess,-linear);C=np.einsum('i,iabc->abc',x,basis)
  q=24/(M2*(1+16*f*f/M2**2))*(ETA*df+A/8+f/M2*J);t_cov=-f/M2*ETA*q+3/(2*M2)*ETA*J
  expected=contortion(torsion(t_cov,q));err=np.max(abs(C-expected));assert err<1e-12,err
  on=.5*x@hess@x+linear@x;target=3/(4*M2)*np.sum(ETA*J*J)-12/(M2*(1+16*f*f/M2**2))*np.sum(ETA*(ETA*df+A/8+f/M2*J)**2)
  assert abs(on-target)<1e-11
  # All 24 first variations vanish; remaining tensor torsion is not prescribed away.
  records.append({'f':f,'trace_source_norm':float(np.linalg.norm(J)),'hessian_rank':int(np.linalg.matrix_rank(hess)),'max_full_connection_error':float(err),'max_Euler_residual':float(np.max(abs(hess@x+linear))),'on_shell_action_error':float(abs(on-target))})
 geom=[]
 for _ in range(5):
  tc=rng.normal(size=4);q=rng.normal(size=4);R,P,_=contractions(contortion(torsion(tc,q)))
  er=R-(-2/3*np.sum(ETA*tc*tc)+np.sum(ETA*q*q)/24);ep=P+2/3*np.dot(tc,q)
  assert abs(er)<1e-13 and abs(ep)<1e-13;geom.append([float(er),float(ep)])
 result={'conventions':'eta=(-+++), epsilon_lower0123=+1, Rprime=epsilon^abcd R_abcd, C_abc=-C_cba, derivative index middle. alpha=M^2/2.','direct_affine_irreducible_checks':geom,'full_24_component_variations':records,'Rprime_identity':'Rprime=div(q)-(2/3)t.q + tensor-torsion quadratic part','eliminated_action':'Lred=3J^2/(4M^2)-12/[M^2(1+16 f^2/M^4)] (df+A/8+fJ/M^2)^2; contractions use metric.','qualification':'All 24 metric-compatible connection components varied; no nonmetricity sector or quantum stress solved.'}
 (Path(__file__).resolve().parents[1]/'results/01_connection_variation.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS full 24-component variation, gamma coupling and independent affine contractions')
if __name__=='__main__':main()
