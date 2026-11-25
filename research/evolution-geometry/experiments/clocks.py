"""An identifiability check for a graph optical metric. The lapses are prescribed."""
import argparse
import gzip
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra

parser=argparse.ArgumentParser()
parser.add_argument("results",type=Path)
out=parser.parse_args().results
p=out/"snapshots_0.json"
with (p.open() if p.is_file() else gzip.open(str(p)+".gz","rt")) as handle:
    data=json.load(handle)
rows=[]
for L in [12,20,28]:
    for seed in range(1,13):
        r=[s for s in data if s["L"]==L and s["seed"]==seed and s["treatment"]=="mutation"]
        n=L**2
        edges=np.array(r[0]["edges"])
        labels=np.array(r[-1]["labels"])
        trait=np.array(r[-1]["strategies"])
        i,j=edges.T
        active=(labels[i]>=0)&(labels[j]>=0)&((labels[i]==labels[j])|
                                             (abs(trait[labels[i]]-trait[labels[j]])<=.01+1e-12))
        i,j=edges[active].T
        if not len(i):
            continue
        c=1.7
        # First metric: unit length and unit lapse.
        length=np.ones(len(i))
        lapse=np.ones(n)
        # Second metric: the same local conformal factor for length and time.
        new_lapse=1+.4*np.cos(2*np.pi*np.arange(n)/L)
        edge_clock=np.sqrt(new_lapse[i]*new_lapse[j])
        new_length=length*edge_clock
        duration=length/c
        new_duration=new_length/(edge_clock*c)
        assert np.allclose(new_duration,duration,atol=1e-15)
        a=np.r_[i,j]; b=np.r_[j,i]
        def paths(delay):
            model=csr_matrix((np.r_[delay,delay],(a,b)),shape=(n,n))
            return dijkstra(model,indices=np.unique(i)[:12])
        old,new=paths(duration),paths(new_duration)
        finite=np.isfinite(old)
        change=np.max(abs(new[finite]-old[finite]))
        spatial_change=np.max(abs(paths(new_length)[finite]-paths(length)[finite]))
        speed_error=np.max(abs(new_length/(new_duration*edge_clock)-c))
        rows.append((L,seed,len(i),change,spatial_change,new_lapse.max()/new_lapse.min(),speed_error))
cols=["L","seed","active_edges","arrival_difference","spatial_difference","clock_ratio","c_error"]
pd.DataFrame(rows,columns=cols).to_csv(out/"clock_ambiguity.csv",index=False)
