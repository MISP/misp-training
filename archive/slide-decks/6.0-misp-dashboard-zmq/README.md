# Standalone ZeroMQ dashboard course — archived

**Historical reference. Outside standard training.**

This presentation describes the separate `misp-dashboard` application, its
ZeroMQ subscriber/dispatcher architecture, Flask service and older screenshots.
It does not teach the integrated dashboard inside MISP 2.5.

[Original published PDF](original-published.pdf) · [Slide source](slide.tex) · [Historical content](content.tex) · [Current integrated-dashboard course](../../../6.0-misp-dashboard/README.md) · [Archive catalog](../../README.md)

| Field | Value |
| --- | --- |
| Archived | 29 October 2026 |
| Original source directory | `6.0-misp-dashboard/` |
| Original PDF | `output/6.0-misp-dashboard.pdf` |
| Last pre-archive revision | [c83c8aeae8b990fcfb9f3227119ee4388b738638](https://github.com/MISP/misp-training/tree/c83c8aeae8b990fcfb9f3227119ee4388b738638/6.0-misp-dashboard) |
| Runtime compatibility | Not revalidated for the archived examples |

All original images, assets and the published PDF are preserved. The PDF remains
byte-identical and has no new banner inside its original pages. Rebuildable
sources add an archive subtitle/notice and correct the shared-author include
path. The historical examples are unchanged.

This retires the **course from standard training**, not the standalone project.
No assertion is made about that project's maintenance status.

## Build explicitly

Use the repository's [theme setup](../../../themes/README.md). From the repository root:

```sh
export TEXINPUTS="$PWD/themes:${TEXINPUTS:-}:"
mkdir -p /tmp/misp-zmq-dashboard-archive
cd archive/slide-decks/6.0-misp-dashboard-zmq
for pass in 1 2 3; do
  pdflatex -interaction=nonstopmode -halt-on-error \
    -output-directory=/tmp/misp-zmq-dashboard-archive slide.tex || exit 1
done
```

The standard build continues to select the new course at `6.0-misp-dashboard`;
it never selects this archive path. Compiling these documents does not validate
the standalone runtime or make its older setup instructions current.
