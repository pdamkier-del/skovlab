import argparse
from pathlib import Path

import numpy as np
import pandas as pd

parser=argparse.ArgumentParser()
parser.add_argument("results",type=Path)
out=parser.parse_args().results
out.mkdir(exist_ok=True,parents=True)
rng=np.random.default_rng(57963)


def waves():
    rows=[]
    profiles=[]
    for n in [128,256,512]:
        for dt in [.2,.45]:
            for seed in range(1,9):
                x=(np.arange(n)-n//2)*64/n
                dx=64/n
                dispersion=dt*dx
                q0=np.zeros(n)
                support=np.abs(x)<3
                q0[support]=(1-(x[support]/3)**2)**2
                q0*=rng.uniform(.5,1.5)
                p0=np.zeros_like(q0)
                q,p=q0.copy(),p0.copy()
                steps=round(18/dispersion)
                def shift(field):
                    return np.roll(field,-1)
                def force(q):
                    return (shift(q)+np.roll(q,1)-2*q)/dx**2
                def step(q,p):
                    p=p+.5*dispersion*force(q)
                    q=q+dispersion*p
                    return q,p+.5*dispersion*force(q)
                def measures(q,p):
                    # Exact shadow energy for velocity Verlet on a harmonic lattice.
                    bonds=(shift(q)-q)/dx
                    e=.5*p*p+.25*(bonds*bonds+np.roll(bonds*bonds,1))
                    shadow=e.sum()-.125*dispersion**2*np.sum(force(q)**2)
                    prob=e/e.sum()
                    entropy=-np.dot(prob[prob>0],np.log(prob[prob>0]))
                    rms=np.sqrt(np.dot(x*x,e)/e.sum())
                    return shadow,e.sum(),entropy,rms,e
                h0,standard,initial_entropy,_,_=measures(q,p)
                for stage in ("forward","reverse"):
                    if stage=="reverse":
                        p=-p
                    for k in range(steps+1):
                        if k in [0,steps//4,steps//2,3*steps//4,steps]:
                            h,energy,entropy,rms,e=measures(q,p)
                            assert abs(h/h0-1)<1e-11
                            if stage=="forward":
                                assert not np.any(q[np.abs(x)>3+k*dx+1e-12])
                            error=np.linalg.norm(q-q0)/np.linalg.norm(q0)
                            rows.append((n,dt,seed,stage,k*dispersion,k,h/h0-1,energy/standard-1,
                                         entropy-initial_entropy,rms,error))
                            if n==256 and dt==.45 and seed==1:
                                profiles.append((stage,k*dispersion,e.copy()))
                        if k<steps:
                            q,p=step(q,p)
                assert np.max(abs(q-q0))<1e-11 and np.max(abs(p-p0))<1e-11
    pd.DataFrame(rows,columns=["L","courant","seed","stage","t","steps","shadow_error","energy_error",
                               "entropy_delta","rms","return_error"]).to_csv(out/"wave.csv",index=False)
    pd.DataFrame([(stage,t,i,float(x)) for stage,t,e in profiles for i,x in enumerate(e)],
                 columns=["stage","t","i","energy"]).to_csv(out/"wave_profiles.csv",index=False)


def fluctuation():
    # Biased local ring walk, uniform stationary distribution, positive reverse rates.
    rows=[]
    for p,q in [(.3,.3),(.45,.25),(.55,.15)]:
        distribution=np.array([1.])
        log_ratio=np.log(p/q)
        for n in range(1,161):
            distribution=np.convolve(distribution,[q,1-p-q,p])
            if n not in [10,40,160]:
                continue
            currents=np.arange(-n,n+1)
            sigma=currents*log_ratio
            relation=np.max(abs(np.log(distribution/distribution[::-1])-sigma))
            assert relation<1e-11
            exact=np.dot(distribution,np.exp(-sigma))
            assert abs(exact-1)<1e-12
            for seed in range(1,17):
                samples=rng.choice(currents,20000,p=distribution)
                estimator=np.exp(-samples*log_ratio).mean()
                rows.append((p,q,n,seed,exact,estimator,np.mean(samples<0),
                             distribution[currents<0].sum(),relation))
    pd.DataFrame(rows,columns=["p","q","n","seed","ift_exact","ift_mc","fraction_negative",
                               "prob_negative_exact","dft_residual"]).to_csv(out/"fluctuation.csv",index=False)


waves()
fluctuation()
