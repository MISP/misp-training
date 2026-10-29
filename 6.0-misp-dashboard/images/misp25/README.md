# MISP 2.5 dashboard screenshots

**Genuine browser captures of the integrated dashboard, using synthetic data.**

These PNGs were captured on **29 October 2026** from an isolated local MISP
**2.5.50** instance. They are not generated illustrations, redrawn controls or
older screenshots relabelled as 2.5.

| Image | What it shows | Pixels |
| --- | --- | --- |
| [dashboard-overview.png](dashboard-overview.png) | Header and top three tiles of the five-widget training board | 1600 × 743 |
| [widget-gallery.png](widget-gallery.png) | Actual gallery search for “Trending Tags” | 821 × 472 |
| [widget-configure.png](widget-configure.png) | Typed Trending settings and live preview | 821 × 850 |
| [shared-time-filter.png](shared-time-filter.png) | The shared time-window control, targeting four tiles | 400 × 309 |
| [template-gallery.png](template-gallery.png) | The three imported built-in template cards | 1600 × 850 |

Captures use the **default MISP theme** and a **site-admin training account**.
Role, patch level, theme and installed widgets can change what another user sees.
The gallery's widget count is specific to this account and snapshot.

## Source and runtime provenance

- MISP source: [`fc99c9e3fc85beddc6ef18835359f3c8b7f44608`](https://github.com/MISP/MISP/tree/fc99c9e3fc85beddc6ef18835359f3c8b7f44608),
  `VERSION.json` reports 2.5.50.
- The reviewed source was copied into the isolated core and static-web containers.
  SHA-256 checks confirmed that the running `DashboardsController.php` and
  `board.module.mjs` matched the reviewed files.
- Base core image: `ghcr.io/misp/misp-docker/misp-core` at digest
  `sha256:1bf559bf280021da2adead9e715a8c84786e378b107e34e8b834d518596fcab7`.
- Base web image: `ghcr.io/misp/misp-docker/misp-nginx` at digest
  `sha256:0ddc6730db7433220b821d6aa640cb3205ec59166364daf50272090bf4d066cd`.
- Deployment reference:
  [misp-docker `7e55a0f507012f3699350faab9cdf60a851e2b2f`](https://github.com/MISP/misp-docker/tree/7e55a0f507012f3699350faab9cdf60a851e2b2f).
  The temporary stack used MariaDB and Valkey, with only its web port bound to
  loopback. No production instance or provider account was used.
- Captured with Playwright and Chromium. The overview used a 1600 × 1050 viewport;
  subsequent captures used 1600 × 850. Panel and overview crops were taken
  directly by the browser screenshot API. No controls, labels, counters or chart
  contents were painted over or composited. The configuration slide additionally
  crops the lower part of the full PNG to make its first controls readable.

MISP UI assets remain the MISP Project's work; the source is distributed under
[MISP's AGPL-3.0 license](https://github.com/MISP/MISP/blob/fc99c9e3fc85beddc6ef18835359f3c8b7f44608/LICENSE).
These captures document that interface; no relicensing of third-party UI assets
is implied.

## Data context

The board uses [dashboard-layout.json](../../examples/dashboard-layout.json).
Three synthetic events contain reserved `.example` domains and public CVE
identifiers used as invented observations. Three short synthetic event reports
were added separately. The generated organisation and trainer identity are local
training fixtures.

The events remain organisation-only, unpublished and non-IDS. The Trending
minimum-count setting of one demonstrates the tiny corpus; its counts and NEW
badges are not production findings. Zero values elsewhere are real results for
this small lab, not concealed production data.

See the [course workshop](../../README.md#workshop-build-inspect-restore) to recreate
the exercise. The screenshots do not claim that every widget, role, theme,
browser or deployment has been tested.
