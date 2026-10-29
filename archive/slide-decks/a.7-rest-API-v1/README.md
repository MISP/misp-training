# Earlier REST API course — archived

**Historical reference. Outside standard training.**

This presentation describes the original API redesign and its then-future
plans. The accompanying notebooks, Postman exports and sample files belong to
older workshops. Use the [MISP 2.5 REST API course](../../../a.7-rest-API/README.md)
for current guidance.

[Original published PDF](original-published.pdf) · [Slide source](slide.tex) · [Historical lesson](content.tex) · [Archive catalog](../../README.md)

| Field | Value |
| --- | --- |
| Archived | 29 October 2026 |
| Original directory | `a.7-rest-API/` |
| Original PDF | `output/a.7-rest-API.pdf` |
| Last pre-archive revision | [6774568](https://github.com/MISP/misp-training/tree/6774568/a.7-rest-API) |
| Runtime compatibility | Not revalidated for the archived notebooks, collections or samples |

Original notebooks, outputs, images, Postman files, test files and published PDF
are retained byte-for-byte for provenance. They include embedded historical lab
keys, fixed instance IDs, certificate-verification bypasses and executable test
samples. They are not runnable prerequisites for the current course. Do not
reuse the old credentials or execute these samples as part of the new workshop.

Rebuildable sources add an archive subtitle/notice and fix shared include paths;
whitespace is normalised. The historical lesson remains intact.

## Build explicitly

Use the repository's [theme setup](../../../themes/README.md), then from its root:

```sh
export TEXINPUTS="$PWD/themes:${TEXINPUTS:-}:"
mkdir -p /tmp/misp-rest-archive
cd archive/slide-decks/a.7-rest-API-v1
for pass in 1 2 3; do
  pdflatex -interaction=nonstopmode -halt-on-error \
    -output-directory=/tmp/misp-rest-archive slide.tex || exit 1
done
```

The original PDF has no new banner inside its pages. This archive path is
excluded from the standard training build.
