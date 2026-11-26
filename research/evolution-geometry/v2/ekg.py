"""Exact homogeneous reductions of fixed-dimensional Einstein–Klein–Gordon."""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp

parser=argparse.ArgumentParser()
parser.add_argument("results",type=Path)
out=parser.parse_args().results
out.mkdir(exist_ok=True,parents=True)

# m=1, kappa=8*pi*G_D=1 after separately rescaling the scalar in each D.
rows=[]
checks=[]
for n in [2,3,4,5,8,16,32,64,np.inf]:
    inv=0 if np.isinf(n) else 1/n
    for normalization in ["density","Hubble"]:
        if normalization=="Hubble" and not np.isfinite(n):
            continue
        for k in [0,-.001,.001]:
            if not np.isfinite(n) and k!=0:
                continue
            for phase in [0.,np.pi/3]:
                rho0=.018 if normalization=="density" else .5*(1-inv)*((n*.04)**2+n*n*k)
                if rho0<=0:
                    continue
                K=n*n*k if k else 0.
                if 2*rho0/(1-inv)-K<=0:
                    continue
                X=np.sqrt(2*rho0)*np.cos(phase)
                Y=np.sqrt(2*rho0)*np.sin(phase)
                h0=np.sqrt(2*rho0/(1-inv)-K)
                def evolve(t,state):
                    x,y,logvol,h,ray=state
                    logscale=logvol*inv
                    return [y,-h*y-x,h,inv*K*np.exp(-2*logscale)-y*y/(1-inv),np.exp(-logscale)]
                def turn(t,state):
                    return state[3]
                turn.terminal=True
                turn.direction=-1
                def constraint(state):
                    x,y,logvol,h,_=state
                    return .5*(1-inv)*(h*h+K*np.exp(-2*inv*logvol))-(x*x+y*y)/2
                sols=[]
                for rtol in [1e-7,1e-10]:
                    sol=solve_ivp(evolve,(0,140),[X,Y,0,h0,0],rtol=rtol,atol=rtol/50,
                                  method="DOP853",dense_output=True,events=turn,max_step=.6)
                    assert sol.success
                    test=np.linspace(0,sol.t[-1],1001)
                    error=np.max(abs(constraint(sol.sol(test))))/rho0
                    checks.append((n,normalization,k,phase,rtol,sol.t[-1],error))
                    sols.append(sol)
                sol=sols[-1]
                assert error<1e-7
                if k<=0:
                    def reduced(_,state):
                        x,y,lv,ray=state
                        h=np.sqrt((x*x+y*y)/(1-inv)-K*np.exp(-2*inv*lv))
                        return [y,-h*y-x,h,np.exp(-inv*lv)]
                    alternative=solve_ivp(reduced,(0,sol.t[-1]),[X,Y,0,0],dense_output=True,
                                          atol=2e-12,rtol=1e-10,method="DOP853",max_step=.6)
                    assert np.max(abs(alternative.sol(test)-sol.sol(test)[[0,1,2,4]]))<2e-6
                for t in np.linspace(0,sol.t[-1],401):
                    x,y,lv,h,ray=sol.sol(t)
                    rho=(x*x+y*y)/2
                    pressure=(y*y-x*x)/2
                    # Trace of Einstein equation in D=n+1.
                    ricci=((1+inv)*x*x-(1-inv)*y*y)/(1-inv)
                    rows.append((n,normalization,k,phase,t,rho,pressure,lv,h,h*inv,
                                 ricci,ray,constraint(sol.sol(t))/rho0,rho*np.exp(lv)/rho0))
columns=["n","normalization","curvature","phase","proper_time","density","pressure","log_volume",
         "volume_rate","Hubble","Ricci_scalar","comoving_light_distance","constraint","rho_volume_ratio"]
pd.DataFrame(rows,columns=columns).to_csv(out/"flrw.csv",index=False)
pd.DataFrame(checks,columns=["n","normalization","curvature","phase","rtol","end","constraint"]
             ).to_csv(out/"constraints.csv",index=False)

# Bianchi I in 3+1. Two identical directions and a periodic third direction can be read as a KK circle.
# Shear dynamics follows the differences of spatial Einstein equations for isotropic stress.
rows=[]
for phase in [0.,np.pi/3]:
    for sign in [-1,0,1]:
        for radius in [.3,1,3]:
            rho0=.018
            sigma=np.array([-.07,-.07,.14])*sign
            H0=np.sqrt((rho0+.5*np.dot(sigma,sigma))/3)
            def ode(t,y):
                phi,p=y[:2]
                logs=y[2:5]
                H=y[5]
                shear=sigma*np.exp(-sum(logs))
                return [p,-3*H*p-phi,*(H+shear),-.5*(p*p+np.dot(shear,shear))]
            initial=[np.sqrt(2*rho0)*np.cos(phase),np.sqrt(2*rho0)*np.sin(phase),0,0,0,H0]
            solution=solve_ivp(ode,(0,80),initial,dense_output=True,rtol=1e-10,atol=1e-12,method="DOP853")
            for t in np.linspace(0,80,161):
                phi,p,lx,ly,lz,H=solution.sol(t)
                shear=sigma*np.exp(-lx-ly-lz)
                error=(3*H*H-.5*np.dot(shear,shear)-.5*(phi*phi+p*p))/rho0
                R=radius*np.exp(lz)
                # R frozen at each time for the heat-kernel diagnostic; the other two
                # spatial directions are treated as effectively infinite.
                for scale in [.2,1.,5.]:
                    modes=np.arange(-2000,2001)
                    exponent=scale*modes**2/R**2
                    weights=np.exp(-exponent)
                    ds=2+2*np.dot(exponent,weights)/weights.sum()
                    rows.append((phase,sign,radius,t,R,H+shear[2],H,error,scale,ds))
pd.DataFrame(rows,columns=["phase","shear_sign","R0","t","R","circle_rate","Hubble","constraint","heat_time",
                            "spectral_dimension"]).to_csv(out/"circle.csv",index=False)
