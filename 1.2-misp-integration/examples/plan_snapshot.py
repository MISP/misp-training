#!/usr/bin/env python3
"""Print a consumer-state reconciliation plan; never call a service or apply it.

Inputs are training consumer manifests, not native MISP API responses. Their
completeness assertion must be established by a separate exporter in real use.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from uuid import UUID


def validate_snapshot(snapshot):
    if not isinstance(snapshot, dict) or snapshot.get("complete") is not True:
        raise ValueError("Refusing an incomplete or unverified snapshot.")
    policy = snapshot.get("policy")
    if not isinstance(policy, str) or not policy.strip():
        raise ValueError("A nonempty selection-policy version is required.")
    rows = snapshot.get("indicators")
    if not isinstance(rows, list):
        raise ValueError("indicators must be a complete array.")
    by_uuid = {}
    for row in rows:
        fields = {"uuid", "event_uuid", "type", "value"}
        if not isinstance(row, dict) or set(row) != fields:
            raise ValueError("Each indicator needs uuid, event_uuid, type and value only.")
        if any(not isinstance(row[k], str) or not row[k].strip() for k in fields):
            raise ValueError("Indicator fields must be nonempty strings.")
        try:
            identifier = str(UUID(row["uuid"]))
            event_identifier = str(UUID(row["event_uuid"]))
        except ValueError:
            raise ValueError("Indicator or event UUID is invalid.") from None
        if identifier in by_uuid:
            raise ValueError("Duplicate attribute UUID; refusing ambiguous state.")
        by_uuid[identifier] = dict(row, uuid=identifier, event_uuid=event_identifier)
    return policy, by_uuid


def plan(current, desired):
    current_policy, old = validate_snapshot(current)
    desired_policy, new = validate_snapshot(desired)
    if current_policy != desired_policy:
        raise ValueError("Policy versions differ; review the policy transition first.")
    shared = old.keys() & new.keys()
    return {
        "mode": "plan-only",
        "policy": desired_policy,
        "add": [new[k] for k in sorted(new.keys() - old.keys())],
        "update": [{"before": old[k], "after": new[k]}
                   for k in sorted(shared) if old[k] != new[k]],
        "remove": [old[k] for k in sorted(old.keys() - new.keys())],
        "unchanged": [k for k in sorted(shared) if old[k] == new[k]],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("current", type=Path)
    parser.add_argument("desired", type=Path)
    args = parser.parse_args()
    try:
        result = plan(json.loads(args.current.read_text()),
                      json.loads(args.desired.read_text()))
    except (OSError, ValueError) as exc:
        parser.exit(2, f"No plan produced: {exc}\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
