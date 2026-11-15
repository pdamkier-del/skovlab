"""A constrained inhomogeneous S^3 perturbation of a curvature-assisted turn.
Time-symmetric canonical-scalar data; not a nonlinear evolution or a flat bounce.
"""
import json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_bvp
from closed_turn import pot,MU2

def main():
 w0=.5;V0,_=pot(w0);b2=3/V0;out=[]
 for eps in [.001,.002]:
  def scalar(x):return w0+eps*(4*np.cos(x)**2-1),-8*eps*np.cos(x)*np.sin(x)
  def fun(x,y):
   w,dw=scalar(x);V,_=pot(w)
   regular=np.zeros_like(x);good=x>1e-6;regular[good]=1/np.tan(x[good])-1/x[good];regular[~good]=-x[~good]/3
   return np.array([y[1],(6*y[0]-y[0]*dw*dw-2*b2*y[0]**5*V)/8-2*regular*y[1]])
  grid=np.linspace(0,np.pi/2,97);S=np.diag([0.,-2.])
  sol=solve_bvp(fun,lambda a,b:np.array([a[1],b[1]]),grid,np.array([np.ones_like(grid),np.zeros_like(grid)]),S=S,tol=1e-10,max_nodes=4000)
  assert sol.success,sol.message
  refs=[]
  for n in [65,129,257]:
   x=np.linspace(0,np.pi,n);xx=np.minimum(x,np.pi-x);chi=sol.sol(xx)[0];w,dw=scalar(x);V,_=pot(w);dx=x[1]-x[0]
   grad=np.zeros(n);grad[1:-1]=(chi[2:]-chi[:-2])/(2*dx)
   second=np.zeros(n);second[1:-1]=(chi[2:]-2*chi[1:-1]+chi[:-2])/dx**2
   lap=second.copy();lap[1:-1]+=2/np.tan(x[1:-1])*grad[1:-1];lap[0]=6*(chi[1]-chi[0])/dx**2;lap[-1]=6*(chi[-2]-chi[-1])/dx**2
   residual=-8*lap+6*chi-chi*dw*dw-2*b2*chi**5*V
   refs.append({'nodes':n,'independent_FD_Hamiltonian_max':float(np.max(abs(residual))),'conformal_factor_min':float(chi.min()),'normal_Theta_dot_min_in_mu2':float(V.min()),'normal_Theta_dot_max_in_mu2':float(V.max())})
  ratios=[refs[i]['independent_FD_Hamiltonian_max']/refs[i+1]['independent_FD_Hamiltonian_max'] for i in range(2)]
  assert all(3.5<r<4.5 for r in ratios),ratios
  assert refs[-1]['conformal_factor_min']>0 and refs[-1]['normal_Theta_dot_min_in_mu2']>0
  # Linear solution, independent l=2 harmonic check: (Delta+3)u=-b^2 V_w eps Q/4.
  x=np.linspace(0,np.pi/2,33);Q=4*np.cos(x)**2-1;_,dV=pot(w0);u=b2*dV*eps/(4*(8-3))*Q
  out.append({'epsilon':eps,'raw_BVP_angles':sol.x.tolist(),'raw_BVP_chi':sol.y[0].tolist(),'raw_BVP_dchi':sol.y[1].tolist(),'BVP_nodes':int(sol.x.size),'BVP_reported_rms_residual_max':float(np.max(sol.rms_residuals)),'independent_refinement':refs,'FD_error_ratios':ratios,'linearized_solution_error':float(np.max(abs(sol.sol(x)[0]-1-u))),'retained_half_sphere':{'angle':x.tolist(),'chi':sol.sol(x)[0].tolist(),'scalar':scalar(x)[0].tolist()}})
 result={'scope':'Nonlinear Hamiltonian solved on reflection-even S^3 scalar data, Kij=0, scalar proper-time momentum=0; momentum constraints vanish exactly.','equation':'-8 Delta(chi)+6chi=chi|Dw|^2+2b0^2 chi^5 W(w); w=.5+epsilon (4cos^2(theta)-1).','parameters':{'mu2':MU2,'b0_squared':b2},'cases':out,'normal_expansion':'On the initial Kij=0 slice, Gaussian-normal Raychaudhuri gives Theta_dot=V/M^2>0 exactly; scalar spatial-gradient terms cancel in rho+S. This is a normal geodesic volume turn, not a scalar matter-flow frame (gradient is spacelike at the slice).','regularity':'Smooth positive conformal factor and scalar data imply finite initial connection/curvature and local regular Einstein-scalar continuation; no global completeness or later stability theorem.','attribution':'Same constraints/normal turn occur in the torsion-free canonical-scalar equivalent theory; this strengthens the curvature-assisted interpretation, not a Level B torsion-bounce claim.'}
 (Path(__file__).resolve().parents[1]/'results/05_inhomogeneous_constraints.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS nonlinear S^3 inhomogeneous constraints and independent second-order FD refinement')
if __name__=='__main__':main()
