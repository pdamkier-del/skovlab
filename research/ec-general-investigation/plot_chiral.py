"""Figure of the checked analytic chiral solution, kept separate from 3D data."""
from pathlib import Path
import os,tempfile
os.environ.setdefault('MPLCONFIGDIR',str(Path(tempfile.gettempdir())/'skovlab-chiral-mpl'))
os.environ.setdefault('XDG_CACHE_HOME',str(Path(tempfile.gettempdir())/'skovlab-chiral-cache'))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from chiral_benchmark import normalized_solution
ROOT=Path(__file__).resolve().parent
x=np.linspace(-3,3,301);r=normalized_solution(x);t=r['proper_time_q_over_ab2'];end=normalized_solution(1.)['proper_time_q_over_ab2']
fig=plt.figure(figsize=(7.2,5.2),layout='constrained');g=fig.add_gridspec(2,2);ax=[fig.add_subplot(g[0,:]),fig.add_subplot(g[1,0]),fig.add_subplot(g[1,1])]
ax[0].plot(t,r['a_over_ab']);ax[0].set(ylabel='a / aᵦ',xlabel='Normaliseret egentid',title='Eksakt skala fra feltligningerne')
ax[1].plot(t,r['H_ab2_over_q']);ax[1].axhline(0,color='#aaa',lw=.6);ax[1].set(ylabel='Normaliseret H',xlabel='Normaliseret egentid',title='Kontraktion → ekspansion')
post=x>=0;ax[2].plot(t[post],r['volume_scale_efolds_from_bounce'][post]);ax[2].axhline(np.log(2)/2,color='#9a6039',ls='--',label='N_acc = 0,347');ax[2].set(ylabel='E-folds efter bounce',xlabel='Normaliseret egentid',title='Accelereret fase er kort');ax[2].legend(fontsize=8)
for a in ax:a.axvspan(0,end,color='#8fbc94',alpha=.25);a.grid(alpha=.2);a.tick_params(labelsize=8)
fig.suptitle('Eksakt seks-felts ECD-benchmark\nFLRW-metrik; ingen afgrænset stofsky',fontsize=11)
fig.savefig(ROOT/'chiral-benchmark.png',dpi=180);fig.savefig(ROOT/'chiral-benchmark.pdf');plt.close(fig)
