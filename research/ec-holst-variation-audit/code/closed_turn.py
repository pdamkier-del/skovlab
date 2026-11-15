"""Closed-FLRW scalar curvature turns, never classified as a flat torsion bounce.
Evolution uses the potential derived from beta R'+c R'^2, not a chosen inflaton EOS.
Cartan curvature includes full reconstructed torsion and spatial S^3 connection.
"""
import json,itertools
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from geometry import ETA,E,torsion,contortion
BETA=.25;CQUAD=1e8;MU2=(1+16*BETA**2)/(48*CQUAD);LAM=np.sqrt(2/3)

def pot(w):
 X=LAM*w+np.arcsinh(4*BETA);d=np.sinh(X)/4-BETA
 return 12*d*d/(1+16*BETA**2),24*d*np.cosh(X)/4*LAM/(1+16*BETA**2)

def rhs(y):
 l,h,w,v=y;V,dV=pot(w)
 return np.array([h,np.exp(-2*l)-v*v/2,v,-3*h*v-dV])

def rk4(y,dt):
 a=rhs(y);b=rhs(y+dt*a/2);c=rhs(y+dt*b/2);d=rhs(y+dt*c)
 return y+dt*(a+2*b+2*c+d)/6

def affine(y,include_torsion=True,return_R=False):
 l,h,w,v=y;b=np.exp(l);dy=rhs(y);dh,dv=dy[1],dy[3];X=LAM*w+np.arcsinh(4*BETA)
 q=np.zeros(4);tc=np.zeros(4);dq=np.zeros(4);dtc=np.zeros(4)
 if include_torsion:
  q[0]=-np.sqrt(24)/np.cosh(X)*v;dq[0]=-np.sqrt(24)/np.cosh(X)*(dv-np.tanh(X)*LAM*v*v)
  tc[0]=np.sinh(X)/4*q[0];dtc[0]=LAM*np.cosh(X)/4*v*q[0]+np.sinh(X)/4*dq[0]
 C=contortion(torsion(tc,q));dC=contortion(torsion(dtc,dq))
 W=np.zeros((4,4,4));dW=W.copy();de=np.zeros((4,4,4))
 # de^i=H e0^ei -(1/b) eps_ijk ej^ek. Coefficient convention de=1/2 de_cd ec^ed.
 for i in range(1,4):
  W[i,0,i]=W[0,i,i]=h;dW[i,0,i]=dW[0,i,i]=dh
  de[i,0,i]=h;de[i,i,0]=-h
  for j,k in itertools.product(range(1,4),repeat=2):
   eps=E[0,i,j,k];W[i,j,k]=-eps/b;dW[i,j,k]=eps*h/b;de[i,j,k]=-2*eps/b
 W+=ETA[:,None,None]*np.transpose(C,(0,2,1));dW+=ETA[:,None,None]*np.transpose(dC,(0,2,1))
 R=np.zeros((4,4,4,4))
 for a,bb,c,d in itertools.product(range(4),repeat=4):
  R[a,bb,c,d]=(dW[a,bb,d] if c==0 else 0)-(dW[a,bb,c] if d==0 else 0)+sum(W[a,bb,e]*de[e,c,d]+W[a,e,c]*W[e,bb,d]-W[a,e,d]*W[e,bb,c] for e in range(4))
 low=ETA[:,None,None,None]*R
 scalar=sum(ETA[bb]*R[a,bb,a,bb] for a,bb in itertools.product(range(4),repeat=2))
 holst=np.einsum('abcd,abcd',-E,low)
 K=np.einsum('a,b,c,d,abcd,abcd',ETA,ETA,ETA,ETA,low,low)
 T=torsion(tc,q);T2=np.einsum('a,b,c,abc,abc',ETA,ETA,ETA,T,T)
 diagnostics=dict(full_scalar_over_mu2=float(scalar),Holst_over_mu2=float(holst),full_K_over_mu4=float(K),torsion_squared_over_mu2=float(T2))
 return (diagnostics,R) if return_R else diagnostics

