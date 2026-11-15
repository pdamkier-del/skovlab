"""Fixed-Minkowski, cutoff Gaussian Hartree-Fock audit for minimal ECD.
No FLRW evolution, curved-space renormalization or physical bounce is claimed.
"""
import json
from pathlib import Path
import numpy as np
from scipy.special import expit
from scipy.integrate import solve_ivp,quad
from numpy.polynomial.legendre import leggauss
G=3/16
MASS=.1;TEMP=.001;MU=.1

def grid(n,cutoff=.1):
 x,w=leggauss(n);p=cutoff*(x+1)/2;weight=w*cutoff/2*p*p/(2*np.pi**2)
 return p,weight

def initial(n,angle=0.,cutoff=.1):
 p,w=grid(n,cutoff);energy=np.hypot(p,MASS);fp=expit((MU-energy)/TEMP);fm=expit((-MU-energy)/TEMP)
 b=np.stack([np.broadcast_to(MASS,(2,n)),np.zeros((2,n)),np.array([1.,-1.])[:,None]*p],axis=-1)
 vacuum=-b/energy[None,:,None];u=1-fp-fm;r=vacuum*u[None,:,None]
 if angle:
  theta=np.array([1.,-1.])[:,None]*angle*np.exp(-(p/.03)**2)
  old=r.copy();r[:,:,0]=np.cos(theta)*old[:,:,0]+np.sin(theta)*old[:,:,2]
  r[:,:,2]=-np.sin(theta)*old[:,:,0]+np.cos(theta)*old[:,:,2]
 return {'p':p,'w':w,'b':b,'vacuum':vacuum,'charge_mode':fp-fm,'initial':r,'fp':fp,'fm':fm,'cutoff':cutoff}

def observables(r,ctx):
 w=ctx['w'];delta=r-ctx['vacuum'];D=2*np.sum(w*ctx['charge_mode']);S=np.sum(w[None,:]*delta[:,:,0]);kin=np.sum(w[None,:]*np.sum(ctx['b']*delta,axis=-1));Q=-D*D/2-S*S
 return dict(D=float(D),S=float(S),rho_free=float(kin),Q=float(Q),rho_total=float(kin+G*Q),mass_shift=float(-2*G*S))

def rhs(r,ctx):
 h=ctx['b'].copy();h[:,:,0]-=2*G*observables(r,ctx)['S']
 return 2*np.cross(h,r)

def rk4(r,dt,ctx):
 k1=rhs(r,ctx);k2=rhs(r+dt*k1/2,ctx);k3=rhs(r+dt*k2/2,ctx);k4=rhs(r+dt*k3,ctx)
 return r+dt*(k1+2*k2+2*k3+k4)/6

def eigvals(r,ctx):
 length=np.linalg.norm(r,axis=-1);trace=1+ctx['charge_mode'][None,:]
 return np.stack([(trace-length)/2,(trace+length)/2],axis=-1)

def gamma_checks():
 I=np.eye(2);Z=np.zeros((2,2));sigma=np.array([[[0,1],[1,0]],[[0,-1j],[1j,0]],[[1,0],[0,-1]]],complex)
 gamma=np.array([np.block([[Z,I],[I,Z]])]+[np.block([[Z,s],[-s,Z]]) for s in sigma]);g5=-1j*gamma[0]@gamma[1]@gamma[2]@gamma[3];M=np.array([gamma[0]@g5@g for g in gamma]);eta=np.array([-1,1,1,1])
 def Q(C):return float(sum(e*(np.trace(A@C)**2-np.trace(A@C@A@C)) for e,A in zip(eta,M)).real)
 def Sigma(C):return 2*G*sum(e*(np.trace(A@C)*A-A@C@A) for e,A in zip(eta,M))
 rng=np.random.default_rng(501);errs=[]
 for _ in range(6):
  z=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4));C=(z+z.conj().T)/20
  z=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4));d=(z+z.conj().T)/20
  numeric=G*(Q(C+1e-5*d)-Q(C-1e-5*d))/(2e-5);analytic=np.trace(Sigma(C)@d).real
  errs.append(float(abs(numeric-analytic)));assert errs[-1]<1e-10
 D=.03;S=.02;C=(D*np.eye(4)+S*gamma[0])/4
 error=np.max(abs(Sigma(C)-(-G*D*np.eye(4)-2*G*S*gamma[0])));assert error<1e-14
 return {'functional_gradient_errors':errs,'unpolarized_selfenergy_error':float(error)}

