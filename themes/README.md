# MISP Beamer theme

![MISP 2.0 introduction cover](misp-preview.png)

`beamerthememisp.sty` applies the [MISP visual identity 2.0](https://github.com/MISP/visual-identity/tree/main/2.0)
to the bundled Focus theme. Select it with
`\usetheme[numbering=progressbar]{misp}` and remove any old `main`, `textcolor`,
`background`, and `\titlegraphic` overrides. All Focus-based decks now select `misp`. The two CIRCL/Metropolis-based
presentations load the same `mispidentity.sty` branding layer while retaining
their navigation, TLP indicators, and custom commands.
The `fullbar`, `none`, and `nofirafonts` options are also supported.

Copy [misp-template.tex](misp-template.tex) as a starting point for a new deck.
It demonstrates title, section, content, block, notes, and focus slides. The
shared branding layer supplies the official horizontal logo, a white logo area, navy title and
section panels, teal accents, and dark text on white content slides. Fira body
fonts keep the existing pdfLaTeX workflow; the supplied vector wordmark retains
its original outlined typography without requiring Gotham to be installed.

Long title metadata is scaled only when needed to fit the cover panel. Event
partners can add a logo in the white area at the upper right without replacing
the MISP logo:

```tex
\misppartnergraphic{\includegraphics[width=.30\paperwidth,height=.22\paperheight,keepaspectratio]{partner.png}}
```

## Assets and palette

The unchanged [source SVG](assets/misp-logo.svg) comes from
`2.0/misp/1_horizontal/2_screen/svg/misp-logo-main-rvb-_hori-.svg`
in `MISP/visual-identity` at commit
`e3f4a3e93d39a9bf7d8d3cb907e31af77e755ebd`.
Credit: MISP Project, distributed under CC-BY as stated in that repository's
[README](https://github.com/MISP/visual-identity/blob/e3f4a3e93d39a9bf7d8d3cb907e31af77e755ebd/README.md).
`misp-logo.pdf` is a vector conversion of that SVG, bundled so builds need no
network access, SVG converter, or shell escape. To regenerate it from the
repository root:

```sh
inkscape themes/assets/misp-logo.svg --export-type=pdf --export-filename=themes/misp-logo.pdf
```

The theme uses exact colors from the screen logo:

| Color | Hex | Use |
| --- | --- | --- |
| Deep blue | `#02394A` | Titles, section backgrounds, progress bar |
| Dark teal | `#00708D` | Links and primary bullets |
| Blue | `#0091B0` | Secondary bullets and block tint |
| Cyan | `#19C9F0` | Title accent and links on dark backgrounds |
| Ink | `#28191B` | Body text |

## Build individual decks

Use a recent TeX Live with Beamer, TikZ, Fira Sans, and Fira Mono, as for the
existing Focus decks. Put the bundled themes first in `TEXINPUTS`; this also
makes `misp-logo.pdf` discoverable. Run from the repository root:

```sh
export TEXINPUTS="$PWD/themes:${TEXINPUTS:-}:"
mkdir -p /tmp/misp-template
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=/tmp/misp-template themes/misp-template.tex
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=/tmp/misp-template themes/misp-template.tex
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=/tmp/misp-template themes/misp-template.tex

mkdir -p /tmp/misp-intro
cd 0-intro-shorter
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=/tmp/misp-intro slide.tex
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=/tmp/misp-intro slide.tex
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=/tmp/misp-intro slide.tex
```

Three passes stabilize Beamer navigation and remembered TikZ page positions on
a fresh build. Use `slide_es.tex` or `slide_nl.tex` for the translations. Keep the current 4:3
aspect ratio for existing decks and their fixed-size diagrams. Notes handouts
continue to use `pgfpages` and `show notes on second screen=right`, as in
`build.sh`. Notes setup is inserted immediately before `\begin{document}` so
it works with both short and long preambles.

## Repository-wide builds

The full collection also uses Font Awesome (including Font Awesome 5), Fourier,
Soul, and TrackLang. On Debian these are supplied by `texlive-fonts-extra`,
`texlive-latex-extra`, `texlive-plain-generic`, and `texlive-science` in addition
to the existing base, recommended, pictures, and XeTeX packages. A custom local
TeX tree also needs the corresponding font maps enabled (`fira.map`,
`fontawesome.map`, `fontawesome5.map`, and `fourier.map`).
The two Metropolis-based decks require `minted`/`latexminted` and shell escape;
their Makefiles include the shared theme path and three compilation passes.

Historical screenshots and diagrams retain their content; standalone MISP logo
inclusions use the official 2.0 vector asset. Existing partner logos are retained
in the cover's partner slot. Generated publication PDFs are not checked in as
part of the migration.
