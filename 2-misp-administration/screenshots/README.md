# Authentic MISP 2.5 administration screenshots

These 19 PNGs were captured directly from a running, disposable **MISP 2.5.50**
instance on **3 November 2026**. They are browser clips of the default English UI,
not mockups or reconstructed interfaces. The [manifest](manifest.json) records every
route, crop, pixel size and SHA-256, plus pinned backend/frontend image digests,
knowledge references and version evidence.

The lab used Playwright 1.62.1 with Chromium, a 1600×1100 CSS-pixel viewport,
2× device scale and UTC. The frontend bound only to loopback at
`http://localhost:8082`. All captures use synthetic site administrator
`operator@example.test`. Ordinary-account API checks were performed separately;
site-admin screenshots do not establish ordinary-user visibility.

## Reproduce the views

Prepare the [lab fixture](../lab/README.md) and resolve IDs on your own installation.
Navigate through the UI or substitute those IDs in the manifest routes. Use direct
browser screenshots and crop only the relevant content. Do not paste new labels,
values or status icons into a captured UI.

| Capture | Preparation or selected state |
| --- | --- |
| role-permissions | Open the standard Org Admin role; review flags above the crop boundary |
| organisation-add | New Practice Partner local organisation, generated UUID, before Submit |
| organisations | Saved synthetic local/external organisation list, before the delegate is created |
| user-add | Delegate, Practice Partner, Org Admin; before password entry |
| users | Saved delegate and disabled retired account in the users index |
| authkey-scope | Analyst, purpose and Read only selected; before generation; expiry/source fields shown blank for discussion |
| sharing-group-organisations | Editor's Organisations tab; no changes saved during capture |
| sharing-group-review | Saved two-member, local-instance group, All orgs unchecked |
| taxonomy | Enabled tlp taxonomy, version 10 |
| object-templates | Active domain-ip template, version 11 |
| warninglist-check | Search enabled lists for 192.0.2.25; actual RFC 5735 match |
| disabled-peer | Saved synthetic peer, transfer directions off; no connection test |
| disabled-feed | Synthetic feed selected with `Admin lab` filter; enabled/caching off |
| default-distribution | Focused Server Settings rows after setting organisation-only default |
| diagnostics | Version, container update notice and writable-directory checks |
| workers | Visible cache/default/email queues and healthy processes; other workers checked separately |
| jobs | Completed local taxonomy-refresh job at top; adjacent startup jobs can also appear |
| scheduled-tasks | Admin tasks and linked last-job status; task status may still say Enqueued |
| audit-log | Audit filter model Organisation; synthetic organisation changes only |

The manifest records the named `searchall:taxonomies` Jobs URL used for capture;
this view still includes adjacent job rows in the reference UI. Inspect the intended
job's type/input and final status instead of assuming that URL isolates one job.

Diagnostics intentionally shows a failed online version retrieval and an unknown
latest version; the displayed installed version/source commit and container
VERSION.json establish the local version. The Docker deployment disables MISP's
in-application self-update; updates use the deployment workflow. These warnings
are retained for interpretation, not concealed. The shown public source commit
was checked against the public MISP repository.

## Review before publication

Only reserved example identities/URLs, random public record UUIDs and disposable
container-network addresses appear. Captures avoid generated keys, password entry,
connection credentials, user/key audit changes and unreviewed settings exports.
Visible crop contents were checked against generated lab secrets, all PNGs were
visually reviewed and OCR-checked, and the built slide/notes text was checked too.

Inspect each new capture rather than reusing this assurance. Keep credentials,
browser storage, API responses and private lab state outside the repository. Update
PNG hashes and rebuild the slides after replacing images. The pictures inherit the
training repository's licensing and attribution.
