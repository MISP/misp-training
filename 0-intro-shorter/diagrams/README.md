# Edit and reuse the introduction diagrams

The primary format is **TikZ**, with selectable text and vector shapes in the
compiled PDFs. The decks use the `.tikz` files directly; the supplied English
PDFs and PNGs are exports for reuse and preview, not inputs to the slides.

| File | Edit here |
| --- | --- |
| [overview.tikz](overview.tikz) | Four-part project overview: card geometry and spacing |
| [sharing-flow.tikz](sharing-flow.tikz) | Sources, MISP stages, use and the dashed feedback arrow |
| [community.tikz](community.tikz) | Contribution cycle and edge routing |
| [labels-en.tex](labels-en.tex) | English text |
| [labels-es.tex](labels-es.tex) | Spanish text |
| [labels-nl.tex](labels-nl.tex) | Dutch text |
| [style.tex](style.tex) | Typography, palette, boxes and arrow styles |
| [standalone.tex](standalone.tex) | Standalone PDF wrapper |
| [build.sh](build.sh) | Export all three diagrams in all three languages |

## Change a label or shape

For example, edit the `software-body` label in the appropriate language file
to change the first overview card. `\\` inserts an intentional line break;
long compounds may use `\-` for an optional hyphenation point. Keep corresponding
label keys in all three language files. Identifiers such as `MISP`, `PyMISP`
and `misp-modules` retain their project names.

Edit the `.tikz` file to move a node, change a text width or reroute an arrow.
Change geometry once to update every language. The style uses the shared MISP
palette (`#02394A`, `#00708D`, `#0091B0`, `#28191B`) and Fira Sans, matching the
[training theme](../../themes/README.md). `\providecolor` also lets the standalone
wrapper use the same colors without loading Beamer.

Keep arrow meaning clear:

- The overview has **no arrows**: its four parts are complementary, not a hierarchy.
- Solid arrows in the sharing flow show information flow. The **dashed arrow**
  returns feedback to review; no automatic publication or trust decision is implied.
- The community cycle shows needs, contributions, review and reuse. It explains
  collaboration rather than a formal organisation or legal governance structure.

## Export standalone PDFs

After the shared TeX/font setup, run from `0-intro-shorter`:

```sh
bash diagrams/build.sh /tmp/misp-intro-diagrams
```

This produces `overview-en.pdf`, `sharing-flow-en.pdf`, `community-en.pdf` and
the corresponding `-es` and `-nl` exports. The script requires an explicit output
directory and does not need network access, shell escape or external artwork.

For a single custom export:

```sh
pdflatex -interaction=nonstopmode -halt-on-error \
  -jobname=overview-es -output-directory=/tmp/misp-intro-diagrams \
  '\def\IntroLanguage{es}\def\IntroDiagram{overview}\input{diagrams/standalone.tex}'
```

Compile from the course directory so the relative style/label paths resolve.
The editable source can also be used in another LaTeX document: load TikZ and
`style.tex`, make the referenced `diagrams/` files available, and input the
chosen `.tikz` file.

## Refresh the supplied English exports

After inspecting all language variants:

```sh
for diagram in overview sharing-flow community; do
  cp "/tmp/misp-intro-diagrams/${diagram}-en.pdf" "diagrams/${diagram}.pdf"
  pdftoppm -singlefile -scale-to 1600 -png \
    "diagrams/${diagram}.pdf" "diagrams/${diagram}-preview"
done
```

`pdftoppm`, `pdftotext`, `pdfinfo` and `pdfimages` come from Poppler. Check PDF
text extraction, the absence of embedded raster images in standalone exports,
and labels/arrow routing at presentation scale. Rebuild the slide PDFs after
source changes. The materials retain the repository's existing license and
attribution terms; see the [training README](../../README.md#license-attribution-and-funding).
