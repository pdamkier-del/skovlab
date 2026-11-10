"""Run this from the repository root; records what was actually checked."""
import hashlib,json,platform,subprocess,sys,time,unittest
from pathlib import Path
import sympy

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
class RecordedResult(unittest.TextTestResult):
    def __init__(self,*args,**kwargs): super().__init__(*args,**kwargs);self.records=[]
    def addSuccess(self,test): super().addSuccess(test);self.records.append({'test':test.id(),'status':'passed'})
    def addFailure(self,test,error): super().addFailure(test,error);self.records.append({'test':test.id(),'status':'failed'})
    def addError(self,test,error): super().addError(test,error);self.records.append({'test':test.id(),'status':'error'})

def run():
    start=time.monotonic();suite=unittest.defaultTestLoader.discover(str(HERE),pattern='test_*.py')
    result=unittest.TextTestRunner(verbosity=2,resultclass=RecordedResult).run(suite)
    manifest=HERE.parent/'baseline-flrw.sha256';matches=True;files=0
    for row in manifest.read_text().splitlines():
        expected,path=row.split(maxsplit=1);files+=1
        actual=hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
        if actual!=expected: matches=False
    report={'audit_version':1,'baseline_commit':'6d9e7ff95b11160afa869d6cd9f6da73bb2dc8e4','python':platform.python_version(),'sympy':sympy.__version__,'node':subprocess.run(['node','--version'],capture_output=True,text=True,check=True).stdout.strip(),'tests_run':result.testsRun,'success':result.wasSuccessful(),'tests':result.records,'elapsed_seconds':round(time.monotonic()-start,3),'existing_flrw_files_checked':files,'existing_flrw_files_unchanged':matches,'limitations':['Not a spherical PDE simulation or proof of discrete stability.','Microscopic averaging and general retained-correlation closure are not validated.','Spinful junction conditions and a complete exterior construction are not implemented.']}
    target=HERE.parent/'validation-results.json';target.write_text(json.dumps(report,indent=2)+'\n')
    print('Wrote',target, file=sys.stderr)
    return 0 if result.wasSuccessful() and matches else 1
if __name__=='__main__':sys.exit(run())
