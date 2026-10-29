# Earlier object-template course — archived

**Historical reference. Outside standard training.**

Use the [current MISP 2.5 course](../../../3.3-misp-object-template/README.md).
This lesson contains older screenshots, field descriptions and enforcement
claims that should not be used as current implementation guidance.

[Original PDF](original-published.pdf) · [Source](slide.tex) · [Archive catalog](../../README.md)

Archived 29 October 2026 from `3.3-misp-object-template/` and
`output/3.3-misp-object-template.pdf` at
[de5bfb8](https://github.com/MISP/misp-training/tree/de5bfb8/3.3-misp-object-template).
Original assets and published PDF are preserved byte-for-byte. Source changes
add archive labelling, fix shared includes and normalise whitespace; the
historical lesson remains intact. Runtime examples are not revalidated.

To rebuild explicitly, use the repository theme setup, then:

```sh
export TEXINPUTS="$PWD/themes:${TEXINPUTS:-}:"
mkdir -p /tmp/misp-object-archive
cd archive/slide-decks/3.3-misp-object-template-v1
for pass in 1 2 3; do
  pdflatex -interaction=nonstopmode -halt-on-error \
    -output-directory=/tmp/misp-object-archive slide.tex || exit 1
done
```

The standard build selects the replacement course, not this archive path.
