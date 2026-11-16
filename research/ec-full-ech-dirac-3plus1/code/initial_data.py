"""Cheap genuinely inhomogeneous constrained data: planar periodic T^3 lift.
The equations derived elsewhere have no symmetry assumption; only this test does.
"""
import json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_bvp
from ech import *
L=8.;KMODE=2*np.pi/L;PARS=Parameters()

def free_data(z,mode='echd'):
 n=1e-4*(1+.1*np.cos(KMODE*z));dn=-1e-5*KMODE*np.sin(KMODE*z)
 w=.2+.01*np.sin(KMODE*z);dw=.01*KMODE*np.cos(KMODE*z)
 if mode=='einstein_dirac':w=np.zeros_like(z);dw=np.zeros_like(z)
 return n,dn,w,dw

def seed_energy(y,z,mode):
 n,_,w,dw=free_data(z,mode);C=couplings(w,PARS);chi=np.exp(y)
 h=C['h'] if mode=='echd' else 0.;g=C['g'] if mode=='echd' else 0.
 return .5*dw*dw/chi**4+C['V']+PARS.mass*n/chi**6+g*n*n/chi**12+h*n*dw/chi**8

def construct(mode='echd'):
 def fun(z,y,p):
  n,_,w,dw=free_data(z,mode);C=couplings(w,PARS);h=C['h'] if mode=='echd' else 0.;g=C['g'] if mode=='echd' else 0.
  yy,dy,I=y
  accel=p[0]**2*np.exp(4*yy)/12-(dw*dw+2*C['V']*np.exp(4*yy)+2*PARS.mass*n*np.exp(-2*yy)+2*g*n*n*np.exp(-8*yy)+2*h*n*dw*np.exp(-4*yy))/(8*PARS.M**2)-dy*dy
  return np.array([dy,accel,yy])
 z=np.linspace(0,L,1025);guess=np.sqrt(3*np.mean(seed_energy(np.zeros_like(z),z,mode))/PARS.M**2)
 sol=solve_bvp(fun,lambda a,b,p:np.array([a[0]-b[0],a[1]-b[1],a[2],b[2]]),z,np.zeros((3,len(z))),p=[guess],tol=2e-13,max_nodes=5000)
 assert sol.success,sol.message
 return sol

def fd(a,dx):return (np.roll(a,-1,axis=0)-np.roll(a,1,axis=0))/(2*dx)
def fd2(a,dx):return (np.roll(a,-1,axis=0)-2*a+np.roll(a,1,axis=0))/dx**2

def fields(sol,n,mode='echd',analytic=False):
 z=np.arange(n)*L/n;dx=L/n;y=sol.sol(z)[0];chi=np.exp(y);n0,dn,w,dw=free_data(z,mode);ktr=float(sol.p[0])
 metric=np.zeros((n,4,4));metric[:,0,0]=-1;metric[:,1:,1:]=chi[:,None,None]**4*np.eye(3)
 K=ktr/3*metric[:,1:,1:];dg=np.zeros((n,4,4,4));dg[:,0,1:,1:]=-2*K
 psi=np.sqrt(n0/2)[:,None]*chi[:,None]**-3*np.array([1.,0,1.,0],complex)
 dp=np.zeros((n,3,4),complex);dphi=np.zeros((n,4));dphi[:,3]=dw if analytic else fd(w,dx)
 if analytic:
  yp=sol.sol(z)[1];dg[:,3,1:,1:]=4*yp[:,None,None]*metric[:,1:,1:];dp[:,2]=psi*(.5*dn/n0-3*yp)[:,None]
 else:dg[:,3]=fd(metric,dx);dp[:,2]=fd(psi,dx)
 src=source(metric,dg,psi,dp,w,dphi,PARS,interactions=mode=='echd')
 # Independent FD geometric scalar, not the BVP's ODE residual.
 R3=-8*fd2(chi,dx)/chi**5
 Ham=R3+2*ktr**2/3-2*src['rho']/PARS.M**2
 return {'z':z,'dx':dx,'chi':chi,'metric':metric,'dg':dg,'psi':psi,'dpsi':dp,'phi':w,'dphi':dphi,'K':K,'ktr':ktr,'src':src,'Hamiltonian':Ham}

def main():
 all_cases=[]
 for mode in ['echd','scalar_GR','einstein_dirac']:
  sol=construct(mode);rows=[]
  for n in [65,129,257]:
   f=fields(sol,n,mode);src=f['src'];a=fields(sol,n,mode,True);rho_formula=seed_energy(np.log(f['chi']),f['z'],mode)
   assert np.max(abs(a['src']['rho']-rho_formula))<1e-14
   assert np.max(abs(src['J']))<1e-13
   rows.append({'nodes':n,'Hamiltonian_max':float(np.max(abs(f['Hamiltonian']))),'momentum_max':float(np.max(abs(src['J']))),'normal_expansion':-f['ktr'],'rho_min':float(src['rho'].min()),'rho_max':float(src['rho'].max()),'analytic_full_source_formula_error':float(np.max(abs(a['src']['rho']-rho_formula)))})
  ratios=[rows[i]['Hamiltonian_max']/rows[i+1]['Hamiltonian_max']for i in range(2)];assert all(3.5<x<4.5 for x in ratios),ratios
  raw={'BVP_grid':sol.x.tolist(),'BVP_logchi':sol.y[0].tolist(),'BVP_derivative':sol.y[1].tolist(),'BVP_integral':sol.y[2].tolist(),'Ktrace':float(sol.p[0])}
  all_cases.append({'mode':mode,'collocation_residual_max':float(np.max(sol.rms_residuals)),'independent_refinement':rows,'Hamiltonian_error_ratios':ratios,'raw':raw})
 result={'main_action':PARS.__dict__,'topology':'T^3, coordinate lengths 8, exact x/y translations only in this numerical test','free_data':'n_seed=1e-4(1+.1 cos(kz)), phi=.2+.01 sin(kz), k=2pi/8, normal scalar Pi=0, rest spinor sqrt(n_seed/2) chi^-3(1,0,1,0), Kij=Ktrace gammaij/3','cases':all_cases,'controls':'scalar_GR removes derivative/contact interactions but retains an independent canonical scalar with same potential; einstein_dirac removes the torsion-origin scalar sector as well. Each theory solves its own constraints; neither is mislabeled as identical microscopic matter.','scope':'Constrained inhomogeneous classical initial data, no physical fermion state, bounce or spacetime evolution.'}
 (Path(__file__).resolve().parents[1]/'results/02_initial_data.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS mixed scalar/Dirac periodic constraints and separately constrained controls')
if __name__=='__main__':main()
