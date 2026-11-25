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
mkdir -p "$results"
python3 "$here/minimal.py" "$results"
python3 "$here/minimal.py" "$results" --interfaces
for script in conductance motifs markov summarize; do
  python3 "$here/$script.py" "$results"
done
python3 "$here/build_lab.py" "$results" "$html"
gzip -9nf "$results"/minimal.csv "$results"/minimal_networks.json
