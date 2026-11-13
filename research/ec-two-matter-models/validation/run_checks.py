"""Record limited two-model checks and preserved earlier research; no solver."""
import hashlib
import json
from pathlib import Path
import platform
import re
import subprocess
import sys
import time
import unittest

import sympy

STAGE=Path(__file__).resolve().parents[1]
ROOT=STAGE.parents[1]
BASELINE="7e1fc4ad3e608cd488dde0b17eed2e7c32641686"


class RecordedResult(unittest.TextTestResult):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.records=[]

    def addSuccess(self,test):
        super().addSuccess(test)
        self.records.append({"test":test.id(),"status":"passed"})

    def addFailure(self,test,error):
        super().addFailure(test,error)
        self.records.append({"test":test.id(),"status":"failed"})

    def addError(self,test,error):
        super().addError(test,error)
        self.records.append({"test":test.id(),"status":"error"})


def run():
    start=time.monotonic()
    dirs=[ROOT/"research/ec-spherical/validation",
          ROOT/"research/ec-spherical/full-weyssenhoff/validation",
          ROOT/"research/ec-matter-models/validation",STAGE/"validation"]
    suite=unittest.TestSuite([unittest.TestLoader().discover(str(d)) for d in dirs])
    result=unittest.TextTestRunner(verbosity=2,resultclass=RecordedResult).run(suite)
    app=subprocess.run(["npm","test"],cwd=ROOT,capture_output=True,text=True)
    count=re.search(r"(?:#|ℹ)\s+tests (\d+)",app.stdout)
    if app.returncode:
        print(app.stdout,file=sys.stderr)
        print(app.stderr,file=sys.stderr)
    preserved=subprocess.run(["git","diff","--quiet",BASELINE,"--",
        "research/ec-spherical","research/ec-matter-models","ec-flrw"],cwd=ROOT).returncode==0
    manifest=[]
    for row in (ROOT/"research/ec-spherical/baseline-flrw.sha256").read_text().splitlines():
        expected,path=row.split(maxsplit=1)
        actual=hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
        manifest.append({"path":path,"unchanged":actual==expected})
    success=(result.wasSuccessful() and app.returncode==0 and count is not None
             and preserved and all(item["unchanged"] for item in manifest))
    record={
        "task_date":"2026-11-13","baseline_commit":BASELINE,
        "python":platform.python_version(),"sympy":sympy.__version__,
        "node":subprocess.check_output(["node","--version"],text=True).strip(),
        "new_checks_run":sum(x["test"].startswith("test_two_matter.") for x in result.records),
        "mathematical_tests_run":result.testsRun,"mathematical_tests":result.records,
        "application_tests_run":int(count.group(1)) if count else None,
        "application_tests_exit_code":app.returncode,
        "previous_research_and_runtime_unchanged":preserved,
        "flrw_file_hashes":manifest,"success":success,
        "elapsed_seconds":round(time.monotonic()-start,3),
        "limitations":[
            "No time evolution, unrestricted ADM expansion or global exterior construction.",
            "The on-shell stress check uses a fixed-background classical matter solution.",
            "No complete dense curved-EC quantum kinetic/collision closure is derived.",
            "Classical compact support does not prove compact renormalized quantum stress.",
            "The full-curvature jump test assumes a smooth metric junction and bounded contortion.",
            "No causal regular bounce is established."]}
    target=STAGE/"validation-results.json"
    target.write_text(json.dumps(record,indent=2)+"\n")
    print(f"Wrote {target}; application tests: {record['application_tests_run']}",file=sys.stderr)
    return 0 if success else 1


if __name__=="__main__":
    sys.exit(run())
