"""Seed-level inference, stationary sequence control, and plots."""
import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

parser=argparse.ArgumentParser()
parser.add_argument("results",type=Path)
out=parser.parse_args().results
rng=np.random.default_rng(4853)
dimensions=["dimension_4","dimension_8","dimension_16"]
coordinates=["axis_x","axis_y","axis_z"]
metrics=["rank1","rank2","rank3",*coordinates,"edges"]


def estimate(values):
    x=np.asarray(values,float)
    x=x[np.isfinite(x)]
    if len(x)==0:
        return np.nan,np.nan,np.nan,0
    resamples=rng.integers(len(x),size=(4000,len(x)))
    lo,hi=np.quantile(x[resamples].mean(axis=1),[.025,.975])
    return x.mean(),lo,hi,len(x)


forest=pd.read_csv(out/"forest_geometry.csv",dtype={"geometry":str})
rows=[]
for (geometry,L,t,tr),d in forest.groupby(["geometry","L","t","treatment"]):
    for metric in ["largest","kappa",*dimensions]:
        tab=d.pivot(index="seed",columns="mode",values=metric)
        for label in tab:
            rows.append((geometry,L,t,tr,metric,label,*estimate(tab[label])))
        for label in ["shuffled","occupied_substrate","matched_edge_count","frozen_initial"]:
            rows.append((geometry,L,t,tr,metric,"observed_minus_"+label,
                         *estimate(tab.observed-tab[label])))
columns=["geometry","L","t","treatment","metric","comparison","mean","lo","hi","n"]
forest_summary=pd.DataFrame(rows,columns=columns)
forest_summary.to_csv(out/"forest_summary.csv",index=False)

architectures=[]
for name in ["architecture","architecture_focused","architecture_replicate"]:
    f=pd.read_csv(out/f"{name}.csv")
    f["series"]=name
    architectures.append(f)
arch=pd.concat(architectures,ignore_index=True)
rows=[]
for (series,L,env,start,t),d in arch.groupby(["series","L","env","start","t"]):
    for metric in metrics:
        tab=d.pivot(index="seed",columns="mode",values=metric)
        for label in tab:
            rows.append((series,L,env,start,t,metric,label,*estimate(tab[label])))
            if label!="selection":
                rows.append((series,L,env,start,t,metric,"selection_minus_"+label,
                             *estimate(tab.selection-tab[label])))
columns=["series","L","env","start","t","metric","comparison","mean","lo","hi","n"]
arch_summary=pd.DataFrame(rows,columns=columns)
arch_summary.to_csv(out/"architecture_summary.csv",index=False)


def words(seq,lag):
    a,b,c=seq[:-2*lag],seq[lag:-lag],seq[2*lag:]
    return np.bincount(16*a+4*b+c,minlength=64)


