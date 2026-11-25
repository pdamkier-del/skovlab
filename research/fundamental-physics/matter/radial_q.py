"""Radial Q-balls in 2 and 3 dimensions, with a Cartesian evolution check in 2D."""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.integrate import simpson, solve_bvp
from scipy.special import gamma

parser = argparse.ArgumentParser()
parser.add_argument("results", type=Path)
out = parser.parse_args().results
out.mkdir(exist_ok=True,parents=True)
b=.6


def solve(dim,amplitude,radius,tol):
    r=np.linspace(0,radius,601)
    def equations(_,values,params):
        f,h=values
        s=params[0]
        return np.array([h,f*(s-2*f*f+3*b*f**4)])
    def conditions(near,far,params):
        return np.array([near[0]-amplitude,near[1],far[0]])
    def try_guess(width):
        f=amplitude*np.exp(-r*r/width**2)
        return solve_bvp(equations,conditions,r,np.array([f,-2*r*f/width**2]),
                         p=[min(.37,.45*amplitude**2)], S=np.diag([0,1-dim]),
                         tol=tol,max_nodes=8000)
    guesses = [lambda w=w:try_guess(w) for w in [2.2/amplitude,4/amplitude,1.4/amplitude]]
    if amplitude>.87 and amplitude<.92:
        def plateau(edge):
            y=(r-edge)/1.8
            norm=1+np.tanh(edge/1.8)
            f=amplitude*(1-np.tanh(y))/norm
            h=-amplitude/1.8/np.cosh(y)**2/norm
            return solve_bvp(equations,conditions,r,np.array([f,h]),p=[.40],
                             S=np.diag([0,1-dim]),tol=tol,max_nodes=12000)
        guesses.extend(lambda edge=edge: plateau(edge) for edge in [5,8,11,15,20])
    for candidate in guesses:
        sol=candidate()
        sample=sol.sol(r)[0]
        if sol.success and 0<sol.p[0]<1/(4*b) and np.all(sample>-1e-6) and sample.max()<=amplitude+1e-5:
            return sol
    return None


def radial_measures(dim,sol,radius):
    r=np.linspace(0,radius,2401)
    f,h=sol.sol(r)
    w=np.sqrt(1-sol.p[0])
    weight=2*np.pi**(dim/2)/gamma(dim/2)*r**(dim-1)
    charge=w*simpson(weight*f*f,x=r)
    energy=.5*simpson(weight*(w*w*f*f+h*h+f*f-f**4+b*f**6),x=r)
    return w,charge,energy


def evolve(sol,search_radius,dx,seed,perturb):
    x=np.arange(-18,18,dx)
    X,Y=np.meshgrid(x,x)
    r=np.sqrt(X*X+Y*Y)
    f=sol.sol(np.minimum(r,search_radius))[0]
    w=np.sqrt(1-sol.p[0])
    rng=np.random.default_rng(seed)
    deformation=sum(rng.uniform(-1,1)*np.cos(k*X/2+k*Y/3+rng.uniform(0,6)) for k in [1,2,3])/3
    q=f*(1+perturb*deformation)+0j
    p=1j*w*q
    dt=.27*dx
    def calc(q):
        return (sum(np.roll(q,s,axis) for s in [-1,1] for axis in [0,1])-4*q)/dx**2 -q*(1-2*abs(q)**2+3*b*abs(q)**4)
    def measures():
        bonds=sum((abs(np.roll(q,s,axis)-q)/dx)**2 for axis in [0,1] for s in [-1,1])/2
        e=.5*(bonds+abs(p)**2+abs(q)**2-abs(q)**4+b*abs(q)**6)
        return np.sum(e)*dx**2,np.vdot(q,p).imag*dx**2,e[r<8].sum()/e.sum()
    E0,Q0,_=measures()
    rows=[]
    steps=round(80/dt)
    for j in range(steps+1):
        if j in [0,steps//4,steps//2,3*steps//4,steps]:
            e,qcharge,local=measures()
            assert abs(qcharge/Q0-1)<1e-10
            rows.append((dx,seed,perturb,j*dt,e,qcharge,local,e/E0-1,qcharge/Q0-1))
        if j<steps:
            p+=.5*dt*calc(q)
            q+=dt*p
            p+=.5*dt*calc(q)
    return rows


rows=[]
for dim in [2,3]:
    for amplitude in [.35,.55,.7,.85,.88,.9,.91,1.]:
        for radius in [30.,45.]:
            sol=solve(dim,amplitude,radius,1e-7)
            if sol is None:
                rows.append((dim,amplitude,radius,False,np.nan,np.nan,np.nan,np.nan))
                continue
            w,Q,E=radial_measures(dim,sol,radius)
            rows.append((dim,amplitude,radius,True,w,Q,E,E/Q))
            if dim==2 and amplitude==.85 and radius==45.:
                selected=sol
pd.DataFrame(rows,columns=["dim","amplitude","radius","solved","omega","charge","energy","energy_charge"]
             ).to_csv(out/"radial_qballs.csv",index=False)
rows=[]
if "selected" in globals():
    for dx in [.30,.20]:
        for perturb in [0.,.06,.16]:
            rows.extend(evolve(selected,45.,dx,1,perturb))
    pd.DataFrame(rows,columns=["dx","seed","perturb","t","energy","charge","localized","energy_error","charge_error"]
                 ).to_csv(out/"radial_q_evolve.csv",index=False)
