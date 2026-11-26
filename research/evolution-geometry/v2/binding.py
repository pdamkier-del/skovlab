"""Controlled weak-field binding tests and explicitly labeled width reduction."""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.integrate import cumulative_trapezoid, quad, simpson, solve_bvp, solve_ivp
from scipy.special import gammaln

p=argparse.ArgumentParser()
p.add_argument("results",type=Path)
out=p.parse_args().results
out.mkdir(exist_ok=True,parents=True)

rows=[]
for n in [3,4,5,6,8,16,32,64,128]:
    for q,start in [(1.,.99),(1.,1.01),(.98,1.),(1.02,1.)]:
        def ode(_,z):
            r,v=z
            return v,r**-3-q*r**(1-n)
        limit=max(.75,(q/100)**(1/(n-4))) if n>4 else .75
        def cutoff(_,z):
            return z[0]-limit
        cutoff.terminal=True
        cutoff.direction=-1
        def energy(r,v):
            return v*v/2+.5/r**2-q/(n-2)*r**(2-n)
        sol=solve_ivp(ode,(0,10),[start,0.],rtol=2e-11,atol=2e-13,
                      dense_output=True,events=cutoff,method="DOP853",max_step=.08)
        assert sol.success
        for t in np.linspace(0,sol.t[-1],201):
            r,v=sol.sol(t)
            error=energy(r,v)-energy(start,0.)
            rows.append((n,q,start,t,r,v,error))
pd.DataFrame(rows,columns=["n","force_ratio","initial_width","time","width","velocity","energy_error"]).to_csv(out/"width.csv",index=False)

rows=[]
profiles=[]
for n in [3,4,5]:
    for radius in [30.,60.]:
        for tolerance in [1e-5,1e-8]:
            r=np.r_[np.linspace(0,12,400),np.linspace(12.1,radius,300)]
            def ode(_,state,param):
                u,ur,U,Ur=state
                return np.array([ur,2*(U-param[0])*u,Ur,u*u])
            def bc(a,b,param):
                return [a[0]-1,a[1],a[3],b[0],b[2]+radius*b[3]/(n-2)]
            solved=None
            for w in [1.6,2.8,4.]:
                u=np.exp(-r*r/(2*w*w))
                q=cumulative_trapezoid(u*u*r**(n-1),r,initial=0)
                d=np.divide(q,r**(n-1),out=np.zeros_like(r),where=r>0)
                U=-q[-1]/((n-2)*radius**(n-2))+cumulative_trapezoid(d[::-1],r[::-1],initial=0)[::-1]
                guess=.55*U[0]
                candidate=solve_bvp(ode,bc,r,np.array([u,-r*u/w**2,U,d]),p=[guess],
                                    S=np.diag([0,1-n,0,1-n]),tol=tolerance,max_nodes=18000)
                if candidate.success and candidate.p[0]<0 and candidate.y[0].min()>-1e-7:
                    solved=candidate
                    break
            if solved is None:
                rows.append((n,radius,tolerance,False,*([np.nan]*5)))
                continue
            if radius==60 and tolerance==1e-8:
                grid=np.linspace(0,radius,3001)
                values=solved.sol(grid)[0]
                profiles.extend(zip(np.full(len(grid),n),grid,values))
            sample=np.linspace(0,radius,16001)
            u,du,phi,_=solved.sol(sample)
            omega=2*np.exp(.5*n*np.log(np.pi)-gammaln(n/2))
            weight=omega*sample**(n-1)
            mass=simpson(weight*u*u,x=sample)
            T=.5*simpson(weight*du*du,x=sample)
            W=.5*simpson(weight*phi*u*u,x=sample)
            rows.append((n,radius,tolerance,True,solved.p[0],mass,T,W,(2*T+(n-2)*W)/T))
pd.DataFrame(rows,columns=["n","box_radius","tolerance","converged","chemical_potential","norm","T","W",
                            "virial_error"]).to_csv(out/"radial_sp.csv",index=False)

pd.DataFrame(profiles,columns=["n","r","u"]).to_csv(out/"sp_profiles.csv",index=False)

# Explicit zero-frequency endpoint n=6; independent numerical integration.
a=np.sqrt(.5)
A=12/a
def density(r): return A/(1+r*r)**2
def grad(r): return -4*A*r/(1+r*r)**3
area=np.pi**3
M=quad(lambda r:area*r**5*density(r)**2,0,np.inf)[0]
T=quad(lambda r:area*r**5*grad(r)**2/2,0,np.inf)[0]
W=quad(lambda r:-area*r**5*a*density(r)**3/2,0,np.inf)[0]
assert abs(2*T+4*W)/T<1e-11 and abs(T+2*W)/T<1e-11
pd.DataFrame([(6,0.,M,T,W,T+W)],columns=["n","chemical_potential","norm","T","W","energy"]
             ).to_csv(out/"critical6.csv",index=False)
