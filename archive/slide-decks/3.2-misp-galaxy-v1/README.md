# Earlier Galaxy lesson — archived

**Historical reference. Outside standard training.**

Use the [current MISP 2.5 Galaxy course](../../../3.2-misp-galaxy/README.md).
This lesson retains older screenshots, catalogue lists and JSON illustrations.
Its claims about editing and synchronisation are not current implementation guidance.

[Original PDF](original-published.pdf) · [Source](slide.tex) · [Archive catalog](../../README.md)

Archived 30 October 2026 from `3.2-misp-galaxy/` and
`output/3.2-misp-galaxy.pdf` at
[6efcae8](https://github.com/MISP/misp-training/tree/6efcae8/3.2-misp-galaxy).
Original assets and PDF are preserved byte-for-byte. Rebuildable sources add
archive labelling, fix shared includes and normalise whitespace; the original
lesson body remains intact. Old examples have not been revalidated.

Use the repository theme setup, then build explicitly from its root:

```sh
export TEXINPUTS="$PWD/themes:${TEXINPUTS:-}:"
mkdir -p /tmp/misp-galaxy-archive
cd archive/slide-decks/3.2-misp-galaxy-v1
for pass in 1 2 3; do
  pdflatex -interaction=nonstopmode -halt-on-error \
    -output-directory=/tmp/misp-galaxy-archive slide.tex || exit 1
done
```

This archive path is excluded from standard training.
