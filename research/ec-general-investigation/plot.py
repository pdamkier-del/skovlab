"""Standalone scientific figure of declared short weak-field measurements."""
import json,os,tempfile
from pathlib import Path
os.environ.setdefault("MPLCONFIGDIR",str(Path(tempfile.gettempdir())/"skovlab-general-mpl"))
os.environ.setdefault("XDG_CACHE_HOME",str(Path(tempfile.gettempdir())/"skovlab-general-cache"))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent
r=json.loads((ROOT/'tracked-fine-example.json').read_text());rows=r['rows'];last=rows[-1]
t=np.array([x['proper_time'][0] for x in rows]);tn=np.array([x['normal_proper_time'][0] for x in rows])
fig=plt.figure(figsize=(7.2,5.2),layout='constrained');gs=fig.add_gridspec(2,2);ax=[fig.add_subplot(gs[0,:]),fig.add_subplot(gs[1,0]),fig.add_subplot(gs[1,1])]
ax[0].plot(t,[x['N_material_integral'][0] for x in rows],'-o',ms=3,label='Volumen/ekspansion')
ax[0].plot(t,[x['N_density_reference'][0] for x in rows],'--',label='Tæthedsreference')
ax[0].set(xlabel='Strømbanens egentid (modelenheder)',ylabel='Lokale e-folds',title='Dirac-strøm · markør 1');ax[0].legend(fontsize=7)
ax[1].plot(tn,[x['N_normal'][0] for x in rows],'-o',ms=3,color='#b96037');ax[1].set(xlabel='Normalbanens egentid (modelenheder)',ylabel='Normal-e-folds',title='ADM-normal · samme startpunkt')
values=last['N_directional_principal_stretches'][0];ax[2].bar(['1','2','3'],values,color=['#b96037' if x<0 else '#356b91' for x in values]);ax[2].axhline(np.mean(values),color='#333',ls='--',label='Gennemsnit');ax[2].axhline(0,color='#aaa',lw=.6);ax[2].set(xlabel='Hovedstrækning (sorteret)',ylabel='Retningsbestemte e-folds',title='Netto ved sidste tidspunkt');ax[2].legend(fontsize=7)
for a in ax:a.grid(alpha=.2);a.ticklabel_format(axis='y',style='sci',scilimits=(0,0));a.tick_params(labelsize=8)
fig.suptitle('Kort 3D-svagfeltstest · 17³ punkter\nIngen global bounce- eller inflationskonklusion',fontsize=11)
fig.savefig(ROOT/'efolds-example.png',dpi=180);fig.savefig(ROOT/'efolds-example.pdf');plt.close(fig)
