#!/usr/bin/env bash
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
results="${1:-$here/results}"
scratch="$(mktemp -d)"
trap 'rm -rf "$scratch"' EXIT
export MPLCONFIGDIR="$scratch/matplotlib"
export XDG_CACHE_HOME="$scratch/cache"
mkdir -p "$results"
node "$here/run.cjs" "$results"
node "$here/superposition.cjs" "$results"
node "$here/controls.cjs" "$results"
g++ -O3 -std=c++17 "$here/kmp.cpp" -o "$scratch/kmp"
"$scratch/kmp" "$results"
python3 "$here/analyse.py" "$results"
python3 "$here/metric.py" "$results"
