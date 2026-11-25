"""Impulse response of a mobile Newtonian probe in a local Klein–Gordon field."""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd

parser=argparse.ArgumentParser()
parser.add_argument("results",type=Path)
out=parser.parse_args().results
out.mkdir(exist_ok=True,parents=True)


def impulse_run(dx,m,g,impulse,duration):
    c=1.
    bare=.65
    width=.65
    x=np.arange(-45,45,dx)
    period=len(x)*dx
    k=2*np.pi*np.fft.fftfreq(len(x),d=dx)
    eigen=m**2+4*(c/dx)**2*np.sin(k*dx/2)**2

    def source(X):
        d=(x-X+period/2)%period-period/2
        S=np.exp(-d*d/(2*width**2))/(np.sqrt(2*np.pi)*width)
        return S,d*S/width**2

    s,ds=source(0)
    phi=g*np.fft.ifft(np.fft.fft(s)/eigen).real
    derivative=g*np.fft.ifft(np.fft.fft(ds)/eigen).real
    delta_M=np.dot(derivative,derivative)*dx
    delta_E=-g/2*np.dot(phi,s)*dx
    pi=np.zeros_like(phi)
    X=V=work=0.
    dt=dx*.28
    finish=duration+30
    values=[]
    def external(t):
        return (2*impulse/duration)*np.sin(np.pi*t/duration)**2 if t<=duration else 0.

    def acceleration(u,loc,t):
        s,ds=source(loc)
        a_phi=(c/dx)**2*(np.roll(u,1)+np.roll(u,-1)-2*u)-m**2*u+g*s
        a_x=(g*np.dot(u,ds)*dx+external(t))/bare
        return a_phi,a_x

    def energy(u,p,loc,vel):
        s,_=source(loc)
        return (.5*bare*vel**2+dx*(.5*np.dot(p,p)+.5*m*m*np.dot(u,u)
                 +.5*(c/dx)**2*np.sum((np.roll(u,1)-u)**2)-g*np.dot(u,s)))

    start=energy(phi,pi,X,V)
    assert abs(start-delta_E)<1e-10
    records=[]
    steps=round(finish/dt)
    for i in range(steps):
        t=i*dt
        a,f=acceleration(phi,X,t)
        pi+=.5*dt*a
        V+=.5*dt*f
        phi+=dt*pi
        dX=dt*V
        X+=dX
        a,f=acceleration(phi,X,t+dt)
        pi+=.5*dt*a
        V+=.5*dt*f
        work+=.5*(external(t)+external(t+dt))*dX
        if i%8==0 or i==steps-1:
            gradient=(np.roll(phi,-1)-np.roll(phi,1))/(2*dx)
            full_p=bare*V-np.dot(pi,gradient)*dx
            err=energy(phi,pi,X,V)-start-work
            records.append((dx,m,g,impulse,duration,t+dt,X,V,full_p,work,err))
            if duration+6<t<finish-1:
                values.append(V)
    mean=np.mean(values)
    inertia=impulse/mean
    metrics=(dx,m,g,impulse,duration,bare,delta_M,delta_E,inertia,np.std(values),max(abs(r[-1]) for r in records))
    assert metrics[-1]<.002, metrics
    return metrics,records


def main():
    rows=[]
    traces=[]
    for dx in [.2,.1,.05]:
        for g in [0.,1.,2.,3.]:
            for impulse,duration in [(.04,24),(.10,24),(.20,24),(.1,1)]:
                summary,trace=impulse_run(dx,.65,g,impulse,duration)
                rows.append(summary)
                if dx==.1:
                    traces.extend(trace)
    for m in [.4,1.2]:
        summary,trace=impulse_run(.1,m,2,.1,24)
        rows.append(summary)
        traces.extend(trace)
    pd.DataFrame(rows,columns=["dx","gap","g","impulse","duration","bare","delta_mass_theory",
                              "delta_rest_energy","mass_impulse","late_velocity_sd","work_error"]).to_csv(out/"dressed_mass.csv",index=False)
    pd.DataFrame(traces,columns=["dx","gap","g","impulse","duration","t","x","v","momentum","work",
                               "balance"]).to_csv(out/"dressed_trace.csv",index=False)


main()
