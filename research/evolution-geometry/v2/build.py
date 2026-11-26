"""Build the offline laboratory and a static figure from the raw results."""
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


def read(name):
    f=args.results/(name+".csv")
    return pd.read_csv(f if f.exists() else f.with_suffix(".csv.gz"))


free=read("free_profiles").query("points==1401")
flrw=read("flrw").query("curvature==0 and phase==0")
sp=read("sp_evolution").query("outer==24 and dr==.05")
circle=read("circle").query("phase==0")
rows={
    "free":free[["n","time","energy_within_r4","radial_entropy"]],
    "expansion":flrw.assign(n=flrw.n.astype(str)).iloc[::4][
        ["n","normalization","proper_time","density","volume_rate","Ricci_scalar","comoving_light_distance"]],
    "binding":sp[["n","perturbation","ratio","time","rms_ratio"]],
    "circle":circle.iloc[::2][["shear_sign","R0","t","R","heat_time","spectral_dimension"]],
}
data={k:json.loads(df.to_json(orient="records",double_precision=9)) for k,df in rows.items()}
template=Path(__file__).with_name("lab.html.in").read_text()
args.html.write_text(template.replace("__DATA__",json.dumps(data,separators=(",",":"))))
plt.rcParams.update({"axes.spines.top":False,"axes.spines.right":False,"figure.constrained_layout.use":True})
fig,axes=plt.subplots(2,2,figsize=(10,7.5))
for n,s in free.query("time>=0").groupby("n"):
    axes[0,0].plot(s.time,s.energy_within_r4,marker="o",ms=3,label=str(n))
axes[0,0].set(xlabel="Tid × m",ylabel="Andel af energi inden for r = 4",title="Frit Klein–Gordon-felt")
axes[0,0].legend(title="Rumlig n",ncol=3,fontsize=8)
for n,s in flrw.query("normalization=='density' and n in [2,3,8,64]").groupby("n"):
    axes[0,1].plot(s.proper_time,s.volume_rate,label=str(int(n)))
axes[0,1].set(xlabel="Egentid × m",ylabel="nH/m",title="Homogen EKG ved samme starttæthed")
axes[0,1].legend(title="Rumlig n",fontsize=8)
for n,s in sp.query("perturbation=='width' and ratio==.97").groupby("n"):
    axes[1,0].plot(s.time,s.rms_ratio,label=str(n))
axes[1,0].set(xlabel="Reskaleret tid",ylabel="Rms-radius / startværdi",title="Schrödinger–Poisson, fast norm")
axes[1,0].legend(title="Rumlig n",fontsize=8)
for scale,s in circle.query("R0==.3 and shear_sign==-1").groupby("heat_time"):
    axes[1,1].plot(s.t,s.spectral_dimension,label=f"u={scale:g}")
axes[1,1].set(xlabel="Egentid × m",ylabel="Rumlig spektral dimension",title="Dynamisk cirkel, fast topologi")
axes[1,1].legend(fontsize=8)
fig.savefig(args.results/"dimensioner.png",dpi=170)
