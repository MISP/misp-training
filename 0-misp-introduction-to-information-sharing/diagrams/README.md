# Edit the information-sharing diagrams

The slides input native **TikZ** sources. PDFs are vector exports with selectable
text; PNGs are previews. Neither export format is an input to the slides.

| File | Purpose |
| --- | --- |
| [data-model.tikz](data-model.tikz) | Event, standalone attribute, object and contextual information |
| [correlation.tikz](correlation.tikz) | Two reports share a domain value; interpretation remains open |
| [exchange.tikz](exchange.tikz) | Selected exchange, a configured feedback path and an isolated instance |
| [timeline.tikz](timeline.tikz) | Observation interval versus record creation/edit times |
| [quality-cycle.tikz](quality-cycle.tikz) | Capture, review, use and reassessment |
| [labels-en.tex](labels-en.tex), [labels-nl.tex](labels-nl.tex) | Translated labels; import the shared short-introduction labels first |
| [style.tex](style.tex) | Shared style import and local extensions |
| [standalone.tex](standalone.tex) | Standalone document wrapper |
| [build.sh](build.sh) | All eight diagrams in both languages |

The [overview](../../0-intro-shorter/diagrams/overview.tikz),
[sharing flow](../../0-intro-shorter/diagrams/sharing-flow.tikz) and
[contribution cycle](../../0-intro-shorter/diagrams/community.tikz) remain shared
sources in the short course. Their [style](../../0-intro-shorter/diagrams/style.tex)
and [editing guide](../../0-intro-shorter/diagrams/README.md) also apply here.
Keep both course directories in the same checkout; no precompiled short-course
artifact is required.

## Edit

Change node positions, widths and arrow routes in `.tikz` files. Change text in
the corresponding language file, keeping the same label keys in both languages.
`\\` forces a line break; `\-` permits hyphenation of a long compound. Literal
case values live in the data-model and correlation geometry and should stay
synthetic unless the lesson is deliberately changed. The colour palette and
Fira fonts match the shared training theme.

For a full-course-only override of a shared label, add a matching `\IntroSetLabel`
after the import in this course's language wrapper. Editing a shared source or
shared label changes both introductions, so inspect both if you do that.

The data-model arrows show containment, not every relationship in the schema.
Correlation arrows do not assert attribution. Exchange arrows indicate configured
paths constrained by policy; they do not imply automatic onward sharing or a
universal network. Timeline dates are fictional. The quality cycle is a review
process, not a formula proving information correct.

## Export

After the [shared TeX/font setup](../../themes/README.md), from the course directory:

```sh
bash diagrams/build.sh /tmp/misp-sharing-diagrams
```

This creates `overview-en.pdf`, `overview-nl.pdf`, and the equivalent files for
`sharing-flow`, `community`, `data-model`, `correlation`, `exchange`, `timeline`
and `quality-cycle`. The output directory is required. No shell escape or
network access is used.

For one diagram:

```sh
mkdir -p /tmp/misp-sharing-diagrams
pdflatex -interaction=nonstopmode -halt-on-error \
  -jobname=exchange-nl -output-directory=/tmp/misp-sharing-diagrams \
  '\def\IntroLanguage{nl}\def\SharingDiagramName{exchange}\input{diagrams/standalone.tex}'
```

Refresh the five supplied English vector exports and PNG previews after checking
both languages:

```sh
for diagram in data-model correlation exchange timeline quality-cycle; do
  cp "/tmp/misp-sharing-diagrams/${diagram}-en.pdf" "diagrams/${diagram}.pdf"
  pdftoppm -singlefile -scale-to 1600 -png \
    "diagrams/${diagram}.pdf" "diagrams/${diagram}-preview"
done
```

For the three shared exports, follow the short introduction's guide. Poppler
provides `pdftoppm`, `pdftotext`, `pdfinfo` and `pdfimages`. Check selectable text,
no embedded raster images in standalone diagrams, long labels and arrow routing
at presentation scale. Rebuild the decks after source changes. Existing
[license and attribution terms](../../README.md#license-attribution-and-funding) apply.
