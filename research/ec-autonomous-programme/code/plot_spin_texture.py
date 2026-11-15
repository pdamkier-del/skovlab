"""Reproduce the spin-texture convergence/curvature/focusing evidence plot."""
import os
os.environ.setdefault('MPLCONFIGDIR','/tmp/skovlab-mpl-cache');os.environ.setdefault('XDG_CACHE_HOME','/tmp/skovlab-cache')
from pathlib import Path
import json,argparse
import numpy as np
import matplotlib
matplotlib.use('Agg');matplotlib.rcParams['svg.fonttype']='none'
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]

def main():
    p=argparse.ArgumentParser();p.add_argument('--preview',type=Path);args=p.parse_args()
    evo=json.loads((ROOT/'results/cycle08_spin_evolution.json').read_text());foc=json.loads((ROOT/'results/cycle09_focusing_balance.json').read_text())
    fig,axes=plt.subplots(1,3,figsize=(14,4.3),layout='constrained')
    rows=evo['spatial_records'];h=np.array([8/r['n'] for r in rows]);err=np.array([r['final']['Hamiltonian_relative'] for r in rows])
    axes[0].loglog(h,err,'o-',label='evolved constraint');axes[0].loglog(h,err[-1]*(h/h[-1])**2,'k:',label='second-order guide')
    axes[0].set(xlabel='grid spacing',ylabel='relative Hamiltonian residual',title='Textured 3D contraction');axes[0].legend(fontsize=8)
    for r in rows:
        axes[1].semilogy([v['time'] for v in r['full_curvature_history']],[v['probes'][-1]['full_K_max'] for v in r['full_curvature_history']],'o-',label=f"{r['n']} cubed")
    axes[1].set(xlabel='harmonic coordinate time',ylabel='maximum full-connection K',title='Three persisted curvature slices');axes[1].legend(fontsize=8)
    terms=foc['records'][-1]['probes'][-1]['terms'];keys=['volume_focusing','shear_focusing','vorticity_defocusing','acceleration_divergence','explicit_contact_source_identity','other_source_identity'];labels=['volume','shear','rotation','accel. div.','contact*','other source']
    values=[terms[k]['mean'] for k in keys];colors=['#a43b35' if x<0 else '#287d88' for x in values]
    axes[2].bar(range(len(values)),values,color=colors);axes[2].set_yscale('symlog',linthresh=1e-4);axes[2].set_xticks(range(len(labels)),labels,rotation=35,ha='right');axes[2].axhline(0,color='black',lw=.6)
    axes[2].set_ylim(-40,1e-3)
    axes[2].set(ylabel='coordinate-grid mean contribution',title='Current Raychaudhuri balance, t=0.2')
    fig.suptitle('Classical periodic spin texture: finite-interval numerical evidence',fontsize=12)
    fig.supxlabel('*Contact splitting is an on-shell identity, not a torsion-free comparison. Means are not proper-volume averages.',fontsize=9)
    for ax in axes:ax.grid(True,alpha=.2)
    out=ROOT/'figures/spin_texture.svg';fig.savefig(out,metadata={'Date':None})
    if args.preview:fig.savefig(args.preview,dpi=130)
    print(out)
if __name__=='__main__':main()
