#!/usr/bin/env bash
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
results="${1:-$here/results}"
html="${2:-$here/lab.html}"
scratch="$(mktemp -d)"
trap 'rm -rf "$scratch"' EXIT
export OPENBLAS_NUM_THREADS=1
export MPLCONFIGDIR="$scratch/matplotlib"
export XDG_CACHE_HOME="$scratch/cache"
python3 "$here/experiments.py" "$results"
python3 "$here/free_modes.py" "$results"
python3 "$here/build.py" "$results" "$html"
