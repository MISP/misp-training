# MISP best practices

A course for CSIRTs, ISAC coordinators and analysts who already know basic MISP
usage. It covers community governance, handling, useful encoding, consumer
selection and feedback. Allow about 45 minutes for discussion and 15 minutes
for the demonstration and exercise. Presenter notes contain caveats, prompts
and expected exercise outcomes.

## Review and scope

Reviewed against the references below on **3 November 2026**. This refresh keeps
the original course's community-building focus and CIRCL experience, while
making the operational recommendations concrete:

| Review finding | Change |
| --- | --- |
| Legacy TLP:WHITE on the cover; no explanation of handling versus access | Use TLP:CLEAR; explain TLP 2.0, AMBER+STRICT and the separate MISP controls. |
| Undated membership counts, participation percentages and growth timelines | Keep community examples; replace unsupported numerical claims with locally measured outcomes. |
| Topology and sub-community advice without verification of recipients | Add sharing-group ownership, finer-grained distribution, excluded-recipient checks and outbound-path review. |
| Drafts and publication could be mistaken for confidentiality controls | Explain unpublished visibility, configured publication effects and the limits of recalling copies. |
| Broad advice to retain data and filter protective tools | Add provenance, retention, `to_ids`, warninglists, freshness and separate investigation/detection/blocking decisions. |
| Feedback described without a complete correction process | Add proposals, sightings, extended events, analyst data and downstream reconciliation. |
| Historical legal references and informal claims of anonymity | Link maintained compliance resources; distinguish technical controls from legal assessment and pseudonymisation from anonymity. |
| Long text lists and decorative images | Use four editable TikZ diagrams, shorter slides and a guided lab. |

The existing image files remain available for reuse. The updated deck does not
depend on the historical screenshots. Its 4:3 aspect ratio, shared MISP theme,
`slide.tex` entry point and included `content.tex` remain compatible with the
repository publication workflow. There are no external lookups or shell-escape
requirements at compile time.

## Build the slides and notes

Use the dependencies in the [theme guide](../themes/README.md). From the
repository root:

```sh
export TEXINPUTS="$PWD/themes:${TEXINPUTS:-}:"
mkdir -p /tmp/misp-best-practices/slides /tmp/misp-best-practices/notes
cd a.4-best-practices
for pass in 1 2 3; do
  pdflatex -interaction=nonstopmode -halt-on-error -file-line-error \
    -output-directory=/tmp/misp-best-practices/slides slide.tex || exit 1
done
```

For a notes handout, use the same insertion as the root `build.sh`. Generate a
temporary entry point outside the checkout, then compile from this directory
so relative content and diagram inputs resolve:

```sh
awk '/\\begin\{document\}/ {print "\\usepackage{pgfpages}"; print "\\setbeameroption{show notes on second screen=right}"} {print}' \
  slide.tex > /tmp/misp-best-practices/notes/slide_handout.tex
for pass in 1 2 3; do
  pdflatex -interaction=nonstopmode -halt-on-error -file-line-error \
    -output-directory=/tmp/misp-best-practices/notes \
    /tmp/misp-best-practices/notes/slide_handout.tex || exit 1
done
```

Inspect the PDF and build log for clipped content, overfull boxes and missing
references. The full repository build also creates the notes variant using
this course's existing `slide.tex` entry point.
The standard Beamer/`pgfpages` notes layout may emit duplicate PDF destination
warnings for its repeated slide thumbnails; inspect notes content separately.

## Edit or export the diagrams

Slides input the `.tikz` files directly; edits appear in the next deck build.
Colours and node styles live in [diagrams/style.tex](diagrams/style.tex).
Arrows describe possible paths or an operating process, not guaranteed
automatic data transfer or policy enforcement.

| Source | Purpose |
| --- | --- |
| [community-models.tikz](diagrams/community-models.tikz) | Hosted accounts, a member instance and a sector hub |
| [sharing-checks.tikz](diagrams/sharing-checks.tikz) | Handling policy, MISP access settings and actual outbound paths |
| [consumer-filters.tikz](diagrams/consumer-filters.tikz) | Different selection for investigation, detection and blocking |
| [feedback-cycle.tikz](diagrams/feedback-cycle.tikz) | Prepare, share, receive feedback and correct downstream data |

To export vector PDFs, run from this course directory after the slide setup:

```sh
mkdir -p /tmp/misp-best-practices/diagrams
for diagram in community-models sharing-checks consumer-filters feedback-cycle; do
  pdflatex -interaction=nonstopmode -halt-on-error -file-line-error \
    -output-directory=/tmp/misp-best-practices/diagrams -jobname="$diagram" \
    "\def\BestPracticeDiagram{$diagram}\input{diagrams/standalone.tex}" || exit 1
done
```

## Workshop setup

Use an isolated lab with fictional data and three organisations: the author,
an included recipient and an excluded recipient. Use non-administrator test accounts.
Disable production synchronisation, enrichment and action consumers. Start
with organisation-only distribution. The reserved `login.example.org` value
is deliberately unsuitable as a production indicator; a warninglist exclusion
is a useful discussion point. Do not browse it or send it to an external service.

Ask participants to explain the actual audience and export payload, then make
a correction and confirm the downstream lab output changes. A successful
publication alone is not evidence of successful delivery or removal.

## References

- [Community-setup guidelines](https://github.com/MISP/misp-compliance/blob/master/setting-up-ISACs/guidelines_to_set-up_an_ISAC.md)
- [Best Practices in Threat Intelligence](https://www.misp-project.org/best-practices-in-threat-intelligence.html)
- [MISP Book: Using the System](https://www.circl.lu/doc/misp/using-the-system/)
- [MISP Book: Synchronization and Sharing](https://www.circl.lu/doc/misp/sharing/index.html)
- [MISP Book: Sightings](https://www.circl.lu/doc/misp/sightings/)
- [MISP Book: Warning Lists](https://www.circl.lu/doc/misp/warninglists/)
- [MISP Book: Analyst Data](https://www.circl.lu/doc/misp/analyst-data/)
- [FIRST TLP 2.0](https://www.first.org/tlp/)
- [MISP compliance resources](https://github.com/MISP/misp-compliance)

Check behaviour on the deployed MISP version and configuration. This course
does not replace the [usage](../1-misp-usage/),
[administration](../2-misp-administration/),
[taxonomies](../3-misp-taxonomy-tagging/),
[feeds](../a.3-misp-feed/), [decay](../a.5-decaying-indicators/) or
[API](../a.7-rest-API/) courses.

Retain Team CIRCL attribution and the repository's dual AGPL-3.0-or-later /
CC-BY-SA-4.0 licensing when adapting these materials.