def main():
 records=[];raw=[]
 for w0,v0 in [(.5,0.),(.45,0.),(.55,.05)]:
  V,_=pot(w0);y0=np.array([.5*np.log(3/(V+v0*v0/2)),0.,w0,v0]);reference={}
  for sign in [-1,1]:
   sol=solve_ivp(lambda t,y:rhs(y),(0,sign*.5),y0,method='DOP853',rtol=2e-12,atol=2e-13,dense_output=True);assert sol.success;reference[sign]=sol
  refinements=[]
  for n in [32,64,128]:
   worst=0.;ends=[]
   for sign in [-1,1]:
    y=y0.copy();dt=sign*.5/n
    for _ in range(n):
     y=rk4(y,dt);V,_=pot(y[2]);constraint=y[1]**2+np.exp(-2*y[0])-(y[3]**2/2+V)/3;worst=max(worst,abs(constraint))
    ends.append(y.copy())
   err=max(np.max(abs(ends[i]-reference[sign].y[:,-1])) for i,sign in enumerate([-1,1]))
   refinements.append({'steps_per_half':n,'max_constraint_in_mu2':float(worst),'endpoint_error':float(err)})
  assert refinements[-1]['endpoint_error']<refinements[0]['endpoint_error']/100
  samples=[]
  for time in np.linspace(-.5,.5,11):
   y=y0 if time==0 else reference[1 if time>0 else -1].sol(time);l,h,w,v=y;V,_=pot(w);dh=rhs(y)[1]
   lc=affine(y,False);full,Rtensor=affine(y,return_R=True);expectedR=6*(dh+2*h*h+np.exp(-2*l));expectedK=12*((dh+h*h)**2+(h*h+np.exp(-2*l))**2)
   assert abs(lc['full_scalar_over_mu2']-expectedR)<1e-12 and abs(lc['full_K_over_mu4']-expectedK)<1e-12
   z_over_mu2=24*(np.sinh(LAM*w+np.arcsinh(4*BETA))/4-BETA)/(1+16*BETA**2)
   assert abs(full['Holst_over_mu2']-z_over_mu2)<1e-12
   assert abs(full['full_scalar_over_mu2']+2*BETA*full['Holst_over_mu2'])<2e-10
   # Original first-order tetrad variation at fixed coordinate curvature and auxiliary z.
   f=np.sinh(LAM*w+np.arcsinh(4*BETA))/4
   def Lfirst(e):
    inv=np.linalg.inv(e)
    ss=np.einsum('ma,nb,b,abmn',inv,inv,ETA,Rtensor)
    hh=np.einsum('abcd,a,mc,nd,abmn',-E,ETA,inv,inv,Rtensor)
    return np.linalg.det(e)*(.5*ss+f*hh-V)
   residual=[]
   for aa,mu in itertools.product(range(4),repeat=2):
    ep=np.eye(4);em=np.eye(4);ep[aa,mu]+=1e-5;em[aa,mu]-=1e-5
    residual.append((Lfirst(ep)-Lfirst(em))/(2e-5))
   tetrad_error=float(np.max(abs(np.array(residual))));assert tetrad_error<1e-8,tetrad_error
   samples.append({'tau':float(time),'H_over_mu':float(h),'phi_over_M':float(w),'phi_dot_over_mu_M':float(v),'a_times_mu':float(np.exp(l)),'original_tetrad_variation_max':tetrad_error,'metric_R_over_mu2':float(expectedR),'metric_K_over_mu4':float(expectedK),**full})
  assert samples[0]['H_over_mu']<0 and samples[-1]['H_over_mu']>0 and rhs(y0)[1]>0
  records.append({'initial_phi':w0,'initial_velocity':v0,'a_mu_at_turn':float(np.exp(y0[0])),'Hdot_over_mu2_at_turn':float(rhs(y0)[1]),'refinement':refinements,'samples':samples})
  raw.append({'initial_turn_state':y0.tolist(),'negative_time_state':reference[-1].y[:,-1].tolist(),'positive_time_state':reference[1].y[:,-1].tolist()})
 result={'classification':'Finite regular k=+1 scalar-potential curvature turns; not a Level B torsion-caused or flat-FLRW bounce.','parameters':{'M':1.,'beta':BETA,'c':CQUAD,'mu_squared':MU2,'tau':'mu*t','k':1},'cases':records,'raw_endpoints':raw,'counterfactuals':'Torsion-free GR with the same canonical scalar action reproduces the metric exactly, with its own identical constraint. Scalar-free GR+Lambda=V(phi_turn) has an independently constrained closed de Sitter turn, but is a distinct matter action. Pure scalar-free vacuum GR has no real closed-FLRW H=0 data at this a.','limits':'Three homogeneous data points are not B6 inhomogeneous robustness or global completeness. Small curvature alone does not certify omitted operators or quantum state control.'}
 (Path(__file__).resolve().parents[1]/'results/03_closed_turns.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS closed curvature turns, temporal refinement and full Cartan curvature/auxiliary equation')
if __name__=='__main__':main()
