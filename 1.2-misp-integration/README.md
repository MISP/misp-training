# Integrating MISP

**Follow a finding from ingestion to operational use, then close the feedback loop.**

This 37-slide course is for analysts, SOC engineers and operators with basic
MISP knowledge. Allow about 60 minutes for discussion and 20 minutes for the
exercises. Presenter notes explain contracts, configuration dependencies,
failure modes and expected exercise outcomes.

[Slide source](slide.tex) · [Presenter notes](content.tex) · [Offline lab](#offline-lab-no-services-required) · [Optional service lab](#optional-service-lab) · [Source audit](#source-audit)

## What changed and why

Reviewed on **4 November 2026**. The original course's ingestion, SIEM and
feedback use cases remain, with a fuller explanation of how integration works.

| Review finding | Revision |
| --- | --- |
| Static integration overview without editable sources | Six TikZ diagrams show interfaces, context, module requests, workflows, delivery and reconciliation. |
| Little coverage of modules, workflows and authenticated API clients | Add worked requests, family/trigger selection, execution context and service boundaries. |
| Fixed attribute-count sizing advice | Use measured workload, worker backlog, latency, retention and recovery requirements. |
| Historical OpenDXL and standalone-dashboard examples presented as new | Focus on maintained integration mechanisms; name Zeek rather than Bro and direct product-specific work to its connector contract. |
| Blanket statements about format limitations | Review STIX/TAXII versions, mappings, extensions and actual consumer support. |
| Export success could be mistaken for operational deployment | Separate selection, artefact generation, publication, reload and activation checks. |
| Feedback described without complete update/removal handling | Explain sightings and add a runnable, offline consumer-state planning exercise. |
| Unattributed or outdated interface illustrations | Reuse two existing, documented captures and identify which application each shows. |

The course keeps the shared MISP theme, original 4:3 format, author attribution
and `slide.tex` / `content.tex` publication entry points. Historical images
remain in this directory but are not presented as current screenshots.

## Reading the diagrams

The six editable [TikZ sources](diagrams/) are input directly by the slides.
Solid arrows describe a request or process path; dashed arrows describe a
return or reconciliation path. The overview's double arrow represents the
module request/result exchange. Arrows do not guarantee installation,
delivery, replay, access enforcement or an automatic write to MISP.

| Diagram | Question it answers |
| --- | --- |
| [integration-map](diagrams/integration-map.tikz) | Where do feeds, modules, workflows and consumers fit? |
| [data-contract](diagrams/data-contract.tikz) | Which context and identifiers should survive conversion? |
| [module-roundtrip](diagrams/module-roundtrip.tikz) | What leaves the client, and when are results actually saved? |
| [workflow-guard](diagrams/workflow-guard.tikz) | How can a blocking publication check allow or stop the original operation? |
| [delivery-loop](diagrams/delivery-loop.tikz) | How do notifications, authorised API retrieval and periodic repair complement each other? |
| [snapshot-plan](diagrams/snapshot-plan.tikz) | How do additions, corrections and removals reach a consumer? |

## Offline lab: no services required

Python 3.10+ and its standard library are sufficient. From this course directory:

```sh
python3 examples/check_lab.py -v
python3 examples/plan_snapshot.py examples/current-state.json examples/desired-state.json
```

Expected: **six checks pass**. The plan adds `new.example`, removes
`old.example` and retains `keep.example`. It does not call MISP, modify a
manifest or configure a tool.

These are **consumer manifests**, not native MISP API responses. Each has a
`complete` assertion, a versioned selection `policy` and an `indicators` array.
Each indicator retains its attribute UUID, event UUID, type and value. A
production exporter must separately establish completeness and apply its
selection policy; setting `complete=true` is not proof that an API run succeeded.

The checks also demonstrate that:

- A corrected value under the same UUID becomes an update.
- An incomplete empty export produces an error, not a plan to remove everything.
- Policy changes, duplicate UUIDs and malformed identities require review.

Only compare a verified current state with a complete desired snapshot under
the same policy. A missing UUID means removal from this **consumer's selected
set**, not deletion of the MISP record. A real connector must also handle
consumer-side value deduplication, atomic application, acknowledgement,
recovery and access/selection changes. The sample deliberately prints plans only.

## Optional service lab

Use synthetic data in a disposable MISP instance. Keep production sync,
external lookups, callbacks and action consumers disabled. Use three
organisations when testing visibility: author, included recipient and excluded
recipient, with non-administrator test accounts. This lab is separate from the
offline checks and requires the relevant MISP roles and services.
A facilitator with site-admin access configures the workflow; ordinary test
users exercise its effects. Check the deployed feature status and support:
the current MISP Book describes workflows as experimental.

### 1. Preview an authenticated API query

Set `MISP_URL` to your trusted lab base URL and provide `MISP_API_KEY` through
your secret-management mechanism. For private certificates configure a trusted
CA bundle, not `curl -k`. Run from this directory:

```sh
curl --fail-with-body --silent --show-error --connect-timeout 5 --max-time 60 \
  -H "Authorization: $MISP_API_KEY" \
  -H 'Accept: application/json' -H 'Content-Type: application/json' \
  --data-binary @examples/attribute-search.json \
  "$MISP_URL/attributes/restSearch"
```

This requests **one page** of published, IDS-marked domain attributes in the
reserved `.example` namespace, with warninglist enforcement. Empty results are
normal when no matching lab records exist or warninglists exclude them.
Inspect `response.Attribute`, UUIDs and event context. A result is not a
complete production export.

Role caps, concurrent changes and post-query filtering complicate pagination;
in particular, a filtered empty output page need not mean there are no later
candidates. Choose and verify the endpoint-specific completion strategy. Use
overlapping incremental windows plus periodic reconciliation to cover parent
metadata, permission changes and removals. Advance state only after successful
retrieval **and** consumer application.

For a runnable bounded JSON client and authenticated PyMISP setup, continue with
the [API course](../a.7-rest-API/README.md), its
[raw client](../a.7-rest-API/examples/search_attributes.py),
[PyMISP example](../a.7-rest-API/examples/pymisp_search.py) or the
[PyMISP course](../a.2-pymisp/README.md). The API course's bounded client
deliberately excludes post-query filters from its supported query set; do not
pass this course's `enforceWarninglist` example unchanged into that iterator.

### 2. Query a local module service

Install and start an isolated service using the [modules course](../3.1-misp-modules/README.md).
Check the deployed version, discovery and module-specific requirements. The
reviewed parser request uses no external provider credentials:

```sh
curl --fail --silent --show-error http://127.0.0.1:6666/modules
curl --fail-with-body --silent --show-error --connect-timeout 5 --max-time 30 \
  -H 'Content-Type: application/json' \
  --data-binary @examples/module-query.json \
  http://127.0.0.1:6666/query
```

`extract_url_components` parses the fictional URL locally. Do not browse it.
Inspect `results.Object` and its `generated-from` reference to the input UUID.
The request does not save anything to MISP. Check module `error` / `errors`
envelopes even when HTTP status is 200.

The module API is a separate service, not MISP's authenticated REST API.
The reviewed routes do not inherit a MISP user's ACL. Keep access controlled;
configure the service URL as reachable from the actual MISP web and worker
environments. Set family enablement, module enablement, provider settings and
timeouts as appropriate; a successful healthcheck does not prove provider access.

The [osquery dry-run request](examples/osquery-dry-run.json) can be sent to the
same `/query` endpoint when `osquery_pack_publish` is loaded. Expected status:
`planned`, with a pack and provenance. Keep `dry_run=true`. This does not
publish files, distribute configuration, execute queries or activate an endpoint.
Use the pinned action documentation below for its actual publication contract.

### 3. Build a small workflow gate

Use the installed workflow editor and the [workflow course](../a.12-misp-workflows/).
The diagram is a design exercise, not an importable blueprint.

1. Check `Plugin.Workflow_enable`, required background-job settings and healthy workers.
2. Attach a lab workflow to the blocking `event-publish` trigger.
3. Use a tag condition as the lab readiness check; route the failing branch to
   **Stop execution**. With the readiness tag absent, publication should stop
   and the reason should appear in workflow diagnostics.
4. Add the tag and retry. The pass branch should allow publication in the
   isolated lab. Verify the actual event state and both recipients' visibility.

The readiness tag is a lab convention, not a disclosure permission. Workflows
use a privileged execution identity; minimise outgoing payloads explicitly.
For MISP-driven enrichment guards, inspect `enrichment-before-query`. Direct
module API callers do not pass through that MISP hook.

If extending the exercise with a webhook, review destination restrictions,
`Security.workflow_enable_arbitrary_urls`, authentication, TLS and payloads.
An empty built-in webhook payload uses the full roaming data. Prefer a minimal
reference plus authorised receiver retrieval when suitable. A pre-publication
side effect is not rolled back if a later workflow step fails.

### 4. Return feedback deliberately

The [sighting fixture](examples/sighting.json) is a fictional type-0 observation
at `2026-11-04T12:00:00Z`. For a deliberate lab write, set `ATTRIBUTE_UUID` to a
real **lab** attribute UUID, review the fixture and use an account allowed to add
sightings:

```sh
: "${ATTRIBUTE_UUID:?Set the intended lab attribute UUID}"
curl --fail-with-body --silent --show-error --connect-timeout 5 --max-time 60 \
  -H "Authorization: $MISP_API_KEY" \
  -H 'Accept: application/json' -H 'Content-Type: application/json' \
  --data-binary @examples/sighting.json \
  "$MISP_URL/sightings/add/$ATTRIBUTE_UUID"
```

In real use, supply the actual observation time and source. Types 0, 1 and 2
mean observation, false positive and expiration. Review sighting visibility
and avoid duplicate submission on retries. Feedback does not automatically
remove an exported rule: verify the correction and the next consumer update.

## Build slides, notes and standalone diagrams

Use the [shared theme dependencies](../themes/README.md). From the repository root:

```sh
make -C 1.2-misp-integration slides notes diagrams
```

Outputs are `/tmp/misp-integration/slides/slide.pdf`,
`/tmp/misp-integration/notes/slide_handout.pdf` and six vector PDFs under
`/tmp/misp-integration/diagrams/`. `make pdf` is an alias for `make slides`.
The refreshed Makefile uses three pdfLaTeX passes for slides and notes, the
bundled theme and generated entry points outside the source directory. For
another destination set `BUILD_DIR` to an **absolute path**. No shell escape or
network lookup is needed to compile. `make check-lab` runs the offline exercise.

The root [publication script](../build.sh) can still build this deck and its
notes through the existing entry point. The standard Beamer/`pgfpages` notes
layout can emit duplicate PDF destination warnings for repeated thumbnails;
inspect actual notes content and links separately.

## Screenshot provenance

Both screenshots are reused unchanged from existing courses in this repository.
They are illustrations, not evidence that this refresh exercised a live service.
Open the source images for readable full-resolution views.

| Image | What it actually shows |
| --- | --- |
| [MISP REST client](../a.7-rest-API/images/rest-client.png) | Genuine isolated MISP 2.5.50 capture, 29 October 2026, with a placeholder key and an unsubmitted request. [Full provenance](../a.7-rest-API/images/README.md). |
| [Module results](../3.1-misp-modules/screenshots/current/results.png) | The separate misp-modules website, using upstream browser-fixture results. It is not the MISP event view. [Attribution and original snapshot](../3.1-misp-modules/README.md#screenshot-attribution). |

The module website capture comes from `website/doc/object_result_cards.png`
at misp-modules revision `3a903305cf374ff7cc5ca0290857c54382c1f933`.
Credit: MISP Project / CIRCL and the respective contributors. Retain the
repository's AGPL-3.0-or-later / CC-BY-SA-4.0 notices and upstream asset attribution.

## Source audit

The reference snapshot was checked against:

- [MISP `2.5`, `04fc5f8b7ccb52bb6614ca3e9ccdbfdf6585d985`](https://github.com/MISP/MISP/tree/04fc5f8b7ccb52bb6614ca3e9ccdbfdf6585d985).
- [misp-modules `main`, `a123fc2ee99fd30b37d0879a1e576b684a826829`](https://github.com/MISP/misp-modules/tree/a123fc2ee99fd30b37d0879a1e576b684a826829).
- [PyMISP `main`, `9bb7d6b5b9683885536e5b42f70a4cb3eefe2728`](https://github.com/MISP/PyMISP/tree/9bb7d6b5b9683885536e5b42f70a4cb3eefe2728).

| Contract | Implementation evidence |
| --- | --- |
| Search parameter names and export selection | [RestSearchComponent.php](https://github.com/MISP/MISP/blob/04fc5f8b7ccb52bb6614ca3e9ccdbfdf6585d985/app/Controller/Component/RestSearchComponent.php) and the companion API course's source audit |
| PyMISP search and attribute-targeted sightings | [pymisp/api.py](https://github.com/MISP/PyMISP/blob/9bb7d6b5b9683885536e5b42f70a4cb3eefe2728/pymisp/api.py) |
| Module families, service requests and enrichment hook | [Module.php](https://github.com/MISP/MISP/blob/04fc5f8b7ccb52bb6614ca3e9ccdbfdf6585d985/app/Model/Module.php) |
| Workflow routing and privileged execution identity | [Workflow.php](https://github.com/MISP/MISP/blob/04fc5f8b7ccb52bb6614ca3e9ccdbfdf6585d985/app/Model/Workflow.php) |
| Blocking publication trigger | [Module_event_publish.php](https://github.com/MISP/MISP/blob/04fc5f8b7ccb52bb6614ca3e9ccdbfdf6585d985/app/Model/WorkflowModules/trigger/Module_event_publish.php) |
| Enrichment-query trigger | [Module_enrichment_before_query.php](https://github.com/MISP/MISP/blob/04fc5f8b7ccb52bb6614ca3e9ccdbfdf6585d985/app/Model/WorkflowModules/trigger/Module_enrichment_before_query.php) |
| Transient versus persistent enrichment | [Module_attach_enrichment.php](https://github.com/MISP/MISP/blob/04fc5f8b7ccb52bb6614ca3e9ccdbfdf6585d985/app/Model/WorkflowModules/action/Module_attach_enrichment.php) and [Module_enrich_event.php](https://github.com/MISP/MISP/blob/04fc5f8b7ccb52bb6614ca3e9ccdbfdf6585d985/app/Model/WorkflowModules/action/Module_enrich_event.php) |
| Webhook payload fallback and URL setting | [Module_webhook.php](https://github.com/MISP/MISP/blob/04fc5f8b7ccb52bb6614ca3e9ccdbfdf6585d985/app/Model/WorkflowModules/action/Module_webhook.php) |
| Module discovery, query routes and errors | [misp_modules/__main__.py](https://github.com/MISP/misp-modules/blob/a123fc2ee99fd30b37d0879a1e576b684a826829/misp_modules/__main__.py) |
| Local structured parsing | [extract_url_components.py](https://github.com/MISP/misp-modules/blob/a123fc2ee99fd30b37d0879a1e576b684a826829/misp_modules/modules/expansion/extract_url_components.py) |
| osquery planning versus publication/activation | [osquery_pack_publish.md](https://github.com/MISP/misp-modules/blob/a123fc2ee99fd30b37d0879a1e576b684a826829/documentation/action_mod/osquery_pack_publish.md) |

Development-branch capabilities may postdate a packaged release. Recheck the
runtime version, available modules/triggers, permissions and consumer schema.
The linked specialist courses supply deeper deployment and development labs;
their previous live-test results are not new validation of this refresh.

## Validation scope

The offline planner and its six failure-boundary checks use only synthetic
fixtures. Slide, notes and diagram builds can be verified with the commands
above. Live MISP requests, workflow execution, provider calls, module-service
execution and endpoint activation require a separately configured lab and
are not claimed by the offline checks.
