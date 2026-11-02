#!/usr/bin/env python3
"""Offline schema and semantic checks against a supplied misp-galaxy checkout."""
import copy
import json
from pathlib import Path
import sys
from uuid import UUID

import jsonschema

from explore import search


def check_fixture(galaxy, package, repository):
    for definition, schema in [(galaxy, "schema_galaxies.json"), (package, "schema_clusters.json")]:
        jsonschema.validate(definition, json.loads((repository / schema).read_text()))
        UUID(definition["uuid"])
    assert galaxy["type"] == package["type"]
    ids = [v["uuid"] for v in package["values"]]
    assert len(ids) == len(set(ids)), "Duplicate fixture cluster UUID"
    for value in package["values"]:
        UUID(value["uuid"])
        assert value["value"].strip()
        for edge in value.get("related", []):
            assert edge["dest-uuid"] in ids, "Dangling fixture reference"
            assert edge["type"].strip()


if __name__ == "__main__":
    repository = Path(sys.argv[1])
    root = Path(__file__).parent
    galaxy = json.loads((root / "galaxy.json").read_text())
    package = json.loads((root / "clusters.json").read_text())
    check_fixture(galaxy, package, repository)
    for kind in ("type", "reference", "duplicate", "empty"):
        bad = copy.deepcopy(package)
        if kind == "type":
            bad["type"] = "other"
        elif kind == "reference":
            bad["values"][0]["related"][0]["dest-uuid"] = str(UUID(int=0))
        elif kind == "duplicate":
            bad["values"][1]["uuid"] = bad["values"][0]["uuid"]
        else:
            bad["values"][0]["value"] = " "
        try:
            check_fixture(galaxy, bad, repository)
        except AssertionError:
            pass
        else:
            raise AssertionError(f"Negative case passed: {kind}")
    results = search(repository, "T1059", "mitre-enterprise-attack-attack-pattern", limit=3)
    assert results and any("T1059" in str(r["meta"].get("external_id")) for r in results)
    assert search(repository, "no-such-training-concept-76b1d3") == []
    try:
        search(repository, "T1059", "../outside")
    except ValueError:
        pass
    else:
        raise AssertionError("Unknown collection accepted")
    print("PASS: fixture schemas, identities, relation targets, four negative cases and real knowledge-base lookup.")
