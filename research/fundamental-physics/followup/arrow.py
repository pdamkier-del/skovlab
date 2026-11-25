import argparse
from itertools import product
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import brentq

parser = argparse.ArgumentParser()
parser.add_argument("results", type=Path)
out = parser.parse_args().results
out.mkdir(exist_ok=True, parents=True)
rng = np.random.default_rng(45112)


def ratchet(v, force):
    """Uniformized nearest-neighbour flashing ratchet, in units kBT=1."""
    rates = np.zeros((6,6))
    signs = np.zeros_like(rates)
    for state in range(6):
        mode, x = divmod(state,3)
        for step in (-1,1):
            j = (x+step)%3
            other = 3*mode+j
            rates[state,other] = np.exp((mode*v*(x-j)+step*force)/2)
            signs[state,other] = step
        rates[state,(1-mode)*3+x] = 1
    p = rates/ (2 * rates.sum(axis=1).max())
    p += np.diag(1-p.sum(axis=1))
    a = p.T-np.eye(6)
    a[-1] = 1
    pi = np.linalg.solve(a,[0,0,0,0,0,1])
    flux = pi[:,None]*p
    assert np.allclose(pi@p,pi) and np.isclose(pi.sum(),1)
    active = flux>0
    sigma = np.sum(flux[active]*np.log(flux[active]/flux.T[active]))
    bath = np.sum(flux[active]*np.log(p[active]/p.T[active]))
    assert np.isclose(sigma,bath,atol=1e-12)
    return p,pi,np.sum(flux*signs),sigma


def hidden_exact(p,pi,n):
    sequences = np.array(list(product(range(3), repeat=n)))
    probabilities = pi * (sequences[:,0,None]==np.arange(6)%3)
    for i in range(1,n):
        probabilities = probabilities@p * (sequences[:,i,None]==np.arange(6)%3)
    f = probabilities.sum(axis=1)
    rev = np.ravel_multi_index(sequences[:,::-1].T,[3]*n)
    assert np.isclose(f.sum(),1)
    return np.dot(f,np.log(f/f[rev]))


def counts(values, n, lag, alphabet):
    n_words = len(values)-(n-1)*lag
    words = np.zeros(n_words,dtype=int)
    for i in range(n):
        words = words*alphabet+values[i*lag:i*lag+n_words]
    return np.bincount(words,minlength=alphabet**n)


def evaluate(arrays, n, lag, alphabet):
    """Out-of-sample improvement in log score for forward versus reversed."""
    c = np.array([counts(a,n,lag,alphabet) for a in arrays])
    reverse = np.array([int(sum(v*alphabet**i for i,v in enumerate(word)))
                        for word in product(range(alphabet),repeat=n)])
    train, test = np.split(c,2)
    f = train.sum(axis=0)+.5
    logratio = np.log(f/f[reverse])
    observed = test@logratio/test.sum(axis=1)
    resamples = rng.integers(len(test),size=(3000,len(test)))
    lo,hi = np.quantile(observed[resamples].mean(axis=1),[.025,.975])
    orientations = np.array(list(product([-1,1],repeat=len(test))))
    p = np.mean((orientations@observed/len(test))>=observed.mean()-1e-12)
    return observed.mean(),lo,hi,p


def benchmark():
    results=[]
    stall=brentq(lambda f:ratchet(2.,f)[2],-2,2,xtol=1e-14)
    for name,v,force in [("reversibel",2.,0.),("drevet",2.,0.),("stall",2.,stall)]:
        if name=="reversibel":
            # Uniform mode flips are driven when v is nonzero.
            v=0.
        p,pi,drift,sigma=ratchet(v,force)
        chains=np.zeros((24,24000),dtype=int)
        chains[:,0]=rng.choice(6,size=len(chains),p=pi)
        cdf=p.cumsum(axis=1)
        cdf[:,-1]=1.
        for i in range(1,chains.shape[1]):
            chains[:,i]=np.sum(rng.random((len(chains),1))>cdf[chains[:,i-1]],axis=1)
        for alphabet in [3,6]:
            for n in range(2,9 if alphabet==3 else 5):
                exact = hidden_exact(p,pi,n) if alphabet==3 else (n-1)*sigma
                measured=evaluate(chains%alphabet,n,1,alphabet) if n<=5 else (np.nan,)*4
                results.append((name,alphabet,n,force,drift,sigma,exact,*measured))
    pd.DataFrame(results,columns=["model","alphabet","n","force","drift","sigma","exact","kl","lo","hi","p"]).to_csv(out/"ratchet.csv",index=False)


def forest():
    rows, checks = [], []
    file_names = ["shared_original","peter_original","peter_bounded","peter_no_diffusion","peter_no_combat"]
    for case in file_names:
        source = out/(case+".csv")
        if not source.exists():
            source = source.with_suffix(".csv.gz")
        if not source.exists():
            continue
        f=pd.read_csv(source)
        for L,data in f.groupby("L"):
            end=int(data.t.max())
            start=end-800
            by_seed = [x for _,x in data.groupby("seed")]
            margins={"reserve":.28,"structure":.28,"pool":.28,"height":.3,"live":.025}
            accepted=True
            for observable, margin in margins.items():
                four=np.array([[run.loc[run.t.between(t,t+198),observable].mean()
                                for t in range(start,end,200)] for run in by_seed])
                indices = rng.integers(len(four),size=(3000,len(four)))
                changes=four[:,1:]-four[:,[0]]
                lo,hi=np.quantile(changes[indices].mean(axis=1),[.025,.975],axis=0)
                constant=bool(np.all(np.abs(four-four[0,0])<1e-10))
                equivalent=bool(np.all((lo>-margin)&(hi<margin)))
                accepted &= equivalent
                checks.append((case,L,observable,start,margin,*four.mean(axis=0),
                               lo.min(),hi.max(),equivalent,constant))
            for observable in ["reserve","variance","roughness","structure","pool","height","up","down"]:
                values=np.array([run.loc[run.t>=start,observable].to_numpy() for run in by_seed])
                # Blind bin edges learned once from seeds 1–8. Avoid labelling roundoff.
                values=np.round(values,9)
                training=values[:8].ravel()
                edges=np.unique(np.quantile(training,[.25,.5,.75]))
                edges=edges[(edges>training.min())&(edges<training.max())]
                if not len(edges):
                    continue
                symbols=np.digitize(values,edges)
                for n,lag in product([2,3,4],[1,4,16]):
                    rows.append((case,L,observable,start,accepted,n,2*lag,*evaluate(symbols,n,lag,len(edges)+1)))
    pd.DataFrame(checks,columns=["model","L","observable","start","margin","w1","w2","w3","w4","lo","hi","equivalent","constant"]).to_csv(out/"stationarity.csv",index=False)
    pd.DataFrame(rows,columns=["model","L","observable","start","stationary_screen","n","lag","kl","lo","hi","p"]).to_csv(out/"forest_kl.csv",index=False)


if __name__ == "__main__":
    benchmark()
    forest()
