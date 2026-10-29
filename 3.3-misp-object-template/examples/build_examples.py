#!/usr/bin/env python3
"""Create a synthetic event offline using explicitly supplied template definitions."""
import argparse
import json
from pathlib import Path

import jsonschema
from pymisp import MISPEvent, MISPObject


def load_definitions(repository):
    schema = json.loads((repository / "schema_objects.json").read_text())
    domain = json.loads((repository / "objects/domain-ip/definition.json").read_text())
    review = json.loads(Path(__file__).with_name("training-review.json").read_text())
    for definition in (domain, review):
        jsonschema.validate(definition, schema)
        relations = set(definition["attributes"])
        for key in ("required", "requiredOneOf"):
            if not set(definition.get(key, [])) <= relations:
                raise ValueError(f"{key} refers to an undefined relation")
    return domain, review


def new_object(definition):
    return MISPObject(definition["name"], strict=True, standalone=False,
                      misp_objects_template_custom=definition,
                      default_attributes_parameters={"to_ids": False})


def build_event(repository):
    domain_definition, review_definition = load_definitions(repository)
    observation = new_object(domain_definition)
    observation.add_attribute("domain", value="workshop.example", to_ids=False)
    observation.add_attribute("ip", value="192.0.2.10", to_ids=False)
    observation.add_attribute("ip", value="192.0.2.11", to_ids=False)
    review = new_object(review_definition)
    review.add_attribute("case-reference", value="TRAINING-001", to_ids=False)
    review.add_attribute("domain", value="workshop.example", to_ids=False)
    review.add_attribute("status", value="reviewed", to_ids=False)
    # Object references use instance UUIDs, never template UUIDs.
    relationships = json.loads((repository / "relationships/definition.json").read_text())
    if not any(r["name"] == "related-to" for r in relationships["values"]):
        raise ValueError("The selected relationship catalogue lacks related-to")
    review.add_reference(observation.uuid, "related-to")
    # Validate each object explicitly before serialising its containing event.
    observation.to_json(strict=True)
    review.to_json(strict=True)
    event = MISPEvent()
    event.info = "Object-template training: synthetic review"
    event.distribution = 0
    event.threat_level_id = 4
    event.analysis = 0
    event.published = False
    event.add_object(observation)
    event.add_object(review)
    return event


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", type=Path, help="Local MISP/misp-objects checkout")
    args = parser.parse_args()
    print(build_event(args.repository).to_json(indent=2))
