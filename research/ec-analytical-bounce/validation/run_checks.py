"""Check analytical claims and existing regressions; never modify old reports."""
import hashlib,json,platform,re,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];STAGE=ROOT/'research/ec-analytical-bounce'
commands=[['python','-m','unittest','discover','-s','research/ec-analytical-bounce/tests','-v'],['python','research/ec-full-3plus1/validation/run_checks.py']]
records=[]
for command in commands:
    r=subprocess.run(command,cwd=ROOT,capture_output=True,text=True);output=r.stdout+r.stderr;print(output,flush=True)
    count=sum(int(v) for v in re.findall(r'(?:Ran |(?:ℹ|#) tests )(\d+)',output))
    records.append({'command':command,'exit_code':r.returncode,'tests_counted':count,'output':output})
success=all(x['exit_code']==0 for x in records)
if '--record' in sys.argv:
    baseline='84a9756';old=['ec-flrw','research/ec-spherical','research/ec-matter-models','research/ec-two-matter-models','research/ec-dirac-collapse','research/ec-full-3plus1']
    preserved=subprocess.run(['git','diff','--quiet',baseline,'--',*old],cwd=ROOT).returncode==0
    pdf=subprocess.run(['bash','research/ec-analytical-bounce/build_pdf.sh'],cwd=ROOT,capture_output=True,text=True)
    success=success and preserved and pdf.returncode==0
    report={'date':'2026-11-13','python':platform.python_version(),'baseline':baseline,'success':success,'existing_research_and_simulators_unchanged':preserved,'pdf_build_exit_code':pdf.returncode,'runs':records,'scope':['No numerical time evolution or initial-condition parameter search in the new analysis.','Exact local analytic constrained family and local Cauchy-continuation argument.','The witness violates longitudinal NEC and has no established positive-frequency quantum-matter interpretation.','The local bounce also occurs in the torsion-free comparison; not a demonstrated torsion-induced cloud or black-hole bounce.']}
    (STAGE/'validation-results.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS' if success else 'FAIL');sys.exit(0 if success else 1)
