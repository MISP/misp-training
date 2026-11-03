# Earlier MISP administration course

**Historical reference — outside the standard training.** Archived on 3 November
2026 from `2-misp-administration/` at revision
`f6b74bbb5ca5760e0ceeda42cf8cf8f44ab4948e`. Use the
[current MISP 2.5 course](../../../2-misp-administration/README.md) for teaching.

The original English entry point/content and ten binary assets are retained here.
The assets are unchanged. The source cover is marked archived, shared-include paths
were repaired for this location and trailing whitespace was normalised. Two lines
containing obsolete default VM credentials were omitted from the copied source;
one named historical example email was replaced by an omission notice. No new
copy of the old PDF is distributed here; its unchanged publication remains available
at the original revision:

[Read the original published PDF](https://github.com/MISP/misp-training/blob/f6b74bbb5ca5760e0ceeda42cf8cf8f44ab4948e/output/2-misp-administration.pdf).

The old slides describe VM assumptions, MISP 2.4 interfaces, Resque-era logs and
update/repair commands. They are historical material, not current operational advice.
The omitted defaults are not suitable credentials for any new training instance.
No historical runtime or repair procedure was executed as part of this archive.

To rebuild the marked historical source with the repository's TeX dependencies,
from this directory:

```sh
mkdir -p /tmp/misp-admin-archive
TEXINPUTS="$(pwd)/../../../themes//:" pdflatex -interaction=nonstopmode -halt-on-error \
  -output-directory=/tmp/misp-admin-archive slide.tex
# Repeat twice for navigation and references.
```

Historical layout warnings may remain. The current deck's normal build excludes
this archive. Original attribution and repository licensing remain applicable.
