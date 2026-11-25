"""Compare static forces, relative zeta, heat kernel, and mode quantization."""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.integrate import simpson
from scipy.special import ive

parser = argparse.ArgumentParser()
parser.add_argument("results", type=Path)
out = parser.parse_args().results
out.mkdir(parents=True, exist_ok=True)


def infinite_green():
    # Laplace representation of the resolvent on the infinite hypercubic lattice.
    y=np.linspace(-22,15,1801)
    t=np.exp(y)
    bessel=ive(np.arange(83)[:,None],2*t)
    transverse=ive(1,2*t)
    xfreq=np.r_[0.,np.geomspace(.0005,9,170)]
    rows=[]
    for d in [1,2,3]:
        axial=bessel*bessel[0,None,:]**(d-1)
        for mass in [.0125,.05,.15]:
            resolvent=axial @ (((t*np.exp(-mass**2*t))[None,:])*np.exp(-xfreq[:,None]**2*t)).T*(y[1]-y[0])
            g=resolvent[:,0]
            dip_axial=g[2:]+g[:-2]-2*g[1:-1]
            if d>=2:
                dip_transverse=2*(g-simpson(axial*0 + bessel*bessel[0,None,:]**(d-2)
                                              *transverse*t*np.exp(-mass*mass*t),x=y,axis=1))
            soft=.5*np.log1p(-(resolvent/(1+resolvent[0]))**2)
            zero_point=simpson(soft,x=xfreq,axis=1)/np.pi
            for r in range(2,81):
                for model,energy in [
                    ("monopole",-g),
                    ("opposite_monopole",g),
                    ("axial_dipole",np.r_[0,dip_axial,0]),
                    ("thermal_pin",soft[:,0]),
                    ("quantized_pin",zero_point)
                ]+([("transverse_dipole",-dip_transverse)] if d>=2 else []):
                    force=energy[r]-energy[r+1]
                    rows.append((d,mass,r,model,g[r],energy[r],force))
    cols=["dim","gap","r","coupling","green","potential","force"]
    data=pd.DataFrame(rows,columns=cols)
    data.to_csv(out/"force_range.csv",index=False)
    rows=[]
    for (d,mass,coupling),s in data.groupby(["dim","gap","coupling"]):
        for low,high in [(6,14),(12,24),(24,48)]:
            select=s.query("@low<=r<=@high")
            slope=-np.polyfit(np.log(select.r+.5),np.log(abs(select.force)),1)[0]
            rows.append((d,mass,coupling,low,high,slope))
    pd.DataFrame(rows,columns=["dim","gap","coupling","low","high","exponent"]).to_csv(out/"force_exponents.csv",index=False)


def matrix(size,dim,mu):
    n=size**dim
    indexes=np.arange(n).reshape((size,)*dim)
    K=np.eye(n)*(mu*mu+2*dim)
    for axis in range(dim):
        for step in [-1,1]:
            K[indexes.ravel(),np.roll(indexes,step,axis).ravel()] -= 1
    return K


def spectrum():
    rows, kernels, tz=[],[],[]
    y=np.linspace(-15,10,1501)
    t=np.exp(y)
    for d,L in [(1,32),(1,64),(2,8),(2,12),(3,5)]:
        for gap in [.25,.6]:
            K=matrix(L,d,gap)
            E0=np.linalg.eigvalsh(K)
            inv=np.linalg.inv(K)
            for r in [1,2,L//2]:
                site=r*L**(d-1)
                for strength in [.7,2.,6.]:
                    A,B,AB=K.copy(),K.copy(),K.copy()
                    A[0,0]+=strength
                    B[site,site]+=strength
                    AB[0,0]+=strength
                    AB[site,site]+=strength
                    a,b,ab=[np.linalg.eigvalsh(mat) for mat in (A,B,AB)]
                    spectra=np.array([ab,a,b,E0])
                    signs=np.array([1,-1,-1,1])
                    rank=.5*np.log1p(-(strength*inv[0,site]/(1+strength*inv[0,0]))**2)
                    logs=np.log(spectra)
                    determinant=.5*np.sum(signs*logs.sum(axis=1))
                    ds=.0001
                    # Use expm1 to reduce cancellation near s=0.
                    z=lambda s:np.dot(signs,np.expm1(-s*logs).sum(axis=1))
                    fd=-(z(ds)-z(-ds))/(4*ds)
                    traces=np.exp(-t[:,None,None]*spectra[None,:,:]).sum(axis=2)@signs
                    heat=-.5*simpson(traces,x=y)
                    w=np.sqrt(spectra)
                    vacuum=.5*np.dot(signs,w.sum(axis=1))
                    assert max(abs(determinant-rank),abs(heat-rank),abs(fd-rank))<5e-8
                    rows.append((d,L,gap,r,strength,rank,determinant,fd,heat,vacuum))
                    if strength==2. and gap==.25:
                        for i in range(0,len(t),10):
                            kernels.append((d,L,gap,r,t[i],traces[i]))
                        for temperature in [.01,.03,.1,.3,1.,3.,10.,30.]:
                            quantum=.5*w+temperature*np.log(-np.expm1(-w/temperature))
                            free=np.dot(signs,quantum.sum(axis=1))
                            tz.append((d,L,gap,r,temperature,free,rank*temperature,vacuum))
    pd.DataFrame(rows,columns=["dim","L","gap","r","strength","rank","determinant","zeta_derivative",
                              "heat_kernel","vacuum"]).to_csv(out/"relative_zeta.csv",index=False)
    pd.DataFrame(kernels,columns=["dim","L","gap","r","t","trace"]).to_csv(out/"relative_heat.csv",index=False)
    pd.DataFrame(tz,columns=["dim","L","gap","r","T","quantum_free","classical_free","quantum_vacuum"]
                 ).to_csv(out/"thermal_crossover.csv",index=False)


infinite_green()
spectrum()
