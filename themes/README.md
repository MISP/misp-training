# MISP presentation theme

**A shared visual identity for training slides, workshops, and event decks.**

The MISP theme pairs the official 2.0 logo and blue palette with readable text,
a reusable cover, and support for presenter notes and partner logos.

[Training home](../README.md) · [Quick start](#quick-start) · [Customize a deck](#customize-a-deck) · [Build validation](validation.md)

![MISP 2.0 introduction cover with the official logo and deep-blue title panel](misp-preview.png)

## Quick start

Use a recent TeX Live installation with Beamer, TikZ, Fira Sans, and Fira Mono.
From the repository root, build the example without writing outputs into the
checkout:

```sh
export TEXINPUTS="$PWD/themes:${TEXINPUTS:-}:"
mkdir -p /tmp/misp-template

for pass in 1 2 3; do
  pdflatex -interaction=nonstopmode -halt-on-error \
    -output-directory=/tmp/misp-template themes/misp-template.tex || exit 1
done
```

Open `/tmp/misp-template/misp-template.pdf` to see title, section, content,
block, and focus slides. Copy [misp-template.tex](misp-template.tex) into your
new deck directory and replace the sample title, author, and content.

Three passes stabilize Beamer navigation and remembered TikZ page positions
on a fresh build. Putting `themes/` first in `TEXINPUTS` selects the bundled
styles and makes `misp-logo.pdf` discoverable.

## Customize a deck

### Select the theme

```tex
\usetheme[numbering=progressbar]{misp}
```

When migrating an older deck, remove its old `main`, `textcolor`, `background`,
and `\titlegraphic` overrides so the shared branding can take effect.

| Option | Result |
| --- | --- |
| `numbering=progressbar` | Show slide progress along the footline. |
| `numbering=fullbar` | Use a full-width bar with slide numbers. |
| `numbering=none` | Hide slide numbering. |
| `nofirafonts` | Leave font selection to the presentation. |

The default Fira body fonts keep the pdfLaTeX workflow portable. The official
vector wordmark retains its outlined typography, so Gotham does not need to be
installed. Long title metadata scales only when needed to fit the cover panel.

### Add a partner logo

Keep the MISP logo on the left and place an event or partner logo in the white
area at the upper right:

```tex
\misppartnergraphic{%
  \includegraphics[width=.30\paperwidth,height=.22\paperheight,keepaspectratio]{partner.png}%
}
```

### Build an existing deck

Run from the repository root:

```sh
export TEXINPUTS="$PWD/themes:${TEXINPUTS:-}:"
mkdir -p /tmp/misp-intro
cd 0-intro-shorter

for pass in 1 2 3; do
  pdflatex -interaction=nonstopmode -halt-on-error \
    -output-directory=/tmp/misp-intro slide.tex || exit 1
done
```

Use `slide_es.tex` or `slide_nl.tex` for the introduction's translations.
Preserve the existing aspect ratio when adapting a deck: older 4:3 decks contain
fixed-size diagrams, while the Metropolis-based presentations use 16:9.

### Include presenter notes

Notes handouts use `pgfpages` and `show notes on second screen=right`.
The root [build script](../build.sh) inserts that setup immediately before
`\begin{document}`, so it works with both short and long preambles.

## How the templates fit together

| File | Role |
| --- | --- |
| [misp-template.tex](misp-template.tex) | Starting point for a new presentation. |
| [beamerthememisp.sty](beamerthememisp.sty) | MISP theme built on the bundled Focus theme. |
| [mispidentity.sty](mispidentity.sty) | Shared logo, palette, typography, cover, and section styling. |
| [misp-logo.pdf](misp-logo.pdf) | Vector logo used directly by LaTeX. |

All Focus-based decks select `misp`. The two CIRCL/Metropolis presentations load
`mispidentity.sty` while retaining their custom navigation, TLP indicators, and
commands. Historical screenshots and diagrams retain their original content;
standalone MISP logo inclusions use the official 2.0 asset.

## Color palette

These are exact RGB colors from the official screen logo.

| Color | Hex | Used for |
| --- | --- | --- |
| Deep blue | `#02394A` | Titles, section backgrounds, and progress bar |
| Dark teal | `#00708D` | Links and primary bullets |
| Blue | `#0091B0` | Secondary bullets and block tint |
| Cyan | `#19C9F0` | Cover accents and links on dark backgrounds |
| Ink | `#28191B` | Body text |

## Repository-wide builds

The full collection also uses Font Awesome (including Font Awesome 5), Fourier,
Soul, and TrackLang. On Debian, install `texlive-fonts-extra`,
`texlive-latex-extra`, `texlive-plain-generic`, and `texlive-science` alongside
the existing base, recommended, pictures, and XeTeX packages.

| Workflow | Additional setup |
| --- | --- |
| Custom local TeX tree | Enable `fira.map`, `fontawesome.map`, `fontawesome5.map`, and `fourier.map`. |
| CIRCL/Metropolis decks | Install `minted`/`latexminted` and compile with shell escape; their Makefiles supply the theme path and three passes. |
| Complete publication bundle | Follow the root [build instructions](../README.md#build-and-customize), including `pdfunite` and `exiftool`. |

See the [validation report](validation.md) for build coverage and known failures
in archived material. Generated publication PDFs are not checked in as part of
the identity migration.

## Assets and attribution

The [source SVG](assets/misp-logo.svg) is unchanged from the official
[MISP visual identity 2.0](https://github.com/MISP/visual-identity/tree/main/2.0):

| Provenance | Value |
| --- | --- |
| Repository | `MISP/visual-identity` |
| Source path | `2.0/misp/1_horizontal/2_screen/svg/misp-logo-main-rvb-_hori-.svg` |
| Commit | `e3f4a3e93d39a9bf7d8d3cb907e31af77e755ebd` |
| Credit | MISP Project |
| License | CC-BY, as stated in the upstream [README](https://github.com/MISP/visual-identity/blob/e3f4a3e93d39a9bf7d8d3cb907e31af77e755ebd/README.md) |

The bundled PDF is a vector conversion of this SVG. Normal builds need no
network access, SVG converter, or shell escape for the logo. Regenerate it from
the repository root with:

```sh
inkscape themes/assets/misp-logo.svg --export-type=pdf --export-filename=themes/misp-logo.pdf
```

Theme code retains its GPL-3.0-or-later notices. Keep the asset attribution and
code notices when reusing or adapting the theme.
