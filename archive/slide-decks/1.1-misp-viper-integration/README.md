# Viper and MISP integration — archived

**Historical reference. This course is no longer part of the standard training.**

The original terminal integration course and screenshots are retained for older
references. Commands, provider integrations and setup assumptions may no longer
apply. Compatibility with current MISP or Viper versions has not been verified.
This archives the training material; it makes no claim about the Viper project's
own maintenance status.

[Original published PDF](original-published.pdf) · [Slide source](slide.tex) · [Historical content](content.tex) · [Archive catalog](../../README.md) · [Current training](../../../README.md#slide-catalog)

## Provenance

| Field | Value |
| --- | --- |
| Archived | 29 October 2026 |
| Original source path | `1.1-misp-viper-integration/` |
| Original PDF path | `output/1.1-misp-viper-integration.pdf` |
| Last pre-archive revision | [d3b335680f8b0113536d89a0e55e4daeb7a49853](https://github.com/MISP/misp-training/tree/d3b335680f8b0113536d89a0e55e4daeb7a49853/1.1-misp-viper-integration) |
| Historical runtime versions | Not established; do not infer current compatibility |

All original assets and the published PDF are preserved. The PDF is unchanged,
so it has its original cover rather than a new archive banner. The rebuildable
source adds an archive subtitle and notice, fixes the shared-author include path,
and records the archival date. The historical teaching content is retained.

Related material: the [legacy VM cheat sheet](../../supporting-material/compact-cheatsheet/README.md)
and the [older combined training bundles](../../publications/combined-training/README.md).

## Current alternatives

- [PyMISP](../../../a.2-pymisp/) for programmatic access.
- [Command-line tools](../../../a.b-cli/) for terminal-oriented training.
- [MISP modules](../../../3.1-misp-modules/README.md) for enrichment and integrations.

## Build the archived slides explicitly

The root publication script excludes this course. Use the repository's
[theme setup](../../../themes/README.md), then run from the repository root:

```sh
export TEXINPUTS="$PWD/themes:${TEXINPUTS:-}:"
mkdir -p /tmp/misp-viper-archive
cd archive/slide-decks/1.1-misp-viper-integration

for pass in 1 2 3; do
  pdflatex -interaction=nonstopmode -halt-on-error \
    -output-directory=/tmp/misp-viper-archive slide.tex || exit 1
done
```

For a notes handout, continue from that directory:

```sh
awk '/\\begin\{document\}/ {
  print "\\usepackage{pgfpages}"
  print "\\setbeameroption{show notes on second screen=right}"
} {print}' slide.tex > /tmp/misp-viper-archive/slide_handout.tex

for pass in 1 2 3; do
  pdflatex -interaction=nonstopmode -halt-on-error \
    -output-directory=/tmp/misp-viper-archive \
    /tmp/misp-viper-archive/slide_handout.tex || exit 1
done
```

Historical layouts and screenshots have not been redesigned. A successful
document build does not validate old commands or recreate a supported Viper/MISP
environment.
