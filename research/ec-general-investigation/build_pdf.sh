#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
for pass in 1 2; do pdflatex -interaction=nonstopmode -halt-on-error rapport.tex > /tmp/ec-general-latex.log; done
if rg 'Undefined control sequence|undefined references|Overfull' rapport.log; then exit 1; fi
