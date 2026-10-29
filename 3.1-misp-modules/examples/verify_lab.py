#!/usr/bin/env python3
"""Exercise the documented loopback lab; no provider APIs or publication calls."""

import argparse
import base64
import importlib.util
import json
from pathlib import Path
import unittest
from urllib.request import Request, urlopen
import uuid

HERE = Path(__file__).resolve().parent
BASE_URL = "http://127.0.0.1:6666"
spec = importlib.util.spec_from_file_location("training_uppercase", HERE / "custom/expansion/training_uppercase.py")
training = importlib.util.module_from_spec(spec)
spec.loader.exec_module(training)


class ModuleContract(unittest.TestCase):
    def test_dictionary_and_legacy_interfaces_agree(self):
        body = {"text": "misp training", "config": {"prefix": "DEMO: "}}
        expected = {"results": [{"types": ["text"], "values": ["DEMO: MISP TRAINING"]}]}
        self.assertEqual(training.dict_handler(body), expected)
        self.assertEqual(training.handler(json.dumps(body)), expected)

    def test_invalid_inputs_produce_module_errors(self):
        for body in (None, {}, {"text": ""}, {"text": 42}, {"text": "x", "config": []},
                     {"text": "x", "config": {"prefix": False}}):
            with self.subTest(body=body):
                self.assertIn("error", training.dict_handler(body))
        self.assertIn("error", training.handler("not JSON"))

    def test_metadata_is_not_mutated_by_a_caller(self):
        metadata = training.version()
        metadata["config"].append("unexpected")
        self.assertEqual(training.version()["config"], ["prefix"])


class ServiceContract(unittest.TestCase):
    def request(self, path, body=None):
        data = json.dumps(body).encode() if body is not None else None
        req = Request(BASE_URL + path, data=data, headers={"Content-Type": "application/json"})
        with urlopen(req, timeout=15) as response:
            self.assertEqual(response.status, 200)
            return json.load(response)

    def fixture(self, name):
        return json.loads((HERE / name).read_text())

    def first_value(self, result):
        self.assertNotIn("error", result)
        return result["results"][0]["values"][0]

    def test_health_and_version(self):
        self.assertIs(self.request("/healthcheck")["status"], True)
        self.assertTrue(self.request("/version")["version"])

    def test_runtime_discovery_and_openapi(self):
        modules = {m["name"]: m for m in self.request("/modules")}
        for name in ("training_uppercase", "extract_url_components", "zeek_intel_export", "osquery_pack_publish"):
            self.assertIn(name, modules, f"Missing {name}: check the installed package and startup logs")
        self.assertEqual(modules["training_uppercase"]["type"], "expansion")
        api = self.request("/openapi.json")
        for path in ("/query", "/modules", "/statistics", "/healthcheck", "/version"):
            self.assertIn(path, api["paths"])

    def test_local_default_and_api_override(self):
        self.assertEqual(self.first_value(self.request("/query", {"module": "training_uppercase", "text": "misp"})), "LOCAL: MISP")
        self.assertEqual(self.first_value(self.request("/query", {"module": "training_uppercase", "text": "misp", "config": {"prefix": "API: "}})), "API: MISP")

    def test_empty_config_uses_explicit_fallback(self):
        for prefix in ("", None):
            with self.subTest(prefix=prefix):
                result = self.request("/query", {"module": "training_uppercase", "text": "misp", "config": {"prefix": prefix}})
                self.assertEqual(self.first_value(result), "LOCAL: MISP")

    def test_error_envelope_even_with_http_success(self):
        self.assertIn("error", self.request("/query", {"module": "training_uppercase", "text": ""}))

    def test_url_object_retains_source_reference(self):
        body = self.fixture("url-request.json")
        result = self.request("/query", body)
        self.assertNotIn("error", result)
        obj = next(o for o in result["results"]["Object"] if o["name"] == "url")
        values = {a["object_relation"]: a["value"] for a in obj["Attribute"]}
        self.assertEqual(values["host"], "portal.example.org")
        self.assertEqual(values["domain"], "example.org")
        self.assertEqual(values["resource_path"], "/a")
        self.assertTrue(any(r["referenced_uuid"] == body["attribute"]["uuid"] for r in obj["ObjectReference"]))

    def test_zeek_export_decodes_and_filters_non_ids(self):
        result = self.request("/query", self.fixture("export-request.json"))
        self.assertNotIn("error", result)
        content = base64.b64decode(result["data"], validate=True).decode("ascii")
        self.assertIn("#fields", content)
        self.assertIn("example.org\tIntel::DOMAIN", content)
        self.assertIn("192.0.2.10\tIntel::ADDR", content)
        self.assertNotIn("not-selected.example", content)

    def test_osquery_action_is_only_a_dry_run(self):
        result = self.request("/query", self.fixture("action-request.json"))
        self.assertNotIn("error", result)
        self.assertEqual(result["data"]["status"], "planned")
        self.assertEqual(result["data"]["filename"], "misp-training.conf")
        self.assertTrue(result["data"]["pack"]["queries"])

    def test_cache_hit_is_visible_in_statistics(self):
        before = self.request("/statistics")["cache"]["modules"]["training_uppercase"]["hits"]
        body = {"module": "training_uppercase", "text": "cache-" + str(uuid.uuid4())}
        self.assertEqual(self.request("/query", body), self.request("/query", body))
        stats = self.request("/statistics")
        self.assertGreater(stats["cache"]["modules"]["training_uppercase"]["hits"], before)
        self.assertIn("queries", stats["modules"]["training_uppercase"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default=BASE_URL, help="URL of the service started with this lab's flags")
    args, unittest_args = parser.parse_known_args()
    BASE_URL = args.url.rstrip("/")
    unittest.main(argv=[__file__, *unittest_args])
