# Earlier information-sharing introduction — archived

**Historical reference. Outside the standard training build.**

Use the [current full introduction and editable diagrams](../../../0-misp-introduction-to-information-sharing/README.md).
The earlier English and Dutch lessons differ in scope and retain dated community
counts, institutional descriptions, TLP:WHITE references, UI screenshots and
static artwork. They are not maintained as current guidance.

[English source](slide.tex) · [Dutch source](slide_nl.tex) · [Original English PDF](original-published.pdf) · [Original Dutch PDF](original-published_nl.pdf) · [Archive catalog](../../README.md)

Archived on 3 November 2026 from `0-misp-introduction-to-information-sharing/`
and its two published PDFs at
[`644d83458fa5f9cdca308006b86fc9b009c4dbfd`](https://github.com/MISP/misp-training/tree/644d83458fa5f9cdca308006b86fc9b009c4dbfd/0-misp-introduction-to-information-sharing).
All original image/PDF assets and both publication snapshots are preserved
byte-for-byte. Source changes are limited to archive cover labels, relative
shared-include path fixes and trailing-whitespace cleanup. Historical lesson
bodies remain; rebuilding does not validate their claims or interfaces.

Original static artwork: [overview](misp-overview-simplified.pdf),
[governance](governance.png), [distributed sharing](misp-distributed.pdf).

Rebuild explicitly after the shared theme/font setup, from this archive directory:

```sh
export TEXINPUTS="/path/to/misp-training/themes:${TEXINPUTS:-}:"
mkdir -p /tmp/misp-sharing-archive
for source in slide slide_nl; do
  for pass in 1 2 3; do
    pdflatex -interaction=nonstopmode -halt-on-error \
      -output-directory=/tmp/misp-sharing-archive "$source.tex" || exit 1
  done
done
```

Historical layouts may retain warnings. Current slide and diagram validation is
reported separately in the maintained course.
