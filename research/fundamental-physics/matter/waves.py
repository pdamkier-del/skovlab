"""Measure inertia of localised field states on a conservative wave lattice."""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("results", type=Path)
out = parser.parse_args().results
out.mkdir(parents=True, exist_ok=True)


def sech(x):
    return 1 / np.cosh(np.clip(x, -710, 710))


def breather(x, c, omega, v):
    eta = np.sqrt(1 - omega**2)
    gamma = 1 / np.sqrt(1 - (v / c)**2)
    tau = -gamma * v * x / c**2
    envelope = sech(eta * gamma * x / c)
    w = eta/omega * np.sin(omega*tau) * envelope
    wt = eta*gamma*np.cos(omega*tau)*envelope + w*eta*gamma*v/c*np.tanh(eta*gamma*x/c)
    return 4*np.arctan(w), 4*wt/(1+w*w)


def wave_step(q, p, dt, dx, c, grad):
    def acceleration(x):
        return (c/dx)**2*(np.roll(x, 1) + np.roll(x, -1) - 2*x) - grad(x)
    p = p + dt/2*acceleration(q)
    q = q + dt*p
    return q, p + dt/2*acceleration(q)


def quantities(q, p, x, dx, c, potential, expected, radius):
    n = len(x)
    bond = c*(np.roll(q,-1)-q)/dx
    energy = abs(p)**2/2+(abs(bond)**2+abs(np.roll(bond,1))**2)/4+potential(q)
    E = energy.sum()*dx
    gradient = (np.roll(q,-1)-np.roll(q,1))/(2*dx)
    P = -np.vdot(p,gradient).real*dx
    center = n*dx/(2*np.pi)*np.angle(np.dot(energy,np.exp(2j*np.pi*x/(n*dx))))
    distance = (x-expected+n*dx/2)%(n*dx)-n*dx/2
    return E, P, center, energy[abs(distance)<radius].sum()*dx/E


def sine_gordon():
    rows = []
    for c in [.7, 1., 1.4]:
        for dx in [.32, .16, .08]:
            x = np.arange(-80,80,dx)
            for w in [.64, .83, .93]:
                for f in [0,.05,.10,.20,.40,.65]:
                    v=c*f
                    for case in ["nonlinear"] + (["linear","perturbed"] if c==1 and f in [0,.4] else []):
                        q,p=breather(x,c,w,v)
                        if case=="perturbed":
                            p *= 1.05
                        force = (lambda q:q) if case=="linear" else np.sin
                        potential = (lambda q:q*q/2) if case=="linear" else (lambda q:2*np.sin(q/2)**2)
                        dt = dx/c*.34
                        start=quantities(q,p,x,dx,c,potential,0,10*c)
                        steps=round(54/dt)
                        for i in range(steps+1):
                            if i in (0,steps//4,steps//2,3*steps//4,steps):
                                t=i*dt
                                row=quantities(q,p,x,dx,c,potential,v*t,10*c)
                                assert abs(row[0]/start[0]-1)<.025
                                rows.append((c,dx,w,f,case,t,*row))
                            if i<steps:
                                q,p=wave_step(q,p,dt,dx,c,force)
    columns=["c","dx","omega","v_over_c","case","t","energy","momentum","center","localized"]
    pd.DataFrame(rows,columns=columns).to_csv(out/"breathers.csv",index=False)


def q_balls():
    rows=[]
    b=.6
    gradient=lambda q:q*(1-2*abs(q)**2+3*b*abs(q)**4)
    potential=lambda q:(abs(q)**2-abs(q)**4+b*abs(q)**6)/2
    for dx in [.32,.16,.08]:
        c=1.
        x=np.arange(-80,80,dx)
        for w in [.78,.86,.95]:
            s=1-w*w
            f=np.sqrt(2*s/(1+np.sqrt(1-4*b*s)*np.cosh(2*np.sqrt(s)*x)))
            for perturb in [0.,.03,.1]:
                for seed in ([1] if perturb==0 else [1,2,3]):
                    rng=np.random.default_rng(seed)
                    noise=sum(rng.uniform(-1,1)*np.cos(k*x+rng.uniform(0,6)) for k in [1.,2.,3.])/3
                    q=f*(1+perturb*noise)+0j
                    p=1j*w*q
                    dt=.34*dx
                    initial_charge=np.vdot(q,p).imag*dx
                    initial_energy=quantities(q,p,x,dx,c,potential,0,10)[0]
                    steps=round(120/dt)
                    for i in range(steps+1):
                        if i in [0,steps//3,2*steps//3,steps]:
                            energy,_,center,local=quantities(q,p,x,dx,c,potential,0,10)
                            charge=np.vdot(q,p).imag*dx
                            assert abs(charge/initial_charge-1)<1e-10
                            rows.append((dx,w,perturb,seed,i*dt,energy,charge,center,local,
                                         energy/initial_energy-1,charge/initial_charge-1))
                        if i<steps:
                            q,p=wave_step(q,p,dt,dx,c,gradient)
    columns=["dx","omega","perturb","seed","t","energy","charge","center","localized","energy_error","charge_error"]
    pd.DataFrame(rows,columns=columns).to_csv(out/"qballs.csv",index=False)


def analyze_breathers():
    data=pd.read_csv(out/"breathers.csv")
    rows=[]
    for (c,dx,w),run in data.query("case=='nonlinear'").groupby(["c","dx","omega"]):
        each=[]
        for nominal, traj in run.groupby("v_over_c"):
            actual=np.polyfit(traj.t,traj.center,1)[0]
            each.append((nominal,actual,traj.energy.mean(),traj.momentum.mean(),traj.localized.min()))
        all_values=np.array(each)
        rest=all_values[0,2]
        speed=all_values[1:4,1]
        M=np.polyfit(speed**2,all_values[1:4,3]/speed,1)[1]
        M_E=np.dot(speed**2,2*(all_values[1:4,2]-rest))/np.dot(speed**2,speed**2)
        v=all_values[-1,1]
        gamma=1/np.sqrt(1-(v/c)**2)
        Eerr=all_values[-1,2]/(gamma*rest)-1
        Perr=all_values[-1,3]/(gamma*rest*v/c**2)-1
        rows.append((c,dx,w,rest,M,M_E,M*c*c/rest-1,Eerr,Perr,all_values[:,4].min()))
    result=pd.DataFrame(rows,columns=["c","dx","omega","rest","mass_P","mass_E","ratio_error","boost_E_error",
                                      "boost_P_error","localized"])
    result.to_csv(out/"breather_masses.csv",index=False)
    rows=[]
    for (c,dx),data in result.groupby(["c","dx"]):
        endpoints=data.set_index("omega").loc[[.64,.93]]
        dE,dM=endpoints[["rest","mass_P"]].iloc[0]-endpoints[["rest","mass_P"]].iloc[1]
        rows.append((c,dx,dE,dM,dM*c*c/dE))
    pd.DataFrame(rows,columns=["c","dx","delta_E","delta_M","ratio"]).to_csv(out/"mass_energy.csv",index=False)


if __name__ == "__main__":
    sine_gordon()
    q_balls()
    analyze_breathers()
