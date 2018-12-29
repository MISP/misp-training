#!/bin/bash
#

slidedecks=("0-misp-introduction-to-information-sharing" "1-misp-usage" "1.2-misp-integration" "1.1-misp-viper-integration" "1.2.1-misp-integration-mail2misp" "2-misp-administration" "3-misp-taxonomy-tagging" "3.1-misp-modules" "3.2-misp-galaxy" "3.3-misp-object-template" "6.0-misp-dashboard" "a.0-contributing" "a.1-devintro" "a.2-pymisp" "a.3-misp-feed" "a.4-best-practices")
mkdir output
export TEXINPUTS=::`pwd`/themes/
echo ${TEXINPUTS}
for slide in ${slidedecks[@]}; do
        cd ${slide}
        pdflatex slide.tex
        pdflatex slide.tex
        rm *.aux *.toc *.snm *.log *.out *.nav *.vrb
        cp slide.pdf ../output/${slide}.pdf
        rm slide.pdf
        cd ..
done

echo "Generating ack page..."
cd complementary/ack
pdflatex ack.tex
rm *.aux *.log *.out
cp ack.pdf ../../output
rm ack.pdf
cd ../..

echo "Generating cheatsheet..."
cd training-support/compact-cheatsheet/
pdflatex cheatsheet.tex
rm *.aux *.toc *.snm *.log *.out *.nav *.vrb
cp cheatsheet.pdf ../../output
rm cheatsheet.pdf
cd ../..

echo "Generating checklist..."
cd training-support/checklist
pdflatex usage.tex
rm *.aux *.toc *.snm *.log *.out *.nav *.vrb
cp usage.pdf ../../output
rm usage.pdf
cd ../..

echo "Generating handout..."
cd output
for pdf in ${slidedecks[@]}; do
        listofpdf+="${pdf}.pdf "
done
echo ${listofpdf}

pdfunite ${listofpdf} cheatsheet.pdf usage.pdf ack.pdf ../misp-training.pdf
cd ..

exiftool -overwrite_original_in_place -Title="MISP Training and Slide Decks" -Author="CIRCL Computer Incident Response Center Luxembourg" -Subject="MISP Threat Intelligence Platform Training Materials" -Keywords="MISP Threat Intelligence CTI STIX information sharing yara sigma suricata snort bro openioc threat-actor TIP threat intelligence platform circl.lu training cybersecurity MISPProject" misp-training.pdf