def main():
 checks=gamma_checks();thermal=[]
 for n in [48,96,192]:
  c=initial(n);o=observables(c['initial'],c);ev=eigvals(c['initial'],c)
  expected=np.stack([np.broadcast_to(c['fp'],(2,n)),np.broadcast_to(1-c['fm'],(2,n))],axis=-1)
  err=float(np.max(abs(np.sort(ev,axis=-1)-np.sort(expected,axis=-1))));assert err<1e-14
  thermal.append({'radial_nodes':n,**o,'occupation_spectrum_error':err,'occupation_min':float(ev.min()),'occupation_max':float(ev.max()),'max_initial_covariance_derivative':float(np.max(abs(rhs(c['initial'],c))))})
 # Independent adaptive radial integrals, at the precise predeclared state point.
 fun=lambda p:expit((MU-np.hypot(p,MASS))/TEMP)
 D=quad(lambda p:p*p*fun(p),0,.1,epsabs=1e-16,epsrel=1e-12)[0]/np.pi**2
 S=quad(lambda p:p*p*MASS/np.hypot(p,MASS)*fun(p),0,.1,epsabs=1e-16,epsrel=1e-12)[0]/np.pi**2
 assert abs(thermal[-1]['D']-D)<1e-15 and abs(thermal[-1]['S']-S)<1e-15
 # Admissible coherent perturbation, deliberately declared before evolution.
 # It rotates full covariance eigenvectors rather than assigning new occupations.
 c=initial(96,angle=.05);r0=c['initial'];E0=observables(r0,c)['rho_total'];lam0=eigvals(r0,c);duration=100.
 sol=solve_ivp(lambda t,y:rhs(y.reshape(r0.shape),c).ravel(),(0,duration),r0.ravel(),method='DOP853',rtol=2e-12,atol=2e-13)
 assert sol.success;ref=sol.y[:,-1].reshape(r0.shape);records=[]
 for steps in [64,128,256]:
  r=r0.copy();dt=duration/steps;maxE=maxL=0.
  for _ in range(steps):
   r=rk4(r,dt,c);maxE=max(maxE,abs(observables(r,c)['rho_total']-E0));maxL=max(maxL,float(np.max(abs(eigvals(r,c)-lam0))))
  records.append({'steps':steps,'covariance_endpoint_error':float(np.sqrt(np.mean((r-ref)**2))),'max_energy_drift_absolute':float(maxE),'max_energy_drift_over_initial_energy':float(maxE/abs(E0)),'max_occupation_eigenvalue_drift':maxL,'endpoint':observables(r,c)})
 ratios=[records[i]['covariance_endpoint_error']/records[i+1]['covariance_endpoint_error'] for i in range(2)]
 assert all(12<x<20 for x in ratios),ratios
 # Independent tangent check of the complete conserved functional, no EOS.
 d=rhs(r0,c);der=[]
 for eps in [1e-4,5e-5]:der.append((observables(r0+eps*d,c)['rho_total']-observables(r0-eps*d,c)['rho_total'])/(2*eps))
 assert max(abs(x) for x in der)<1e-15
 # Momentum quadrature convergence and cutoff sensitivity use independent high-order time solves.
 radial=[]
 for nodes in [48,96,192]:
  cc=initial(nodes,angle=.05);rr=cc['initial']
  zz=solve_ivp(lambda t,y:rhs(y.reshape(rr.shape),cc).ravel(),(0,duration),rr.ravel(),method='DOP853',rtol=2e-12,atol=2e-13)
  assert zz.success
  radial.append({'radial_nodes':nodes,'endpoint':observables(zz.y[:,-1].reshape(rr.shape),cc)})
 assert max(abs(z['endpoint']['S']-radial[-1]['endpoint']['S']) for z in radial)<1e-13
 cutoff_tests=[]
 for cutoff in [.08,.1,.12]:
  cc=initial(96,angle=.05,cutoff=cutoff);rr=cc['initial']
  zz=solve_ivp(lambda t,y:rhs(y.reshape(rr.shape),cc).ravel(),(0,duration),rr.ravel(),method='DOP853',rtol=2e-12,atol=2e-13)
  assert zz.success
  cutoff_tests.append({'cutoff':cutoff,'initial':observables(rr,cc),'endpoint':observables(zz.y[:,-1].reshape(rr.shape),cc)})
 checkpoint={'scope':'Regulated fixed-Minkowski Gaussian covariance, not a continuum quantum field checkpoint','mass':MASS,'G':G,'cutoff':c['cutoff'],'T':TEMP,'mu':MU,'time_initial':0.,'time_final':duration,'coherent_rotation_angle':.05,'momentum':c['p'].tolist(),'radial_weights':c['w'].tolist(),'trace_charge_mode':c['charge_mode'].tolist(),'vacuum_bloch':c['vacuum'].tolist(),'initial_full_bloch':r0.tolist(),'final_DOP853_full_bloch':ref.tolist(),'final_RK4_256_full_bloch':r.tolist(),'matrix_reconstruction':'R_h(p)=[(1+q(p)) I + r_h(p).sigma]/2; r axes mass-x, imaginary-y, helicity-z'}
 (Path(__file__).resolve().parents[1]/'results/06_covariance_modes.json').write_text(json.dumps(checkpoint,indent=2)+'\n')
 result={'scope':'Fixed Minkowski a=1, one unpolarized Dirac species, minimal G=3/16, fixed physical UV cutoff. Full covariance includes filled negative-energy reference; Q is vacuum-Wick ordered relative to that fixed vacuum.','parameters':{'mass':MASS,'T':TEMP,'mu':MU,'cutoff':.1,'proper_time_interval':[0,duration],'coherent_rotation_angle':.05,'rotation_envelope_momentum':.03},'matrix_checks':checks,'thermal_state_checks':thermal,'independent_adaptive_D':D,'independent_adaptive_S':S,'coherent_time_refinement':records,'observed_time_error_ratios':ratios,'radial_endpoint_refinement':radial,'cutoff_sensitivity':cutoff_tests,'energy_tangent_derivatives':der,'limitations':'Gaussian Hartree-Fock is a conserving truncation, not an error bound for omitted cumulants. No cosmological evolution, renormalized curved-space stress, stress-noise or actual bounce.'}
 (Path(__file__).resolve().parents[1]/'results/06_covariance_hf.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS covariance HF, occupations, energy gradient and RK4 refinement',ratios)
if __name__=='__main__':main()
