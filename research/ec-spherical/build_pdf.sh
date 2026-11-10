#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
build_dir=$(mktemp -d /tmp/ec-spherical-tex.XXXXXX)
trap 'rm -rf "$build_dir"' EXIT
for pass in 1 2 3; do
  pdflatex -interaction=nonstopmode -halt-on-error -output-directory="$build_dir" derivation.tex > "$build_dir/compiler.txt"
done
if rg -n 'undefined references|undefined on input|Overfull' "$build_dir/derivation.log"; then
  cat "$build_dir/compiler.txt"
  exit 1
fi
cp "$build_dir/derivation.pdf" derivation.pdf
