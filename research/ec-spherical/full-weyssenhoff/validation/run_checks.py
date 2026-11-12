"""Record both research suites, existing application tests and unchanged FLRW files."""
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

STAGE = Path(__file__).resolve().parents[1]
AUDIT = STAGE.parent
ROOT = AUDIT.parents[1]


class RecordedResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.records = []

    def addSuccess(self, test):
        super().addSuccess(test)
        self.records.append({"test": test.id(), "status": "passed"})

    def addFailure(self, test, error):
        super().addFailure(test, error)
        self.records.append({"test": test.id(), "status": "failed"})

    def addError(self, test, error):
        super().addError(test, error)
        self.records.append({"test": test.id(), "status": "error"})


def run():
    start = time.monotonic()
    suites = []
    for directory in [AUDIT / "validation", STAGE / "validation"]:
        suites.append(unittest.TestLoader().discover(str(directory)))
    result = unittest.TextTestRunner(verbosity=2, resultclass=RecordedResult).run(
        unittest.TestSuite(suites))
    manifest = []
    for line in (AUDIT / "baseline-flrw.sha256").read_text().splitlines():
        expected, path = line.split(maxsplit=1)
        actual = hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
        manifest.append({"path": path, "unchanged": expected == actual})
    application = subprocess.run(["npm", "test"], cwd=ROOT, capture_output=True, text=True)
    # Keep failures reviewable; successful routine output is summarized in the JSON.
    if application.returncode:
        print(application.stdout, file=sys.stderr)
        print(application.stderr, file=sys.stderr)
    count = re.search(r"(?:#|ℹ)\s+tests (\d+)", application.stdout)
    success = (result.wasSuccessful() and application.returncode == 0
               and count is not None and all(item["unchanged"] for item in manifest))
    report = {
        "stage": 2,
        "task_date": "2026-11-12",
        "models_compared": ["GSM + local averaged Weyssenhoff", "GSM + full ideal radial Weyssenhoff"],
        "previous_audit_commit": "3efc96159537e834313ded3ba359624abaa8b26f",
        "python": platform.python_version(),
        "sympy": sympy.__version__,
        "node": subprocess.check_output(["node", "--version"], text=True).strip(),
        "research_tests_run": result.testsRun,
        "research_tests": result.records,
        "application_tests_run": int(count.group(1)) if count else None,
        "application_tests_exit_code": application.returncode,
        "existing_flrw_files": manifest,
        "success": success,
        "elapsed_seconds": round(time.monotonic()-start, 3),
        "limitations": [
            "No spherical PDE time evolution or full coupled well-posedness proof.",
            "Full microscopic action and dense-matter EOS not independently established.",
            "Generic retained correlations and spinful surface layers remain unclosed.",
            "The full-Riemann interface test assumes Darmois metric matching and bounded contortion.",
            "No regular finite exterior construction or global bounce outcome computed.",
        ],
    }
    target = STAGE / "validation-results.json"
    target.write_text(json.dumps(report, indent=2)+"\n")
    print(f"Wrote {target}; application tests: {report['application_tests_run']}", file=sys.stderr)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(run())
