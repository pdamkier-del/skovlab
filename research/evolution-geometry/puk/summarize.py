import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

p=argparse.ArgumentParser()
p.add_argument("output",type=Path)
out=p.parse_args().output
rng=np.random.default_rng(526285)


def interval(data):
    v=np.asarray(data)
    draws=rng.integers(len(v),size=(4000,len(v)))
    lo,hi=np.quantile(v[draws].mean(axis=1),[.025,.975])
    return v.mean(),lo,hi


source=out/"minimal.csv"
raw=pd.read_csv(source if source.exists() else source.with_suffix(".csv.gz"))
thin=raw[raw.t.isin([0,40,120,240,360,480])]
axes=["L","env","mode","start","energy_density","beta","periodic","t"]
g=thin.groupby(axes)
rows=[]
for group,data in g:
    rows.append((*group,*interval(data.open),data.edge_x.mean()))
minimal=pd.DataFrame(rows,columns=axes+["mean","lo","hi","edge_x"])
minimal.to_csv(out/"minimal_summary.csv",index=False)
rows=[]
comparison=thin.query("t==480 and start==.5 and energy_density==2 and beta==14 and periodic")
for (L,env),d in comparison.groupby(["L","env"]):
    z=d.pivot(index="seed",columns="mode",values="open")
    for mode in ["neutral","frozen","decoupled","no_mutation"]:
        rows.append((L,env,mode,*interval(z.selection-z[mode])))
pd.DataFrame(rows,columns=["L","env","comparison","mean","lo","hi"]).to_csv(out/"minimal_contrasts.csv",index=False)

# Exact positive linear changes under a simultaneous inverse scaling of fitness.
same=thin.query("L==24 and env=='x' and mode=='selection' and start==.5 and periodic")
reference=same.query("energy_density==2 and beta==14").set_index(["seed","t"])
for density in [.5,1.,4.,8.]:
    s=same.query("energy_density==@density and abs(beta*energy_density-28)<1e-10").set_index(["seed","t"])
    assert np.array_equal(reference.open,s.open)
    assert np.max(abs(reference.reserve/2-s.reserve/density))<1e-12

motif=pd.read_csv(out/"motif_population.csv")
axes=["receiver","mode","relaxation_steps","t"]
summary=pd.DataFrame([(*k,*interval(a.cluster_share)) for k,a in motif.groupby(axes)],
                     columns=axes+["mean","lo","hi"])
summary.to_csv(out/"motif_summary.csv",index=False)
rows=[]
for (receiver,wait),data in motif.groupby(["receiver","relaxation_steps"]):
    last=data[data.t==data.t.max()].pivot(index="seed",columns="mode",values="cluster_share")
    for mode in ["neutral","frozen","decoupled"]:
        rows.append((receiver,wait,mode,*interval(last.selection-last[mode])))
pd.DataFrame(rows,columns=["receiver","relaxation_steps","comparison","mean","lo","hi"]
             ).to_csv(out/"motif_contrasts.csv",index=False)

interfaces=pd.read_csv(out/"interfaces.csv")
interfaces=interfaces[interfaces.t.isin([0,40,120,240,360,480])]
axes=["L","env","mode","t"]
interface_summary=pd.DataFrame([(*k,*interval(d.open)) for k,d in interfaces.groupby(axes)],
                               columns=axes+["mean","lo","hi"])
interface_summary.to_csv(out/"interface_summary.csv",index=False)
rows=[]
for (L,environment),d in interfaces.query("t==480").groupby(["L","env"]):
    tab=d.pivot(index="seed",columns="mode",values="open")
    rows.append((L,environment,*interval(tab.selection-tab.neutral)))
pd.DataFrame(rows,columns=["L","env","mean","lo","hi"]).to_csv(out/"interface_contrasts.csv",index=False)

plt.rcParams.update({"axes.spines.top":False,"axes.spines.right":False,
                     "figure.constrained_layout.use":True})
fig,axes=plt.subplots(1,2,figsize=(10.2,4.4))
test=minimal.query("L==24 and env=='x' and start==.5 and energy_density==2 and beta==14 and periodic")
styles={"selection":("#196f60","Selektion"),"neutral":("#415f83","Neutral"),
        "frozen":("#915527","Frossen graf"),"decoupled":("#79639a","Frakoblet graf"),
        "no_mutation":("#a14d64","Uden mutation")}
for mode,(color,label) in styles.items():
    s=test[test["mode"]==mode]
    axes[0].plot(s.t,s["mean"],"o-",color=color,label=label,ms=3)
    axes[0].fill_between(s.t,s.lo,s.hi,color=color,alpha=.13)
axes[0].set(xlabel="Sweep",ylabel="Andel med åbent tværgående anlæg",ylim=(0,1))
axes[0].legend(fontsize=8)
for (receiver,mode),s in summary.query("relaxation_steps==12 and mode in ['selection','neutral','frozen']").groupby(["receiver","mode"]):
    color,label=styles[mode]
    axes[1].plot(s.t,s["mean"],"o",color=color,ls="-" if receiver==3 else "--",
                 label=f"{label}, modtager {receiver}",ms=3)
    axes[1].fill_between(s.t,s.lo,s.hi,color=color,alpha=.08)
axes[1].set(xlabel="Generation",ylabel="Andel med positivt krumt motiv",ylim=(0,1))
axes[1].legend(fontsize=7.4)
fig.savefig(out/"minimal-og-krumning.png",dpi=175)
plt.close(fig)
