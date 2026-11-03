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
for diagram_language in en nl; do
  for diagram_name in overview sharing-flow community data-model correlation exchange timeline quality-cycle; do
    pdflatex -interaction=nonstopmode -halt-on-error -file-line-error \
      -jobname="${diagram_name}-${diagram_language}" -output-directory="$diagram_out" \
      "\def\IntroLanguage{${diagram_language}}\def\SharingDiagramName{${diagram_name}}\input{diagrams/standalone.tex}"
  done
done
