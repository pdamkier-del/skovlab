#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
build_dir=$(mktemp -d /tmp/ec-full-weyssenhoff-tex.XXXXXX)
trap 'rm -rf "$build_dir"' EXIT
for pass in 1 2 3; do
  if ! pdflatex -interaction=nonstopmode -halt-on-error -output-directory="$build_dir" derivation.tex > "$build_dir/compiler.txt"; then
    cat "$build_dir/compiler.txt"
    exit 1
  fi
done
if rg -n 'undefined references|undefined on input|Overfull' "$build_dir/derivation.log"; then
  exit 1
fi
cp "$build_dir/derivation.pdf" derivation.pdf
