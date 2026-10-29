# MISP modules: enrichment, data exchange and workflow actions

**Discover what is available, operate the service, and build integrations you can verify.**

This revised course is for analysts, operators and developers. It uses the
shared [MISP 2.0 theme](../themes/README.md) and the existing 4:3 format.

[Slides](slide.tex) · [Presenter notes](content.tex) · [Lab](#hands-on-lab) · [Sources](#source-audit) · [Training home](../README.md)

## Teaching routes

The 43-page deck contains a title, 37 teaching slides and five section pages.
It was reviewed on **29 October 2026**.

| Audience | Route | Suggested time |
| --- | --- | --- |
| Analysts | Discovery, structured enrichment, import/export and the website | 30–45 minutes |
| Operators | Add installation, configuration, caching, statistics and troubleshooting | 60–90 minutes total |
| Developers | Add custom loading, module contracts and the full lab | A further 25–40 minutes |

Presenter notes explain limitations and expected exercise outcomes. The course
replaces the old global-pip/rc.local installation, hardcoded DNS answer, incomplete
code samples, static default-module list and speculative roadmap. It adds workflow
actions, current operational features, website workflows and runnable examples.

## Reference snapshot

Reviewed against [MISP/misp-modules at `3a903305cf374ff7cc5ca0290857c54382c1f933`](https://github.com/MISP/misp-modules/tree/3a903305cf374ff7cc5ca0290857c54382c1f933).
Package metadata declares **3.1.1**, but features on `main` can postdate a
published package with that version. Use the pinned checkout for the lab.

The source contains 270 candidate files: 203 expansion, 22 import, 32 export and
13 action modules, excluding `__init__.py` and underscore-prefixed files.
These counts do not establish installed dependencies, credentials or provider
availability. Inspect `/version`, `/modules` and `/openapi.json` at runtime.

MISP settings were checked against [MISP/MISP revision `fc99c9e3fc85beddc6ef18835359f3c8b7f44608`](https://github.com/MISP/MISP/blob/fc99c9e3fc85beddc6ef18835359f3c8b7f44608/app/Model/Module.php)
on `2.5`. Menus depend on the deployed version.

## Hands-on lab

Use Python **3.10–3.x**; validation used Python 3.12. Neither a MISP instance nor
provider credentials are required. Selected handlers process synthetic data
locally; the publication action is explicitly a dry run.

### 1. Install the reviewed service

Start in this training repository's root. Choose different temporary directory
names if these already exist.

```sh
TRAINING_DIR="$PWD/3.1-misp-modules"
git clone https://github.com/MISP/misp-modules.git /tmp/misp-modules-workshop
git -C /tmp/misp-modules-workshop checkout 3a903305cf374ff7cc5ca0290857c54382c1f933
python3 -m venv /tmp/misp-modules-workshop-venv
. /tmp/misp-modules-workshop-venv/bin/activate
python -m pip install /tmp/misp-modules-workshop
cd "$TRAINING_DIR"
```

The **base installation** is sufficient. Missing optional dependency warnings
are expected; check the specific lab modules in `/modules`. Other integrations
may need `minimal`/`all` extras, system libraries, credentials and network access.
See the [installation guide](https://misp.github.io/misp-modules/install/).

### 2. Start the lab service

Run from `3.1-misp-modules/` with the virtual environment active:

```sh
misp-modules -l 127.0.0.1 -p 6666 \
  --custom "$PWD/examples/custom" \
  --module-config "$PWD/examples/module-defaults.json" \
  --cache-config "$PWD/examples/cache.json"
```

Keep this terminal running. These files contain synthetic prefix text and cache
settings, not credentials. Restart after code/configuration changes. If port
6666 is occupied, choose another port and pass that URL to the verifier.

### 3. Verify behavior

In another terminal, from `3.1-misp-modules/`:

```sh
python3 examples/verify_lab.py --url http://127.0.0.1:6666 -v
```

Expected: **12 tests pass**. Missing modules or startup flags fail verification.

| Capability | Expected outcome |
| --- | --- |
| Health, version, discovery, OpenAPI | Required routes and lab modules are present |
| Dictionary and legacy handlers | Same result for the same synthetic text |
| Validation | Invalid text/config returns a module error |
| Defaults and API overrides | `LOCAL: MISP` by default; `API: MISP` when overridden |
| Empty-value policy | Empty string/null use explicit prefix fallback |
| Structured enrichment | URL components and a reference to the input UUID |
| Zeek export | Decoded domain/IP feed excludes the non-IDS attribute |
| osquery plan | `planned`, a pack and `misp-training.conf`; no publication |
| Cache/statistics | Identical repeated request increases cache hits |

HTTP 200 can still carry `error`/`errors`. Tests check JSON results, not just status.

### 4. Explore the requests

```sh
curl --fail --silent --show-error \
  http://127.0.0.1:6666/query \
  -H 'Content-Type: application/json' \
  --data @examples/url-request.json
```

Use that pattern with each request file:

| File | What to inspect |
| --- | --- |
| [url-request.json](examples/url-request.json) | `results.Object`, components and the `generated-from` reference |
| [export-request.json](examples/export-request.json) | Base64 `data`, Zeek types and non-IDS filtering |
| [action-request.json](examples/action-request.json) | `data.status`, pack, provenance and activation notice |
| [training_uppercase.py](examples/custom/expansion/training_uppercase.py) | Metadata, dictionary handler and legacy adapter |
| [module-defaults.json](examples/module-defaults.json) | Precedence and empty-value fallback |
| [cache.json](examples/cache.json) | TTL, entry and response-byte limits |

The uppercase module demonstrates an interface, not an intelligence source.

### Discussion prompts and answers

1. **Why can HTTP 200 still fail?**

   Module errors use the JSON envelope. Inspect `error`/`errors` and statistics.
2. **Why might the same observable miss the cache?**

   The whole effective request matters, including UUIDs, context, credentials,
   configuration and timeout.
3. **Did the osquery action activate detection?**

   No. A dry run plans a pack. Local publication, distribution, configuration
   references, reload and endpoint verification are separate.
4. **Why is a new module missing in MISP?**

   Check the actual package/custom root, dependencies, restart, `/modules`,
   family settings, enablement, organisation restrictions and input compatibility.

Stop the service with **Ctrl+C** when finished.

## Standalone website

The website is a separate client with its own database, settings, history and
administrator login. It supports enrichment, import, export, investigation trees
and configured external tools. See the pinned guides below for deployment.

The reviewed checkout ships `website/sample.env`. Production requires suitable
`ADMIN_PASSWORD` and application configuration. For an existing installation,
back up the database and apply shipped migrations with `poetry run mmw db upgrade`
before restarting. `db init` is not an update migration; `db migrate` generates
developer migrations. The reviewed update repairs legacy external-tools API-key
column/index state.

The API lab does **not** install or exercise the website. Screenshots are
unchanged upstream browser-fixture captures, not live provider/MISP test evidence.

## Build slides and notes

From the training repository root:

```sh
export TEXINPUTS="$PWD/themes:${TEXINPUTS:-}:"
mkdir -p /tmp/misp-modules-slides
cd 3.1-misp-modules
for pass in 1 2 3; do
  pdflatex -interaction=nonstopmode -halt-on-error \
    -output-directory=/tmp/misp-modules-slides slide.tex || exit 1
done
```

Generate a notes handout without changing tracked source:

```sh
awk '/\\begin\{document\}/ {
  print "\\usepackage{pgfpages}"
  print "\\setbeameroption{show notes on second screen=right}"
} {print}' slide.tex > /tmp/misp-modules-slides/slide_handout.tex

for pass in 1 2 3; do
  pdflatex -interaction=nonstopmode -halt-on-error \
    -output-directory=/tmp/misp-modules-slides \
    /tmp/misp-modules-slides/slide_handout.tex || exit 1
done
```

Outputs are `slide.pdf` and `slide_handout.pdf`. The repository
[publication script](../build.sh) also includes this deck.

## Next: contribute with an AI agent

The [companion course](../a.14-ai-assisted-misp-modules/README.md) explains how to
brief a coding agent, preserve module contracts, verify generated code and prepare
an upstream contribution. It includes a reusable agent brief and a tested local
MISP-standard reference exercise.

## Source audit

Evidence is pinned to the reviewed revision. Recheck it, runtime availability,
requests and screenshots before updating this course.

| Topic | Primary source |
| --- | --- |
| Python, package version and extras | [pyproject.toml](https://github.com/MISP/misp-modules/blob/3a903305cf374ff7cc5ca0290857c54382c1f933/pyproject.toml) |
| Loader families and candidate-file rules | [misp_modules/__init__.py](https://github.com/MISP/misp-modules/blob/3a903305cf374ff7cc5ca0290857c54382c1f933/misp_modules/__init__.py) |
| Routes, dispatch, timeouts and custom loading | [misp_modules/__main__.py](https://github.com/MISP/misp-modules/blob/3a903305cf374ff7cc5ca0290857c54382c1f933/misp_modules/__main__.py) |
| Developer contracts and MISP enablement | [documentation/mkdocs/contribute.md](https://github.com/MISP/misp-modules/blob/3a903305cf374ff7cc5ca0290857c54382c1f933/documentation/mkdocs/contribute.md) |
| Defaults and empty-value policy | [documentation/mkdocs/module-config.md](https://github.com/MISP/misp-modules/blob/3a903305cf374ff7cc5ca0290857c54382c1f933/documentation/mkdocs/module-config.md) |
| Opt-in process-local cache | [documentation/mkdocs/caching.md](https://github.com/MISP/misp-modules/blob/3a903305cf374ff7cc5ca0290857c54382c1f933/documentation/mkdocs/caching.md) |
| DNS objects and source references | [misp_modules/modules/expansion/dns.py](https://github.com/MISP/misp-modules/blob/3a903305cf374ff7cc5ca0290857c54382c1f933/misp_modules/modules/expansion/dns.py) |
| Local URL parsing | [misp_modules/modules/expansion/extract_url_components.py](https://github.com/MISP/misp-modules/blob/3a903305cf374ff7cc5ca0290857c54382c1f933/misp_modules/modules/expansion/extract_url_components.py) |
| Zeek export and selection semantics | [documentation/export_mod/zeek_intel_export.md](https://github.com/MISP/misp-modules/blob/3a903305cf374ff7cc5ca0290857c54382c1f933/documentation/export_mod/zeek_intel_export.md) |
| Network ACL exports | [documentation/export_mod/network_acl_exports.md](https://github.com/MISP/misp-modules/blob/3a903305cf374ff7cc5ca0290857c54382c1f933/documentation/export_mod/network_acl_exports.md) |
| osquery generation | [documentation/export_mod/osqueryexport.md](https://github.com/MISP/misp-modules/blob/3a903305cf374ff7cc5ca0290857c54382c1f933/documentation/export_mod/osqueryexport.md) |
| osquery publication action | [documentation/action_mod/osquery_pack_publish.md](https://github.com/MISP/misp-modules/blob/3a903305cf374ff7cc5ca0290857c54382c1f933/documentation/action_mod/osquery_pack_publish.md) |
| Website workflows and updates | [website/README.md](https://github.com/MISP/misp-modules/blob/3a903305cf374ff7cc5ca0290857c54382c1f933/website/README.md) |
| Website interface and screenshots | [website/doc/interface.md](https://github.com/MISP/misp-modules/blob/3a903305cf374ff7cc5ca0290857c54382c1f933/website/doc/interface.md) |

### Screenshot attribution

Files in [screenshots/current](screenshots/current/) are unchanged copies from
`MISP/misp-modules/website/doc` at the reviewed revision:

| Local file | Upstream file |
| --- | --- |
| `workspace.png` | `home_misp_module.png` |
| `results.png` | `object_result_cards.png` |
| `investigations.png` | `investigation_trees.png` |

Credit: MISP Project / misp-modules contributors. Retain the upstream
[AGPL-3.0 notice](https://github.com/MISP/misp-modules/blob/3a903305cf374ff7cc5ca0290857c54382c1f933/LICENSE).
Embedded MISP and MISP Modules artwork is credited in the upstream
[image attribution](https://github.com/MISP/misp-modules/blob/3a903305cf374ff7cc5ca0290857c54382c1f933/website/app/static/images/README.md).
Older assets remain historical resources; this deck does not present them
as the current interface.

## Validation scope

The base installation at the reviewed revision passed all **12 tests** on
Python 3.12. They exercise local contracts and HTTP dispatch, including
structured parsing, export generation and a publication dry run.

Provider credentials, external lookups/submissions, real publication, endpoint
activation, the MISP UI and the website runtime are outside this lab.

The slides and notes handout each passed three pdfLaTeX passes, producing
43-page PDFs with extractable text and no overfull-box or missing-glyph warnings.
Representative tables, diagrams, code, screenshots and presenter-note layouts
were inspected after rendering. README links, pinned source paths, shell snippets,
JSON fixtures and Python syntax were also checked.
