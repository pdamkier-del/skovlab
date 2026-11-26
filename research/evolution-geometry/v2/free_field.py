"""Exact Fourier evolution on fixed Minkowski space, with radial quadrature checks."""
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.integrate import simpson
from scipy.special import gamma, jv

p=argparse.ArgumentParser()
p.add_argument("results",type=Path)
out=p.parse_args().results
out.mkdir(exist_ok=True,parents=True)
rows=[]
for n in [1,2,3,4,6,8,16,32,64]:
    for width in [1.,2.,4.]:
        # Fixed proper radius, not fixed coordinate variance per dimension.
        w=width*np.sqrt(2/n)
        for points in [1001,3001]:
            k=np.linspace(0,max(12,np.sqrt(n+65)/w),points)
            omega=np.sqrt(1+k*k)
            amp=np.exp(-w*w*k*k/2)
            initial=simpson(k**(n-1)*omega**2*amp**2,x=k)
            ballistic=simpson(k**(n+1)*amp**2,x=k)/initial
            for t in [0,1,3,6,12,24]:
                c,s=np.cos(t*omega),np.sin(t*omega)
                f=amp*c
                g=-omega*amp*s
                df=-w*w*k*f-t*k/omega*amp*s
                dg=-k/omega*amp*s-omega*(-w*w*k*amp*s+t*k/omega*amp*c)
                energy=simpson(k**(n-1)*(g*g+omega**2*f*f),x=k)
                radius=simpson(k**(n-1)*(dg*dg+omega**2*df*df+n*f*f+2*k*f*df),x=k)/energy
                assert abs(energy/initial-1)<1e-12
                rows.append((n,width,points,t,radius,ballistic,energy/initial-1))
pd.DataFrame(rows,columns=["n","target_scale","quadrature_points","time","rms_squared",
                           "asymptotic_speed_squared","energy_error"]).to_csv(out/"free_moments.csv",index=False)

rows=[]
for n in [1,2,3,4,6,8]:
    for points in [701,1401]:
        k=np.linspace(0,14,points)
        r=np.linspace(0,48,points)
        w=2*np.sqrt(2/n)
        order=n/2-1
        z=np.outer(r,k)
        transform=np.divide(jv(order,z[1:,1:]),z[1:,1:]**order)
        limit=1/(2**order*gamma(order+1))
        kernel=np.full(z.shape,limit)
        kernel[1:,1:]=transform
        derivative=np.zeros_like(z)
        derivative[1:,1:]=-k[1:]*jv(order+1,z[1:,1:])/z[1:,1:]**order
        integrator=np.ones(points)
        integrator[1:-1:2]=4
        integrator[2:-1:2]=2
        fourier_weights=k**(n-1)*np.exp(-w*w*k*k/2)*integrator*(k[1]-k[0])/3
        omega=np.sqrt(1+k*k)
        energies=[]
        for t in [-12.,0.,3.,6.,12.,24.]:
            f=np.cos(t*omega)*fourier_weights
            phi=kernel@f
            vel=kernel@(-omega*np.sin(t*omega)*fourier_weights)
            grad=derivative@f
            radial_energy=r**(n-1)*(phi*phi+vel*vel+grad*grad)
            energy=simpson(radial_energy,x=r)
            energies.append(energy)
            radial_probability=radial_energy*(r[1]-r[0])
            prob=radial_probability/radial_probability.sum()
            valid=prob>0
            shannon=-sum(prob[valid]*np.log(prob[valid]))+np.log(r[1]-r[0])
            cumulative=np.r_[0,np.cumsum((radial_energy[1:]+radial_energy[:-1])*.5*(r[1]-r[0]))]
            core=np.interp(4,r,cumulative)/energy
            rows.append((n,points,t,energy,core,shannon,simpson(r*r*radial_energy,x=r)/energy))
        assert max(abs(np.array(energies)/energies[1]-1))<2e-6
pd.DataFrame(rows,columns=["n","points","time","energy_integral","energy_within_r4","radial_entropy",
                           "rms_squared"]).to_csv(out/"free_profiles.csv",index=False)
