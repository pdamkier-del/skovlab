"""Independent local all-metric-component, axial Ward and chiral-source tests."""
import json,itertools
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from ech import *
import reference_ecd as old

EPS=np.zeros((4,4,4,4))
for perm in itertools.permutations(range(4)):EPS[perm]=(-1)**sum(perm[i]>perm[j]for i in range(4)for j in range(i+1,4))

def original_contortion(g,df,A,f,M):
 inv=np.linalg.inv(g);D=1+16*f*f/M**4;q=24/(M*M*D)*(inv@df+A/8);tc=-f/(M*M)*(g@q)
 T=np.array([[[(g[a,c]*tc[b]-g[a,b]*tc[c])/3-np.sqrt(-np.linalg.det(g))*EPS[a,b,c]@q/6 for c in range(4)]for b in range(4)]for a in range(4)])
 C=np.array([[[(T[a,b,c]-T[b,c,a]+T[c,a,b])/2 for c in range(4)]for b in range(4)]for a in range(4)])
 return C

def original_aux_density(e,C,df,f,U,psi,jets,M,mass):
 inv=e@np.diag(ETA)@e.T;g=np.linalg.inv(inv);vol=1/np.linalg.det(e);up=np.einsum('ar,rcb->acb',inv,C)
 R=np.einsum('ace,edb->abcd',up,up)-np.einsum('ade,ecb->abcd',up,up)
 rc=np.einsum('bd,abad->',inv,R);ep=-EPS/vol;holst=np.einsum('abcd,ar,rbcd->',ep,g,R)
 T=C-np.transpose(C,(0,2,1));q=np.einsum('abcd,abc->d',ep,T)
 bar=psi.conj()@GAMMA[0];cur=np.einsum('ma,aij->mij',e,GAMMA);A=e@np.array([(bar@a@psi).real for a in AX])
 kin=.5j*(np.einsum('i,mij,mj->',bar,cur,jets)-np.einsum('mi,mij,j->',jets.conj()@GAMMA[0],cur,psi))
 return float((vol*(M*M*rc/2+f*holst-df@q-q@g@A/8+kin-mass*np.sum(bar*psi)-U)).real)

def old_basis_map():
 # Solve old_gamma S=S new_gamma without assuming representations identical.
 mat=np.concatenate([np.kron(np.eye(4),a)-np.kron(b.T,np.eye(4))for a,b in zip(old.GAMMA,GAMMA)])
 _,_,vh=np.linalg.svd(mat);U=vh[-1].conj().reshape(4,4,order='F');U*=np.sqrt(4/np.trace(U.conj().T@U).real)
 assert np.max(abs(U.conj().T@U-np.eye(4)))<1e-13
 assert max(np.max(abs(a@U-U@b))for a,b in zip(old.GAMMA,GAMMA))<1e-13
 return U

