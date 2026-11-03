#!/usr/bin/env bash
set -euo pipefail
if [[ $# -ne 1 ]]; then
  echo 'Usage: bash diagrams/build.sh OUTPUT_DIRECTORY' >&2
  exit 2
fi
course_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
mkdir -p -- "$1"
diagram_out="$(cd -- "$1" && pwd)"
cd -- "$course_dir"
for diagram_name in responsibilities change-cycle; do
  pdflatex -interaction=nonstopmode -halt-on-error -file-line-error \
    -jobname="$diagram_name" -output-directory="$diagram_out" \
    "\def\AdminDiagramName{${diagram_name}}\input{diagrams/standalone.tex}"
done
