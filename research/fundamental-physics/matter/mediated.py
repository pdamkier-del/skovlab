"""Two moving Q-balls interact through a third local, dynamic scalar field."""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd

parser=argparse.ArgumentParser()
parser.add_argument("results",type=Path)
out=parser.parse_args().results
out.mkdir(exist_ok=True,parents=True)


def experiment(dx,g,sign,dist,omega,phase):
    x=np.arange(-60,60,dx)
    L=len(x)*dx
    b=.6
    mu=.22
    dt=.32*dx
    n=round(35/dt)
    def profile(center,w,angle):
        s=1-w*w
        return np.exp(1j*angle)*np.sqrt(2*s/(1+np.sqrt(1-4*b*s)*np.cosh(2*np.sqrt(s)*(x-center))))
    def lap(y):
        return (np.roll(y,-1,axis=-1)+np.roll(y,1,axis=-1)-2*y)/dx**2
    def grad(y):
        return (np.roll(y,-1,axis=-1)-np.roll(y,1,axis=-1))/(2*dx)
    def local_energy(q,p):
        edge=(np.roll(q,-1,axis=-1)-q)/dx
        return .5*(abs(p)**2+(abs(edge)**2+abs(np.roll(edge,1,axis=-1))**2)/2+
                   abs(q)**2-abs(q)**4+b*abs(q)**6)
    w=np.array([.78,omega])
    q=np.array([profile(-dist/2,w[0],phase),profile(dist/2,w[1],phase+.6)])
    p=1j*w[:,None]*q
    initial_density=abs(q)**2
    charges=initial_density.sum(axis=1)*dx
    masses=local_energy(q,p).sum(axis=1)*dx
    field_source=np.array([1,sign])[:,None]
    k=2*np.pi*np.fft.fftfreq(len(x),d=dx)
    eig=mu**2+4*np.sin(k*dx/2)**2/dx**2
    resolved=np.fft.ifft(np.fft.fft(initial_density,axis=-1)/eig,axis=-1).real
    phi=g*(resolved[0]+sign*resolved[1])
    chi=np.zeros_like(phi)
    initial_force=g*g*sign*dx*np.dot(initial_density[0],grad(resolved[1]))
    initial_charge=(q.conj()*p).imag.sum(axis=1)*dx
    def acceleration(q,u):
        a=lap(q)-q*(1-2*abs(q)**2+3*b*abs(q)**4-2*g*field_source*u)
        a_u=lap(u)-mu**2*u+g*np.sum(field_source*abs(q)**2,axis=0)
        return a,a_u
    def energy(q,p,u,udot):
        return dx*(local_energy(q,p).sum()+.5*np.dot(udot,udot)
                   +.5*np.sum(((np.roll(u,-1)-u)/dx)**2)+.5*mu**2*np.dot(u,u)
                   -g*np.dot(u,np.sum(field_source*abs(q)**2,axis=0)))
    initial_E=energy(q,p,phi,chi)
    trajectory=[]
    for i in range(n+1):
        if i%10==0 or i==n:
            H=energy(q,p,phi,chi)
            charge=(q.conj()*p).imag.sum(axis=1)*dx
            assert np.max(abs(charge-initial_charge))<1e-9
            assert abs(H/initial_E-1)<.002
            P=-(p.conj()*grad(q)).real.sum(axis=1)*dx
            P_field=-np.dot(chi,grad(phi))*dx
            local=local_energy(q,p)
            centers=np.dot(local,x)/local.sum(axis=1)
            trajectory.append((i*dt,*centers,*P,P_field,H/initial_E-1))
        if i==n:
            break
        a,f=acceleration(q,phi)
        p+=.5*dt*a
        chi+=.5*dt*f
        q+=dt*p
        phi+=dt*chi
        a,f=acceleration(q,phi)
        p+=.5*dt*a
        chi+=.5*dt*f
    records=np.array(trajectory)
    short=records[(records[:,0]>1)&(records[:,0]<10)]
    force=np.polyfit(short[:,0],short[:,3],1)[0]
    long=records[-1,1:3]-records[0,1:3]
    return (dx,g,sign,dist,omega,phase,*charges,*masses,initial_force,force,*long,
            np.max(abs(records[:,-1])),np.max(abs(records[:,3:6].sum(axis=1)))),records


rows,traces=[],[]
for dx in [.20,.10]:
    for g,sgn in [(0,1),(.035,1),(.07,1),(.07,-1)]:
        for d in [8,12,18]:
            for w in [.78,.92]:
                for phase in [0.,.7]:
                    row,trace=experiment(dx,g,sgn,d,w,phase)
                    rows.append(row)
                    if dx==.10 and phase==0:
                        traces.extend([(dx,g,sgn,d,w,*a) for a in trace])
cols=["dx","g","sign","separation","omega_B","phase","source_A","source_B","rest_A","rest_B",
      "static_force","measured_force","shift_A","shift_B","energy_error","momentum_error"]
pd.DataFrame(rows,columns=cols).to_csv(out/"mediated.csv",index=False)
cols=["dx","g","sign","separation","omega_B","t","x_A","x_B","P_A","P_B","P_field","energy_error"]
pd.DataFrame(traces,columns=cols).to_csv(out/"mediated_trace.csv",index=False)
