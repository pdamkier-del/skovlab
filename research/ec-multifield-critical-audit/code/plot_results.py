"""Regenerate a standalone scientific SVG from recorded ODE results."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path(__file__).resolve().parents[1]
d=json.loads((root/'results/03_classical_robustness.json').read_text())
fig,ax=plt.subplots(1,2,figsize=(10,4))
r=d['exact_refinement'][-1];v0=r['event']['volume']
for rec,label in [(r,'Exact background')]+[(x['records'][-1],x['case'].replace('_',' ')) for x in d['perturbations']]:
 ax[0].plot([z['t'] for z in rec['rows']],[z['volume']/v0 for z in rec['rows']],label=label)
ax[0].set(xlabel='Proper time (κ=1)',ylabel='Volume / exact minimum',title='Classical homogeneous full-field tests');ax[0].legend(fontsize=6)
n=[x['steps'] for x in d['exact_refinement']];e=[x['exact_endpoint_errors'][2] for x in d['exact_refinement']]
ax[1].loglog(n,e,'o-',label='Spinor endpoint norm error');ax[1].loglog(n,[e[0]*(n[0]/x)**4 for x in n],'--',label='Fourth order');ax[1].set(xlabel='RK4 steps',ylabel='Error',title='Exact-background refinement');ax[1].legend(fontsize=8)
fig.suptitle('Mathematical tests only: physical EFT control is not established',fontsize=10);fig.tight_layout();fig.savefig(root/'results/classical_tests.svg');plt.close(fig)
