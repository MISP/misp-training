#!/usr/bin/env python3
"""Check the reference exercise; add --url to check a running custom-module service."""

import argparse
import importlib.util
import json
import sys
import unittest
from copy import deepcopy
from pathlib import Path
from urllib.request import Request, urlopen

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    "training_domain_normalize", HERE / "custom/expansion/training_domain_normalize.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
FIXTURE = json.loads((HERE / "request.json").read_text())
BASE_URL = None


def output_name(result):
    return result["results"]["Object"][0]["Attribute"][0]["value"]


class ModuleContract(unittest.TestCase):
    def body(self, value="Example.ORG.", kind="domain"):
        body = deepcopy(FIXTURE)
        body["attribute"].update(value=value, type=kind)
        return body

    def test_ascii_and_hostname(self):
        for kind in ("domain", "hostname"):
            with self.subTest(kind=kind):
                self.assertEqual(output_name(module.dict_handler(self.body(kind=kind))), "example.org")

    def test_idna(self):
        self.assertEqual(output_name(module.dict_handler(deepcopy(FIXTURE))), "xn--bcher-kva.example")

    def test_source_reference_and_detection_flags(self):
        result = module.dict_handler(deepcopy(FIXTURE))["results"]
        source = result["Attribute"][0]
        self.assertEqual(source["uuid"], FIXTURE["attribute"]["uuid"])
        self.assertEqual(source["value"], FIXTURE["attribute"]["value"])
        self.assertEqual(source["comment"], FIXTURE["attribute"]["comment"])
        self.assertIs(source["to_ids"], True)
        obj = result["Object"][0]
        self.assertEqual(obj["name"], "domain-ip")
        self.assertIs(obj["Attribute"][0]["to_ids"], False)
        reference = obj["ObjectReference"][0]
        self.assertEqual(reference["referenced_uuid"], source["uuid"])
        self.assertEqual(reference["relationship_type"], "derived-from")

    def test_input_is_not_mutated(self):
        body = deepcopy(FIXTURE)
        before = deepcopy(body)
        module.dict_handler(body)
        self.assertEqual(body, before)

    def test_results_are_independent(self):
        first = module.dict_handler(self.body())
        first["results"]["Object"][0]["Attribute"][0]["value"] = "modified"
        second = module.dict_handler(self.body())
        self.assertEqual(output_name(second), "example.org")
        self.assertNotEqual(first["results"]["Object"][0]["uuid"], second["results"]["Object"][0]["uuid"])

    def test_invalid_inputs(self):
        bodies = [None, {}, {"attribute": []}, self.body(kind="text")]
        for value in (
            "",
            None,
            42,
            "*.example.org",
            "https://example.org",
            "_srv.example",
            "-bad.example",
            "bad-.example",
            "bad..example",
            "example.org..",
            "localhost",
            "192.0.2.10",
            "2001:db8::1",
            "a" * 64 + ".example",
            ".".join(["a" * 63] * 5),
        ):
            bodies.append(self.body(value))
        missing_uuid = self.body()
        del missing_uuid["attribute"]["uuid"]
        invalid_uuid = self.body()
        invalid_uuid["attribute"]["uuid"] = "not-a-uuid"
        bodies.extend([missing_uuid, invalid_uuid])
        for body in bodies:
            with self.subTest(body=body):
                self.assertIn("error", module.dict_handler(body))
        self.assertIn("error", module.handler("not JSON"))
        self.assertIs(module.handler(), False)

    def test_legacy_and_dictionary_contracts(self):
        body = self.body()
        self.assertEqual(output_name(module.handler(json.dumps(body))), output_name(module.dict_handler(body)))
        json.dumps(module.dict_handler(body))

    def test_metadata_is_a_fresh_copy(self):
        meta = module.version()
        meta["config"].append("unexpected")
        meta["requirements"].append("unexpected")
        introspection = module.introspection()
        introspection["input"].append("unexpected")
        self.assertEqual(module.version()["config"], [])
        self.assertEqual(module.version()["requirements"], ["pymisp"])
        self.assertEqual(module.introspection()["input"], ["domain", "hostname"])


class ServiceContract(unittest.TestCase):
    def request(self, path, body=None):
        req = Request(
            BASE_URL + path,
            data=json.dumps(body).encode() if body is not None else None,
            headers={"Content-Type": "application/json"},
        )
        with urlopen(req, timeout=15) as response:
            self.assertEqual(response.status, 200)
            return json.load(response)

    def test_discovery_and_openapi(self):
        self.assertIs(self.request("/healthcheck")["status"], True)
        entries = [m for m in self.request("/modules") if m["name"] == "training_domain_normalize"]
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["type"], "expansion")
        self.assertEqual(entries[0]["mispattributes"]["format"], "misp_standard")
        self.assertIn("/query", self.request("/openapi.json")["paths"])

    def test_structured_query(self):
        result = self.request("/query", deepcopy(FIXTURE))
        self.assertEqual(output_name(result), "xn--bcher-kva.example")
        self.assertEqual(
            result["results"]["Object"][0]["ObjectReference"][0]["referenced_uuid"], FIXTURE["attribute"]["uuid"]
        )

    def test_invalid_query_is_an_error_envelope(self):
        body = deepcopy(FIXTURE)
        body["attribute"]["value"] = "*.example.org"
        result = self.request("/query", body)
        self.assertIn("error", result)
        self.assertNotIn("results", result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", help="Add HTTP checks against a running local training service")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(ModuleContract)
    if args.url:
        BASE_URL = args.url.rstrip("/")
        suite.addTests(loader.loadTestsFromTestCase(ServiceContract))
    else:
        print("Running 8 unit tests; HTTP checks not requested (use --url).", flush=True)
    result = unittest.TextTestRunner(verbosity=2 if args.verbose else 1).run(suite)
    sys.exit(not result.wasSuccessful())
