# MISP 2.5 administration

A 90–120 minute English workshop on delegated access, sharing policy and observable
operations. The 32-page deck includes 31 presenter notes, 19 real MISP screenshots,
two editable TikZ diagrams and two practical checkpoints. It uses 16:9 pages to
keep wide administration tables legible.

- [Read the built slides](../output/2-misp-administration.pdf).
- [Run the guided lab](lab/README.md) and [rehearse recovery and updates](lab/operations.md).
- [Edit the lesson](content.tex), [entry point](slide.tex) or [diagrams](diagrams/README.md).
- [Screenshot provenance and reproduction](screenshots/README.md).
- [Historical course](../archive/slide-decks/2-misp-administration-v1/README.md).

## Teaching sequence

| Part | Practise | Approximate time |
| --- | --- | --- |
| Responsibility and identity | Role flags, organisations, users, lifecycle and client keys | 20 min |
| Audience | Sharing-group membership, instance constraints and ordinary-account checks | 20 min |
| Configuration | Knowledge bases, disabled peers/feeds and defaults | 20 min |
| Operations | Diagnostics, workers, jobs, scheduled tasks and audit evidence | 20 min |
| Handover | Recovery/update rehearsal and checkpoints | 20–40 min |

Learners should already understand events, attributes, distribution and publication
from [Using MISP](../1-misp-usage/README.md). The trainer needs a disposable instance,
a site administrator and separately scoped ordinary accounts. The platform operator
remains responsible for deployment, storage, services and recovery. Custom roles,
identity providers, deployment methods and later patches can change the controls.

## Reference and observed outcomes

Captured on **3 November 2026**, in MISP **2.5.50**, the latest published MISP release
checked that day. The version JSON and diagnostics report 2.5.50; the displayed
[source commit](https://github.com/MISP/MISP/commit/fc99c9e3fc85beddc6ef18835359f3c8b7f44608)
was verified against the public repository. Exact backend/frontend image digests,
knowledge references, browser dimensions and PNG hashes are in the
[manifest](screenshots/manifest.json).

The local checks verified member/outside visibility, denied Org Admin site-setting
access, disabled-account access, a read-only key's rejected write, a warninglist
match and a completed local taxonomy-refresh job. A new-event form uses the revised
organisation-only default while the two existing events keep their original scopes.
See the scoped [validation record](lab/reference-validation.json).

All identities and records are synthetic. Peer transfer flags and feed fetching/
caching remain disabled. The diagnostics screenshot deliberately retains the local
failure to retrieve the latest GitHub version and the container self-update notice;
it is useful evidence to interpret, not a production health certificate. There is
no remote-exchange, mail-delivery, restore or production-upgrade claim.

## Build and adapt

Use the repository's TeX dependencies and shared MISP theme. From this directory:

```sh
mkdir -p /tmp/misp-admin-slides
TEXINPUTS="$(pwd)/../themes//:" pdflatex -interaction=nonstopmode -halt-on-error \
  -output-directory=/tmp/misp-admin-slides slide.tex
# Repeat the same command twice to settle navigation and references.
```

For presenter notes, copy `slide.tex` to the ignored `slide_handout.tex` and insert
`\setbeameroption{show notes on second screen=right}` before `\begin{document}`;
build it three times in a separate output directory. Each PDF has 32 pages;
the notes version places the notes beside their slide.

Keep the editable diagrams as the teaching source. Re-capture UI views when the
reference changes and update the manifest, notes, lab evidence and published PDF
together. The usual repository build still selects this course; archives are excluded.
The material retains the repository's attribution and licensing.

## Reference material

- [MISP 2.5.50 release](https://github.com/MISP/MISP/releases/tag/v2.5.50) and
  [MISP Docker deployment](https://github.com/MISP/misp-docker).
- [Advanced-key handling](https://github.com/MISP/MISP/blob/v2.5.50/app/Controller/AuthKeysController.php),
  [scheduled tasks](https://github.com/MISP/MISP/blob/v2.5.50/app/Controller/TasksController.php)
  and [jobs](https://github.com/MISP/MISP/blob/v2.5.50/app/Controller/JobsController.php)
  in the pinned reference source.
- [MISP documentation](https://www.circl.lu/doc/misp/) and the
  [deployment course](../a.c-deployment/).
