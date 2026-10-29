# Repository-wide identity migration validation

Validated on 2026-10-29 with TeX Live 2025/dev (Debian), the bundled themes first
in `TEXINPUTS`, Fira/Font Awesome/Fourier font maps, and the packages listed in
[the theme instructions](README.md#repository-wide-builds). Outputs and logs
were written outside the checkout.

- Inventoried 139 presentation entry points, including translations, saved
  handouts, the reusable template, and the `beamerswitch` feed deck.
- Migrated the remaining 135 documents. Focus-based decks select `misp`; both
  CIRCL/Metropolis presentations load the same `mispidentity` branding layer.
- All 36 slide sources listed in the root publication script compiled.
- Full builds passed for 133 of 139 documents, using three noninteractive
  `pdflatex` passes with `-halt-on-error` and nonempty PDF text extraction.
  The two `minted` presentations additionally used shell escape.
- All 139 cover previews passed PDF text extraction. Previews came from
  successful full builds or separate three-pass cover builds where body content
  prevents compilation. Text position checks verified cover headings stay in
  the title panel. Inspected standard, long-subtitle, partner-logo, Metropolis,
  and notes layouts visually.
- Shell syntax checks passed for the root and seven standalone build scripts;
  `git diff --check` passed.

The following six full-document failures also reproduce with their original
entry points from `main` and the previous theme. Their cover builds pass. The
body-content errors are retained for a separate correction:

| Entry point | Existing failure |
| --- | --- |
| `20250526_NATO_MUG/slide.tex` | Unescaped underscore in `user_notification`; missing math delimiter at `content.tex:87`. |
| `20230930-cakefest/slide.tex` | Missing `dashboard.png` at `content.tex:175`. |
| `events/20230605-FIRSTCON23-Workflows/slide_handout.tex` | Invalid leading line break at `content.tex:116`. |
| `events/20230707-GeekWeek-Workflows/slide_handout.tex` | Invalid leading line break at `content.tex:91`. |
| `events/20231114-NATO-MUG-Workflow/slide_handout.tex` | Undefined `\Wider` command at `content.tex:386`. |
| `x.1-belgomisp/slide.tex` | Unterminated frame in `content.tex`; runaway argument at end of file. |

Existing layout, duplicate-destination, and PDF metadata warnings remain in
historical material. The complete publication bundle, ancillary cheatsheets,
and merged `misp-training.pdf` were not rebuilt or replaced. Passing all 36
publication slide sources does not assert that those separate outputs passed.
