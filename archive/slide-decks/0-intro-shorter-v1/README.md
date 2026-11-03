# Earlier short introduction — archived

**Historical reference. Outside the standard training build.**

Use the [current short introduction and editable diagrams](../../../0-intro-shorter/README.md).
The earlier English, Spanish and Dutch lessons have different lengths and retain
dated user counts, feature lists, screenshots, institutional descriptions and
static overview/governance artwork. They are not maintained as current guidance.

[English source](slide.tex) · [Spanish source](slide_es.tex) · [Dutch source](slide_nl.tex) · [Original published Spanish PDF](original-published-es.pdf) · [Archive catalog](../../README.md)

Archived on 3 November 2026 from `0-intro-shorter/` and
`output/0-intro-shorter_es.pdf` at
[`c818ca9838e1466da08823f0f26a614c1c15f061`](https://github.com/MISP/misp-training/tree/c818ca9838e1466da08823f0f26a614c1c15f061/0-intro-shorter).
All original image/PDF assets and the available published Spanish PDF are
preserved byte-for-byte. No English or Dutch publication PDF was tracked for
this course at that revision. Source changes are limited to archive labels,
shared-include path fixes and whitespace cleanup; historical lesson bodies remain.

The original artwork remains available for comparison:
[project overview](misp-overview-simplified.pdf), [governance image](governance.png)
and [distributed-sharing diagram](misp-distributed.pdf).

Rebuild explicitly with the shared theme setup, from this archive directory:

```sh
export TEXINPUTS="/path/to/misp-training/themes:${TEXINPUTS:-}:"
mkdir -p /tmp/misp-intro-archive
for source in slide slide_es slide_nl; do
  for pass in 1 2 3; do
    pdflatex -interaction=nonstopmode -halt-on-error \
      -output-directory=/tmp/misp-intro-archive "$source.tex" || exit 1
  done
done
```

Rebuilding historical slides does not revalidate their assertions or screenshots.
