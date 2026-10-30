# MISP Galaxy in 2.5

**Explore a large knowledge base, assess the evidence, attach precise context.**

A practical course on finding and evaluating Galaxy clusters, attaching them in
MISP, interpreting relationships and matrices, and contributing reusable knowledge.

[Slides](slide.tex) · [PDF](../output/3.2-misp-galaxy.pdf) · [Presenter notes](content.tex) · [Offline explorer](examples/explore.py) · [Workshop](#workshop-find-assess-attach) · [Training home](../README.md)

The deck has **28 pages**, including 24 content slides with presenter notes.
Allow 35–45 minutes for the slides and 25–35 minutes for the workshop. Basic
event/attribute and tagging knowledge is enough. The offline exercise needs no
MISP account, API key or external provider.

## Start with the knowledge base

- **[Browse misp-galaxy.org](https://www.misp-galaxy.org/)** for the human-readable
  catalogue and cluster pages.
- **[Read the source repository](https://github.com/MISP/misp-galaxy)** for JSON
  definitions, original references, authors, versions and generation tools.
- **[Read the contribution guidance](https://github.com/MISP/misp-galaxy/blob/main/CONTRIBUTE.md)**
  before editing generated or manually maintained knowledge.

Reviewed **30 October 2026**, using MISP **2.5.50**
([fc99c9e3fc85beddc6ef18835359f3c8b7f44608](https://github.com/MISP/MISP/tree/fc99c9e3fc85beddc6ef18835359f3c8b7f44608))
and misp-galaxy
([285d147754492321eed5deda8af6e4196b465ad8](https://github.com/MISP/misp-galaxy/tree/285d147754492321eed5deda8af6e4196b465ad8)).

| Measured in that checkout | Count |
| --- | ---: |
| Galaxy definition files | 136 |
| Cluster collection files | 136 |
| Entries across collections | 58,528 |
| Distinct cluster UUIDs across those entries | 56,551 |
| Listed directed relationship edges | 79,372 |

These are reproducible repository counts, not numbers of unique threat actors,
validated claims, active clusters or records visible on every MISP instance.
Collections can overlap and reuse cluster UUIDs, including different ATT&CK
views. Pin the revision when comparing counts.

| Starting question | Useful source collections |
| --- | --- |
| Which technique describes the observed behaviour? | [Enterprise ATT&CK JSON](https://github.com/MISP/misp-galaxy/blob/285d147754492321eed5deda8af6e4196b465ad8/clusters/mitre-enterprise-attack-attack-pattern.json), Mobile/ICS collections |
| What defensive action or concept applies? | [D3FEND](https://www.misp-galaxy.org/mitre-d3fend), course-of-action and preventive measures |
| What activity group or software does a report describe? | [Threat actor](https://www.misp-galaxy.org/threat-actor), intrusion sets, malware and tools |
| How can information manipulation be contextualised? | [DISARM techniques](https://www.misp-galaxy.org/disarm-techniques), countermeasures and detections |
| What wider context helps the analyst? | Country, sector, targeting and other contextual collections |
| What detection concepts support the investigation? | MITRE detection strategies, data components and analytics collections |

The [published ATT&CK catalogue](https://www.misp-galaxy.org/mitre-attack-pattern/)
is also useful for browsing. Website publication can lag repository additions;
use the pinned JSON link for the enterprise-specific collection above.

Collection names and scope matter. Prefer the relevant domain-specific ATT&CK
collection when that is your analytical scope; inspect the combined collection
and historical entries deliberately rather than treating everything as one
interchangeable, current matrix.

## Understand the model

| Concept | Meaning |
| --- | --- |
| Galaxy | A knowledge family and its presentation metadata: type, namespace, description and optionally matrix ordering |
| Cluster | One named concept, with a UUID, description, metadata and possible relations |
| Element | A key/value item of cluster metadata, such as a synonym, reference or external ID |
| Cluster relation | Directed knowledge edge to another cluster UUID, with a relationship type and optional tags |
| Attachment | Association of a cluster-derived tag with an event, attribute or supported tag collection |

In the repository, `galaxies/<name>.json` describes the family and
`clusters/<name>.json` is a collection whose `values` array contains individual
clusters. The collection's UUID is not an individual cluster UUID. Match the
family and collection by their `type`; do not assume every identity field is
the same.

A Galaxy cluster adds structured context. A taxonomy classifies using its own
vocabulary; a MISP object groups typed attributes. Correlation and object
references are separate mechanisms. See the [taxonomy](../3-misp-taxonomy-tagging/)
and [object-template](../3.3-misp-object-template/README.md) courses.

## Assess a cluster before attaching it

1. Check the collection, namespace, cluster UUID and external identifier.
2. Read the description, original references and source date/version.
3. Inspect synonyms as discovery aids, not proof of equivalent identity.
4. Check revoked/deprecation indicators, historical descriptions and scope.
5. Explain why the event or attribute supports that particular concept.

Different providers can use overlapping or disputed names. A synonym is not a
guaranteed one-to-one attribution mapping. An actor cluster attached to a report
records an analyst assertion; it does not prove that actor caused every activity
in the event. Keep evidence, confidence and alternative explanations explicit.

Relations are directed assertions in the knowledge base. Inspect the type,
source and any confidence/handling tags. A graph path is not automatically a
causal chain or an assertion that can safely be copied into an incident.
Do not merge entities solely because two clusters share a name or alias.

## Attach context in current MISP

Use the event or attribute's Galaxy controls to search and attach the intended
cluster. Inspect its details before selecting it, then verify where it appeared.
An event-level attachment describes the event's scope; an attribute-level
attachment can express a narrower assertion. Parent context can appear in an
attribute export without being directly attached there.

MISP maintains a cluster-associated tag, commonly shaped like
`misp-galaxy:<type>="<value>"` for imported defaults. Use the actual tag/cluster
metadata returned by your instance; do not construct identity from a label or
assume all custom tags use the same naming convention.

Keep these boundaries separate:

| Boundary | What it controls |
| --- | --- |
| Event/attribute visibility | Access to incident data |
| Custom cluster distribution/sharing group | Access to that custom knowledge |
| Local attachment | Whether the association is local to the instance |
| Local-only Galaxy restriction | Whether a cluster can be attached outside local scope |
| Cluster publication and sync policy | Distribution of eligible custom knowledge |

An attachment does not automatically grant access to a private cluster or make
it available to every peer. A cluster relation is not the same operation as
attaching a cluster to an event. Attaching, detaching, editing definitions and
publishing require different permissions.

Current 2.5 source includes bulk attachment and optional attribute-to-event
mirroring, controlled by settings and user choices. Review the resulting scope:
mirroring an attribute assertion to the whole event can change its meaning.
UI labels and available actions depend on patch level, theme, role and settings.

## Read matrices and graphs carefully

Galaxy `kill_chain_order` describes matrix tabs/columns; cluster
`meta.kill_chain` places entries using the matching key/prefix. Inspect the
selected collection's current ordering, domains and platforms.

An ATT&CK matrix highlights selected or observed techniques. It is not a measure
of detection coverage, efficacy, attribution certainty or defensive maturity.
Separate “observed behaviour”, “available detection”, “tested detection” and
“effective prevention”. Counts can also change when deprecated techniques or
different collection views are included.

## Custom clusters, forks and updates

The reviewed MISP supports creating custom clusters, editing permitted custom
knowledge, forking existing clusters, relations, publication and synchronisation.
Default imported clusters are protected from normal editing; fork a concept
when adding local analysis instead of overwriting upstream knowledge.
Fork metadata records `extends_uuid` and `extends_version`.

Keep local conclusions, references, ownership, distribution and publication
intent explicit. A fork is a separate identity with provenance, not automatic
agreement with every later upstream change. Review updates and relation targets.

Git data and the database catalogue are separate. Operators update the selected
`app/files/misp-galaxy` checkout and use the Galaxy update/import workflow.
The reviewed `Admin updateGalaxies` command imports from disk; it is not a Git
fetch. Avoid force/wipe operations as a routine training step.
For custom-knowledge sync, check permissions, publication, sharing groups and
peer configuration. A Galaxy tag alone is not a complete knowledge package.

## Workshop: find, assess, attach

### Offline: explore the actual knowledge base

From this course directory:

```sh
git clone https://github.com/MISP/misp-galaxy.git /tmp/misp-galaxy-lab
git -C /tmp/misp-galaxy-lab checkout 285d147754492321eed5deda8af6e4196b465ad8
python3 examples/explore.py /tmp/misp-galaxy-lab --stats
python3 examples/explore.py /tmp/misp-galaxy-lab \
  --search T1059 --collection mitre-enterprise-attack-attack-pattern --limit 3
```

The standard-library explorer searches values, synonyms and external IDs.
It returns bounded results with UUIDs, collection versions, metadata, descriptions
and relations. Results are candidates for review, not automatic entity resolution.
It never modifies the checkout or calls MISP.

Read one returned entry's original references, external ID and status. Follow a
related UUID into the appropriate collection. Compare a synonym search with an
identifier search and explain why the results can differ.

### Offline: validate a synthetic contribution

[galaxy.json](examples/galaxy.json) and [clusters.json](examples/clusters.json)
define a teaching family, two synthetic concepts and one directed relation.
They are **repository-format examples**, not MISP API import envelopes.

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r examples/requirements.txt
python examples/verify.py /tmp/misp-galaxy-lab
```

Inspect the family UUID, collection UUID and two individual UUIDs. Try changing
the type, breaking the edge target, duplicating a fixture cluster UUID or clearing
a label. The verifier checks the two schemas and these semantic failures; schema
success alone is insufficient, especially for relationship content.
The fixture requires its targets to exist within itself. Real repositories can
have cross-collection references and need a broader target-resolution policy.

### Optional: apply the result in MISP

Use a disposable unpublished, organisation-only event and a permitted user.
Have the operator confirm the chosen Galaxy revision is installed.

1. Find an ATT&CK technique supported by the synthetic event's described behaviour.
2. Read its collection, references, external ID and status.
3. Attach at event scope, then compare an attribute-scoped attachment.
4. Inspect local versus shared association options and the exported representation.
5. Inspect the matrix and explain what its highlight proves and does not prove.
6. If authorised, fork a default cluster, keep the fork restricted and inspect its
   provenance. Test with a second ordinary user before sharing.
7. Detach training associations and remove disposable data/forks under lab policy.

The reviewed API includes `/galaxies/view/{id}`,
`/galaxy_clusters/view/{id}`, `/galaxy_clusters/restSearch` and
`/galaxies/attachCluster/{target_id}/{target_type}`. The attachment endpoint
expects `Galaxy.target_id` containing the selected installed cluster ID; it
checks target permissions and local scope. Do not substitute a repository UUID
without checking that endpoint's accepted identifier. See the
[REST API course](../a.7-rest-API/README.md) for trusted TLS and authentication.

Validation in this update is offline plus a MISP source audit. It does not claim
new live-server testing or current UI screenshots.

## Contribute knowledge with provenance

For manually maintained collections, update JSON with original references and
clear descriptions. For generated collections such as ATT&CK, inspect the
generator and upstream source first; editing only generated output can be lost.
Preserve existing concept UUIDs, generate fresh identities for new concepts and
increment the relevant definition/collection versions as appropriate.

Use established metadata conventions: `refs`, `synonyms`, `external_id`,
`kill_chain` and source-specific fields. In threat-actor contributions,
`cfr-*` fields require CFR-sourced evidence; the documented
`attribution-confidence` concerns country-of-origin attribution, not universal
confidence in every incident attachment. Cite references rather than copying an
old alias list without its uncertainty.

Run the repository's formatter in a dedicated checkout, review the result,
commit the intended normalised JSON and run `./validate_all.sh` with its current
dependencies. The current CI also runs PyMISPGalaxies tests and checks the generated
README index. Follow current workflow files rather than treating this lesson's
offline verifier as a substitute for upstream CI.

## Build and implementation references

Use the [shared theme setup](../themes/README.md). From the repository root:

```sh
export TEXINPUTS="$PWD/themes:${TEXINPUTS:-}:"
mkdir -p /tmp/misp-galaxy-slides
cd 3.2-misp-galaxy
for pass in 1 2 3; do
  pdflatex -interaction=nonstopmode -halt-on-error \
    -output-directory=/tmp/misp-galaxy-slides slide.tex || exit 1
done
```

The standard build includes this course and generates its presenter-notes handout.
The [earlier slides and images](../archive/slide-decks/3.2-misp-galaxy-v1/README.md)
remain archived outside the standard build.

Pinned evidence:

- [Galaxy schema](https://github.com/MISP/misp-galaxy/blob/285d147754492321eed5deda8af6e4196b465ad8/schema_galaxies.json), [cluster schema](https://github.com/MISP/misp-galaxy/blob/285d147754492321eed5deda8af6e4196b465ad8/schema_clusters.json), [contribution guidance](https://github.com/MISP/misp-galaxy/blob/285d147754492321eed5deda8af6e4196b465ad8/CONTRIBUTE.md) and [CI workflow](https://github.com/MISP/misp-galaxy/blob/285d147754492321eed5deda8af6e4196b465ad8/.github/workflows/pytest.yml).
- [MISP Galaxy model](https://github.com/MISP/MISP/blob/fc99c9e3fc85beddc6ef18835359f3c8b7f44608/app/Model/Galaxy.php), [cluster model](https://github.com/MISP/MISP/blob/fc99c9e3fc85beddc6ef18835359f3c8b7f44608/app/Model/GalaxyCluster.php), [Galaxy controller](https://github.com/MISP/MISP/blob/fc99c9e3fc85beddc6ef18835359f3c8b7f44608/app/Controller/GalaxiesController.php) and [cluster controller](https://github.com/MISP/MISP/blob/fc99c9e3fc85beddc6ef18835359f3c8b7f44608/app/Controller/GalaxyClustersController.php).

Validation: both synthetic JSON definitions and all 136 Galaxy/136 cluster files
passed the pinned schemas. The offline verifier passed its semantic negative
cases and real ATT&CK lookup. Standard and presenter-notes PDFs were built in
three passes and the original assets/PDF were checked byte-for-byte. These are
source and offline checks, not the full upstream CI suite or live-server tests.
