# MISP data model overview

A short introduction to the MISP 2.5 data model for analysts and integrators.
Allow 25–35 minutes, including a five-minute modelling exercise. Basic knowledge
of threat intelligence is enough. Each content slide has presenter notes,
including caveats and the exercise answers.
The deck contains **22 pages**: a cover and 21 content slides, with seven editable
TikZ diagrams.

[PDF](../complementary/other-slides/a.11.a-misp-data-model-overview.pdf) ·
[Slide entry point](slide.tex) · [Content and notes](content.tex) ·
[Full data-model course](../a.11-misp-data-model/) · [Training home](../README.md)

## Review of the earlier overview

Reviewed on **7 November 2026** against MISP **2.5.51**, commit
[`04fc5f8b7ccb52bb6614ca3e9ccdbfdf6585d985`](https://github.com/MISP/MISP/tree/04fc5f8b7ccb52bb6614ca3e9ccdbfdf6585d985).
The [original 19-page English PDF](https://github.com/MISP/misp-training/blob/ac3cc9614467a3665c304732e0d142e75e5fcd8e/complementary/other-slides/a.11.a-misp-data-model-overview.pdf)
is available in Git history. The existing
complementary PDF path now contains the rebuilt deck; the Spanish edition and
other complementary variants have not been translated or refreshed by this change.

| Earlier material | Updated explanation |
| --- | --- |
| Pages 2 and 12: data/context overview places galaxies alongside simple tags | Separate the galaxy collection, cluster records and cluster tag attachments; show feedback and sharing alongside structure/context. |
| Page 4: attributes “cannot be duplicated inside the same Event” | Distinguish record UUID from value; avoid a universal uniqueness claim across object and standalone attributes and import paths. |
| Page 4: indicator versus supporting data tied mainly to `to_ids` | Explain intended detection use separately from truth, confidence, access and correlation. |
| Page 5: template versus instance and unavailable-template editing | Show template UUID/version, instance UUID and per-field attribute UUIDs; qualify conformity/editing by the selected definition and path. |
| Page 6: event context and distribution “propagated” to underlying data | Separate context scope from copying tag attachments; explain parent/child sharing and separate analyst-data controls. |
| Pages 7–10: dense images, report and graph screenshots | Replace with editable event containment, Markdown reference examples and a directed object-reference graph. |
| Pages 8–9: references presented as general entity relationships | Specify object source and object/attribute target; use a same-event example and explain authorised extension-to-parent resolution and capture-path differences in the notes; distinguish analyst Relationships and cluster relations. |
| Missing analyst-data overview | Add Note, Opinion and Relationship, with authorship and independent distribution; distinguish sightings and proposals. |
| Pages 17–18: correlations created whenever attributes change | Explain eligible types, enablement, exclusions and engine/configuration limits; a match is an investigative lead. |
| Page 18: “CDIR” and unconditional CIDR/ssdeep examples | Correct CIDR; state advanced-correlation and ssdeep runtime/threshold requirements; use documentation addresses. |
| Page 19: grouping and extended events | Explain coherent event boundaries and `extends_uuid`, retaining the extension's ownership and access constraints. |
| Legacy branding and no editable source beside the PDF | Use the shared MISP theme, vector logo, palette, progress bar and TikZ sources. |

This is a conceptual overview, not an exhaustive database schema or import/API
contract. It complements the full data-model course rather than replacing it.
The four-part map is a teaching aid, not a claim about separate storage layers.
The 16:9 aspect ratio of the original is retained using the repository's shared
Beamer theme and standard `slide.tex` / `content.tex` structure.

## Build slides and presenter notes

Install the dependencies in the [theme guide](../themes/README.md). No shell
escape, network lookup or screenshot assets are needed at compile time.
From the repository root:

```sh
export TEXINPUTS="$PWD/themes:${TEXINPUTS:-}:"
mkdir -p /tmp/misp-model-overview/slides /tmp/misp-model-overview/notes
cd a.11.a-misp-data-model-overview
for pass in 1 2 3; do
  pdflatex -interaction=nonstopmode -halt-on-error -file-line-error \
    -output-directory=/tmp/misp-model-overview/slides slide.tex || exit 1
done
```

For the same presenter-notes layout as the repository's `build.sh`:

```sh
awk '/\\begin\{document\}/ {print "\\usepackage{pgfpages}"; print "\\setbeameroption{show notes on second screen=right}"} {print}' \
  slide.tex > /tmp/misp-model-overview/notes/slide_handout.tex
for pass in 1 2 3; do
  pdflatex -interaction=nonstopmode -halt-on-error -file-line-error \
    -output-directory=/tmp/misp-model-overview/notes \
    /tmp/misp-model-overview/notes/slide_handout.tex || exit 1
done
```

The root build includes this deck immediately after `a.11-misp-data-model` and
publishes it as `output/a.11.a-misp-data-model-overview.pdf`, with its notes
variant in `output/handout/`. To refresh the tracked quick-reference copy after
reviewing a new build, run from the course directory:

```sh
cp /tmp/misp-model-overview/slides/slide.pdf \
  ../complementary/other-slides/a.11.a-misp-data-model-overview.pdf
```

## Edit and export the diagrams

Slides input `.tikz` files directly. Shared colours, fonts and node styles live
in [diagrams/style.tex](diagrams/style.tex). Containment arrows, explicit
relationship arrows and dashed correlation arrows are explained on their slides;
they do not imply automatic data transfer or tag inheritance.

| Diagram | Purpose |
| --- | --- |
| [model-map.tikz](diagrams/model-map.tikz) | Structure, context, analysis/feedback and sharing |
| [event-anatomy.tikz](diagrams/event-anatomy.tikz) | Optional event contents and object attributes |
| [object-template.tikz](diagrams/object-template.tikz) | Template definition versus object instance |
| [object-references.tikz](diagrams/object-references.tikz) | Directed object-to-object/attribute assertions |
| [context.tikz](diagrams/context.tikz) | Free tags, taxonomy vocabularies and galaxy clusters |
| [analyst-data.tikz](diagrams/analyst-data.tikz) | Notes, opinions and relationships on supported targets |
| [correlation.tikz](diagrams/correlation.tikz) | A computed match between distinct attribute records |

Export individual vector PDFs from the course directory, with the same
`TEXINPUTS` setup:

```sh
mkdir -p /tmp/misp-model-overview/diagrams
for diagram in model-map event-anatomy object-template object-references context analyst-data correlation; do
  pdflatex -interaction=nonstopmode -halt-on-error -file-line-error \
    -output-directory=/tmp/misp-model-overview/diagrams -jobname="$diagram" \
    "\def\DataModelDiagram{$diagram}\input{diagrams/standalone.tex}" || exit 1
done
```

## Evidence and further reading

Implementation links below are pinned to the reviewed MISP revision. The MISP
standard describes interchange; deployed behaviour also depends on version,
configuration, permissions, correlation engine and consumer/export path.

| Topic | Implementation reference |
| --- | --- |
| Attribute identity, fields and non-correlating types | [MispAttribute.php](https://github.com/MISP/MISP/blob/04fc5f8b7ccb52bb6614ca3e9ccdbfdf6585d985/app/Model/MispAttribute.php) |
| Object templates, identity and conformity | [MispObject.php](https://github.com/MISP/MISP/blob/04fc5f8b7ccb52bb6614ca3e9ccdbfdf6585d985/app/Model/MispObject.php) |
| Object-reference source/target resolution | [ObjectReference.php](https://github.com/MISP/MISP/blob/04fc5f8b7ccb52bb6614ca3e9ccdbfdf6585d985/app/Model/ObjectReference.php), especially `captureReference`, `getReferencedInfo` and `isValidExtendedEventForReference` |
| Report capture, distribution and element references | [EventReport.php](https://github.com/MISP/MISP/blob/04fc5f8b7ccb52bb6614ca3e9ccdbfdf6585d985/app/Model/EventReport.php) |
| Analyst-data types, supported targets and distribution | [AnalystData.php](https://github.com/MISP/MISP/blob/04fc5f8b7ccb52bb6614ca3e9ccdbfdf6585d985/app/Model/AnalystData.php) and [Relationship.php](https://github.com/MISP/MISP/blob/04fc5f8b7ccb52bb6614ca3e9ccdbfdf6585d985/app/Model/Relationship.php) |
| Sighting types and visibility policy | [Sighting.php](https://github.com/MISP/MISP/blob/04fc5f8b7ccb52bb6614ca3e9ccdbfdf6585d985/app/Model/Sighting.php) |
| Cluster records, tag identity and relations | [GalaxyCluster.php](https://github.com/MISP/MISP/blob/04fc5f8b7ccb52bb6614ca3e9ccdbfdf6585d985/app/Model/GalaxyCluster.php) |
| Correlation eligibility, advanced matching and thresholds | [Correlation.php](https://github.com/MISP/MISP/blob/04fc5f8b7ccb52bb6614ca3e9ccdbfdf6585d985/app/Model/Correlation.php) and [DefaultCorrelationBehavior.php](https://github.com/MISP/MISP/blob/04fc5f8b7ccb52bb6614ca3e9ccdbfdf6585d985/app/Model/Behavior/DefaultCorrelationBehavior.php) |

- [MISP standard](https://www.misp-standard.org/)
- [MISP Book](https://www.circl.lu/doc/misp/), including [analyst data](https://www.circl.lu/doc/misp/analyst-data/), [sightings](https://www.circl.lu/doc/misp/sightings/) and [sharing](https://www.circl.lu/doc/misp/sharing/index.html)
- [MISP Objects](https://github.com/MISP/misp-objects), [Taxonomies](https://github.com/MISP/misp-taxonomies) and [Galaxy](https://github.com/MISP/misp-galaxy)
- [FIRST TLP 2.0](https://www.first.org/tlp/)
- Training: [objects](../3.3-misp-object-template/README.md), [Galaxy](../3.2-misp-galaxy/README.md), [usage](../1-misp-usage/README.md) and [REST API](../a.7-rest-API/README.md)

Validation: three-pass pdfLaTeX builds of the 22-page slides and 22-page notes
handout, builds of all seven standalone diagrams, extracted PDF text and visual
inspection of rendered slides/notes. Slide and diagram builds have no overfull
boxes, missing characters or unresolved references. The standard `pgfpages`
notes layout emits duplicate PDF destination warnings for its repeated slide
thumbnails. `bash -n build.sh` and `git diff --check` also pass. The complete
repository publication build and a live-instance exercise were not run.
Examples use reserved `.example` names and documentation IP addresses.

Adapted from the MISP training complementary overview. Retain MISP / Team CIRCL
attribution and the repository's AGPL-3.0-or-later / CC-BY-SA-4.0 licensing when
reusing these materials. The shared theme and logo retain their own notices.
