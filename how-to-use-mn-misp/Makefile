# Makefile for LaTeX Beamer presentation

# Main .tex file (without extension)
MAIN_FILE = presentation

# Flags for pdflatex and bibliography tools
LATEX_FLAGS = -interaction=nonstopmode -shell-escape -halt-on-error
BIBTEX = bibtex

.PHONY: all clean

# Default target: Build the PDF
all: $(MAIN_FILE).pdf

# Compile the PDF from .tex file, including styles directory
$(MAIN_FILE).pdf: $(MAIN_FILE).tex
	@echo "Compiling LaTeX..."
	TEXINPUTS=styles: pdflatex $(LATEX_FLAGS) $(MAIN_FILE).tex
	@if grep -q "Citation" $(MAIN_FILE).aux; then \
	  echo "Running BibTeX..."; \
	  TEXINPUTS=styles: $(BIBTEX) $(MAIN_FILE).aux; \
	  TEXINPUTS=styles: pdflatex $(LATEX_FLAGS) $(MAIN_FILE).tex; \
	  TEXINPUTS=styles: pdflatex $(LATEX_FLAGS) $(MAIN_FILE).tex; \
	fi

# Clean up auxiliary files
clean:
	@echo "Cleaning up..."
	rm -f *.aux *.log *.nav *.out *.snm *.toc *.bbl *.blg *.vrb
	rm -Rf _minted-presentation/

# Full clean including the PDF
cleanall: clean
	rm -f $(MAIN_FILE).pdf

# Open the PDF file (Linux users can replace open with xdg-open or similar)
open: $(MAIN_FILE).pdf
	xdg-open $(MAIN_FILE).pdf

# Recompile slidedeck
recompile:
	@echo "Compiling LaTeX..."
	TEXINPUTS=styles: pdflatex $(LATEX_FLAGS) $(MAIN_FILE).tex
	@if grep -q "Citation" $(MAIN_FILE).aux; then \
	  echo "Running BibTeX..."; \
	  TEXINPUTS=styles: $(BIBTEX) $(MAIN_FILE).aux; \
	  TEXINPUTS=styles: pdflatex $(LATEX_FLAGS) $(MAIN_FILE).tex; \
	  TEXINPUTS=styles: pdflatex $(LATEX_FLAGS) $(MAIN_FILE).tex; \
	fi
