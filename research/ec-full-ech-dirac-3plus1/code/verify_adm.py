"""Independent Gauss/Codazzi and ADM evolution checks against 4D curvature.
Arbitrary metric first/second jets include varying lapse, shift and offdiagonal gamma.
"""
import json
from pathlib import Path
import numpy as np
from ech import *
from curvature import metric_curvature

def kinematics(g,dg):
 f=frame(g,dg);inv=f['inv'];N=f['N'];b=f['shift'];sp=g[1:,1:];di=-np.einsum('ab,lbc,cd->lad',inv,dg,inv);dN=.5*N**3*di[:,0,0];db=2*N*dN[:,None]*inv[None,0,1:]+N*N*di[:,0,1:]
 lie=np.einsum('k,kij->ij',b,dg[1:,1:,1:])+np.einsum('ik,jk->ij',sp,db[1:])+np.einsum('jk,ik->ij',sp,db[1:]);K=-(dg[0,1:,1:]-lie)/(2*N)
 return f,K,dN,db,lie

def main():
 rng=np.random.default_rng(913);rows=[]
 for case in range(5):
  sp=np.eye(3)+.1*rng.normal(size=(3,3));sp=sp@sp.T;N=.8+.1*case;b=rng.normal(size=3)*.15
  g=np.zeros((4,4));g[1:,1:]=sp;g[0,1:]=g[1:,0]=sp@b;g[0,0]=-N*N+b@sp@b
  dg=rng.normal(size=(4,4,4))*.04;dg=(dg+dg.swapaxes(-1,-2))/2
  dd=rng.normal(size=(4,4,4,4))*.03;dd=(dd+dd.swapaxes(0,1))/2;dd=(dd+dd.swapaxes(-1,-2))/2
  C4=metric_curvature(g,dg,dd);C3=metric_curvature(sp,dg[1:,1:,1:],dd[1:,1:,1:,1:]);f,K,dN,db,lie=kinematics(g,dg);iv=np.linalg.inv(sp);n=f['e'][:,0];E=np.einsum('a,ab,b',n,C4['G'],n);J=-np.einsum('ia,a->i',C4['G'][1:,:],n);S=C4['G'][1:,1:];tr=np.trace(iv@K)
  H=C3['scalar']+tr*tr-np.trace(iv@K@iv@K)-2*E;assert abs(H)<1e-12
  probes=[]
  for step in [1e-3,5e-4]:
   dk=[];dgradN=[]
   for mu in range(4):
    gp=g+step*dg[mu];gm=g-step*dg[mu];dp=dg+step*dd[mu];dm=dg-step*dd[mu]
    _,kp,np_,_,_=kinematics(gp,dp);_,km,nm,_,_=kinematics(gm,dm);dk.append((kp-km)/(2*step));dgradN.append((np_-nm)/(2*step))
   dk=np.asarray(dk);dgradN=np.asarray(dgradN);div=np.zeros(3);km=iv@K;dmix=[]
   for i in range(3):dmix.append(-iv@dg[i+1,1:,1:]@iv@K+iv@dk[i+1])
   dmix=np.array(dmix);con=C3['Gamma']
   for i in range(3):div[i]=sum(dmix[j,j,i]for j in range(3))-np.trace(dmix[i])+sum(con[j,j,l]*km[l,i]-con[l,j,i]*km[j,l]for j in range(3)for l in range(3))
   me=np.max(abs(div-J))
   hess=dgradN[1:,1:]-np.einsum('kij,k->ij',con,dN[1:])
   lieK=np.einsum('k,kij->ij',b,dk[1:])+np.einsum('ik,jk->ij',K,db[1:])+np.einsum('jk,ik->ij',K,db[1:])
   dg_rhs,dK_rhs,_=adm_rhs(sp,K,np.asarray(N),b,dN[1:],hess,C3['Ricci'],lie,lieK,E,J,S)
   ke=np.max(abs(dK_rhs-dk[0]));assert np.max(abs(dg_rhs-dg[0,1:,1:]))<1e-13
   probes.append({'tangent_step':step,'momentum_Codazzi_error':float(me),'extrinsic_evolution_error':float(ke)})
  assert probes[-1]['momentum_Codazzi_error']<1e-8 and probes[-1]['extrinsic_evolution_error']<1e-8
  rows.append({'case':case,'lapse':N,'shift':b.tolist(),'Hamiltonian_Gauss_error':float(abs(H)),'tangent_probes':probes})
 (Path(__file__).resolve().parents[1]/'results/03_ADM_geometry.json').write_text(json.dumps({'checks':rows,'scope':'Local geometric identities for arbitrary inhomogeneous jets, not a PDE evolution or a physical bounce.'},indent=2)+'\n');print('PASS general lapse/shift Gauss, Codazzi and ADM extrinsic evolution identities')
if __name__=='__main__':main()
