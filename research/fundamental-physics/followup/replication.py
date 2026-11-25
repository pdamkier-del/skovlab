from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import wasserstein_distance

from arrow import counts, evaluate, out

rows=[]
distribution=[]
stationarity=[]
for L in [10,20]:
    source = out/f"shared_validation_{L}.csv"
    data=pd.read_csv(source if source.exists() else source.with_suffix(".csv.gz"))
    for observable in ["reserve","structure","height","live"]:
        for first,last in [(2400,2799),(2800,3199),(3200,3599)]:
            for seed,chain in data.groupby("seed"):
                x=chain.loc[chain.t.between(first,last),observable].to_numpy()
                reference=chain.loc[chain.t.between(2400,2799),observable].to_numpy()
                stationarity.append((L,observable,first,seed,x.mean(),x.std(),
                                     wasserstein_distance(x,reference)))
    for window in [(2400,2800),(2800,3200),(3200,3600),(2400,3600)]:
        selected=data[data.t.between(*window)]
        e=np.array([run.reserve.to_numpy() for _,run in selected.groupby("seed")])
        train=e[:len(e)//2].ravel()
        edges_options=[("quartiles",np.quantile(train,[.25,.5,.75])),
                       ("tertiles",np.quantile(train,[1/3,2/3])),
                       ("fixed",[.75,1.,1.25])]
        for (label,edges),lag,n in product(edges_options,[1,2,8],[2,3,4]):
            edges=np.unique(edges)
            symbols=np.digitize(e,edges)
            rows.append((L,*window,label,lag,n,*evaluate(symbols,n,lag,len(edges)+1)))
            if window==(2400,3600) and n==3 and lag in [1,2] and label=="quartiles":
                alphabet=len(edges)+1
                c=np.array([counts(a,n,lag,alphabet) for a in symbols])
                train,test=np.split(c,2)
                for i,w in enumerate(product(range(alphabet),repeat=n)):
                    reverse=sum(s*alphabet**j for j,s in enumerate(w))
                    distribution.append((L,lag,"".join(map(str,w)),train[:,i].sum()/train.sum(),
                                         test[:,i].sum()/test.sum(),test[:,reverse].sum()/test.sum()))
cols=["L","start","stop","bins","lag","n","kl","lo","hi","p"]
pd.DataFrame(rows,columns=cols).to_csv(out/"shared_validation_kl.csv",index=False)
pd.DataFrame(distribution,columns=["L","lag","word","train_forward","test_forward","test_reverse"]
             ).to_csv(out/"shared_words.csv",index=False)
pd.DataFrame(stationarity,columns=["L","observable","start","seed","mean","sd","distance_to_first"]
             ).to_csv(out/"shared_validation_stationarity.csv",index=False)
