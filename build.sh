export TEXINPUTS=::`pwd`/themes/
echo ${TEXINPUTS}
cd 0-misp-introduction-to-information-sharing
pdflatex infosharing-introduction.tex
