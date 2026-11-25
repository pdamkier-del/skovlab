import argparse
from pathlib import Path

import numpy as np
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("results", type=Path)
out = parser.parse_args().results
out.mkdir(parents=True,exist_ok=True)
rng = np.random.default_rng(85326)


def estimate(values):
    mean = np.mean(values)
    half = 1.96*np.std(values,ddof=1)/np.sqrt(len(values))
    return mean,mean-half,mean+half


def green(dim,L,mass):
    spectrum=4*np.sin(np.pi*np.fft.fftfreq(L))**2
    return np.fft.ifftn(1/(mass**2+sum(np.ix_(*[spectrum]*dim)))).real


def statics():
    rows=[]
    for dim in [1,2,3]:
        for L in [32,64,128]:
            for mass in [.12,.3,.65]:
                field=green(dim,L,mass)
                g=field[(slice(None),)+(0,)*(dim-1)]
                for r in range(1,L//2-1):
                    for strength in [0.,1.,4.]:
                        f=.5*np.log1p(-(strength*g/(1+strength*g[0]))**2)
                        # Positive separation is the coordinate of the moving second pin.
                        force=-(f[r+1]-f[r])
                        rows.append((dim,L,mass,r,strength,g[r],g[r]**2/2,f[r],force))
    pd.DataFrame(rows,columns=["dim","L","mass","r","strength","green","energy_cov","free","force"]).to_csv(out/"casimir.csv",index=False)


def sampling():
    rows=[]
    for dim in [1,2,3]:
        L=64
        for mass in [.12,.3]:
            field=green(dim,L,mass)
            g=field[(slice(None),)+(0,)*(dim-1)]
            for r in [2,4,8,12,16]:
                # Three sites of the exact finite-volume Gaussian Gibbs distribution.
                covariance = g[np.abs(np.subtract.outer([0,r,r+1],[0,r,r+1]))]
                normals=rng.standard_normal((48,8192,3))@np.linalg.cholesky(covariance).T
                a,b,c=normals.transpose(2,0,1)
                cov=np.mean((a*a-g[0])*(b*b-g[0])/4,axis=1)
                for strength in [1.,4.]:
                    # Bayes update of a Gaussian conditional on a noisy pinned field.
                    innovation=a+rng.normal(0,strength**-.5,size=a.shape)
                    pinned_b=b-g[r]*innovation/(g[0]+1/strength)
                    pinned_c=c-g[r+1]*innovation/(g[0]+1/strength)
                    # Paired thermodynamic free-energy perturbation with one anchored pin.
                    vb=np.exp(-strength*pinned_b**2/2).mean(axis=1)
                    vc=np.exp(-strength*pinned_c**2/2).mean(axis=1)
                    vb0=np.exp(-strength*b**2/2).mean(axis=1)
                    vc0=np.exp(-strength*c**2/2).mean(axis=1)
                    f=-np.log(vb/vb0)
                    force=np.log(vc/vb)-np.log(vc0/vb0)
                    rows.append((dim,L,mass,r,strength,*estimate(cov),*estimate(f),*estimate(force)))
    columns=["dim","L","mass","r","strength"]
    columns += [k+s for k in ("cov","free","force") for s in ("","_lo","_hi")]
    pd.DataFrame(rows,columns=columns).to_csv(out/"casimir_mc.csv",index=False)


def local_exchange():
    # Common random bonds and splits on all four preparations.
    rows=[]
    for L in [32,64,128]:
        for r in [4,8,L//2]:
            n=768
            ensembles=np.ones((4,n,L))
            lanes=np.arange(n)
            ensembles[1,:,0]+=4
            ensembles[2,:,r]+=4
            ensembles[3,:,0]+=4
            ensembles[3,:,r]+=4
            for sweep in range(65):
                if sweep in [0,1,4,16,64]:
                    baseline,a,b,ab=ensembles
                    residual=ab-a-b+baseline
                    error=np.max(abs(residual))
                    balance=np.max(abs(ensembles.sum(axis=-1)-np.array([L,L+4,L+4,L+8])[:,None]))
                    assert error<1e-11 and balance<1e-10
                    # Measure the excess reaching the other structure from a single hotspot.
                    rows.append((L,r,sweep,error,balance,*estimate((a-baseline)[:,r])))
                if sweep==64:
                    break
                for _ in range(L):
                    i=rng.integers(L,size=n)
                    j=(i+1)%L
                    p=rng.uniform(size=n)
                    total=ensembles[:,lanes,i]+ensembles[:,lanes,j]
                    ensembles[:,lanes,i]=p*total
                    ensembles[:,lanes,j]=(1-p)*total
    pd.DataFrame(rows,columns=["L","r","t","superposition","balance","response","lo","hi"]).to_csv(out/"hot_exchange.csv",index=False)


def microcanonical():
    rows=[]
    for L in [32,64,128]:
        for condition in ["canonical","microcanonical"]:
            e=rng.exponential(size=(48,4096,L))
            if condition=="microcanonical":
                e*=L/e.sum(axis=-1,keepdims=True)
            for r in [4,L//4,L//2]:
                covariance=((e[:,:,0]-1)*(e[:,:,r]-1)).mean(axis=1)
                target=0. if condition=="canonical" else -1/(L+1)
                rows.append((L,condition,r,target,*estimate(covariance)))
    pd.DataFrame(rows,columns=["L","model","r","exact","cov","lo","hi"]).to_csv(out/"exchange_cov.csv",index=False)


def local_gibbs():
    """Only nearest-neighbour Gibbs updates, starting with a zero field."""
    rows=[]
    for dim,L in [(1,32),(2,20)]:
        mass=.3
        field=np.zeros((32,)+(L,)*dim)
        g=green(dim,L,mass)[(slice(None),)+(0,)*(dim-1)]
        precision=2*dim+mass**2
        parity=np.indices(field.shape[1:]).sum(axis=0)%2
        sites=[(slice(None),r)+(0,)*(dim-1) for r in range(6)]
        sums={(r,k):np.zeros((5,len(field))) for r in [2,4] for k in [1.,4.]}
        for sweep in range(9000):
            for color in [0,1]:
                mask=parity==color
                neighbours=sum(np.roll(field,s,axis) for axis in range(1,dim+1) for s in [-1,1])
                field[:,mask]=neighbours[:,mask]/precision+rng.standard_normal((len(field),mask.sum()))/np.sqrt(precision)
            if sweep<1000:
                continue
            a=field[sites[0]]
            for (r,k),moments in sums.items():
                b,c=field[sites[r]],field[sites[r+1]]
                wa,wb,wc=np.exp(-.5*k*a*a),np.exp(-.5*k*b*b),np.exp(-.5*k*c*c)
                moments += np.array([wa*wb,wa*wc,wb,wc,(a*a-g[0])*(b*b-g[0])/4])
        for (r,k),(ab,ac,b,c,cov) in sums.items():
            f=.5*np.log1p(-(k*g/(1+k*g[0]))**2)
            force=np.log(ac/ab)-np.log(c/b)
            rows.append((dim,L,mass,r,k,f[r]-f[r+1],*estimate(force),g[r]**2/2,*estimate(cov/8000)))
    pd.DataFrame(rows,columns=["dim","L","mass","r","strength","force_exact","force","force_lo","force_hi",
                               "cov_exact","cov","cov_lo","cov_hi"]).to_csv(out/"local_gibbs.csv",index=False)


statics()
sampling()
local_exchange()
microcanonical()

local_gibbs()
