#!/bin/bash
#

slidedecks=("0-misp-introduction-to-information-sharing")
mkdir output
export TEXINPUTS=::`pwd`/themes/
echo ${TEXINPUTS}
for slide in ${slidedecks[@]}; do
        cd ${slide}
        pdflatex slide.tex
        pdflatex slide.tex
        rm *.aux *.toc *.snm *.log *.out *.nav
        cp slide.pdf ../output/${slide}.pdf
done
