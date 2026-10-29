export TEXINPUTS="$(cd -- "$(dirname -- "$0")/../themes" && pwd):${TEXINPUTS:-}:"
echo ${TEXINPUTS}
pdflatex slide.tex
pdflatex slide.tex
pdflatex slide.tex
