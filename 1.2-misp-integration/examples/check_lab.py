#!/usr/bin/env python3
"""Offline checks of the lab's failure boundaries, with no network or writes."""
import copy
import json
from pathlib import Path
import unittest

from plan_snapshot import plan


class SnapshotLab(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).parent
        self.current = json.loads((root / "current-state.json").read_text())
        self.desired = json.loads((root / "desired-state.json").read_text())

    def test_expected_consumer_changes(self):
        result = plan(self.current, self.desired)
        self.assertEqual([r["value"] for r in result["add"]], ["new.example"])
        self.assertEqual([r["value"] for r in result["remove"]], ["old.example"])
        self.assertEqual(len(result["unchanged"]), 1)
        self.assertEqual(result["update"], [])
        self.assertEqual(result["mode"], "plan-only")

    def test_same_uuid_changed_value_is_an_update(self):
        changed = copy.deepcopy(self.desired)
        changed["indicators"][0]["value"] = "corrected.example"
        result = plan(self.current, changed)
        self.assertEqual(len(result["update"]), 1)
        self.assertEqual(result["update"][0]["before"]["value"], "keep.example")
        self.assertEqual(result["update"][0]["after"]["value"], "corrected.example")

    def test_partial_empty_export_must_not_remove_everything(self):
        incomplete = dict(self.desired, complete=False, indicators=[])
        with self.assertRaisesRegex(ValueError, "incomplete"):
            plan(self.current, incomplete)

    def test_policy_transition_requires_review(self):
        changed = dict(self.desired, policy="different-selection-v2")
        with self.assertRaisesRegex(ValueError, "Policy versions differ"):
            plan(self.current, changed)

    def test_duplicate_identity_is_ambiguous(self):
        duplicate = copy.deepcopy(self.desired)
        duplicate["indicators"].append(copy.deepcopy(duplicate["indicators"][0]))
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            plan(self.current, duplicate)

    def test_invalid_identity_is_not_a_removal_signal(self):
        broken = copy.deepcopy(self.desired)
        broken["indicators"][0]["uuid"] = "not-a-uuid"
        with self.assertRaisesRegex(ValueError, "UUID is invalid"):
            plan(self.current, broken)


if __name__ == "__main__":
    unittest.main()
