"""Execute actual checks; --record writes this task's validation snapshot."""
from pathlib import Path
import hashlib,json,platform,re,subprocess,sys
ROOT=Path(__file__).resolve().parents[3]
STAGE=ROOT/'research/ec-dirac-collapse'
commands=[
 ['python','-m','unittest','discover','-s','research/ec-spherical/validation','-v'],
 ['python','-m','unittest','discover','-s','research/ec-spherical/full-weyssenhoff/validation','-v'],
 ['python','-m','unittest','discover','-s','research/ec-matter-models/validation','-v'],
 ['python','-m','unittest','discover','-s','research/ec-two-matter-models/validation','-v'],
 ['python','research/ec-dirac-collapse/validation/test_symbolic.py'],
 ['node','--test','research/ec-dirac-collapse/validation/model.test.mjs'],
 ['npm','test'],
 ['node','research/ec-dirac-collapse/validation/browser.test.cjs'],
]
runs=[]
for cmd in commands:
    result=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True)
    output=result.stdout+result.stderr
    print(output)
    count=re.search(r'(?:Ran |(?:ℹ|#) tests )(\d+)',output)
    runs.append({'command':cmd,'exit_code':result.returncode,'tests':int(count.group(1)) if count else None,'output':output})
checks=[]
for line in (ROOT/'research/ec-spherical/baseline-flrw.sha256').read_text().splitlines():
    expected,path=line.split(maxsplit=1)
    checks.append({'path':path,'unchanged':hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==expected})
success=all(r['exit_code']==0 for r in runs) and all(x['unchanged'] for x in checks)
if '--record' in sys.argv:
    pdf=subprocess.run(['bash','research/ec-dirac-collapse/build_pdf.sh'],cwd=ROOT,capture_output=True,text=True)
    baseline='efeb67c66af89c202bc7fe7017b781a41dd4afc8'
    unchanged=subprocess.run(['git','diff','--quiet',baseline,'--','ec-flrw','research/ec-spherical','research/ec-matter-models','research/ec-two-matter-models'],cwd=ROOT).returncode==0
    success=success and pdf.returncode==0 and unchanged
    (STAGE/'validation-results.json').write_text(json.dumps({'task_date':'2026-11-13','python':platform.python_version(),'baseline':baseline,'success':success,'previous_research_and_runtime_unchanged':unchanged,'flrw_hashes':checks,'pdf_build_exit_code':pdf.returncode,'runs':runs,'scope':'Reduced homogeneous LRS classical ECD only; no general 3+1 PDE or exterior matching.'},indent=2)+'\n')
print('PASS' if success else 'FAIL')
sys.exit(0 if success else 1)
