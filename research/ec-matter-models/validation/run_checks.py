"""Record limited matter checks and read-only regressions; no time evolution code."""
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
BASELINE="e5e8aa651dcafb72b18e5f95ad3c0de03b1863da"


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
    directories=[ROOT/"research/ec-spherical/validation",
                 ROOT/"research/ec-spherical/full-weyssenhoff/validation",
                 STAGE/"validation"]
    suite=unittest.TestSuite([unittest.TestLoader().discover(str(d)) for d in directories])
    result=unittest.TextTestRunner(verbosity=2,resultclass=RecordedResult).run(suite)
    application=subprocess.run(["npm","test"],cwd=ROOT,capture_output=True,text=True)
    count=re.search(r"(?:#|ℹ)\s+tests (\d+)",application.stdout)
    if application.returncode:
        print(application.stdout,file=sys.stderr)
        print(application.stderr,file=sys.stderr)
    preserved=subprocess.run(["git","diff","--quiet",BASELINE,"--",
                              "research/ec-spherical","ec-flrw"],cwd=ROOT).returncode==0
    manifest=[]
    for line in (ROOT/"research/ec-spherical/baseline-flrw.sha256").read_text().splitlines():
        expected,path=line.split(maxsplit=1)
        actual=hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
        manifest.append({"path":path,"unchanged":actual==expected})
    M=2.435e18
    GA=3/(16*M*M)
    hbarc=.1973269804
    n0=.16*hbarc**3
    m=.939
    nNR=m/(1.5*GA)
    import math
    success=(result.wasSuccessful() and application.returncode==0 and count is not None
             and preserved and all(item["unchanged"] for item in manifest))
    record={
        "task_date":"2026-11-13",
        "baseline_commit":BASELINE,
        "python":platform.python_version(),
        "sympy":sympy.__version__,
        "node":subprocess.check_output(["node","--version"],text=True).strip(),
        "mathematical_tests_run":result.testsRun,
        "mathematical_tests":result.records,
        "application_tests_run":int(count.group(1)) if count else None,
        "application_tests_exit_code":application.returncode,
        "previous_research_and_runtime_unchanged":preserved,
        "flrw_file_hashes":manifest,
        "scale_inputs":{"reduced_Planck_GeV":M,"hbar_c_GeV_fm":hbarc,
                        "reference_density_fm^-3":.16,"reference_mass_GeV":m},
        "scale_estimates":{
            "G_A_GeV^-2":GA,"reference_density_GeV^3":n0,
            "illustrative_NR_ratio":1.5*GA*n0/m,
            "invalid_NR_threshold_density_GeV^3":nNR,
            "invalid_NR_threshold_pF_GeV":(3*math.pi**2*nNR)**(1/3),
            "UR_ratio_at_1GeV_g2_C1":1/(12*math.pi**2*M*M),
            "uncontrolled_UR_equality_pF_GeV_g2_C1":M*math.sqrt(12*math.pi**2)},
        "success":success,
        "elapsed_seconds":round(time.monotonic()-start,3),
        "limitations":[
            "No ADM calculation, numerical collapse/evolution solver or plots.",
            "The free-sea state check is a nonrelativistic first-order normal-state approximation.",
            "No realistic nuclear/QCD axial correlator or EC dense-matter EOS is calculated.",
            "No coupled dense quantum EC stability or bounce theorem is established.",
            "The Planckian equality estimate lies outside controlled low-energy EFT validity."]}
    target=STAGE/"validation-results.json"
    target.write_text(json.dumps(record,indent=2)+"\n")
    print(f"Wrote {target}; application tests: {record['application_tests_run']}",file=sys.stderr)
    return 0 if success else 1


if __name__=="__main__":
    sys.exit(run())
