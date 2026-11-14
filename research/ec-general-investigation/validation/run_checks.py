"""New general/efold checks plus existing regression suite, without old-file writes."""
from pathlib import Path
import json,platform,re,subprocess,sys
ROOT=Path(__file__).resolve().parents[3];STAGE=ROOT/'research/ec-general-investigation'
commands=[['python','-m','unittest','discover','-s','research/ec-general-investigation/tests','-v'],['python','research/ec-analytical-bounce/validation/run_checks.py']]
records=[]
for cmd in commands:
    r=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True);out=r.stdout+r.stderr;print(out,flush=True)
    records.append({'command':cmd,'exit_code':r.returncode,'tests_counted':sum(int(x) for x in re.findall(r'(?:Ran |(?:ℹ|#) tests )(\d+)',out)),'output':out})
success=all(x['exit_code']==0 for x in records)
if '--record' in sys.argv:
    baseline='183bd20';old=['ec-flrw','research/ec-spherical','research/ec-matter-models','research/ec-two-matter-models','research/ec-dirac-collapse','research/ec-full-3plus1','research/ec-analytical-bounce']
    preserved=subprocess.run(['git','diff','--quiet',baseline,'--',*old],cwd=ROOT).returncode==0
    pdf=subprocess.run(['bash','research/ec-general-investigation/build_pdf.sh'],cwd=ROOT,capture_output=True,text=True)
    success=success and preserved and pdf.returncode==0
    samples=json.loads((STAGE/'tracking-refinement.json').read_text())
    record={'date':'2026-11-14','python':platform.python_version(),'baseline':baseline,'success':success,'existing_modules_unchanged':preserved,'pdf_exit_code':pdf.returncode,'runs':records,'tracking_resolution_report':'tracking-refinement.json','tracked_grids':[x['n'] for x in samples['records']],'scope':['Exact covariant e-fold/current relations and single-spinor conditional invariant blow-up bound.','Passive infinitesimal-volume tracking on the unchanged weak-field prototype.','Numerical current reconstruction defects and non-asymptotic tracer grid differences remain visible.','Exact six-field chiral cosmological bounce and accelerating e-fold count verified; no general finite-cloud bounce, complete exterior or physical quantum state established.']}
    (STAGE/'validation-results.json').write_text(json.dumps(record,indent=2)+'\n')
print('PASS' if success else 'FAIL');sys.exit(0 if success else 1)
