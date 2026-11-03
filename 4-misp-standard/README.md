# MISP Standard training

A 20-minute introduction to the MISP formats, shared vocabularies and their
publication status. The deck has **14 pages**: a title and 13 content slides,
with presenter notes for every content slide. It retains the shared MISP theme
and the existing 4:3 aspect ratio.

[Published training PDF](https://www.misp-project.org/misp-training/4-misp-standard.pdf) ·
[Repository PDF](../output/4-misp-standard.pdf) ·
[Slide source](content.tex) · [Training home](../README.md)

## Review scope and findings

Reviewed on **3 November 2026** against the
[published standards catalog](https://www.misp-standard.org/standards/), the
individual published documents, IETF Datatracker and the official
[MISP/misp-rfc source snapshot](https://github.com/MISP/misp-rfc/tree/9ee0b9ce5313dabc82724980064016d44f756030).
The source snapshot is commit `9ee0b9ce5313dabc82724980064016d44f756030`.

The earlier deck covered core, object templates, galaxies and SightingDB, but
omitted taxonomy and Threat Actor Naming from the current published catalog.
It also lacked revision evidence and implied a single linear publication
process. The refreshed lesson covers all six catalog entries, explains analyst
data and EventReport in core draft-20, and distinguishes core sightings from
the SightingDB connector format. It adds an integration checklist and separates
supporting repository formats from the published catalog.

The source repository's README still advertises some older draft numbers.
The table below uses the documents themselves and Datatracker instead.
Numbers identify document revisions, not MISP software releases or versions
of the public object, taxonomy and galaxy libraries.

| Specification | MISP-hosted document at review | Latest submitted IETF revision at review |
| --- | --- | --- |
| [Core](https://www.misp-standard.org/rfc/misp-standard-core.html) | draft-20; 26 November 2025 | [-20](https://datatracker.ietf.org/doc/draft-dulaunoy-misp-core-format/); expired |
| [Object template](https://www.misp-standard.org/rfc/misp-standard-object-template-format.html) | draft-06; 24 December 2023 | [-06](https://datatracker.ietf.org/doc/draft-dulaunoy-misp-object-template-format/); expired |
| [Taxonomy](https://www.misp-standard.org/rfc/misp-standard-taxonomy-format.html) | draft-11; 6 January 2026 | [-12](https://datatracker.ietf.org/doc/draft-dulaunoy-misp-taxonomy-format/); expired |
| [Galaxy](https://www.misp-standard.org/rfc/misp-standard-galaxy-format.html) | draft-08; 24 December 2023 | [-08](https://datatracker.ietf.org/doc/draft-dulaunoy-misp-galaxy-format/); expired |
| [Threat Actor Naming](https://www.misp-standard.org/rfc/threat-actor-naming.html) | draft-00; 6 August 2026 | No submission status asserted here; the lesson cites the MISP-hosted guidance |
| [SightingDB](https://www.misp-standard.org/rfc/sightingdb-format.txt) | text dated 13 April 2020 | No numbered submitted revision asserted here; the lesson cites the catalog's document |

**Taxonomy discrepancy:** the MISP website and source metadata identify
`draft-11`, while the latest submitted document is
[draft-dulaunoy-misp-taxonomy-format-12](https://www.ietf.org/archive/id/draft-dulaunoy-misp-taxonomy-format-12.txt).
The taxonomy slide cites that submitted -12 text, including section 2.4 on
UUIDs for the taxonomy, predicates and values. The revision table preserves
both labels rather than silently treating them as equal.

The four linked IETF records were expired at review. Internet-Drafts are work
in progress; their submission does not establish IETF endorsement or RFC
status. Expiration is a publication-process fact, not evidence that deployed
MISP software has stopped using a format. Recheck the links before teaching
or citing a latest revision. The Naming source metadata has a January date;
the published site's August date is reported as publication evidence rather
than inferred from that source field.

Additional source documents reviewed, outside the six-entry published catalog:

- [Warninglist format](https://github.com/MISP/misp-rfc/blob/9ee0b9ce5313dabc82724980064016d44f756030/misp-warninglist-format/raw.md)
- [Noticelist format](https://github.com/MISP/misp-rfc/blob/9ee0b9ce5313dabc82724980064016d44f756030/misp-noticelist-format/raw.md)
- [Query format](https://github.com/MISP/misp-rfc/blob/9ee0b9ce5313dabc82724980064016d44f756030/misp-query-format/raw.md)

These are repository specifications with differing maturity and publication
histories. The query-format document is not a substitute for the deployed
MISP API reference. This lesson does not claim a new conformance profile or
complete coverage of every MISP feature or endpoint.

## Editable TikZ diagrams

The slides input the `.tikz` sources directly. Geometry and labels remain
editable text; no screenshots or flattened diagram images are needed to build.

| Diagram | Source | Standalone vector export |
| --- | --- | --- |
| Published standards family | [standards-family.tikz](diagrams/standards-family.tikz) | [PDF](diagrams/standards-family.pdf) |
| Simplified core model | [core-model.tikz](diagrams/core-model.tikz) | [PDF](diagrams/core-model.pdf) |

[styles.tex](diagrams/styles.tex) defines shared node and arrow styles using the
MISP palette. [export.tex](diagrams/export.tex) provides a standalone wrapper.
The family diagram shows roles, not a mandatory processing pipeline. The model
diagram uses solid arrows for containment and dashed arrows for example links.
It omits some structures and links to stay readable; it is not a JSON schema.

## Build and validate

Use the [shared theme setup](../themes/README.md): a recent TeX Live with Beamer,
TikZ, Fira Sans/Fira Mono, listings and booktabs. Diagram exports also need
`standalone`. No shell escape, network access or running MISP instance is
needed to compile.

Run from the repository root:

```sh
export TEXINPUTS="$PWD/themes:${TEXINPUTS:-}:"
mkdir -p /tmp/misp-standard
cd 4-misp-standard
for pass in 1 2 3; do
  pdflatex -interaction=nonstopmode -halt-on-error -file-line-error \
    -output-directory=/tmp/misp-standard slide.tex || exit 1
done
```

Export each diagram from the same directory:

```sh
for diagram in standards-family core-model; do
  pdflatex -interaction=nonstopmode -halt-on-error -file-line-error \
    -output-directory=/tmp/misp-standard -jobname="$diagram" \
    "\def\diagram{$diagram}\input{diagrams/export.tex}" || exit 1
done
```

Create a presenter-notes handout using the same insertion as the root build:

```sh
awk '/\\begin\{document\}/ {
  print "\\usepackage{pgfpages}"
  print "\\setbeameroption{show notes on second screen=right}"
} {print}' slide.tex > /tmp/misp-standard/slide_handout.tex
for pass in 1 2 3; do
  pdflatex -interaction=nonstopmode -halt-on-error -file-line-error \
    -output-directory=/tmp/misp-standard \
    /tmp/misp-standard/slide_handout.tex || exit 1
done
```

Review the PDF and extracted text, check the final logs for overflow and missing
references, and confirm the handout retains all 13 notes. The main deck and
standalone diagram PDFs are committed for convenient review. Temporary build
files and the handout need not be committed. Reuse under the repository's
[existing license and attribution terms](../README.md#license-attribution-and-funding).
