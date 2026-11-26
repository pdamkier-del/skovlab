"""Finite-volume radial Schrödinger–Poisson evolution in the weak-field limit."""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline
from scipy.sparse import diags, eye
from scipy.sparse.linalg import splu

p=argparse.ArgumentParser()
p.add_argument("results",type=Path)
out=p.parse_args().results
profiles=pd.read_csv(out/"sp_profiles.csv")
rows=[]
for n,data in profiles.groupby("n"):
    initial=CubicSpline(data.r,data.u,bc_type=((1,0.),"natural"))
    for outer,dr,dt in [(24.,.10,.020),(24.,.05,.010),(36.,.10,.020)]:
        N=round(outer/dr)
        faces=np.linspace(0,outer,N+1)
        r=(faces[:-1]+faces[1:])/2
        volume=np.diff(faces**n)/n
        root=np.sqrt(volume)
        faces_area=faces**(n-1)
        conductance=faces_area[1:-1]/dr
        diag=np.r_[0,conductance]+np.r_[conductance,0]
        off=-conductance/(root[:-1]*root[1:])
        boundary=faces_area[-1]/(dr/2)
        # Robin match for U = constant * r^(2-n), with vacuum outside.
        boundary_U=faces_area[-1]/(dr/2+outer/(n-2))
        def stiffness(last):
            d=diag.copy()
            d[-1]+=last
            return diags([off,d/volume,off],[-1,0,1],format="csc")
        K=stiffness(boundary)
        poisson=splu(stiffness(boundary_U))
        unit=eye(N,format="csc")
        step=splu(unit+.25j*dt*K)
        previous=unit-.25j*dt*K
        def grav(z):
            return -poisson.solve(abs(z)**2/root)/root
        def measurement(z,U):
            M=np.vdot(z,z).real
            E=.5*(np.vdot(z,K@z).real+np.dot(U,abs(z)**2))
            radius=np.sqrt(np.dot(r*r,abs(z)**2)/M)
            outer_mass=np.sum(abs(z[r>.8*outer])**2)/M
            return M,E,radius,outer_mass
        for mode,ratio in [("amplitude",.985),("amplitude",1.),("amplitude",1.015),
                           ("width",.97),("width",1.03)]:
            if mode=="amplitude":
                z=(initial(r)*root*ratio).astype(complex)
            else:
                z=(initial(r/ratio)*root).astype(complex)
                z*=np.linalg.norm(initial(r)*root)/np.linalg.norm(z)
            U=grav(z)
            start=measurement(z,U)
            for i in range(round(16/dt)+1):
                if i%round(.5/dt)==0:
                    M,E,rms,edge=measurement(z,U)
                    mass_error=M/start[0]-1
                    energy_error=(E-start[1])/start[0]
                    assert abs(mass_error)<1e-10
                    rows.append((n,outer,dr,dt,mode,ratio,i*dt,rms,rms/start[2],mass_error,energy_error,edge))
                    # Beyond this point increasingly steep cores are not resolved.
                    if rms<.55*start[2]:
                        break
                z*=np.exp(-.5j*dt*U)
                z=step.solve(previous@z)
                U=grav(z)
                z*=np.exp(-.5j*dt*U)
pd.DataFrame(rows,columns=["n","outer","dr","dt","perturbation","ratio","time","rms","rms_ratio",
                           "mass_error","energy_error_per_norm","outer_mass_fraction"]
             ).to_csv(out/"sp_evolution.csv",index=False)
