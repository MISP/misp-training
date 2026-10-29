# Earlier dashboard widget-development lesson — archived

**Historical reference. Outside standard training.**

This lesson describes the earlier widget-development model, a Whoami-style
example, older renderer guidance and `cacheLifetime` metadata. Use the
[current MISP 2.5 course](../../../a.a-widget-dev/README.md) for new development.

[Original published PDF](original-published.pdf) · [Slide source](slide.tex) · [Historical content](content.tex) · [Archive catalog](../../README.md)

| Field | Value |
| --- | --- |
| Archived | 29 October 2026 |
| Original source directory | `a.a-widget-dev/` |
| Original PDF | `output/a.a-widget-dev.pdf` |
| Last pre-archive revision | [4be0c3b0284e3adad34fe344c7c40619a635646b](https://github.com/MISP/misp-training/tree/4be0c3b0284e3adad34fe344c7c40619a635646b/a.a-widget-dev) |
| Runtime compatibility | Historical examples not revalidated for current MISP |

All original images/assets and the published PDF are preserved byte-for-byte.
The original PDF has no new banner inside its pages. Rebuildable sources add an
archive subtitle and notice and correct the shared-author include path; the
historical lesson body remains intact.

Do not deploy older snippets unchanged. The class/filename, built-in widget
name, cache metadata and renderer contracts need review. Archiving this lesson
does not retire custom dashboard widgets as a feature.

## Build explicitly

Use the repository's [theme setup](../../../themes/README.md). From its root:

```sh
export TEXINPUTS="$PWD/themes:${TEXINPUTS:-}:"
mkdir -p /tmp/misp-widget-archive
cd archive/slide-decks/a.a-widget-dev-v1
for pass in 1 2 3; do
  pdflatex -interaction=nonstopmode -halt-on-error \
    -output-directory=/tmp/misp-widget-archive slide.tex || exit 1
done
```

This path is excluded from the standard build. Compiling it does not validate
its historical examples.
