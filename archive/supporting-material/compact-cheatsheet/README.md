# Legacy training-VM cheat sheet — archived

**Historical reference. Outside the standard training.**

This sheet documents an older multi-application training VM, including Viper-web
access details and MISP 2.4 update instructions. Its URLs, credentials and setup
commands must not be treated as current deployment guidance.

[LaTeX source](cheatsheet.tex) · [Viper course](../../slide-decks/1.1-misp-viper-integration/README.md) · [Archive catalog](../../README.md) · [Current cheat sheet](../../../cheatsheets/)

| Field | Value |
| --- | --- |
| Archived | 29 October 2026 |
| Original path | `training-support/compact-cheatsheet/` |
| Last pre-archive revision | [d3b335680f8b0113536d89a0e55e4daeb7a49853](https://github.com/MISP/misp-training/tree/d3b335680f8b0113536d89a0e55e4daeb7a49853/training-support/compact-cheatsheet) |
| Scope | Historical VM support; not a current integration or upgrade procedure |

The source and local image are preserved with an archive banner added to the
sheet. The standard publication script builds `cheatsheets/cheatsheet.tex`,
not this compact VM sheet.

To build this historical document, with the required TeX fonts installed, run
from the repository root:

```sh
mkdir -p /tmp/misp-legacy-vm-sheet
cd archive/supporting-material/compact-cheatsheet
pdflatex -interaction=nonstopmode -halt-on-error \
  -output-directory=/tmp/misp-legacy-vm-sheet cheatsheet.tex
```

This only builds the document. The old VM, logins, services and commands have
not been tested.
