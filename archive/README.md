# Training archive

**Historical references — outside the standard MISP training.**

This archive preserves retired courses, their assets and related publications.
These materials are not maintained as current guidance and may describe obsolete
interfaces, dependencies, commands or integrations. Their presence is not a
recommendation to install or use a particular tool.

[Current training](../README.md#slide-catalog) · [Archive catalog](#archive-catalog) · [How to archive a topic](#how-to-archive-a-topic)

## Archive catalog

| Material | Preserved here | Status |
| --- | --- | --- |
| Viper and MISP integration | [Course and original PDF](slide-decks/1.1-misp-viper-integration/README.md) | Retired from standard training on 29 October 2026 |
| Standalone ZeroMQ dashboard | [Course and original PDF](slide-decks/6.0-misp-dashboard-zmq/README.md) | Replaced in standard training by the integrated MISP 2.5 dashboard course |
| Earlier widget-development model | [Lesson and original PDF](slide-decks/a.a-widget-dev-v1/README.md) | Replaced in standard training by the MISP 2.5 widget-development course |
| Earlier object-template lesson | [Course and original PDF](slide-decks/3.3-misp-object-template-v1/README.md) | Replaced by the MISP 2.5 object/template course |
| Earlier REST API workshops | [Lesson, notebooks and original PDF](slide-decks/a.7-rest-API-v1/README.md) | Replaced in standard training by the MISP 2.5 REST API course |
| Legacy training-VM cheat sheet | [Source and VM context](supporting-material/compact-cheatsheet/README.md) | Historical companion with Viper-web details and MISP 2.4-era instructions |
| Earlier combined training PDFs | [Publication snapshots](publications/combined-training/README.md) | Historical bundles that include the retired Viper course |

The root [build script](../build.sh) selects only standard courses. Archived
decks are excluded from its builds, generated catalog and combined PDF.
Old source locations contain small README pointers rather than active entry
points. Archived PDFs are linked from this catalog, outside the standard
`output/` publication directory.

The original PDFs are preserved byte for byte and therefore do not gain new
archive banners inside their pages. Read them in the context of their archive
entry. Rebuilt archived sources display an archive notice.

## Directory structure

```text
archive/
  README.md
  slide-decks/
    <original-course-directory>/
      README.md
      slide.tex
      content.tex
      ... original assets ...
      original-published.pdf        # when a PDF snapshot exists
  supporting-material/
    <original-material-directory>/
      README.md
      ... historical sources and assets ...
  publications/
    <publication-group>/
      README.md
      ... original PDF snapshots ...
```

Use the original directory name for a recognisable course or support item.
Record the archival date and source revision in its README instead of inventing
a release year or supported version. Publication groups can retain multiple
snapshots when their original files differ.

## How to archive a topic

1. Identify the complete teaching unit: entry points, translations, notes,
   supporting files, assets and existing published copies.
2. Move files with `git mv` so their history and original content remain
   traceable. Preserve original PDF snapshots.
3. Add an entry README with **outside standard training** status, date, original
   paths, the last pre-archive revision, limitations and current alternatives.
4. Mark rebuilt covers and add an archive notice to presentation sources.
   Keep historical examples intact; document path fixes needed for rebuilding.
5. Remove the topic from `build.sh` and the standard catalogs. Check references
   in active courses and keep small pointers at old source locations where useful.
6. Update this catalog, verify local links and confirm the default build selects
   no archived paths. Rebuild moved sources when practical and report limitations.

Archive a coherent course, not every conference talk that happens to mention
the same tool. Dated event and conference collections retain their original
historical context; they are not automatically part of the standard build.

## Reading and rebuilding

Start with an item's README for the original PDF and explicit build commands.
Archived courses use their own local assets and may still rely on the repository's
shared theme. Rebuilding documents is separate from recreating the old runtime:
no archived integration has been tested against current services merely because
its slides compile.

For current terminal and programmatic use, see [PyMISP](../a.2-pymisp/),
[command-line tools](../a.b-cli/) and [MISP modules](../3.1-misp-modules/README.md).