def arrow():
    source=out/"architecture_time.csv"
    df=pd.read_csv(source if source.is_file() else source.with_suffix(".csv.gz"))
    rows=[]
    for (L,env),g in df.groupby(["L","env"]):
        for observable,margin in [("reserve",.001),("roughness",.001)]:
            late=g[g.t>=600]
            mode_sequences={mode:np.array([d[observable].to_numpy() for _,d in s.groupby("seed")])
                            for mode,s in late.groupby("mode")}
            reverse=np.array([(i%4)*16 + (i//4%4)*4 + i//16 for i in range(64)])
            mesh=np.arange(next(iter(mode_sequences.values())).shape[1],dtype=float)
            mesh-=mesh.mean()
            def residual(x):
                return x-x.mean()-np.dot(mesh,x)*mesh/np.dot(mesh,mesh)
            for control in ["raw","detrended"]:
                arrays={mode:np.array([residual(a) for a in seq]) if control=="detrended" else seq
                        for mode,seq in mode_sequences.items()}
                pool=np.concatenate([v[:6].ravel() for v in arrays.values()])
                quartiles=np.quantile(pool,[.25,.5,.75])
                for mode,samples in arrays.items():
                    original=mode_sequences[mode]
                    changes=[seq[51:].mean()-seq[:50].mean() for seq in original]
                    md,lo,hi,_=estimate(changes)
                    accepted=lo>-margin and hi<margin
                    for lag in [1,4,8]:
                        count=np.array([words(np.digitize(seq,quartiles),lag) for seq in samples])
                        train=count[:6].sum(axis=0)+.5
                        score=np.log(train/train[reverse])
                        heldout=count[6:]@score/count[6:].sum(axis=1)
                        rows.append((L,env,observable,mode,control,2*lag,md,lo,hi,accepted,*estimate(heldout)))
    cols=["L","env","observable","mode","control","lag","drift","drift_lo","drift_hi","passes",
          "kl","lo","hi","n"]
    pd.DataFrame(rows,columns=cols).to_csv(out/"architecture_arrow.csv",index=False)


arrow()

plt.rcParams.update({"axes.spines.top":False,"axes.spines.right":False,
                     "figure.constrained_layout.use":True})
palette=["#297065","#47668c","#9a5a29"]
fig,ax=plt.subplots(1,2,figsize=(10,4.4))
a=forest_summary.query("L==20 and t==260 and treatment=='mutation' and metric=='kappa'")
order=["cliques","torus","regular"]
names=["Klikegitter","Kvadrattorus","Tilfældig 4-regulær"]
for j,(mode,name) in enumerate([("occupied_substrate","Besat substrat"),
                                ("observed","Aktive transportkanter"),
                                ("matched_edge_count","Samme kantantal")]):
    subset=a[a.comparison==mode].set_index("geometry").loc[order]
    x=np.arange(len(order))+(j-1)*.20
    ax[0].errorbar(x,subset["mean"],yerr=[subset["mean"]-subset.lo,subset.hi-subset["mean"]],
                   fmt="o",capsize=3,color=palette[j],label=name)
ax[0].axhline(0,color="0.55",lw=.8)
ax[0].set(xticks=np.arange(3),xticklabels=names,ylabel="Ollivier–Ricci-krumning")
ax[0].tick_params(axis="x",labelrotation=12)
ax[0].legend(fontsize=8)
q=arch_summary.query("L==16 and start=='balanced' and env=='strong_layers' and metric=='axis_x'")
for j,(mode,name) in enumerate([("selection","Med selektion"),
                                ("neutral","Neutral arv"),
                                ("decoupled","Genotype frakoblet")]):
    sub=q[q.comparison==mode]
    ax[1].plot(sub.t,sub["mean"],"o-",color=palette[j],label=name,ms=3)
    ax[1].fill_between(sub.t,sub.lo,sub.hi,color=palette[j],alpha=.16)
ax[1].set(xlabel="Sweep",ylabel="Andel med ledning på tværs af lag",ylim=(0,1))
ax[1].legend(fontsize=8)
fig.savefig(out/"krumning-og-selektion.png",dpi=170)
plt.close(fig)

c=pd.read_csv(out/"calibration.csv")
fig,ax=plt.subplots(1,2,figsize=(10,4.2))
x=np.array([2,4,8,16,32,64])
for row in c.query("model!='sierpinski_stochastic'").itertuples():
    ax[0].plot(x,[getattr(row,f"dimension_{t}") for t in x],"o-",label=row.model,ms=4)
ax[0].set(xscale="log",xlabel="Start på dyadisk tidsinterval",ylabel="Effektiv spektral dimension")
ax[0].legend()
f=forest.query("t==260 and treatment=='mutation' and mode=='observed' and L==20")
for geometry,name in zip(order,names):
    y=f[f.geometry==geometry][[f"dimension_{t}" for t in x]].mean().to_numpy()
    ax[1].plot(x,y,"o-",label=name,ms=4)
ax[1].set(xscale="log",xlabel="Start på dyadisk tidsinterval",ylabel="Effektiv spektral dimension")
ax[1].legend()
fig.savefig(out/"transportdimension.png",dpi=170)
plt.close(fig)
