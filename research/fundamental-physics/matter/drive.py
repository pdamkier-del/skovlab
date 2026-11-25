"""Accelerate a field-only breather through a weak, spatially varying onsite potential."""
import numpy as np
import pandas as pd

from waves import breather, out, quantities, wave_step

rows=[]
for c in [.7,1.,1.4]:
    for dx in [.16,.08]:
        for w in [.64,.83,.93]:
            for epsilon in [-.025,.0125,.025]:
                x=np.arange(-70,70,dx)
                q,p=breather(x,c,w,0.)
                W=lambda u:2*np.sin(u/2)**2
                rest=quantities(q,p,x,dx,c,W,0,12*c)[0]
                dt=.34*dx/c
                T=26.
                k=.12/c
                def gate(t):
                    return np.sin(np.pi*t/T)**2 if 0<=t<T else 0.
                slope=np.sin(k*x)
                t=0.
                impulse=work=0.
                record=[]
                while t<50:
                    p2=p+dt/2*((c/dx)**2*(np.roll(q,-1)+np.roll(q,1)-2*q)
                                 -(1+epsilon*gate(t)*slope)*np.sin(q))
                    prev=q
                    q=q+dt*p2
                    p=p2+dt/2*((c/dx)**2*(np.roll(q,-1)+np.roll(q,1)-2*q)
                                 -(1+epsilon*gate(t+dt)*slope)*np.sin(q))
                    current=gate(t+dt)
                    previous=gate(t)
                    impulse-=epsilon*k*dt*dx/2*np.dot(np.cos(k*x),previous*W(prev)+current*W(q))
                    work+=epsilon*(current-previous)*dx/2*np.dot(slope,W(prev)+W(q))
                    t+=dt
                    if t>32 and round(t/dt)%8==0:
                        e,momentum,center,local=quantities(q,p,x,dx,c,W,0,12*c)
                        record.append((t,e,momentum,center,local))
                t,e,momentum,center,locale=np.array(record).T
                v=np.polyfit(t,center,1)[0]
                rows.append((c,dx,w,epsilon,rest,impulse,work,v,impulse/v,impulse/v*c*c/rest,
                             momentum.mean()/impulse,np.max(np.abs(e-rest-work)),locale.min()))
columns=["c","dx","omega","epsilon","rest","impulse","work","velocity","mass_force","ratio",
         "momentum_budget","work_error","localized"]
pd.DataFrame(rows,columns=columns).to_csv(out/"breather_drive.csv",index=False)
