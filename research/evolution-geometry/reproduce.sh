#!/usr/bin/env bash
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
results="${1:-$here/results}"
scratch="$(mktemp -d)"
trap 'rm -rf "$scratch"' EXIT
export OPENBLAS_NUM_THREADS=1
export MPLCONFIGDIR="$scratch/matplotlib"
export XDG_CACHE_HOME="$scratch/cache"
mkdir -p "$results"
for geometry in -1 0 1; do
    node "$here/experiments/snapshot.cjs" "$results" "$geometry"
done
for substrate in cliques torus regular; do
    node "$here/experiments/contrasts.cjs" "$results" "$substrate"
done
for variant in base --focused --replicate; do
    options=()
    if [[ "$variant" != base ]]; then options+=("$variant"); fi
    python3 "$here/experiments/architecture.py" "$results" "${options[@]}"
done
python3 "$here/experiments/geometry.py" "$results"
python3 "$here/experiments/clocks.py" "$results"
python3 "$here/experiments/summary.py" "$results"
gzip -9nf "$results"/snapshots_*.json "$results"/architectures*.json "$results"/architecture_time.csv
