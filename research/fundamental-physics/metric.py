"""A static, area-weighted conformal torus with conservative edge flux."""
import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.sparse import diags, kronsum
from scipy.sparse.linalg import eigsh

parser = argparse.ArgumentParser()
parser.add_argument("results", type=Path, nargs="?", default=Path(__file__).parent / "results")
out = parser.parse_args().results
out.mkdir(parents=True, exist_ok=True)
rows = []
for n in [16,32,64,96]:
    x = 2*np.pi*np.arange(n)/n
    bump = np.cos(x[:,None])+np.cos(x[None,:])
    local = np.exp(.35*bump)
    local /= local.mean()
    one = diags([-np.ones(n-1),2*np.ones(n),-np.ones(n-1)],[-1,0,1],format="lil")
    one[0,-1] = one[-1,0] = -1
    lap = kronsum(one.tocsr(),one.tocsr())*(n/(2*np.pi))**2
    for label, area in [("flat",np.ones_like(local)),("conformal",local)]:
        invsqrt = diags(area.ravel()**-.5)
        op = (invsqrt @ lap @ invsqrt).tocsc()
        grid_cell_area = (2*np.pi/n)**2
        assert np.max(np.abs(op @ np.sqrt(area.ravel()))) < 1e-10
        # A positive shift away from the nonnegative spectrum avoids the null mode.
        values = np.sort(eigsh(op,k=13,sigma=-.01,which="LM",return_eigenvectors=False))
        assert abs(values[0])<1e-8 and values[1]>0
        assert np.isclose(area.sum()*grid_cell_area,(2*np.pi)**2)
        for j,value in enumerate(values):
            rows.append((n,label,j,value,area.max()/area.min()))
        # One conservative update at a CFL-safe step, localized initial mass.
        energy = np.zeros(n*n)
        energy[0]=1
        next_energy = energy - (.1/np.max(lap.diagonal()/area.ravel())) * (lap @ (energy/area.ravel()))
        assert np.isclose(next_energy.sum(),1) and next_energy.min()>=0
data = pd.DataFrame(rows,columns=["L","metric","index","lambda","stationary_mass_ratio"])
data.to_csv(out/"metric.csv",index=False)
fig,ax = plt.subplots(figsize=(6.5,3.7),layout="constrained")
for name, group in data.query("L==96 and index>0").groupby("metric"):
    ax.plot(group["index"],group["lambda"],"o-",label={"flat":"Flad","conformal":"Konform vægt"}[name])
ax.set(xlabel="Egenværdiens indeks",ylabel="Egenværdi")
ax.legend()
fig.savefig(out/"metrik.png",dpi=175)
