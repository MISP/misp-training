# Earlier general-usage course — archived

**Historical reference. Outside the standard training build.**

Use the [current MISP 2.5 usage course](../../../1-misp-usage/README.md).
The earlier material retains old VM setup/repair commands (default credential strings omitted), static
raster diagrams and demo prompts rather than a verified current UI walkthrough.
It is not maintained as current setup or operational guidance.

[English source](slide.tex) · [Spanish source](slide_es.tex) · [Dutch entry point](slide_nl.tex) · [Original English PDF at the earlier revision](https://github.com/MISP/misp-training/blob/56db4e8694e3a1c34d3e01ee3b60fd4eef682821/output/1-misp-usage.pdf) · [Original Spanish PDF at the earlier revision](https://github.com/MISP/misp-training/blob/56db4e8694e3a1c34d3e01ee3b60fd4eef682821/output/1-misp-usage_es.pdf) · [Original Dutch PDF at the earlier revision](https://github.com/MISP/misp-training/blob/56db4e8694e3a1c34d3e01ee3b60fd4eef682821/output/1-misp-usage_nl.pdf) · [Archive catalog](../../README.md)

Archived on 3 November 2026 from `1-misp-usage/` and all three published PDFs at
[`56db4e8694e3a1c34d3e01ee3b60fd4eef682821`](https://github.com/MISP/misp-training/tree/56db4e8694e3a1c34d3e01ee3b60fd4eef682821/1-misp-usage).
Original image/PDF assets are preserved byte for byte. The three original
publication PDFs remain linked at their existing revision instead of being
republished here. Source changes include archive cover labels, shared-include
path repairs, whitespace cleanup and omission of obsolete default VM credential
strings. Other historical lesson content remains.

Rebuild explicitly after the shared theme/font setup, from this archive directory:

```sh
export TEXINPUTS="/path/to/misp-training/themes:${TEXINPUTS:-}:"
mkdir -p /tmp/misp-usage-archive
for source in slide slide_es slide_nl; do
  for pass in 1 2 3; do
    pdflatex -interaction=nonstopmode -halt-on-error \
      -output-directory=/tmp/misp-usage-archive "$source.tex" || exit 1
  done
done
```

Historical layouts may retain warnings. Rebuilding does not validate the old VM
instructions, credentials, interfaces, sharing paths or integration behaviour.
