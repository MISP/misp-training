# PyMISP with MISP 2.5

**Build models offline, query the right context, verify deliberate server changes.**

[Slides](slide.tex) · [PDF](../output/a.2-pymisp.pdf) · [Presenter notes](content.tex) · [Notebook](PyMISP-workshop.ipynb) · [Executable examples](examples/) · [REST API course](../a.7-rest-API/README.md) · [Object-template course](../3.3-misp-object-template/README.md) · [Training home](../README.md)

The deck has **33 pages**: a title, 29 content slides with presenter notes and
three section pages. Allow 40–50 minutes for the slides and 30–40 minutes for
the workshop. Basic Python and MISP event/attribute knowledge are sufficient.
The default notebook and model exercise need no MISP account or network access
after dependencies are installed. Live reads need an API-enabled training
account; the separate write exercise needs a permitted writer on a disposable
instance.

## Reviewed versions

Checked on **2 November 2026**:

| Component | Reviewed reference |
| --- | --- |
| MISP | **2.5.50**, [`fc99c9e3fc85beddc6ef18835359f3c8b7f44608`](https://github.com/MISP/MISP/tree/fc99c9e3fc85beddc6ef18835359f3c8b7f44608) |
| PyMISP | **2.5.34.4**, latest published release on both [PyPI](https://pypi.org/project/pymisp/2.5.34.4/) and [GitHub](https://github.com/MISP/PyMISP/releases/tag/v2.5.34.4) at review time |
| PyMISP source | [`45c906070c287dffeed353069cb3daddceab2ea3`](https://github.com/MISP/PyMISP/tree/45c906070c287dffeed353069cb3daddceab2ea3) |
| Python | Package requires **`>=3.10,<4.0`**; examples checked with **3.12.14** |

The client and server have independent version numbers. Inspect
`misp.misp_instance_version` and its `pymisp_recommended_version` field; a current
client does not establish that an older server supports every method. The
instance's `/api/openapi` and `/api/rest` describe its deployed API. Use
`PyMISP` for new integrations; `ExpandedPyMISP` is a compatibility class in this
release.

## Install and start offline

From this course directory:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r examples/requirements.txt
python -m unittest examples.test_examples -v
python -m examples.models
```

The requirement pins `pymisp==2.5.34.4`. It is a course-version pin rather than
a complete transitive lockfile. To assess a newer release later, use
`python -m pip install --upgrade pymisp` in a separate environment, review its
Python requirements and rerun the checks before changing the course pin.
Do not use an unpinned Git main install as the reproducible classroom baseline.

`examples/models.py` builds an unpublished, organisation-only `MISPEvent`, a
contextual domain attribute, a template-backed `domain-ip` object and an object
reference to the attribute. Each run uses unique `.example` names and the
documentation address `192.0.2.10`; every attribute has `to_ids=False`.
Local construction, `to_json()` and `load()` do not contact MISP or save data.

```python
from pymisp import MISPEvent
from examples.models import build_event

draft = build_event()
encoded = draft.to_json(indent=2)  # JSON string; do not JSON-encode it again.
restored = MISPEvent()
restored.load(encoded)
assert restored.uuid == draft.uuid
assert restored.objects[0].references[0].referenced_uuid == draft.attributes[0].uuid
```

`strict=True` and `obj.to_json(strict=True)` check local object-template
requirements. The wheel's bundled template revision can differ from the server
catalogue. Neither a local round-trip nor a template check proves server
acceptance, access rights or the truth of an analytical relationship.
See the object-template course for template identity and required fields.
Binary/file-analysis helpers need optional dependencies such as
`pymisp[fileobjects]`; this workshop does not install or execute them.

## Connect to a training instance

Set `MISP_URL` and `MISP_API_KEY` through your local environment/secret mechanism
before starting Python or Jupyter. Keep keys outside committed code, notebooks,
outputs and shell history. Obtain a permitted key from your own instance's
profile/auth-key controls. The account needs API access and the relevant role
permissions; advanced keys may add expiration, IP and read-only restrictions.

Use trusted HTTPS. For a private CA, set `REQUESTS_CA_BUNDLE` to an appropriate
CA bundle. The helper passes that path to `ssl`; otherwise it passes `True`.
It permits HTTP only for a disposable loopback lab. It normalises the base URL
to end in `/`, preserving any deployment subdirectory: this released client's
`search` uses `urljoin`.

```python
from examples.common import Config, connect

config = Config.from_env()
misp = connect(config)  # PyMISP(..., ssl=config.verify, timeout=(5, 60))
server = misp.misp_instance_version
print(server["version"], server.get("pymisp_recommended_version"))
```

The constructor makes server requests for versions, user/role/settings and
attribute types. Do not instantiate it in an offline cell. The timeout tuple
bounds connection and socket-read waits, not the duration of an entire workflow.
Normal Requests proxy handling is retained. Authentication uses the **raw key**
in `Authorization`, without a `Bearer` prefix.

A read-only key can **POST a search**; read-only is an operation restriction,
not a ban on the POST verb. A permitted writer still cannot edit arbitrary
organisations' records. A tag is not an access-control grant, and a site-admin's
view is not evidence of ordinary-user visibility.

## Map PyMISP to the REST API

| Python operation | Ordinary REST request in these examples |
| --- | --- |
| `misp.misp_instance_version` | `GET /servers/getVersion` |
| `misp.search_index(...)` | `POST /events/index` |
| `misp.search(controller="events", ...)` | `POST /events/restSearch` |
| `misp.search(controller="attributes", ...)` | `POST /attributes/restSearch` |
| `misp.get_event(uuid, pythonify=True)` | `GET /events/view/{uuid}` |
| `misp.add_event(event, pythonify=True)` | `POST /events/add` |
| `misp.update_attribute(attribute, pythonify=True)` | `POST /attributes/edit/{uuid}` |
| `misp.tag(uuid, tag, local=True)` | `POST /tags/attachTagToObject` |
| `misp.add_sighting(sighting, attribute_uuid, ...)` | `POST /sightings/add/{uuid}` |
| `misp.delete_event(uuid)` | `POST /events/delete/{uuid}` |

Some options change the request shape: for example, `get_event` can use POST
when including certain options. The generic `search` method in this release
accepts `events`, `attributes` and `objects`; other endpoint families have
dedicated methods.

| REST search field | Preferred PyMISP keyword |
| --- | --- |
| `type` | `type_attribute` |
| `returnFormat` | `return_format` |
| `includeEventUuid` | `include_event_uuid` |
| `includeEventTags` | `include_event_tags` |
| `enforceWarninglist` | `enforce_warninglist` |
| `from` / `to` | `date_from` / `date_to` |

The wrapper forwards additional keyword arguments, so a misspelling does not
necessarily fail locally. Check the emitted query and server-supported filters.

## Read one page, then choose a completion policy

```python
from examples.read import one_page

rows = one_page(misp, limit=10, page=1)
for attribute in rows:
    print(attribute.uuid, attribute.type)
```

This uses attribute scope, ordinary JSON, `type_attribute="domain"`,
`value="%.example"`, parent event UUID/tag context and `Attribute.id ASC`.
The helper checks that the result is a list of `MISPAttribute` objects with
valid UUIDs. An empty list is a valid result. An API error dictionary or proposal
is not a successful typed attribute response.

For ordinary JSON in the reviewed source, omitting `published` and `to_ids`
includes both states. Use numeric `0` or `1` to restrict these search flags;
do not assume `False` is interpreted consistently across endpoints.
**PyMISP 2.5.34.4 rejects `to_ids=[0,1]`**, despite the raw endpoint supporting
that array. Omit it for both states in this query.

Choose event scope for matching full events, or `search_index` for index
summaries. A full matching event can contain attributes beyond the type/value
that selected the event. Attribute scope returns the matching rows, including
attributes inside objects. `metadata=True` omits event attributes/proposals;
it does not mean a full event had no attributes.

| Interface | Attribute-search result |
| --- | --- |
| Raw HTTP JSON | `{"response":{"Attribute":[...]}}` |
| PyMISP with `pythonify=False` | Normalised `{"Attribute":[...]}` |
| PyMISP with `pythonify=True` | List of `MISPAttribute` objects |

The notebook compares raw and typed UUID sets for the same bounded query.
Do not run the raw-envelope parser on pythonified output.

```sh
python -m examples.read --limit 10
python -m examples.read --event-uuid "$MISP_EVENT_UUID" --all-pages --max-pages 20
```

`collect_pages` is limited to the fixed ordinary JSON/SQL-filtered query. It
starts at page 1, continues through short role-capped pages until an empty page,
and fails on repeated UUIDs or the maximum-page bound. It accumulates this small
workshop result in memory and saves no checkpoint. It is not a generic exporter
or sync client. Stable order reduces drift without freezing concurrent edits.
Warninglist/decay post-filtering can create empty output pages before later
matches; do not add those filters to this loop unchanged.

For detection exports, define publication, `to_ids`, handling-tag and warninglist
policy explicitly. Changing only `return_format` can change selected records;
text-like detection formats have restrictive defaults. Use `pythonify=False`
with text output and handle the returned string. Inherited event tags are
context, not proof of a direct attribute attachment. See the REST API course for
format defaults, inclusive timestamp windows, overlap/checkpoint policy and
reconciliation of deletions, access loss and event-only context changes.

## Notebook workshop

```sh
python -m pip install -r examples/notebook-requirements.txt
python -m ipykernel install --user --name misp-pymisp-training
jupyter lab PyMISP-workshop.ipynb
```

Select the installed training kernel. The committed notebook has no saved
outputs or execution counts. **Run all** executes only local model exercises
unless you set `MISP_LIVE=1` before launching the kernel. Live read cells compare
raw and typed pages and traverse the fixed query. Set `MISP_EVENT_UUID` to a
known visible training fixture for a stable comparison; otherwise they query
visible `.example` domains. Concurrent edits can change the two result sets.

The write cell is separate: it additionally requires `MISP_LAB_WRITE=1`.
Review the code before enabling either flag. Clear outputs before sharing;
avoid printing clients, keys, full responses or private incident data.

### Adapted notebook examples and provenance

| Source | Examples adapted here |
| --- | --- |
| [PyMISP FullOverview](https://github.com/MISP/PyMISP/blob/45c906070c287dffeed353069cb3daddceab2ea3/docs/tutorial/FullOverview.ipynb), zero-based cells 4, 10, 27–31 and 61–63 | Offline event/attribute construction, domain-ip objects, references, JSON and local edits |
| [PyMISP Search-FullOverview](https://github.com/MISP/PyMISP/blob/45c906070c287dffeed353069cb3daddceab2ea3/docs/tutorial/Search-FullOverview.ipynb), cells 41, 44–49 and 51–54 | Attribute scope, typed results, change/publication clocks, bounded searches and export formats |
| [Archived Introduction_to_PyMISP](../archive/slide-decks/a.7-rest-API-v1/Introduction_to_PyMISP.ipynb), cells 1, 7–9, 47–65 and 76–80 | The build → persist → refetch → update teaching sequence |
| [Current REST API workshop](../a.7-rest-API/REST-API-workshop.ipynb) | Raw-envelope comparison and current selection/completion semantics |

Credit: the MISP/PyMISP tutorial contributors; see the pinned repository and
its [license](https://github.com/MISP/PyMISP/blob/45c906070c287dffeed353069cb3daddceab2ea3/LICENSE).
These are adapted examples rather than blanket endorsement of every old cell.
The update replaces stale installation instructions, real malware/sample paths,
old tags, implicit publication and ambiguous search flags with the current,
synthetic workflow above. Upstream notebooks remain useful references but need
the same version/permission checks as other integration code.

## Optional live write workshop

Use a disposable MISP 2.5.50 lab. The operator must make the `domain-ip` template
and `tlp:clear` tag available. The learner needs permission to create, modify,
tag, sight and delete its own event; no site-admin role is required.

```sh
python -m examples.workshop --run
```

Read [workshop.py](examples/workshop.py) first. It creates a unique, unpublished,
organisation-only event with one top-level domain attribute, a domain-ip object
and an object-to-attribute reference. It updates the domain comment, attaches
an event tag and a direct **local** attribute tag, submits a **synthetic type-0
sighting**, refetches saved state and searches only that event's UUID.
Its `finally` block deletes only the confirmed fixture it created and checks
that the event is absent. It never publishes or accepts an arbitrary UUID to
delete. The final summary contains a UUID/counts, not incident values.

Local `event.add_attribute`, `event.add_object` and `attribute.add_tag` only edit
models. Remote `misp.add_attribute`, `misp.add_object` and `misp.tag` call MISP.
An object attribute's first argument is its **object relation**, not an
arbitrary MISP type. Object references, Galaxy attachments and correlations
are separate mechanisms.

Single-attribute add/update/delete can fall back to proposals on specific
permission failures in this client release. A `MISPShadowAttribute` is not a
saved modification to the original attribute. Bulk-add responses have their own
`attributes`/`errors` shape and need per-item checks. The workshop requires the
expected model and refetches the persisted result.

If creation times out, inspect the intended draft UUID before retrying: a write
may already have persisted. If cleanup cannot be confirmed, inspect the lab
before rerunning. Do not use these examples as automatic production retry,
publication or synchronisation logic. PyMISP logging can contain server bodies
and private data, especially with DEBUG enabled; keep diagnostics local and
review them before sharing. The sample CLI gives concise failure messages but
does not promise to sanitise every library log.

## Build, audit and validation

Use the [shared theme setup](../themes/README.md). From the repository root:

```sh
export TEXINPUTS="$PWD/themes:${TEXINPUTS:-}:"
mkdir -p /tmp/pymisp-slides
cd a.2-pymisp
for pass in 1 2 3; do
  pdflatex -interaction=nonstopmode -halt-on-error \
    -output-directory=/tmp/pymisp-slides slide.tex || exit 1
done
```

The standard build also generates the presenter-notes handout. The earlier
[source, notes, images and original PDF](../archive/slide-decks/a.2-pymisp-v1/README.md)
remain archived outside the standard build.

Implementation evidence:

- Released [PyMISP API](https://github.com/MISP/PyMISP/blob/45c906070c287dffeed353069cb3daddceab2ea3/pymisp/api.py), [models](https://github.com/MISP/PyMISP/blob/45c906070c287dffeed353069cb3daddceab2ea3/pymisp/mispevent.py), [serialisation](https://github.com/MISP/PyMISP/blob/45c906070c287dffeed353069cb3daddceab2ea3/pymisp/abstract.py) and [package/Python requirements](https://github.com/MISP/PyMISP/blob/45c906070c287dffeed353069cb3daddceab2ea3/pyproject.toml).
- MISP 2.5.50 [event controller](https://github.com/MISP/MISP/blob/fc99c9e3fc85beddc6ef18835359f3c8b7f44608/app/Controller/EventsController.php), [attribute controller](https://github.com/MISP/MISP/blob/fc99c9e3fc85beddc6ef18835359f3c8b7f44608/app/Controller/AttributesController.php), [attribute search model](https://github.com/MISP/MISP/blob/fc99c9e3fc85beddc6ef18835359f3c8b7f44608/app/Model/MispAttribute.php) and [auth-key controller](https://github.com/MISP/MISP/blob/fc99c9e3fc85beddc6ef18835359f3c8b7f44608/app/Controller/AuthKeysController.php).

Validation on 2 November 2026:

- **Eight offline tests passed**: released-client parameter/response behaviour,
  model/reference round-trips, strict domain-ip template requirements,
  typed-error/proposal rejection, configuration checks, short-page traversal,
  repeated-page detection and maximum-page failure.
- **All 17 notebook cells executed** in offline mode, live writer mode with the
  disposable write cell enabled, and read-only mode with writes disabled.
  Raw and typed attribute UUID sets matched for the same stable fixture/page.
  Executed outputs remain outside the repository; the committed notebook is clean.
- **Live MISP 2.5.50 checks passed with ordinary users**: create/refetch/update,
  event tagging, direct local attribute tagging, synthetic type-0 sighting,
  exact object-reference target, two domain rows including an object attribute,
  and confirmed event cleanup. A read-only key could POST `restSearch` and
  received HTTP 403 on event creation. Another organisation's user saw no
  matching rows and HTTP 404 when fetching the private fixture.
- A live `restsearch_limit_result=1` role cap returned **one** row despite
  `limit=100`; the bounded loop continued to retrieve **both** domain rows.
- Standard and double-width presenter-notes PDFs were built in **three passes**,
  33 pages each, with rendered-page inspection. Local links, notebook structure,
  whitespace and the six original archived notes/assets/PDF byte comparisons
  passed. The archived lesson body was checked for preservation apart from whitespace.

The disposable lab used the official backend image
`ghcr.io/misp/misp-docker/misp-core:v2.5.50` at
`sha256:1bf559bf280021da2adead9e715a8c84786e378b107e34e8b834d518596fcab7`
and frontend image `ghcr.io/misp/misp-docker/misp-nginx:v2.5.50` at
`sha256:0ddc6730db7433220b821d6aa640cb3205ec59166364daf50272090bf4d066cd`.
It was bound to loopback HTTP; this was not a live private-CA/TLS deployment
test. PyMISP 2.5.34.4 with Requests 2.34.2 ran on Python 3.12.14. These checks
do not claim the full upstream PyMISP CI suite, production synchronisation,
external enrichments, binary analysis or every 2.5 patch/role combination.
