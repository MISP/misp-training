# MISP objects and templates in 2.5

**Model one observation, preserve its meaning, share a reusable definition.**

Learn when to use an object, how templates describe its attributes, how object
references connect instances, and how to validate and contribute a template.

[Slides](slide.tex) · [PDF](../output/3.3-misp-object-template.pdf) · [Presenter notes](content.tex) · [Offline exercise](examples/build_examples.py) · [Verifier](examples/verify_examples.py) · [Training home](../README.md)

The deck has **30 pages**, including 26 content slides with presenter notes.
Allow 35–45 minutes plus a 25–35 minute workshop. Basic MISP attribute and JSON
knowledge is enough; the offline exercise also uses Python.

Reviewed on **29 October 2026** against:

| Component | Reviewed revision |
| --- | --- |
| MISP 2.5.50 | [fc99c9e3fc85beddc6ef18835359f3c8b7f44608](https://github.com/MISP/MISP/tree/fc99c9e3fc85beddc6ef18835359f3c8b7f44608) |
| misp-objects | [999ec328fcfbdb4a0748a55d5c19691d5cd49899](https://github.com/MISP/misp-objects/tree/999ec328fcfbdb4a0748a55d5c19691d5cd49899) — 454 definitions |
| PyMISP | 2.5.34.4, tested with Python 3.12 |

Counts and UI details are snapshots, not promises about every 2.5 installation.
The [earlier course and original PDF](../archive/slide-decks/3.3-misp-object-template-v1/README.md)
are preserved outside standard training.

## Keep the three concepts separate

| Concept | Example | Identity / purpose |
| --- | --- | --- |
| Attribute | A domain value | A typed observation with its own UUID |
| Object instance | A domain and observed IPs | Groups related attributes; has an instance UUID |
| Object template | `domain-ip` definition | Describes relations, types and constraints; has a template UUID/version |
| Object reference | Review object `related-to` observation object | Directed edge between instance UUIDs |

An object relation such as `ip` names a field **inside** an object.
Its `misp-attribute` type may be `ip-dst`. A relationship such as `related-to`
connects instances; it is not that field name. Shared values/correlation,
template identity and analyst-data relationships are also different mechanisms.

Choose a template around a meaningful entity or observation. Several IPs in one
object should describe the same observation context, not unrelated sightings
that happened to arrive in one batch. Separate observations when their sources,
time windows or meanings differ.

## Reuse before extending

Search `objects/*/definition.json` and inspect the actual definition before
designing a new one. The current repository covers network, file, identity,
financial, vulnerability, detection and threat-hunting use cases.

The live `domain-ip` definition is **version 11**, with `requiredOneOf` containing
`ip`, `domain` and `hostname`. It does **not** require both domain and IP.
The repository README's older illustrative version 8 differs: use the actual
definition and schema as the implementation reference.

Check whether an existing relation already has the meaning you need. Adding a
relation can be appropriate; changing an existing relation's meaning or type can
break consumers and requires a compatibility discussion.

## Read a definition

Definitions live at `objects/<name>/definition.json`. The required top-level
fields are `name`, `uuid`, integer `version`, `description`, `meta-category` and
`attributes`. Select the meta-category and case-sensitive MISP types from
`schema_objects.json`; this snapshot includes `threat-hunting`.

Each relation requires `description`, `misp-attribute` and `ui-priority`:

| Field | Meaning |
| --- | --- |
| `required` | Every named relation must be present |
| `requiredOneOf` | At least one named relation must be present; can coexist with `required` |
| `multiple` | Permit repeated attributes with that relation |
| `categories` | Categories appropriate to the underlying attribute |
| `values_list` | Vocabulary used by the template's selection control |
| `sane_default` | Suggested values; the UI also permits manual entry |
| `to_ids` | Suggested detection flag |
| `disable_correlation` | Suggested correlation behaviour |
| `ui-priority` | Presentation priority; higher-priority fields are ordered first in current object views |
| `recommended` | Optional recommendation metadata; client/UI handling can differ |

The spelling is **`sane_default`**, not `sane_defaults`. Optional icons live at
`objects/<name>/icon/icon.svg`, not inside the definition JSON. The schema rejects
unknown properties. UI priority is implemented in current MISP; it is not an
access rule, confidence score or substitute for `required`.

## Validate the right layer

1. **Definition syntax/schema:** JSON structure, recognised fields, types and categories.
2. **Definition semantics:** valid UUID, unique template identity, requirement names
   that exist, meaningful relations and compatible changes.
3. **Instance conformity:** required relations and repetition rules against the
   selected definition.
4. **Attribute validity and policy:** valid values, detection/correlation choices,
   distribution, permissions and intended sharing.

The JSON schema alone does not validate all semantics. PyMISP `strict=True` checks
template-aware construction and required/repeated relations on strict
serialisation. It is **not** a universal validator for vocabulary membership or
every downstream policy. Validate those explicitly where your workflow needs it.

MISP's template-backed object-add path performs attribute validation and
`checkTemplateConformity`. Direct event/object capture, editing and synchronisation
have different paths. Avoid the old lesson's blanket claim that every template
rule is enforced on every API import. Inspect the selected path and test it.

Unknown-template objects can retain their attributes and metadata for exchange.
Normal UI editing needs a suitable template; the reviewed controller also offers
a force-update/recovery path. Resolve the intended template and review unmatched
fields rather than treating that recovery action as an automatic safe migration.

## Workshop: build and inspect offline

The exercise makes no network calls and needs no API key. It loads the current
official `domain-ip` definition from a supplied checkout and a teaching-only
[training-review definition](examples/training-review.json). The latter demonstrates
both requirement mechanisms, repetition and a vocabulary; it is not a proposed
replacement for existing review/annotation models.

From this course directory:

```sh
git clone https://github.com/MISP/misp-objects.git /tmp/misp-objects-lab
git -C /tmp/misp-objects-lab checkout 999ec328fcfbdb4a0748a55d5c19691d5cd49899
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r examples/requirements.txt
python examples/verify_examples.py /tmp/misp-objects-lab
python examples/build_examples.py /tmp/misp-objects-lab > training-event.json
```

Inspect the resulting bare event JSON:

- Two object instances have fresh UUIDs; their template UUIDs identify definitions.
- The domain/IP observation has one domain and two IP attributes.
- The review refers to the observation's **instance UUID** through `related-to`.
- The event is unpublished and organisation-only; attributes explicitly use
  `to_ids=False`. Reserved `.example` and documentation IPs keep data synthetic.
- Every object is strictly validated before event serialisation.

Try removing the case reference, removing both locator alternatives, duplicating
the non-repeatable case reference and introducing an unknown relation. The
verifier exercises those failures plus a schema-invalid property spelling.
It also checks identity, repetition, references, flag choices and JSON round-trip.

The explicit definition argument avoids silently selecting a different
template revision bundled with PyMISP. Keep the template revision visible in
reproducible integrations. Requirements/defaults in client libraries need not
match a separately updated server.

## Optional MISP lab

Use a disposable MISP 2.5 instance and a writer account authorised for its event.
Have the operator make the selected template definitions available in the
instance's template directory and update the database template catalogue.
Changing the Git files and updating the catalogue are separate operations.
Keep local training definitions out of an unattended upstream update path.

1. Open an unpublished organisation-only event and add a `domain-ip` object.
2. Inspect required alternatives, additional fields and repeated IP rows.
3. Save, inspect attributes and detection flags, and view the object card.
4. Add the teaching review only if its definition has been installed.
5. Link review to observation, checking direction and target instance UUID.
6. Export/read back the event and compare template UUID/version and references.
7. Test missing requirements and repeated unique relations through your actual
   UI/API path; inspect the returned validation error rather than assuming success.
8. Remove the disposable event and local teaching template according to lab policy.

The reviewed API supports `/objects/add/{eventId}/{templateUuid}/{version}` and
`/objects/restSearch`. Obtain real identifiers from the lab, retain normal TLS,
authentication and permissions, and inspect the deployed API contract.
For full request/authentication practice use the
[REST API course](../a.7-rest-API/README.md).

This update validates the exercise **offline** and audits MISP source. It does
not claim a new live-server or screenshot validation of these steps.

## Update and contribute

For an existing template, retain its UUID and increment the version when changing
the definition. A new template needs a new UUID and an initial version. Existing
objects retain their recorded revision; installing a newer template does not
silently rewrite all object instances. Review the upgrade form's transferable
and unmatched attributes, preserve data and re-check references.

MISP reads definitions from `app/files/misp-objects/objects`. Use the instance's
template-update control with appropriate operator permissions. The reviewed CLI
also has `Admin updateObjectTemplates <userId>`; it updates the database from disk,
not the Git checkout. Review imported changes before using force-update options.

For a contribution to **misp-objects**:

1. Explain the use case, alternatives considered and why existing templates are insufficient.
2. Add/edit `objects/<name>/definition.json` with meaningful descriptions and
   appropriate detection/correlation defaults. Use a fresh UUID only for a new model.
3. Check `schema_objects.json`, requirements, repetition and sample instances.
4. Install `jq`, `moreutils` (`sponge`), `uuidparse` and Python `jsonschema`.
5. Run `./jq_all_the_things.sh`; review its repository-wide formatting changes.
   Commit the intended normalised JSON with no executable bit.
6. Run `./validate_all.sh` from a clean checkout. It checks formatting cleanliness,
   schemas, relationship opposites/tests and UUID uniqueness.
7. Follow the repository's current documentation/icon guidance and open a focused
   PR with a synthetic example, negative cases and compatibility notes.

An inverse relationship must have a coherent definition and valid opposite;
an edge does not automatically create its inverse. Reuse the relationship
catalogue and do not infer causality from a generic `related-to` link.

## Build and evidence

Use the [theme setup](../themes/README.md). From the repository root:

```sh
export TEXINPUTS="$PWD/themes:${TEXINPUTS:-}:"
mkdir -p /tmp/misp-object-slides
cd 3.3-misp-object-template
for pass in 1 2 3; do
  pdflatex -interaction=nonstopmode -halt-on-error \
    -output-directory=/tmp/misp-object-slides slide.tex || exit 1
done
```

The standard build includes this course and generates presenter notes.
Validated: both supplied definitions against the current schema, all **454**
official definitions against that schema, the offline event builder and its
negative/round-trip checks. These checks do not replace the upstream full CI suite.

Pinned implementation references:

- [Definition schema](https://github.com/MISP/misp-objects/blob/999ec328fcfbdb4a0748a55d5c19691d5cd49899/schema_objects.json), [domain-ip v11](https://github.com/MISP/misp-objects/blob/999ec328fcfbdb4a0748a55d5c19691d5cd49899/objects/domain-ip/definition.json), [relationships](https://github.com/MISP/misp-objects/blob/999ec328fcfbdb4a0748a55d5c19691d5cd49899/relationships/definition.json) and [upstream validation](https://github.com/MISP/misp-objects/blob/999ec328fcfbdb4a0748a55d5c19691d5cd49899/validate_all.sh).
- [Template conformity/update model](https://github.com/MISP/MISP/blob/fc99c9e3fc85beddc6ef18835359f3c8b7f44608/app/Model/ObjectTemplate.php), [object model and field ordering](https://github.com/MISP/MISP/blob/fc99c9e3fc85beddc6ef18835359f3c8b7f44608/app/Model/MispObject.php), [object controller](https://github.com/MISP/MISP/blob/fc99c9e3fc85beddc6ef18835359f3c8b7f44608/app/Controller/ObjectsController.php) and [UI value controls](https://github.com/MISP/MISP/blob/fc99c9e3fc85beddc6ef18835359f3c8b7f44608/app/View/Elements/Objects/object_value_field.ctp).
