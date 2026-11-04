# Build this course with the shared theme; keep generated files out of source.
LATEX ?= pdflatex
PYTHON ?= python3
BUILD_DIR ?= /tmp/misp-integration
DECK_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
ROOT_DIR := $(abspath $(DECK_DIR)/..)
DIAGRAMS := integration-map data-contract module-roundtrip workflow-guard delivery-loop snapshot-plan

.PHONY: all pdf slides notes diagrams check-lab
all: slides
pdf: slides

slides:
	mkdir -p "$(BUILD_DIR)/slides"
	cd "$(DECK_DIR)" && export TEXINPUTS="$(ROOT_DIR)/themes:$(TEXINPUTS):"; \
	for pass in 1 2 3; do \
	  $(LATEX) -interaction=nonstopmode -halt-on-error -file-line-error \
	    -output-directory="$(BUILD_DIR)/slides" slide.tex || exit 1; \
	done

notes:
	mkdir -p "$(BUILD_DIR)/notes"
	cd "$(DECK_DIR)" && \
	awk '/\\begin\{document\}/ {print "\\usepackage{pgfpages}"; print "\\setbeameroption{show notes on second screen=right}"} {print}' \
	  slide.tex > "$(BUILD_DIR)/notes/slide_handout.tex"
	cd "$(DECK_DIR)" && export TEXINPUTS="$(ROOT_DIR)/themes:$(TEXINPUTS):"; \
	for pass in 1 2 3; do \
	  $(LATEX) -interaction=nonstopmode -halt-on-error -file-line-error \
	    -output-directory="$(BUILD_DIR)/notes" \
	    "$(BUILD_DIR)/notes/slide_handout.tex" || exit 1; \
	done

diagrams:
	mkdir -p "$(BUILD_DIR)/diagrams"
	cd "$(DECK_DIR)" && export TEXINPUTS="$(ROOT_DIR)/themes:$(TEXINPUTS):"; \
	for diagram in $(DIAGRAMS); do \
	  $(LATEX) -interaction=nonstopmode -halt-on-error -file-line-error \
	    -output-directory="$(BUILD_DIR)/diagrams" -jobname="$$diagram" \
	    "\def\IntegrationDiagram{$$diagram}\input{diagrams/standalone.tex}" || exit 1; \
	done

check-lab:
	$(PYTHON) "$(DECK_DIR)/examples/check_lab.py" -v
	$(PYTHON) "$(DECK_DIR)/examples/plan_snapshot.py" \
	  "$(DECK_DIR)/examples/current-state.json" "$(DECK_DIR)/examples/desired-state.json"
