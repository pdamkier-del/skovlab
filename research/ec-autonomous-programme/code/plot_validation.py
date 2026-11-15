"""Reproduce the standalone SVG from recorded numerical results."""
import os
os.environ.setdefault('MPLCONFIGDIR','/tmp/skovlab-mpl-cache')
os.environ.setdefault('XDG_CACHE_HOME','/tmp/skovlab-cache')
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['svg.fonttype']='none'
import matplotlib.pyplot as plt
import numpy as np
ROOT=Path(__file__).resolve().parents[1]

def load(name):return json.loads((ROOT/'results'/name).read_text())
def main():
    c1=load('cycle01_homogeneous.json');c3=load('cycle03_perturbations.json');c4=load('cycle04_3d_initial.json')
    fig,axes=plt.subplots(1,3,figsize=(13,3.8),layout='constrained')
    ax=axes[0];dt=np.array([r['dt'] for r in c1['records']]);err=np.array([r['state_relative_errors'] for r in c1['records']])
    for j,label in enumerate(['metric','metric velocity','spinor']):ax.loglog(dt,err[:,j],'o-',label=label)
    ax.loglog(dt,err[-1,0]*(dt/dt[-1])**4,'k:',label='fourth-order guide');ax.set(xlabel='harmonic time step',ylabel='relative endpoint state error',title='C01: exact strong-curvature test');ax.legend(fontsize=8)
    ax=axes[1];ns=np.array([r['n'] for r in c4['records']]);h=8/ns;errors=np.array([r['FD_Hamiltonian_relative'] for r in c4['records']]);ax.loglog(h,errors,'o-',label='C04 initial 3D constraints')
    c5path=ROOT/'results'/'cycle05_full3d.json'
    if c5path.exists():
        c5=json.loads(c5path.read_text());r=c5['spatial_records'];ax.loglog([8/x['n'] for x in r],[x['final']['Hamiltonian_relative'] for x in r],'s-',label='C05 evolved 3D constraints')
    ax.loglog(h,errors[-1]*(h/h[-1])**2,'k:',label='second-order guide');ax.set(xlabel='coordinate grid spacing',ylabel='relative Hamiltonian residual',title='Independent FD constraint checks');ax.legend(fontsize=8)
    ax=axes[2]
    for epsilon in [.1,.3]:
        cases=[c for c in c3['cases'] if c['parameters']['epsilon']==epsilon]
        ax.plot([c['parameters']['mode'] for c in cases],[c['runs'][-1]['density_contrast_amplification'] for c in cases],'o-',label=f'seed amplitude {epsilon}')
    ax.axhline(1,color='k',linestyle=':');ax.set(xlabel='integer seed mode (two tested)',ylabel='endpoint density-contrast amplification',title='C03: mode-dependent response',xticks=[1,4]);ax.legend(fontsize=8)
    for ax in axes:ax.grid(True,alpha=.2)
    fig.suptitle('Classical periodic ECD verification; finite intervals, no general stability theorem',fontsize=11)
    output=ROOT/'figures'/'validation.svg';output.parent.mkdir(parents=True,exist_ok=True);fig.savefig(output,metadata={'Date':None});print(output)
if __name__=='__main__':main()
