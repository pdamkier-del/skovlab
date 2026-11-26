#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export PYTHONPATH=.
export OPENBLAS_NUM_THREADS=1
python reduction/run.py
python reduction/local.py
python reduction/inhomogeneous.py
python reduction/build_lab.py
