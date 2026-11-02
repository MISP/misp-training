"""Deliberate writes to a disposable lab; remove the newly created event in finally."""
import argparse
import sys

from pymisp import MISPAttribute, MISPEvent, MISPSighting

from examples.common import TrainingError, connect, expect_model, expect_success
from examples.models import build_event
from examples.read import collect_pages


def run_workshop(misp):
    draft = build_event()
    # If a create times out, inspect draft.uuid before retrying: it may have persisted.
    created = expect_model(misp.add_event(draft, pythonify=True), MISPEvent)
    try:
        attribute = created.attributes[0]
        attribute.comment = "Synthetic observation reviewed in the PyMISP workshop."
        updated = expect_model(misp.update_attribute(attribute, pythonify=True), MISPAttribute)
        if updated.uuid != attribute.uuid:
            raise TrainingError("Unexpected identity after update.")

        # The operator must make tlp:clear available; tag permissions still apply.
        expect_success(misp.tag(created.uuid, "tlp:clear"))
        expect_success(misp.tag(attribute.uuid, "tlp:clear", local=True))
        sighting = MISPSighting()
        sighting.from_dict(type=0, source="Synthetic PyMISP training sighting")
        expect_model(misp.add_sighting(sighting, attribute.uuid, pythonify=True), MISPSighting)

        saved = expect_model(misp.get_event(created.uuid, pythonify=True), MISPEvent)
        if saved.published or int(saved.distribution) != 0:
            raise TrainingError("The fixture must remain unpublished and organisation-only.")
        saved_attribute = next(a for a in saved.attributes if a.uuid == attribute.uuid)
        if saved_attribute.comment != updated.comment or saved_attribute.to_ids:
            raise TrainingError("The saved attribute does not match the intended update.")
        if not any(t.name == "tlp:clear" for t in saved.tags):
            raise TrainingError("Event tag was not saved.")
        if not any(t.name == "tlp:clear" and int(t.local) == 1 for t in saved_attribute.tags):
            raise TrainingError("Direct local attribute tag was not saved.")
        if not saved.objects or not any(
            ref.referenced_uuid == saved_attribute.uuid and ref.relationship_type == "related-to"
            for ref in saved.objects[0].references
        ):
            raise TrainingError("The intended object/reference target was not saved.")
        if not any(int(s.type) == 0 and s.source == sighting.source for s in saved_attribute.sightings):
            raise TrainingError("The synthetic sighting was not saved.")
        rows = collect_pages(misp, event_uuid=saved.uuid, limit=1, max_pages=10)
        if len(rows) != 2:
            raise TrainingError("Expected the top-level and object domain attributes.")
        summary = {"event_uuid": saved.uuid, "domain_attributes": len(rows),
                   "object_reference": True, "local_attribute_tag": True}
    finally:
        # Only this successfully created fixture is deleted; never an arbitrary input UUID.
        expect_success(misp.delete_event(created.uuid))
        if misp.event_exists(created.uuid):
            raise TrainingError("Cleanup could not be confirmed; inspect the fixture locally.")
    return dict(summary, deleted=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="store_true", help="Create, update, tag, sight and delete synthetic data.")
    args = parser.parse_args()
    if not args.run:
        parser.error("Use --run only with a disposable lab and a permitted writer account.")
    try:
        print(run_workshop(connect()))
    except Exception:
        print("Workshop failed. Inspect the lab before retrying; creation/cleanup may be uncertain.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
