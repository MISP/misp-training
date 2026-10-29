#!/usr/bin/env python3
"""Offline template/instance checks; does not test a live MISP server."""
import json
from pathlib import Path
import sys
from uuid import UUID

import jsonschema
from pymisp import MISPEvent
from pymisp.exceptions import InvalidMISPObject, NewAttributeError

from build_examples import build_event, load_definitions, new_object

repository = Path(sys.argv[1])
domain, definition = load_definitions(repository)
UUID(definition["uuid"])
assert definition["version"] >= 1
assert not any(json.loads(p.read_text())["uuid"] == definition["uuid"]
               for p in (repository / "objects").glob("*/definition.json"))
event = build_event(repository)
roundtrip = MISPEvent()
roundtrip.load(event.to_json())
assert len(roundtrip.objects) == 2
observation, review = roundtrip.objects
assert observation.template_uuid == domain["uuid"]
assert int(observation.template_version) == domain["version"]
assert len([a for a in observation.attributes if a.object_relation == "ip"]) == 2
assert all(not a.to_ids for obj in roundtrip.objects for a in obj.attributes)
assert review.references[0].referenced_uuid == observation.uuid
assert review.references[0].referenced_uuid != observation.template_uuid
assert not roundtrip.published and roundtrip.distribution == 0

def fails(attributes):
    obj = new_object(definition)
    try:
        for relation, value in attributes:
            obj.add_attribute(relation, value=value)
        obj.to_json(strict=True)
    except (InvalidMISPObject, NewAttributeError):
        return
    raise AssertionError("Invalid object unexpectedly passed strict validation")

fails([("domain", "workshop.example")])  # missing required
fails([("case-reference", "TRAINING-001")])  # missing requiredOneOf
fails([("case-reference", "A"), ("case-reference", "B"), ("domain", "workshop.example")])
fails([("unknown-relation", "value")])
# The JSON schema catches unsupported property names.
bad = json.loads(json.dumps(definition))
bad["attributes"]["status"]["sane_defaults"] = ["reviewed"]
try:
    jsonschema.validate(bad, json.loads((repository / "schema_objects.json").read_text()))
except jsonschema.ValidationError:
    pass
else:
    raise AssertionError("Misspelled sane_defaults passed schema validation")
print("PASS: schema/identity, round-trip, references, flags and five negative cases.")
