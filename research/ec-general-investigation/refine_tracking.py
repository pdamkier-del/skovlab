"""Fixed free-data family, resolution audit only; no bounce parameter search."""
import json
from pathlib import Path
from track import run

if __name__=='__main__':
    records=[]
    for n in [9,13,17]:
        r=run(n=n);last=r['rows'][-1]
        records.append({'n':n,'status':r['status'],'final':last})
    out={'units':'c = hbar = kappa = 1 (reduced Planck units)','records':records,'scope':'Short weak-field local tracing; reconstruction/continuity errors are measured, not assumed negligible.'}
    path=Path(__file__).with_name('tracking-refinement.json');path.write_text(json.dumps(out,indent=2)+'\n');print(path)
