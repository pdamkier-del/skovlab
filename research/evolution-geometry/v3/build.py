"""Generate the independent offline laboratory from the Regge pilot CSVs."""
import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

p=argparse.ArgumentParser()
p.add_argument("results",type=Path)
p.add_argument("html",type=Path)
args=p.parse_args()
out=args.results
df=pd.read_csv(out/"homogeneous.csv")
rejected=pd.read_csv(out/"homogeneous_rejections.csv")
tables={"series":df,"rejected":rejected}
payload={name:json.loads(frame.to_json(orient="records",double_precision=13)) for name,frame in tables.items()}
template=Path(__file__).with_name("lab.html.in").read_text()
args.html.write_text(template.replace("__DATA__",json.dumps(payload,separators=(",",":"))))
plt.rcParams.update({"axes.spines.top":False,"axes.spines.right":False,
                     "figure.constrained_layout.use":True})
fig,ax=plt.subplots(1,3,figsize=(12,4))
for n,series in df.query("case=='mass_refine' and h0==.24").groupby("n"):
    label=f"n={n}"
    ax[0].plot(series.time,series.rho_volume,"o-",label=label,ms=4)
    line=ax[1].plot(series.time-series.duration,series.ricci,"o-",label=label,ms=4)[0]
    ax[1].plot(series.time-series.duration,series.ricci_reference,":",color=line.get_color())
    ax[2].plot(series.time,series.effective_dimension,"o-",label=label,ms=4)
for axis,y in zip(ax,["Feltenergi pr. rumcelle","Indre Regge-skalarkrumning","Spektral transportdimension"]):
    axis.set(xlabel="Ortogonal proper tid",ylabel=y)
    axis.legend()
fig.savefig(out/"v3-felt-og-geometri.png",dpi=170)
