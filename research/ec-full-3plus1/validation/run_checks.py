"""Record actual local checks without rewriting older research artifacts."""
from pathlib import Path
import hashlib,json,platform,re,subprocess,sys
ROOT=Path(__file__).resolve().parents[3];STAGE=ROOT/'research/ec-full-3plus1'
commands=[['python','-m','unittest','discover','-s','research/ec-full-3plus1/tests','-v'],
 ['python','-m','unittest','discover','-s','research/ec-spherical/validation','-v'],
 ['python','-m','unittest','discover','-s','research/ec-spherical/full-weyssenhoff/validation','-v'],
 ['python','-m','unittest','discover','-s','research/ec-matter-models/validation','-v'],
 ['python','-m','unittest','discover','-s','research/ec-two-matter-models/validation','-v'],
 ['python','research/ec-dirac-collapse/validation/test_symbolic.py'],
 ['node','--test','research/ec-dirac-collapse/validation/model.test.mjs'],['npm','test'],
 ['node','research/ec-full-3plus1/tests/browser.test.cjs']]
runs=[]
for cmd in commands:
    r=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True);output=r.stdout+r.stderr;print(output,flush=True)
    count=re.search(r'(?:Ran |(?:ℹ|#) tests )(\d+)',output)
    runs.append({'command':cmd,'exit_code':r.returncode,'tests':int(count.group(1)) if count else None,'output':output})
success=all(r['exit_code']==0 for r in runs)
if '--record' in sys.argv:
    baseline='fabd0ee';old=['ec-flrw','research/ec-spherical','research/ec-matter-models','research/ec-two-matter-models','research/ec-dirac-collapse']
    preserved=subprocess.run(['git','diff','--quiet',baseline,'--',*old],cwd=ROOT).returncode==0
    manifest=[]
    for row in (ROOT/'research/ec-spherical/baseline-flrw.sha256').read_text().splitlines():
        expected,path=row.split(maxsplit=1);manifest.append({'path':path,'unchanged':hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==expected})
    sample=json.loads((STAGE/'sample.json').read_text());refinement=json.loads((STAGE/'coupled-convergence-results.json').read_text())
    success=success and preserved and all(x['unchanged'] for x in manifest) and refinement['success']
    (STAGE/'validation-results.json').write_text(json.dumps({'date':'2026-11-13','python':platform.python_version(),'baseline':baseline,'success':success,'previous_modules_unchanged':preserved,'flrw_file_hashes':manifest,'runs':runs,'saved_example_status':sample['status'],'saved_example_final_diagnostics':{k:v for k,v in sample['rows'][-1].items() if not k.endswith('_xy')},'coupled_convergence_report':'coupled-convergence-results.json','scope':'Full local 3+1 ECD equations; validated only for the documented weak-field tests. No strong-collapse/bounce/exterior claim.'},indent=2)+'\n')
print('PASS' if success else 'FAIL');sys.exit(0 if success else 1)
