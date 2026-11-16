"""Reproduce the six bounded classical validation cycles; no time evolution."""
from pathlib import Path
import subprocess, sys, json, hashlib, platform
import numpy, scipy, sympy
here=Path(__file__).resolve().parent
for script in ['verify_local.py','verify_canonical.py','verify_adm.py','initial_data.py','initial_curvature.py','verify_conservation.py']:
    print('Running',script,flush=True)
    subprocess.run([sys.executable,str(here/script)],check=True,cwd=here)
results=here.parent/'results'
for f in results.glob('*.json'):
    json.loads(f.read_text())
manifest={'python':platform.python_version(),'numpy':numpy.__version__,'scipy':scipy.__version__,'sympy':sympy.__version__,'scope':'local identities and initial data; no spacetime time evolution','code_sha256':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(here.glob('*.py'))}}
(results/'validation_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('All six validation scripts passed; JSON reload passed.')
