import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve

parser = argparse.ArgumentParser()
parser.add_argument("results", type=Path, nargs="?", default=Path(__file__).parent / "results")
out = parser.parse_args().results
rng = np.random.default_rng(73042)


def intervals(table, keys, values, name):
    records = []
    for group, data in table.groupby(keys, sort=True):
        a = data[values].to_numpy()
        indices = rng.integers(len(a), size=(4000, len(a)))
        boot = a[indices].mean(axis=1)
        for j, value in enumerate(values):
            lo, hi = np.quantile(boot[:, j], [.025, .975])
            records.append(dict(zip(keys, group)) | dict(
                metric=value, n=len(a), mean=a[:, j].mean(), lo=lo, hi=hi))
    frame = pd.DataFrame(records)
    frame.to_csv(out / f"{name}_summary.csv", index=False)
    return frame


def arrow_scores():
    source = out / "arrow.csv"
    series = pd.read_csv(source if source.exists() else source.with_suffix(".csv.gz"))
    rows = []
    field_features = ["mean", "variance", "roughness", "entropy"]
    for (file, L, protocol, block), data in series.groupby(["file", "L", "protocol", "block"]):
        for start, stop in [(0, 80), (80, 240), (160, 320)]:
            for lag in [4, 20, 80]:
                for feature_set, features in [
                    ("reserve", field_features), ("energy", field_features + ["structure", "pool"])
                ]:
                    differences = []
                    control = []
                    for _, run in data.groupby("seed"):
                        a = run.set_index("t").loc[start:stop, features].to_numpy()
                        delta = a[lag//4:] - a[:-(lag//4)]
                        differences.append(delta)
                        control.append(delta * rng.choice([-1, 1], size=(len(delta), 1)))
                    for case, diffs in [("ordered", differences), ("scrambled", control)]:
                        train = np.concatenate(diffs[:12])
                        scale = train.std(axis=0)
                        scale[scale < 1e-12] = 1
                        train /= scale
                        # Paired forward/backward learning through an odd linear score.
                        weight = np.linalg.solve(train.T @ train + np.eye(len(features))*len(train)*.1,
                                                 train.sum(axis=0))
                        for seed, delta in enumerate(diffs[12:], 13):
                            score = delta / scale @ weight
                            accuracy = np.mean(np.where(np.abs(score)<1e-12, .5, score>0))
                            rows.append((file,L,protocol,block,start,lag,feature_set,case,seed,accuracy))
    keys = ["file","L","protocol","block","start","lag","features","case"]
    scores = pd.DataFrame(rows, columns=keys+["seed","accuracy"])
    scores.to_csv(out / "arrow_seed_scores.csv", index=False)
    return intervals(scores, keys, ["accuracy"], "arrow")


def kmp_theory(n, left, right):
    temperature = np.linspace(left, right, n+2)[1:-1]
    pairs = [(i,j) for i in range(n) for j in range(i,n)]
    lookup = {pair:index for index,pair in enumerate(pairs)}
    system = lil_matrix((len(pairs),len(pairs)))
    constant = np.zeros(len(pairs))
    for row,(i,j) in enumerate(pairs):
        for bond in sorted({i,i+1,j,j+1}):
            affected = {k for k in (bond-1,bond) if 0<=k<n}
            system[row,row] -= 1
            if i in affected and j in affected:
                coefficient = 1/3 if i==j else 1/6
                if 0<bond<n:
                    a,b = sorted(affected)
                    for pair, count in [((a,a),1),((a,b),2),((b,b),1)]:
                        system[row,lookup[pair]] += coefficient*count
                else:
                    bath = left if bond==0 else right
                    system[row,row] += coefficient
                    constant[row] += coefficient * (2*bath*temperature[i] + 2*bath**2)
            else:
                hit, other = (i,j) if i in affected else (j,i)
                system[row,row] += .5
                if 0<bond<n:
                    partner = next(k for k in affected if k!=hit)
                    system[row,lookup[tuple(sorted((partner,other)))]] += .5
                else:
                    bath = left if bond==0 else right
                    constant[row] += .5 * bath * temperature[other]
    moments = spsolve(system.tocsr(), -constant)
    assert np.max(np.abs(system @ moments + constant)) < 1e-10
    i,j = n//4-1,3*n//4-1
    return temperature[i],temperature[j],n*(moments[lookup[i,j]]-temperature[i]*temperature[j]),(left-right)/(2*(n+1))


def spectral():
    raw = []
    graph = []
    for dimension in [1,2,3]:
        for L in [12,24,48,96]:
            theta = 2*np.pi*np.fft.fftfreq(L)
            axis = 4*np.sin(theta/2)**2
            axes = np.ix_(*([axis]*dimension))
            lam = sum(axes)
            positive = lam[lam>0]
            for t in [1,4,16,64,256,1024]:
                p = np.exp(-t*positive).sum()/L**dimension
                ds = 2*t*np.sum(positive*np.exp(-t*positive))/L**dimension/p
                raw.append((dimension,L,t,positive.min(),p,ds,
                            np.sum(positive**-1),np.sum(positive**-2)))
            if dimension==2:
                inverse = np.divide(1,lam,out=np.zeros_like(lam),where=lam>0)
                green = np.fft.ifftn(inverse).real
                for r in range(1,L//2+1):
                    row = [L,r,green[0,r],green[0,0]-green[0,r]]
                    for mass in [.1,.35]:
                        g = np.fft.ifftn(1/(lam+mass**2)).real
                        # Pair excess free energy in kBT units for unit pinning strength.
                        row += [.5*np.log1p(-(g[0,r]/(1+g[0,0]))**2)]
                    graph.append(row)
    frame = pd.DataFrame(raw, columns=["dim","L","t","gap","trace","ds","zeta1","zeta2"])
    frame.to_csv(out / "spectral.csv",index=False)
    g = pd.DataFrame(graph,columns=["L","r","green","potential_kernel","free_m01","free_m035"])
    g.to_csv(out / "green.csv",index=False)
    return frame,g


def figures(arrow,mixing,response,kmp,spec,green):
    plt.rcParams.update({"axes.spines.top":False,"axes.spines.right":False,"font.size":10,
                         "figure.constrained_layout.use":True})

    def line(ax, data, x, y="mean", label=None):
        data = data.sort_values(x)
        ax.plot(data[x],data[y],marker="o",ms=4,label=label)
        if {"lo","hi"} <= set(data):
            ax.fill_between(data[x],data.lo,data.hi,alpha=.18)

    fig, axes = plt.subplots(2,2,figsize=(10,7))
    clip = arrow.query("L==24 and block==1 and lag==20 and features=='reserve'")
    for (file,protocol,case), a in clip.groupby(["file","protocol","case"]):
        if case == "ordered":
            model = "Peter" if file.startswith("peter") else "Fælles"
            climate = "konstant klima" if protocol == "constant" else "udgivet klima"
            line(axes[0,0],a,"start",label=f"{model}, {climate}")
    axes[0,0].axhline(.5,ls="--",color="grey")
    axes[0,0].set(xlabel="Vinduesstart (sweep)",ylabel="Korrekt tidsretning",ylim=(0,1.04))
    axes[0,0].legend(fontsize=8)
    for mask, a in mixing.query("L==36 and curvature==0 and metric=='fraction'").groupby("mask"):
        line(axes[0,1],a,"t",label={"labels":"10 artsmærkater","single":"Én art"}[mask])
    axes[0,1].set(xscale="symlog",xlabel="Diffusionstrin",ylabel="Andel tilbage af kvadratisk udsving")
    axes[0,1].legend()
    for (pool,mode), a in response.query("L==36 and mode!='sweep'").groupby(["pool","mode"]):
        if pool>36**2 and mode=="local":
            continue
        transport = "Diffusion" if mode == "local" else "Optag"
        line(axes[1,0],a,"d",label=f"{transport}, Q = {pool:.0f}")
        if mode == "uptake" and pool < 36**2:
            exact = (pool+12)/(36**2-1)-pool/36**2
            axes[1,0].axhline(exact,ls=":",color=axes[1,0].lines[-1].get_color(),
                              label="Forventet ved knap pulje")
    axes[1,0].axhline(0,color="grey",lw=.7)
    axes[1,0].set(xlabel="Gitterafstand",ylabel="Parret ændring i reserve på ét trin")
    axes[1,0].legend(fontsize=8)
    for (left,right),a in kmp.query("metric=='scaled_cov'").groupby(["left","right"]):
        line(axes[1,1],a,"N",label=f"({left:g}, {right:g})")
        axes[1,1].plot(a.N,a.reference,":",color=axes[1,1].lines[-1].get_color())
    axes[1,1].axhline(0,color="grey",lw=.7)
    axes[1,1].set(xlabel="Kædelængde N",ylabel="N × kovarians")
    axes[1,1].legend(title="Reservoirtemperaturer",fontsize=8)
    fig.savefig(out/"piloter.png",dpi=175)
    plt.close(fig)

    fig, axes = plt.subplots(1,3,figsize=(12,3.6))
    for dim,a in spec.query("L==96").groupby("dim"):
        line(axes[0],a,"t","ds",label=f"d = {dim}")
    axes[0].set(xscale="log",xlabel="Varmekernetid",ylabel="Effektiv spektral dimension")
    axes[0].legend()
    for L,a in green.groupby("L"):
        axes[1].plot(a.r,a.potential_kernel,label=f"L = {L}")
    axes[1].set(xscale="log",xlabel="Afstand (gitterenheder)",ylabel="Green-funktionens differens")
    axes[1].legend(fontsize=8)
    for col,label in [("free_m01","m = 0,1"),("free_m035","m = 0,35")]:
        a=green.query("L==96")
        axes[2].semilogy(a.r,-a[col],label=label)
    axes[2].set(xlabel="Afstand (gitterenheder)",ylabel="− interaktionsfri energi / kBT")
    axes[2].legend()
    fig.savefig(out/"spektrum.png",dpi=175)
    plt.close(fig)


pulse = pd.read_csv(out / "pulse.csv")
for row in pulse.query("curvature==0 and seed==1").itertuples():
    k = 2*np.pi*np.fft.fftfreq(row.L)
    eigenvalues = 4 - 2*np.cos(k[:,None]) - 2*np.cos(k[None,:])
    expected = np.mean((1-row.rate*eigenvalues)**row.t)
    assert abs(expected - pulse.loc[row.Index, "return"]) < 1e-12
control_path = out / "controls.csv"
if control_path.is_file():
    controls = pd.read_csv(control_path)
    intervals(controls, ["L","control"], ["delta","expected"], "controls")
arrow = arrow_scores()
mix = pd.read_csv(out / "mixing.csv")
mix["fraction"] = mix.squared / mix.groupby(["L","curvature","seed","mask"]).squared.transform("first")
mixing = intervals(mix,["L","curvature","mask","t"],["fraction"],"mixing")
pair = pd.read_csv(out / "response.csv").pivot(index=["L","seed","pool","d","mode"],columns="removed",values="reserve")
pair["delta"] = pair[True] - pair[False]
response = intervals(pair.reset_index(),["L","pool","d","mode"],["delta"],"response")
kmp_raw = pd.read_csv(out / "kmp.csv")
assert len(kmp_raw)==432 and np.max(np.abs(kmp_raw.balance))<1e-8
kmp_raw["scaled_cov"] = kmp_raw.N*kmp_raw["cov"]
kmp = intervals(kmp_raw,["N","left","right"],["Ti","Tj","scaled_cov","flux","arrow"],"kmp")
theory = {(n,l,r):dict(zip(["Ti","Tj","scaled_cov","flux"],kmp_theory(n,l,r)))
          for n,l,r in kmp.groupby(["N","left","right"]).groups}
kmp["reference"] = [theory[r.N,r.left,r.right].get(r.metric, 0 if r.left==r.right else np.nan)
                    for r in kmp.itertuples()]
kmp.to_csv(out/"kmp_summary.csv",index=False)
spec,green=spectral()
figures(arrow,mixing,response,kmp,spec,green)
