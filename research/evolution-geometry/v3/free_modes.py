"""Audit discarded independent variations on two accepted homogeneous slices."""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from homogeneous import Frusta
from regge import potential

p=argparse.ArgumentParser()
p.add_argument("results",type=Path)
out=p.parse_args().results
data=pd.read_csv(out/"homogeneous.csv")
rows=[]
for (n,h0),states in data.query("case=='mass_refine' and step in [1,2]").groupby(["n","h0"]):
    if len(states)!=2:
        continue
    case=Frusta(n,.15,potential(.55),matter="axial")
    points=np.vstack([[states.ell0.iloc[0],.22],states[["scale","phi"]].to_numpy()])
    offset=case.offset
    across=case.cross
    slots=[]
    for i,h in enumerate(states.duration):
        a,u=points[i]
        b,v=points[i+1]
        square=-h*h+.25*((n-offset)*(b-a)**2+offset*(a+b)**2)
        intervals=np.where(across,square,offset*np.where(case.side==0,a*a,b*b))
        phi=np.where(case.time==0,u,v)
        _,dg,df,_,_=case.engine.evaluate(intervals,phi,.15,potential(.55))
        slots.append((dg,df,intervals))
    first,last=slots
    mid=first[0][(~across)&(case.side==1)]+last[0][(~across)&(case.side==0)]
    middle_fields=first[1][case.time==1]+last[1][case.time==0]
    cross=max(np.max(abs(record[0][across])) for record in slots)
    time=max(np.max(abs(record[0][across&(record[2]<0)])) for record in slots)
    rows.append((n,h0,cross,time,np.max(abs(mid)),np.max(abs(middle_fields))))
cols=["n","h0","all_cross_edge_residual","timelike_edge_residual","middle_spatial_edge_residual","field_residual"]
pd.DataFrame(rows,columns=cols).to_csv(out/"discarded_modes.csv",index=False)
