# MISP 2.5.50 usage screenshots

Captured on **3 November 2026** from a running, disposable local reference.
These are actual Chromium/Playwright browser captures, cropped to the relevant
UI. No generated interface, added annotations, retouched labels or composited controls
are used. The screenshot files are the direct browser outputs.

| Reference | Value |
| --- | --- |
| MISP version | **2.5.50**, checked in VERSION.json, startup output and UI footer |
| Backend image | `ghcr.io/misp/misp-docker/misp-core:v2.5.50` |
| Backend digest | `sha256:1bf559bf280021da2adead9e715a8c84786e378b107e34e8b834d518596fcab7` |
| Frontend image | `ghcr.io/misp/misp-docker/misp-nginx:v2.5.50` |
| Frontend digest | `sha256:0ddc6730db7433220b821d6aa640cb3205ec59166364daf50272090bf4d066cd` |
| Browser | Chromium via Playwright 1.62.1; 1600 × 1100 CSS viewport; device scale factor 2 |
| Theme and language | Default MISP theme, English interface |
| Ordinary account | `analyst@example.test`, role **User**, no site administration |
| Publication demonstration | Separate `publisher@example.test`, role **Publisher**, no site administration |
| Organisation | **MISP Usage Training Lab**, synthetic |
| Main event | **Usage training - synthetic sign-in report** |
| Reference event | **Usage training - Team B synthetic reference** |
| Object template | domain-ip, UUID `43b3b146-77eb-4931-b4cc-b66c60f28734`, version **11** |
| Tags | Bundled tlp taxonomy enabled; saved tag **tlp:clear**, non-local association |
| Sighting time | **2026-11-03 09:00:00 UTC**, source **Synthetic sensor - UTC** |

The image version does not universally pin a site's knowledge base. This reference
used the bundled taxonomy and object templates and imported the read-only Galaxy
checkout [`285d147754492321eed5deda8af6e4196b465ad8`](https://github.com/MISP/misp-galaxy/tree/285d147754492321eed5deda8af6e4196b465ad8)
at startup. No Galaxy actor association is part of the usage exercise. Numeric
event, attribute, tag, taxonomy and template IDs are installation-specific.
The [manifest](manifest.json) records route patterns, roles, dimensions and
SHA-256 hashes for every original capture.

## Captures

| Image | What is shown |
| --- | --- |
| [event-index](misp-2.5-event-index.png) | Filtered event index with the two synthetic reports |
| [event-create](misp-2.5-event-create.png) | Completed event form before Submit |
| [event-overview](misp-2.5-event-overview.png) | Empty saved event, organisation-only and unpublished |
| [attribute-add](misp-2.5-attribute-add.png) | Typed domain form with inherited distribution and IDS cleared |
| [attributes](misp-2.5-attributes.png) | Filtered saved attribute table with the real Related Events link |
| [freetext-review](misp-2.5-freetext-review.png) | IP candidates reviewed before Submit attributes |
| [object-template](misp-2.5-object-template.png) | domain-ip template metadata before entry |
| [object-add](misp-2.5-object-add.png) | Object pre-save review before Create new object |
| [object-saved](misp-2.5-object-saved.png) | Saved object and member attributes in the actual table |
| [tag-picker](misp-2.5-tag-picker.png) | TLP:CLEAR selected before final Submit |
| [tagged-event](misp-2.5-tagged-event.png) | Saved TLP:CLEAR with unchanged event audience/publication |
| [correlation](misp-2.5-correlation.png) | Reference report attribute table with matching domain |
| [sighting-add](misp-2.5-sighting-add.png) | Advanced sighting input with source and time |
| [sighting-results](misp-2.5-sighting-results.png) | Saved sighting under My org |
| [publication-review](misp-2.5-publication-review.png) | Publisher-only confirmation; No chosen, no publication |
| [export](misp-2.5-export.png) | Actual format choices before the browser JSON download |

## Reproduce

1. Prepare a disposable 2.5.50 instance and ordinary User account as described in
   the [lab guide](../lab/README.md). Install the required template and taxonomy.
   Do not display or capture passwords, keys, tokens or browser session files.
2. Create the optional reference report from the supplied fixture, then follow
   the learner UI steps. Use only the documented synthetic values and keep IDS
   cleared, the events organisation-only and unpublished.
3. Capture the event form before Submit and the empty saved event afterward.
   Capture Add Attribute before Submit, extraction results before Submit attributes,
   template metadata before entry, and Object pre-save review before Create new object.
4. For the tag picker, inspect the exact selected TLP:CLEAR item before Submit.
   Reload before capturing the saved tag and visibility. Do not select an actor
   or legacy TLP:WHITE as a substitute for context.
5. Capture the real attribute tables and related reference report. Add the single
   synthetic UTC sighting and capture its My org entry. Check the instance's
   sighting policy; the reference restricts it to the owning organisation.
6. With a separate non-admin Publisher only, open Publish Event, capture the
   confirmation and choose **No**. The default User role lacks publication rights.
   Verify Published remains No afterward.
7. Capture Download as… and select MISP JSON (metadata + all attributes). Inspect
   the downloaded file. Do not send these documentation values to production tools.
8. Use browser screenshot crops or element captures to keep controls legible.
   Keep the real UI intact. Refresh the manifest hashes/dimensions and rebuild all
   three decks after recapturing. The screenshot UI stays English in all editions.

Live checks and their installation-specific identifiers are recorded in
[reference-validation.json](../lab/reference-validation.json). They confirmed
five values, one domain-ip object, cleared IDS flags, inherited object/attribute
distribution, event distribution 0, Published false, TLP:CLEAR, one real correlation,
one sighting, the cancelled publication confirmation and the browser JSON download.
A separate ordinary organisation was denied access with 404.

Scope is the tested local walkthrough. Peer delivery, mail notifications, feeds,
external enrichment, cross-organisation proposals, delegation, extended events,
other themes/roles and production detection/blocking were not exercised. Captures
can vary across patch versions, knowledge bases, settings and account rights.
Materials retain the repository's [existing license and attribution terms](../../README.md#license-attribution-and-funding).
