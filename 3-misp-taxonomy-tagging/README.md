# Taxonomies and tagging in MISP 2.5

**Classify consistently, filter precisely, share deliberately.**

A practical course for analysts, administrators and trainers. Learn how to choose
a vocabulary, apply canonical tags at the right scope, interpret search results,
and review handling instructions and warninglist hits.

[Slides](slide.tex) · [Presenter notes](content.tex) · [Exercise](#workshop-classify-search-explain) · [Source audit](#source-audit) · [Training home](../README.md)

## What this course covers

| Question | What you will practise |
| --- | --- |
| Which label should I use? | Machine tags, expanded labels, TLP 2.0, source reliability and confidence |
| Where does it belong? | Event and attribute tags, local assessments, event reports and attachment relationships |
| How is it made available? | Taxonomy updates, selectable terms, collections, exclusivity and governance controls |
| How do tools consume it? | Explicit Boolean filters, event context, workflow and synchronisation rules |
| What deserves review? | Warninglist matches, detection intent and endpoint-specific suppression |

The deck contains **35 pages**: a title, 30 content slides and four section pages.
Allow 35–45 minutes for the presentation and about 20 minutes for the workshop.
For an analyst briefing, focus on choosing labels, attachment scope, searches and
warninglists; retain vocabulary maintenance for administrators.

The material is reviewed against **MISP 2.5.50** source, not a claim that every
feature was introduced in 2.5. UI labels and permissions depend on the installed
patch level, theme, user role and instance configuration.

## The distinctions to keep clear

- **Canonical value and display text:** use
  `admiralty-scale:source-reliability="b"` in filters; “Usually reliable” is its
  expanded label, not its machine value.
- **Handling and access:** TLP communicates permitted disclosure. Distribution,
  sharing groups and permissions control access in MISP. A TLP label does not
  automatically change distribution or revoke shared copies.
- **Event and attribute scope:** event tags are stored separately from attribute
  tags. An attribute search may match event context without copying labels onto
  each stored attribute.
- **Local and private:** local attachments are excluded from ordinary external
  synchronisation. Internal-server sync can carry them, and API output can expose
  them unless excluded. “Local” does not mean private to one user.
- **Assignment and visibility:** tag organisation/user restrictions determine
  who can apply a tag; they do not restrict who can read the event. `local_only`
  and `exportable` are tag settings; `local` is an attachment setting.
- **Governance and enforcement:** exclusivity, required and highlighted
  taxonomies serve different purposes. The reviewed required-taxonomy publish
  check is in a non-REST UI path. Automation must validate its own policy;
  classification presence alone does not establish a correct assessment.
- **Warnings and verdicts:** warninglists identify values needing scrutiny. A
  match does not prove harmlessness and does not automatically remove evidence.

Use TLP 2.0 CLEAR, GREEN, AMBER and RED, with AMBER+STRICT to limit AMBER
disclosure to the organisation only.
The MISP taxonomy also retains compatibility labels; those are not all FIRST
standard labels. Read [FIRST's standard](https://www.first.org/tlp/) and the
source's restrictions before deciding who may receive information. Human TLP
markings use FIRST's spelling; MISP machine tags use the canonical lowercase
taxonomy spelling, such as `tlp:amber+strict`.

## Workshop: classify, search, explain

### Prepare the training instance

Use an isolated MISP 2.5 training instance and a user allowed to create an event,
apply the chosen tags and run REST searches. This repository does not start a
MISP server or contain credentials.

Ask the trainer or administrator to:

1. Update the deployed taxonomy files and the MISP taxonomy library.
2. Enable `tlp`, `admiralty-scale` and `misp` and the exact terms used below.
   Updates read the deployment's local `app/files/taxonomies` files; they do not
   fetch GitHub's latest content on demand.
3. Update warninglists and enable **List of RFC 5735 CIDR blocks**
   (`lists/rfc5735/list.json`).
4. Optionally enable `workflow:todo="review"` for the local-assessment step.

The reviewed classic menu provides **List Taxonomies** at `/taxonomies/index`
and **List Tag Collections** at `/tag_collections/index`. Equivalent controls in
another theme may have different labels. Enabling a taxonomy and making its
terms selectable are separate steps. Permissions, hidden tags and assignment
restrictions can also affect the picker.

### 1. Import the synthetic report

Import [examples/tagged-event.json](examples/tagged-event.json) through your
training instance's JSON event import, or use its REST client to POST the file to
`/events/add`. The latter **creates data**: select the training instance first.

| Target | Fixture classification |
| --- | --- |
| Event | `tlp:amber` and `admiralty-scale:source-reliability="b"` |
| Domain attribute, `login.example` | `misp:confidence-level="fairly-confident"` |
| IP attribute, `192.0.2.10` | No attribute confidence tag |

The event has **distribution 0 (your organisation only)** and **published false**.
Both observables use reserved training values and have correlation disabled.
Their `to_ids: true` flags are deliberate demonstration inputs; do not deploy
them as detections, enrich their values, publish the event or synchronise it.

The fixture's event UUID is `7fb18198-5f8f-4fc3-8ea7-d2d791c2c0be`. If it already
exists, reuse the exercise event after checking its state, or regenerate the
event and attribute UUIDs and update all search files to match.
Import permissions and instance policies can affect which tags are accepted:
inspect the stored data before continuing.

### 2. Compare event and attribute context

Locate both event tags. Inspect the domain's confidence label and confirm that
the IP has no explicit confidence label. Explain why “Usually reliable” assesses
the source while “Fairly confident” assesses the selected domain. These do not
imply equal or automatically derived scores.

If permitted, add `workflow:todo="review"` **locally** to the domain and inspect
the attachment's local flag. Who can do this depends on the route and role;
the generic `/tags/attachTagToObject` API restricts local tagging to the host
organisation. Omit this step if your user lacks the permission.
Do not test sync by changing a real partner configuration.

### 3. Search for both classifications

Send [examples/search-tags.json](examples/search-tags.json) to
`POST /attributes/restSearch` using your normal REST client.

The request selects the exercise event and an explicit `AND` group containing
`tlp:amber` and `misp:confidence-level="fairly-confident"`. In the reviewed
attribute-search path, each positive tag can match the attribute or its event.

Expected for an unchanged fixture:

- The domain matches: event handling plus its own confidence tag.
- The IP does not match: it has no confidence tag.
- `includeEventTags: true` adds event context to the response; it does not change
  the stored attachment scope.

For a shell client, run from this deck's directory after configuring `MISP_URL`
and `MISP_API_KEY` for the training instance:

```sh
curl --fail --silent --show-error \
  -H "Authorization: $MISP_API_KEY" \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  --data @examples/search-tags.json \
  "${MISP_URL%/}/attributes/restSearch"
```

Use your deployment's trusted CA configuration; keep TLS verification enabled.
Do not put a real key in the deck, fixture, transcript or Git commit.
Check the response body as well as HTTP status. JSON is used here; other
export formats can introduce defaults such as published/IDS filters.

Repeat with an `OR` group and explain why the IP can now match the event's TLP
label. An unprefixed list means OR in the reviewed parser, not AND. Keep this
exercise scoped to its event; event searches and attribute searches have
different result and matching semantics.

### 4. Inspect and then suppress warninglist hits

Use the same endpoint and client with these files:

| Request | Expected for the unchanged fixture and enabled RFC 5735 list |
| --- | --- |
| [search-warnings.json](examples/search-warnings.json) | Return the `ip-dst` training attribute with warning details |
| [search-enforced.json](examples/search-enforced.json) | Omit that matching attribute from the search result |

`192.0.2.10` belongs to `192.0.2.0/24`, which is present in the pinned CIDR list,
and `ip-dst` is an applicable type. More than one enabled list may match.

These requests differ in `includeWarninglistHits` versus `enforceWarninglist`.
Suppression in this attribute-search endpoint does **not** delete stored data.
Do not generalise to ingestion or every export. Check enabled lists, permissions,
filters, pagination and fixture changes if results differ. Reopen the event to
confirm the evidence still exists.

### Debrief

- Which classifications came from the event, and which from the attribute?
- Which mechanism actually controlled access?
- Would an external partner receive a local assessment? What about internal sync?
- Why is a warninglist match insufficient to classify an indicator as harmless?
- What would automation validate before publishing or deploying rules?

## Maintain a taxonomy

The complete teaching definition is
[examples/training-classification/machinetag.json](examples/training-classification/machinetag.json).
It declares an exclusive `review` predicate and two values:

```text
training-classification:review="draft"
training-classification:review="reviewed"
```

This is a schema example, **not a proposed new upstream vocabulary**. Existing
taxonomies such as `workflow` express review tasks. For a real gap, work in a
separate [misp-taxonomies](https://github.com/MISP/misp-taxonomies) checkout:

1. Cite authoritative definitions and agree the namespace and intended scope.
2. Preserve stable machine values; update the version for vocabulary changes.
3. Validate the schema and links from values to declared predicates.
4. Follow the current formatter, manifest-generation and validation workflow.
5. Review licensing, compatibility and examples before making a focused PR.

At the reviewed revision, the workflow includes `jq_all_the_things.sh`,
`validate_all.py`, `tools/gen_manifest.py`, `validate_all.sh` and a PyTaxonomies
local-manifest check. Some scripts rewrite files and expect clean Git state;
read them and current CI instructions before running them.

For **offline validation of the teaching definition only**, use a local checkout
of the reviewed taxonomy repository and an environment with `jsonschema`
installed. From this deck's directory:

```sh
TAXONOMIES_DIR=/path/to/misp-taxonomies
python3 - "$TAXONOMIES_DIR/schema.json" \
  examples/training-classification/machinetag.json <<'PY'
import json
import sys
from jsonschema import validate

with open(sys.argv[1]) as source:
    schema = json.load(source)
with open(sys.argv[2]) as source:
    taxonomy = json.load(source)
validate(instance=taxonomy, schema=schema)
predicates = {item["value"] for item in taxonomy["predicates"]}
assert all(item["predicate"] in predicates for item in taxonomy.get("values", []))
print("Schema and predicate links valid.")
PY
```

Schema validation does not install or enable a taxonomy in MISP or demonstrate
a publishing/sync policy. PyTaxonomies is useful outside MISP; its installation
also does not enable server-side vocabularies.

## Build the slides and presenter notes

Use the [MISP theme setup](../themes/README.md). From the training repository root:

```sh
export TEXINPUTS="$PWD/themes:${TEXINPUTS:-}:"
mkdir -p /tmp/misp-taxonomy-slides
cd 3-misp-taxonomy-tagging

for pass in 1 2 3; do
  pdflatex -interaction=nonstopmode -halt-on-error \
    -output-directory=/tmp/misp-taxonomy-slides slide.tex || exit 1
done
```

Generate the notes handout from this directory:

```sh
awk '/\\begin\{document\}/ {
  print "\\usepackage{pgfpages}"
  print "\\setbeameroption{show notes on second screen=right}"
} {print}' slide.tex > /tmp/misp-taxonomy-slides/slide_handout.tex

for pass in 1 2 3; do
  pdflatex -interaction=nonstopmode -halt-on-error \
    -output-directory=/tmp/misp-taxonomy-slides \
    /tmp/misp-taxonomy-slides/slide_handout.tex || exit 1
done
```

The deck retains the shared **MISP 2.0 identity and 4:3 format** and is already
included in [build.sh](../build.sh). Diagrams and tables replace the former
2.4-era screenshots; historical assets remain available but are not used by
the revised presentation.

## Source audit

Reviewed on **29 October 2026**. Immutable evidence identifies the code and data
consulted; the course does not imply validation on every 2.5 deployment.

| Source | Reviewed revision |
| --- | --- |
| MISP `2.5` branch (`VERSION.json`: 2.5.50) | `fc99c9e3fc85beddc6ef18835359f3c8b7f44608` |
| misp-taxonomies | `3bb56dbbf54131f4305dfff30dc6c00a622a673f` |
| misp-warninglists | `fe7651f9f9723fda977cc90d07a2cdcb535909aa` |

| Claim | Pinned evidence |
| --- | --- |
| Library update and selectable terms | [Taxonomy.php](https://github.com/MISP/MISP/blob/fc99c9e3fc85beddc6ef18835359f3c8b7f44608/app/Model/Taxonomy.php), [TaxonomiesController.php](https://github.com/MISP/MISP/blob/fc99c9e3fc85beddc6ef18835359f3c8b7f44608/app/Controller/TaxonomiesController.php) |
| Required classification and UI publishing scope | [Event.php](https://github.com/MISP/MISP/blob/fc99c9e3fc85beddc6ef18835359f3c8b7f44608/app/Model/Event.php) (`checkIfPublishable`, `checkMissingTaxonomies`), [EventsController.php](https://github.com/MISP/MISP/blob/fc99c9e3fc85beddc6ef18835359f3c8b7f44608/app/Controller/EventsController.php) (`__prepareForPublish`) |
| Attachment permissions and relationships | [TagsController.php](https://github.com/MISP/MISP/blob/fc99c9e3fc85beddc6ef18835359f3c8b7f44608/app/Controller/TagsController.php), [EventTag.php](https://github.com/MISP/MISP/blob/fc99c9e3fc85beddc6ef18835359f3c8b7f44608/app/Model/EventTag.php), [AttributeTag.php](https://github.com/MISP/MISP/blob/fc99c9e3fc85beddc6ef18835359f3c8b7f44608/app/Model/AttributeTag.php) |
| Collections and default event tags | [TagCollection.php](https://github.com/MISP/MISP/blob/fc99c9e3fc85beddc6ef18835359f3c8b7f44608/app/Model/TagCollection.php), [Event.php](https://github.com/MISP/MISP/blob/fc99c9e3fc85beddc6ef18835359f3c8b7f44608/app/Model/Event.php) |
| Boolean groups, context and warning options | [MispAttribute.php](https://github.com/MISP/MISP/blob/fc99c9e3fc85beddc6ef18835359f3c8b7f44608/app/Model/MispAttribute.php) (`dissectArgs`, `set_filter_tags`, `fetchAttributes`, `restSearch`) |
| External/internal sync and exportable tags | [Event.php](https://github.com/MISP/MISP/blob/fc99c9e3fc85beddc6ef18835359f3c8b7f44608/app/Model/Event.php) (`__removeNonExportableTags`), [Server.php](https://github.com/MISP/MISP/blob/fc99c9e3fc85beddc6ef18835359f3c8b7f44608/app/Model/Server.php) |
| Warning matching and suppression | [Warninglist.php](https://github.com/MISP/MISP/blob/fc99c9e3fc85beddc6ef18835359f3c8b7f44608/app/Model/Warninglist.php), [RFC 5735 list](https://github.com/MISP/misp-warninglists/blob/fe7651f9f9723fda977cc90d07a2cdcb535909aa/lists/rfc5735/list.json) |
| Canonical vocabulary and TLP compatibility | [TLP](https://github.com/MISP/misp-taxonomies/blob/3bb56dbbf54131f4305dfff30dc6c00a622a673f/tlp/machinetag.json), [Admiralty Scale](https://github.com/MISP/misp-taxonomies/blob/3bb56dbbf54131f4305dfff30dc6c00a622a673f/admiralty-scale/machinetag.json), [MISP](https://github.com/MISP/misp-taxonomies/blob/3bb56dbbf54131f4305dfff30dc6c00a622a673f/misp/machinetag.json), [Workflow](https://github.com/MISP/misp-taxonomies/blob/3bb56dbbf54131f4305dfff30dc6c00a622a673f/workflow/machinetag.json) |
| Validation, tooling and license | [Schema](https://github.com/MISP/misp-taxonomies/blob/3bb56dbbf54131f4305dfff30dc6c00a622a673f/schema.json), [Validator](https://github.com/MISP/misp-taxonomies/blob/3bb56dbbf54131f4305dfff30dc6c00a622a673f/validate_all.py), [CI workflow](https://github.com/MISP/misp-taxonomies/blob/3bb56dbbf54131f4305dfff30dc6c00a622a673f/.github/workflows/nosetests.yml), [License](https://github.com/MISP/misp-taxonomies/blob/3bb56dbbf54131f4305dfff30dc6c00a622a673f/LICENSE.md) |

## Validation and limits

The five JSON examples pass checks for canonical taxonomy membership, consistent
UUID references and training scope. Real PyMISP loading and serialization preserve
the fixture's tags, scope, values and flags. The teaching definition is validated against
the pinned upstream schema and predicate links; the RFC 5735 demonstration is
checked against the pinned CIDR list. The documentation check covers 195 link/image
targets, Markdown anchors and shell syntax. Slides and notes are built separately.

A live MISP UI, event import, REST query, publishing workflow or synchronisation
partner was **not exercised**. Workshop outcomes are source-checked expectations,
not reported server test results. The full publication bundle and upstream
MISP CI matrix are outside this documentation change.

Continue with [Galaxy](../3.2-misp-galaxy/),
[workflows](../a.12-misp-workflows/) and the
[data model](../a.11-misp-data-model/).