def main():
 rng=np.random.default_rng(901);p=Parameters();records=[];Uold=old_basis_map()
 for case in range(6):
  a=rng.normal(size=(3,3))*.1;sp=np.eye(3)+a@a.T;N=.7+.1*case;shift=rng.normal(size=3)*.1
  metric=np.zeros((4,4));metric[1:,1:]=sp;metric[0,1:]=metric[1:,0]=sp@shift;metric[0,0]=-N*N+shift@sp@shift
  psi=(rng.normal(size=4)+1j*rng.normal(size=4))*.05;dp=(rng.normal(size=(3,4))+1j*rng.normal(size=(3,4)))*.01
  dphi=rng.normal(size=4)*.02;phi=np.asarray(.2);dg=np.zeros((4,4,4));src=source(metric,dg,psi,dp,phi,dphi,p);f=src['frame'];e=f['e'];bar=psi.conj()@GAMMA[0];A=src['axial'];A2=src['A2'];C=src['couplings'];jets=np.r_[src['dtpsi'][None,:],dp]
  def action(ee):
   inv=ee@np.diag(ETA)@ee.T;cur=np.einsum('ma,aij->mij',ee,GAMMA)
   kin=.5j*(np.einsum('i,mij,mj->',bar,cur,jets)-np.einsum('mi,mij,j->',jets.conj()@GAMMA[0],cur,psi))
   Ac=ee@A
   return float(((kin-p.mass*np.sum(bar*psi)-C['h']*dphi@Ac-C['g']*A2-.5*dphi@inv@dphi-C['V'])/np.linalg.det(ee)).real)
  # Symmetric inverse-metric variation and symmetric tetrad lift; all ten directions.
  maxstress=0.;maxorig=0.;CC=original_contortion(metric,C['fphi']*dphi,src['Acoord'],C['f'],p.M);vol=np.sqrt(-np.linalg.det(metric));eps=1e-5
  for mu in range(4):
   for nu in range(mu,4):
    v=np.zeros((4,4));v[mu,nu]=1;v[nu,mu]=1
    ep=expm(.5*eps*v@metric)@e;em=expm(-.5*eps*v@metric)@e
    derivative=(action(ep)-action(em))/(2*eps)
    expected=-.5*vol*np.sum(src['T']*v);maxstress=max(maxstress,abs(derivative-expected))
    orig=(original_aux_density(ep,CC,C['fphi']*dphi,C['f'],C['V'],psi,jets,p.M,p.mass)-original_aux_density(em,CC,C['fphi']*dphi,C['f'],C['V'],psi,jets,p.M,p.mass))/(2*eps)
    maxorig=max(maxorig,abs(orig-expected))
  assert maxstress<1e-9,maxstress
  assert maxorig<1e-9,maxorig
  # Compatible lowered contortion is held independent, antisymmetric in first/third.
  ce=0.
  for ii in range(4):
   for aa in range(4):
    for bb in range(aa+1,4):
     d=np.zeros((4,4,4));d[aa,ii,bb]=1;d[bb,ii,aa]=-1
     v=(original_aux_density(e,CC+eps*d,C['fphi']*dphi,C['f'],C['V'],psi,jets,p.M,p.mass)-original_aux_density(e,CC-eps*d,C['fphi']*dphi,C['f'],C['V'],psi,jets,p.M,p.mass))/(2*eps)
     ce=max(ce,abs(v))
  assert ce<1e-9,ce
  # Arbitrary metric first jets exercise spin connection and no assumed lapse/shift.
  dg=rng.normal(size=(4,4,4))*.01;dg=(dg+np.swapaxes(dg,-1,-2))/2
  cur=source(metric,dg,psi,dp,phi,dphi,p)
  ff=cur['frame'];dcgam=np.einsum('mna,aij->mnij',ff['de'],GAMMA);compat=0.
  for mu in range(4):
   for nu in range(4):
    comp=dcgam[mu,nu]+np.einsum('l,lij->ij',ff['connection'][nu,mu],ff['gamma'])+ff['omega'][mu]@ff['gamma'][nu]-ff['gamma'][nu]@ff['omega'][mu]
    compat=max(compat,float(np.max(abs(comp))))
  assert compat<1e-12
  ward=abs(cur['axial_divergence']+2*p.mass*cur['pseudoscalar_bilinear']);assert ward<1e-13
  # Instantaneous EC source limit only; heavy pseudoscalaron is removed for the actual c->0 theory.
  pc=Parameters(beta=0.,c=p.c,mass=p.mass);ec=source(metric,dg,psi,dp,np.asarray(0.),np.zeros(4),pc)
  ref=old.matter(metric,dg,Uold@psi,np.einsum('ab,ib->ia',Uold,dp),mass=p.mass,kappa=1.)
  ecerr=max(np.max(abs(ref['stress']-ec['T'])),np.max(abs(ref['dt']-Uold@ec['dtpsi'])));assert ecerr<1e-12
  # Normal energy from the canonical Legendre expression, not unchanged free stress.
  nn=cur['frame']['e'][:,0];Pi=nn@dphi;iv3=np.linalg.inv(metric[1:,1:]);Asp=cur['Acoord'][1:]+cur['frame']['shift']*cur['Acoord'][0]
  split=.5*(Pi*Pi+dphi[1:]@iv3@dphi[1:])+C['V']+p.mass*cur['scalar_bilinear']+np.sum(iv3*cur['KD'][1:,1:])+C['h']*Asp@dphi[1:]+C['g']*cur['A2']
  energy_error=abs(split-cur['rho']);assert energy_error<1e-13
  # Chiral transformation removes derivative coupling from the classical principal part.
  X=C['X'];theta=.75*(np.arctan(np.sinh(X))-np.arctan(4*p.beta/p.M**2));R=expm(1j*theta*G5);chi=R.conj().T@psi
  Dchi=np.einsum('ab,mb->ma',R.conj().T,src['Dpsi']-1j*C['h']*dphi[:,None]*np.einsum('ab,b->a',G5,psi)[None,:])
  massmatrix=p.mass*expm(2j*theta*G5)
  resid=1j*np.einsum('mij,mj->i',f['gamma'],Dchi)-massmatrix@chi-2*C['g']*sum(ETA[b]*A[b]*(AX[b]@chi)for b in range(4))
  assert np.max(abs(resid))<1e-13
  records.append({'case':case,'lapse':N,'shift':shift.tolist(),'all_ten_metric_variation_error':maxstress,'original_metric_at_fixed_contortion_error':maxorig,'original_24_contortion_Euler_error':ce,'axial_Ward_error':float(ward),'metric_Clifford_compatibility_error':compat,'ADM_Legendre_energy_error':float(energy_error),'PR2_EC_source_limit_error':float(ecerr),'chiral_rotated_Dirac_error':float(np.max(abs(resid)))})
 result={'fixed_action_parameters':p.__dict__,'arbitrary_ADM_point_tests':records,'scope':'General local metric/source/Dirac tests, not a PDE evolution. Classical Ward identity omits quantum anomalies. EC comparison is an instantaneous source limit, not a claim that scalar phi=0 is a consistent massive-sector evolution.'}
 (Path(__file__).resolve().parents[1]/'results/01_local_variation.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS all ten metric variations, general-lapse/shift Ward identity, PR2 EC limit and chiral source')
if __name__=='__main__':main()
