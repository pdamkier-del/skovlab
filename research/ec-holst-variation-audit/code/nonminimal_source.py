"""Explicit variation of the nonminimal Hermitian spin-connection term.
This checks an action/gamma convention, not a guessed intermediate trace label.
"""
import json,itertools
from pathlib import Path
import numpy as np
from geometry import ETA,E

def main():
 I=np.eye(2);Z=np.zeros((2,2));sig=np.array([[[0,1],[1,0]],[[0,-1j],[1j,0]],[[1,0],[0,-1]]],complex)
 G=np.array([np.block([[Z,I],[I,Z]])]+[np.block([[Z,s],[-s,Z]])for s in sig]);G5=-1j*G[0]@G[1]@G[2]@G[3]
 P=-1j*G;P5=1j*P[0]@P[1]@P[2]@P[3];assert np.max(abs(P5+G5))<1e-14
 rng=np.random.default_rng(627);rows=[]
 for alpha,betaN in [(0.,0.),(.2,-.4),(-.3,.5)]:
  psi=rng.normal(size=4)+1j*rng.normal(size=4);bar=psi.conj()@G[0];V=np.array([(bar@g@psi).real for g in G]);A=np.array([(bar@G5@g@psi).real for g in G]);errors=[]
  for mu in range(4):
   for a in range(4):
    for b in range(a+1,4):
     C=np.zeros((4,4,4));C[a,mu,b]=1;C[b,mu,a]=-1
     Om=np.array([sum(C[ii,k,jj]*(P[ii]@P[jj]-P[jj]@P[ii])/8 for ii,jj in itertools.product(range(4),repeat=2))for k in range(4)])
     pref=np.eye(4)-1j*alpha*np.eye(4)-1j*betaN*P5
     actual=-sum((bar@pref@P[k]@Om[k]@psi).real for k in range(4))
     T=C-np.transpose(C,(0,2,1));tc=np.array([sum(ETA[ii]*T[ii,j,ii]for ii in range(4))for j in range(4)]);q=np.einsum('abcd,abc->d',-E,T)
     expected=-np.sum(ETA*q*A)/8+tc@(-alpha*V+betaN*A)/2;errors.append(abs(actual-expected))
  assert max(errors)<1e-12
  rows.append({'alpha_p':alpha,'beta_nonminimal_p':betaN,'max_connection_source_error':float(max(errors))})
 result={'primary_source':'https://arxiv.org/html/2406.14982v2','equation':'27, with row adjoint bar_p=psi^dagger i gamma_p^0 and h.c. of the Hermitian scalar density','explicit_map':'gamma_p=-i gamma_here; gamma5_p=-gamma5_here; V_p=V_here; A_p=-A_here; compatible spin representation fixed explicitly.','derived_source':'-q.A/8 + t.(-alpha_p V + beta_N,p A)/2','own_trace_parameter_map':'J=-(a_N V+nu_N A)/2: a_N=alpha_p, nu_N=-beta_N,p, agreeing with independently matched effective formulas.','checks':rows,'limit':'Intermediate printed torsion/trace symbol signs in Eq29 still need their own derivative-index dictionary; this action-level test does not assume those labels. No quantum state or nonminimal cutoff certified.'}
 (Path(__file__).resolve().parents[1]/'results/07_nonminimal_action_source.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS explicit nonminimal action spin-source variation in all 24 directions')
if __name__=='__main__':main()
