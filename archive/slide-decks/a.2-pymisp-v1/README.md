# Earlier PyMISP deep-dive — archived

**Historical reference. Outside standard training.**

Use the [current PyMISP / MISP 2.5 course](../../../a.2-pymisp/README.md).
This lesson retains older Python requirements, API examples, asset references
and speaker notes. It has not been revalidated as current implementation advice.

[Original PDF](original-published.pdf) · [Source](slide.tex) · [Original notes](notes.md) · [Archive catalog](../../README.md)

Archived on 2 November 2026 from `a.2-pymisp/` and `output/a.2-pymisp.pdf`
at [`77f9c745c48e4f0fdfcb7d2a9d786c566f2fead7`](https://github.com/MISP/misp-training/tree/77f9c745c48e4f0fdfcb7d2a9d786c566f2fead7/a.2-pymisp).
The original notes, images and published PDF are preserved byte-for-byte.
The lesson body retains its original content with whitespace cleanup; the slide
wrapper labels the archive and resolves shared includes.

Use the repository theme setup and build explicitly from its root:

```sh
export TEXINPUTS="$PWD/themes:${TEXINPUTS:-}:"
mkdir -p /tmp/pymisp-archive
cd archive/slide-decks/a.2-pymisp-v1
for pass in 1 2 3; do
  pdflatex -interaction=nonstopmode -halt-on-error \
    -output-directory=/tmp/pymisp-archive slide.tex || exit 1
done
```

This archive is excluded from the standard training build.
