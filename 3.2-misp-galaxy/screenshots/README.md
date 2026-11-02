# Threat Actor screenshots — MISP 2.5.50

Captured on **1 November 2026** from a running, disposable local MISP instance.
These are browser screenshots of the actual application, cropped to the relevant
UI. They contain no generated interface, overlays or composited controls.

| Component | Capture reference |
| --- | --- |
| MISP | `2.5.50`, checked in `VERSION.json`, startup output and UI footer |
| Backend image | `ghcr.io/misp/misp-docker/misp-core:v2.5.50` |
| Backend digest | `sha256:1bf559bf280021da2adead9e715a8c84786e378b107e34e8b834d518596fcab7` |
| Frontend image | `ghcr.io/misp/misp-docker/misp-nginx:v2.5.50` |
| Frontend digest | `sha256:0ddc6730db7433220b821d6aa640cb3205ec59166364daf50272090bf4d066cd` |
| Galaxy source, mounted read-only | [`285d147754492321eed5deda8af6e4196b465ad8`](https://github.com/MISP/misp-galaxy/tree/285d147754492321eed5deda8af6e4196b465ad8) |
| Family | `threat-actor`, displayed as **Threat Actor**, namespace `misp` |
| Selected cluster | **APT28**, UUID `5b4ee3ea-eee3-4c8e-8323-85ae32658754` |
| Collection | UUID `7cdff317-a673-4474-84ec-4f1754947823`, version `357` |
| Connector tag | `misp-galaxy:threat-actor="APT28"` |
| Browser | Chromium via Playwright, 1440 × 1200 viewport, device scale factor 2, default MISP theme |
| Account | Disposable site administrator, `trainer@example.test` |
| Organisation | **Galaxy Training Lab** (synthetic) |
| Event | **Galaxy training - synthetic APT28 reference exercise** |

The server imported 58,528 cluster entries and 79,372 knowledge relations from
the pinned checkout. The family version shown in the Galaxy view is **4**;
the cluster/collection version in the APT28 view is **357**. They are different
version fields. Numeric Galaxy, cluster, event and tag IDs in the captures are
installation-specific; use type/UUID when reproducing the selection.

## Captures

| File | What is shown |
| --- | --- |
| [Search](misp-2.5-threat-actor-search.png) | The filter and first result in the Threat Actor collection after searching for Sofacy; the remaining results extend below the crop. |
| [Cluster](misp-2.5-threat-actor-cluster.png) | The APT28 identity panel, including UUIDs, provenance, version and connector tag. |
| [Picker](misp-2.5-threat-actor-picker.png) | The actual nested event selector with `misp`, Threat Actor and APT28 selected, before the final Submit. |
| [Attachment](misp-2.5-threat-actor-attached.png) | The event Galaxies panel after saving and reloading. |

## Reproduce the walkthrough

1. Use a disposable MISP 2.5.50 installation and an authorised account. Have the
   operator install the pinned Galaxy checkout and import it using the normal
   Galaxy update workflow. The runtime image version does not pin its knowledge
   base by itself. Do not wipe an existing catalogue for this exercise.
2. Open **Galaxies → Threat Actor**, filter for **Sofacy**, and open **APT28**.
   This UI search also matches descriptions: in this snapshot it returns
   **Snake Wine** and **White Bear** as well. The offline explorer intentionally
   searches values, synonyms and external IDs, so its result set can differ.
3. Check the individual UUID above and the collection/source. Below the captured
   identity panel, inspect the paginated metadata or JSON view for synonyms and
   `refs`, including [MITRE G0007](https://attack.mitre.org/groups/G0007/).
4. Create an unpublished, **Your organisation only** event with a clearly
   synthetic title and a non-IDS comment explaining that this is an attachment
   exercise, not a real incident or independent attribution.
5. In the **event Galaxies** panel, choose **Add new cluster → misp → Threat
   Actor**, search for **APT28** and select it. Capture the selector before its
   final **Submit**. The warning about omitted context is part of the real UI:
   inspect the separate detail page before selection.
6. Submit, reload and check **Threat Actor → APT28** in the event panel. Confirm
   the expected UUID/tag in the saved event/export, the association's local
   flag and the event's visibility/publication state. The lab used **Add new
   cluster**, not **Add new local cluster**. A non-local association does not
   override organisation-only event visibility.
7. Detach the exercise association and remove disposable data under lab policy.
   Capture only synthetic data and exclude credentials from screenshots.

Live verification confirmed the UUID/tag at event scope, a non-local association,
no direct actor attachment on the comment attribute, event distribution `0`
and `published=false`. Only this discovery/inspection/event-attachment workflow
was exercised. The screenshots do not establish fork publication, peer sync,
attribute attachment, matrix behaviour or ordinary-user visibility. Available
actions and labels can vary with patch version, role, settings and theme.
