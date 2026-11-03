# Usage lab: a synthetic report from creation to feedback

[Course](../README.md) · [Expected record](expected-record.json) · [Capture reference](../screenshots/README.md)

Allow 60–75 minutes with the lesson. All values are fictional documentation
examples. The aim is to explain a useful record and verify its saved state.

## Prepare before class

Use a disposable, authorised MISP 2.5 instance. The screenshot reference is
**2.5.50**, default English UI, ordinary role **User**. The operator supplies the
URL/account and checks add/edit/tag/sighting rights. Learners need no site-admin
access. A separate **Publisher** can demonstrate the publication confirmation
and cancel it; the default User role in the reference cannot publish.

Install/update object templates by the normal administrator workflow and make
`domain-ip` available. The reference template is UUID
`43b3b146-77eb-4931-b4cc-b66c60f28734`, version **11**, with domain and ip relations.
Enable the bundled `tlp` taxonomy and its tags; select **tlp:clear**, rather than
legacy entries that may also be listed. Check configured consumers and keep
feeds, peer synchronisation and external enrichment outside this exercise.

Optionally create **Usage training - Team B synthetic reference** with one
`domain` attribute `login-support.example`. Keep it organisation-only,
unpublished, with IDS cleared and attribute distribution Inherit event.
[reference-event.json](reference-event.json) is the tested `/events/add` API
payload for trainer preparation; the same values can be entered manually.
It is not a command to import data into a production instance. The learner must
be able to read the reference for the illustrated correlation to appear.

The event date is a report/context date, distinct from an observation time.
Repeat learners should use a unique title and avoid duplicate objects. Numeric
IDs and UUIDs in screenshots identify that capture only; resolve your own records.

## Walk through the UI

| Step | Action | Verify after saving |
| --- | --- | --- |
| Find | Event Actions / List Events; choose Event info, enter `Usage training`, Filter | Correct scope, source organisation and date; use Search Attributes for values |
| Create | Add Event; title **Usage training - synthetic sign-in report**; report date; Your organisation only; Undefined; Initial; leave Extends Event blank | Owning organisation, distribution 0, Published No |
| Attribute | Add Attribute; Network activity; domain; `login-support.example`; a synthetic source comment; Inherit event; clear For Intrusion Detection System | Correct type/value, `to_ids=false`, distribution 5, correlation enabled |
| Free text | Populate from… / Freetext import (shortcut F); paste [freetext.txt](freetext.txt); review results | Two ip-dst values: `198.51.100.44`, `203.0.113.77`; Network activity, IDS cleared, Inherit event |
| Object | Add Object; choose domain-ip; inspect metadata; enter domain `relay-service.example` and ip `203.0.113.42`; select the rows to save | Object and its two attributes inherit the event; both IDS flags are cleared; add the synthetic relationship source comment |
| Confirm | Submit the object form, inspect **Object pre-save review**, then **Create new object** | Exactly one domain-ip object with the two intended relations |
| Tag | Event Tags / Add a tag (shortcut T); Taxonomy Library:tlp; choose tlp:clear; inspect selection and Submit | Event tag tlp:clear, non-local association; event still organisation-only and unpublished |
| Compare | Open Related Events for the domain | Team B's report contains the same value; compare source, time and context before assessing meaning |
| Sighting | Attribute row wrench / Advanced sightings; Add sighting; type Sighting, source **Synthetic sensor - UTC**, date `2026-11-03`, time `09:00:00` in the reference UTC setup | Exactly one sighting at `2026-11-03T09:00:00Z`; inspect My org |
| Publish review | Optional Publisher demonstration: Publish Event, inspect confirmation, choose **No** | Event remains unpublished; no publish request is submitted |
| Export | Download as… / MISP JSON (metadata + all attributes) | Inspect downloaded JSON for values, object, tag, IDS, scope and publication state |

The expected final record has **three standalone attributes plus two object
attributes**, for **five values** in total. See [expected-record.json](expected-record.json)
for assessment data; it is a checklist format, not an import payload.

The domain-ip requirements allow several combinations; this scenario deliberately
uses domain and ip. A pre-save review is not the final save. The image named
`object-add` shows that review stage and its final Create new object control.
The template screenshot shows real metadata before entry, rather than a mocked
selector.

Free-text extraction can misclassify reserved example domains as filenames.
Do not accept that guess or use a real suspicious domain just to make a parser
match. Enter the domain explicitly and use the supplied IP-only extraction input.
Review types, selected rows, IDS and distribution before importing. The reference
UI also contains some legacy labels/placeholders; they are not instructions to
use TLP:WHITE or an old integration.

The sighting form uses the instance's date/time handling. This capture used UTC;
confirm your lab time zone or adjust the input to represent the intended UTC time.
The reference restricts sighting visibility to the owning organisation, which is
not a universal setting. Clear unused sighting filters.

## Discuss and assess

- Why does the shared domain justify comparison without proving attribution?
- Which source supports the domain/IP relationship, and what remains uncertain?
- Why can TLP:CLEAR coexist with organisation-only visibility?
- Which output could support a hunt before a blocking decision is justified?
- Who receives a correction, and how is it returned?

Saving and publication are different from visibility. Authorised users/APIs can
read unpublished events; administrators can have privileged access. IDS is not
an access control or a proof of maliciousness. Export formats may omit context or
apply different IDS filters, so inspect the file and its intended recipients.

After assessment, remove only the disposable exercise data under the lab plan.
Do not remove other learners' work or the trainer's seed without coordinating.
The reference lab was isolated from peers and mail relay and did not publish,
block, enrich externally or test cross-organisation proposals.
