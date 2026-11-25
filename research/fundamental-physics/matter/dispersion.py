"""Measure the wave cone from the local stencil, including anisotropy and its limits."""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd

parser=argparse.ArgumentParser()
parser.add_argument("results",type=Path)
out=parser.parse_args().results
rows=[]
for c in [.7,1,1.4]:
    for a in [.32,.16,.08]:
        dt=.34*a/c
        for k_a in [.025,.05,.1,.2,.4,.8,1.5,2.4]:
            for angle in [0,np.pi/8,np.pi/4]:
                wavevector=k_a/a*np.array([np.cos(angle),np.sin(angle)])
                wave_number=k_a/a
                # Spatial eigenvalue from the site's four local neighbours on a plane wave.
                frequency_sq=(c/a)**2*np.sum(2-2*np.cos(a*wavevector))
                past,current=1.,1-.5*dt*dt*frequency_sq
                t=dt
                while current>0:
                    past,current=current,2*current-past-dt*dt*frequency_sq*current
                    t+=dt
                zero=t-dt+dt*past/(past-current)
                frequency=np.pi/(2*zero)
                rows.append((c,a,k_a,angle,wave_number,frequency,frequency/wave_number,
                             frequency/(wave_number*c)-1))
data=pd.DataFrame(rows,columns=["c","dx","ka","angle","k","omega","phase_speed","relative_error"])
data.to_csv(out/"dispersion.csv",index=False)
rows=[]
for (c,dx),s in data.query("ka<=.2").groupby(["c","dx"]):
    phase=np.polyfit(s.ka**2,s.phase_speed,1)[1]
    rows.append((c,dx,phase,phase/c-1))
pd.DataFrame(rows,columns=["c","dx","c_measured","relative_error"]).to_csv(out/"wave_speed.csv",index=False)
