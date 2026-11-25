#!/usr/bin/env bash
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
results="${1:-$here/results}"
html="${2:-$here/lab.html}"
export OPENBLAS_NUM_THREADS=1
mkdir -p "$results"
node "$here/forest.cjs" "$results"
node "$here/validate_shared.cjs" "$results"
node "$here/peter_height.cjs" "$results"
node "$here/sweep_flux.cjs" "$results"
python3 "$here/arrow.py" "$results"
python3 "$here/replication.py" "$results"
python3 "$here/interaction.py" "$results"
python3 "$here/metric_feedback.py" "$results"
python3 "$here/reversible.py" "$results"
python3 "$here/build_lab.py" "$results" "$html"
for series in shared_original peter_original peter_bounded peter_no_diffusion peter_no_combat shared_validation_10 shared_validation_20; do
  gzip -9nf "$results/$series.csv"
done
