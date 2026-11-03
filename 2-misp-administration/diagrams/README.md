# Editable administration diagrams

The slide deck inputs the native TikZ sources directly. Edit the labels, nodes,
coordinates or arrows in these files; there is no raster image to trace.

| Diagram | Editable source | Standalone vector PDF |
| --- | --- | --- |
| Responsibility scopes | [responsibilities.tikz](responsibilities.tikz) | [responsibilities.pdf](responsibilities.pdf) |
| Controlled change and recovery | [change-cycle.tikz](change-cycle.tikz) | [change-cycle.pdf](change-cycle.pdf) |

The responsibility cards represent separate scopes, not a permission inheritance
hierarchy. The dashed recovery arrow represents a planned decision, not automatic
rollback. Shared colours/fonts/shapes are in [style.tex](style.tex).

With pdfLaTeX, TikZ, standalone and the repository's fonts installed, from the course:

```sh
bash diagrams/build.sh /tmp/misp-admin-diagrams
```

The script requires an explicit output directory, uses no network or shell escape,
and writes one single-page vector PDF per diagram. To change one export directly:

```sh
pdflatex -jobname=responsibilities -output-directory=/tmp/misp-admin-diagrams \
  '\def\AdminDiagramName{responsibilities}\input{diagrams/standalone.tex}'
```

Rebuild the deck after edits. Copy verified vector PDFs into this directory when
updating the distributed exports. See the [course build instructions](../README.md).
