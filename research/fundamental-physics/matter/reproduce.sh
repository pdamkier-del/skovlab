#!/usr/bin/env bash
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
output="${1:-$here/results}"
export OPENBLAS_NUM_THREADS=1
mkdir -p "$output"
for code in dispersion dressing waves drive spectral mediated radial_q; do
    python3 "$here/$code.py" "$output"
done
