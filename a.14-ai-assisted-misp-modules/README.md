# Contributing MISP modules with an AI agent

**Turn an implementation request into a tested, reviewable contribution.**

This 29-page companion to the [MISP modules course](../3.1-misp-modules/README.md)
explains how to direct a coding agent without bypassing the project's architecture.
It includes a reusable prompt, a local MISP-standard reference module, and tests.

[Slides](slide.tex) · [Presenter notes](content.tex) · [Agent brief](AGENT_BRIEF.md) · [Worked exercise](#worked-exercise) · [Sources](#source-audit) · [Training home](../README.md)

## How to use this material

| Route | Use |
| --- | --- |
| Contributor briefing | Present the slides, then adapt the task fields in [AGENT_BRIEF.md](AGENT_BRIEF.md). |
| Workshop | Give participants the exercise specification below; keep the implementation as an answer key. |
| Real integration | Replace the exercise with an identified project gap and authoritative provider/schema documentation. |

Allow about 25–35 minutes for the presentation, or 60–90 minutes with the exercise
and review. The deck contains a title, 25 content slides and three section pages.
Presenter notes provide limitations and discussion points.

The agent is a **development assistant**, not a new runtime module type. The
reference implementation has no model calls, agent framework, provider account,
DNS resolution or target writes.

## Brief the agent

Fill in the purpose/gap, unique identifier, family, inputs/outputs, official
contract, configuration, side effects, acceptance cases and execution boundaries.
Give the adapted brief to your coding tool in the **misp-modules checkout**.

The brief is a standalone Markdown prompt. It is not automatically installed as
an agent policy or a replacement for the checkout's own instructions. Preserve
existing work and follow current project conventions.

Ask for evidence at each useful checkpoint:

1. Files and official documentation inspected, with the target revision.
2. Request/result mapping and implementation/test plan.
3. A focused patch that respects the loader, dispatcher and family contracts.
4. Actual test commands, counts, results and remaining limits.
5. Metadata, user documentation and a concise PR description.

An agent's confidence or a syntax-only check cannot demonstrate a correct
integration. Do not substitute invented provider behavior for missing documentation.

## Worked exercise

The reference lives at
[examples/custom/expansion/training_domain_normalize.py](examples/custom/expansion/training_domain_normalize.py).
It demonstrates the architecture; it is **not** a proposal to contribute another
normalization module upstream.

### Acceptance specification

| Area | Required behavior |
| --- | --- |
| Family | Expansion; identifier `training_domain_normalize`; `format: misp_standard` |
| Input | A `domain` or `hostname` attribute with string value and valid UUID |
| Normalization | Trim surrounding whitespace, remove one trailing root dot, apply Python standard-library IDNA and lowercase |
| Bounds | At least two labels; each ASCII label 1–63 characters, alphanumeric ends and optional interior hyphens; full name at most 253 ASCII characters |
| Rejections | Unsupported type, malformed fields/UUID, IP literals, wildcard, URL, empty/interior-empty labels and invalid boundaries |
| Source | Preserve original UUID/value/comment and detection flag; do not mutate the caller's input |
| Derived result | A PyMISP `domain-ip` object with a non-IDS domain attribute and a `derived-from` reference to the original UUID |
| State | Fresh metadata and results across calls |
| Effects | Local processing only; no lookup, submission, publication or runtime model service |

The full name is normalized: the module does not guess a registrable domain,
validate ownership/reachability, use a public-suffix database or classify a threat.
Standard-library IDNA behavior is part of this exercise's contract.

The implementation uses real PyMISP serialization and existing object templates.
The verifier checks those results, not a mocked copy of the expected output.

### 1. Prepare the service environment

Use Python 3.10–3.x. From the training repository root, choose fresh temporary
paths if the following directories already exist:

```sh
TRAINING_DIR="$PWD/a.14-ai-assisted-misp-modules"
git clone https://github.com/MISP/misp-modules.git /tmp/misp-agent-workshop
git -C /tmp/misp-agent-workshop checkout 3a903305cf374ff7cc5ca0290857c54382c1f933
python3 -m venv /tmp/misp-agent-workshop-venv
. /tmp/misp-agent-workshop-venv/bin/activate
python -m pip install /tmp/misp-agent-workshop
cd "$TRAINING_DIR"
```

You can reuse the parent course's base environment if it matches the reviewed
source. Optional dependency warnings do not establish that this particular module
failed; verify its discovery. The broader upstream test/CI environment needs
additional dependencies and native prerequisites.

### 2. Run unit checks

From the companion deck's directory, with PyMISP installed:

```sh
python3 examples/verify_module.py -v
```

Expected: **8 unit tests**. The output explicitly states that HTTP checks were
not requested. Tests cover normalization/IDNA, provenance, detection flags, input
and state isolation, malformed-input subtests, both handler interfaces and metadata.

### 3. Check the real service boundary

In one terminal:

```sh
misp-modules -l 127.0.0.1 -p 6666 --custom "$PWD/examples/custom"
```

In another terminal, from this directory, with the same Python environment:

```sh
python3 examples/verify_module.py --url http://127.0.0.1:6666 -v
```

Expected: **11 tests**, consisting of the eight unit tests and three HTTP tests.
They verify discovery/format, OpenAPI, the structured result and a module error
over HTTP 200. Select a different port and matching URL if needed.

Inspect the sample response yourself:

```sh
curl --fail --silent --show-error \
  http://127.0.0.1:6666/query \
  -H 'Content-Type: application/json' \
  --data @examples/request.json
```

Expected normalized value: `xn--bcher-kva.example`. Compare the source UUID/value,
derived object and reference with [the request](examples/request.json). Check
`error`/`errors` as well as HTTP status. Stop the workshop service with Ctrl+C.

### 4. Review the agent's contribution

Implement in a separate exercise directory before comparing with the answer key.
Review the diff and tests against the acceptance specification. For a genuine
upstream contribution, also verify:

- An identified need rather than a duplicate existing module.
- Official provider/schema compatibility and required configuration.
- Mocked provider error/timeout/rate-limit/partial-result cases when relevant.
- Dependencies, metadata and user documentation.
- Current project formatting/lint, relevant tests and service discovery.
- Clear separation of artifact generation, publication and activation.
- Exact results and limits in the PR description.

Do not submit the training normalizer unchanged just because the exercise passes.

## Build the slides and notes

From the training repository root:

```sh
export TEXINPUTS="$PWD/themes:${TEXINPUTS:-}:"
mkdir -p /tmp/misp-agent-slides
cd a.14-ai-assisted-misp-modules
for pass in 1 2 3; do
  pdflatex -interaction=nonstopmode -halt-on-error \
    -output-directory=/tmp/misp-agent-slides slide.tex || exit 1
done
```

To generate the notes handout:

```sh
awk '/\\begin\{document\}/ {
  print "\\usepackage{pgfpages}"
  print "\\setbeameroption{show notes on second screen=right}"
} {print}' slide.tex > /tmp/misp-agent-slides/slide_handout.tex

for pass in 1 2 3; do
  pdflatex -interaction=nonstopmode -halt-on-error \
    -output-directory=/tmp/misp-agent-slides \
    /tmp/misp-agent-slides/slide_handout.tex || exit 1
done
```

The [root publication script](../build.sh) includes this deck. It uses the shared
MISP 2.0 theme and 4:3 format.

## Source audit

Reviewed against `MISP/misp-modules` revision
`3a903305cf374ff7cc5ca0290857c54382c1f933` on 29 October 2026.
Read the actual target checkout before a real contribution; interfaces, dependencies
and CI can change.

| Topic | Pinned evidence |
| --- | --- |
| Family/discovery rules | [misp_modules/__init__.py](https://github.com/MISP/misp-modules/blob/3a903305cf374ff7cc5ca0290857c54382c1f933/misp_modules/__init__.py) |
| Dispatch and result serialization | [misp_modules/__main__.py](https://github.com/MISP/misp-modules/blob/3a903305cf374ff7cc5ca0290857c54382c1f933/misp_modules/__main__.py) |
| Contribution and MISP enablement | [documentation/mkdocs/contribute.md](https://github.com/MISP/misp-modules/blob/3a903305cf374ff7cc5ca0290857c54382c1f933/documentation/mkdocs/contribute.md) |
| Dependencies and tool configuration | [pyproject.toml](https://github.com/MISP/misp-modules/blob/3a903305cf374ff7cc5ca0290857c54382c1f933/pyproject.toml) |
| CI prerequisites and checks | [.github/workflows/test-package.yml](https://github.com/MISP/misp-modules/blob/3a903305cf374ff7cc5ca0290857c54382c1f933/.github/workflows/test-package.yml) |
| Pre-commit tools | [.pre-commit-config.yaml](https://github.com/MISP/misp-modules/blob/3a903305cf374ff7cc5ca0290857c54382c1f933/.pre-commit-config.yaml) |
| Structured DNS object construction | [misp_modules/modules/expansion/dns.py](https://github.com/MISP/misp-modules/blob/3a903305cf374ff7cc5ca0290857c54382c1f933/misp_modules/modules/expansion/dns.py) |
| Mocked DNS boundary and output tests | [tests/test_dns.py](https://github.com/MISP/misp-modules/blob/3a903305cf374ff7cc5ca0290857c54382c1f933/tests/test_dns.py) |
| Export format/selection tests | [tests/test_zeek_intel_export.py](https://github.com/MISP/misp-modules/blob/3a903305cf374ff7cc5ca0290857c54382c1f933/tests/test_zeek_intel_export.py) |

## Validation and limits

The reference passed **8 unit tests plus 3 HTTP tests** using the reviewed base
service on Python 3.12. Black, isort and flake8 checks passed using the upstream
configuration. The 29-page deck and its notes handout built successfully, as did
the updated 43-page MISP modules deck and its notes handout. Documentation links
and shell snippets were checked; the publication list contains 37 unique decks.

No external provider, runtime model service, live MISP UI or publication target
was exercised. No module contribution was submitted upstream. The reference
demonstrates local contracts and service dispatch, not every module family or
the complete upstream CI matrix. The complete publication bundle was not rebuilt.
