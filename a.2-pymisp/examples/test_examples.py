"""Offline model, failure-path and released-client wire-contract checks."""
import json
import os
import unittest
from unittest.mock import Mock, patch
from uuid import uuid4

from pymisp import MISPAttribute, MISPEvent, MISPShadowAttribute, PyMISP
from requests import Response

from examples.common import Config, TrainingError, expect_model, expect_success
from examples.models import build_event
from examples.read import collect_pages, one_page


def attribute():
    a = MISPAttribute()
    a.from_dict(type="domain", value="unit.example", uuid=str(uuid4()), to_ids=False)
    return a


class ModelsAndConfiguration(unittest.TestCase):
    def test_offline_round_trip_preserves_identity_and_reference(self):
        event = build_event()
        restored = MISPEvent()
        restored.load(event.to_json())
        self.assertEqual(restored.uuid, event.uuid)
        self.assertFalse(restored.published)
        self.assertEqual(int(restored.distribution), 0)
        self.assertFalse(restored.attributes[0].to_ids)
        obj = restored.objects[0]
        obj.to_json(strict=True)  # Validate the domain-ip template requirements.
        self.assertEqual(obj.references[0].referenced_uuid, restored.attributes[0].uuid)
        self.assertEqual({a.object_relation for a in obj.attributes}, {"domain", "ip"})

    def test_url_subpath_ca_and_key_not_in_repr(self):
        with patch.dict(os.environ, {"MISP_URL":"https://misp.example/deployment", "MISP_API_KEY":"test-key", "REQUESTS_CA_BUNDLE":"/tmp/lab-ca.pem"}, clear=True):
            cfg = Config.from_env()
        self.assertEqual(cfg.url, "https://misp.example/deployment/")
        self.assertEqual(cfg.verify, "/tmp/lab-ca.pem")
        self.assertNotIn("test-key", repr(cfg))

    def test_rejects_untrusted_url_shapes_and_missing_key(self):
        for url in ["http://misp.example", "https://user:secret@misp.example", "https://misp.example/?key=x", "https://misp.example/#x", ""]:
            with self.subTest(url=url), patch.dict(os.environ, {"MISP_URL":url, "MISP_API_KEY":"key"}, clear=True):
                with self.assertRaises(ValueError):
                    Config.from_env()
        with patch.dict(os.environ, {"MISP_URL":"http://localhost:8081", "MISP_API_KEY":""}, clear=True):
            with self.assertRaises(ValueError):
                Config.from_env()

    def test_error_or_proposal_is_not_a_saved_attribute(self):
        for response in [{"errors":[403,"denied"]}, MISPShadowAttribute()]:
            with self.assertRaises(TrainingError):
                expect_model(response, MISPAttribute)
        for response in [{"errors":[403,"denied"]}, {"saved":False}, {"success":False}, []]:
            with self.assertRaises(TrainingError):
                expect_success(response)


class ReleasedClientContract(unittest.TestCase):
    def client(self, payload):
        # Exercise the released search/normalisation implementation, not a server.
        misp = PyMISP.__new__(PyMISP)
        misp.root_url = "https://misp.example/deployment/"
        misp.global_pythonify = False
        response = Response()
        response.status_code = 200
        response._content = json.dumps(payload).encode()
        misp._prepare_request = Mock(return_value=response)
        return misp

    def test_search_parameter_mapping_and_typed_response(self):
        a = attribute()
        misp = self.client({"response":{"Attribute":[json.loads(a.to_json())]}})
        rows = one_page(misp)
        self.assertIsInstance(rows[0], MISPAttribute)
        args, kwargs = misp._prepare_request.call_args
        self.assertEqual(args, ("POST", "https://misp.example/deployment/attributes/restSearch"))
        query = kwargs["data"]
        self.assertEqual(query["type"], "domain")
        self.assertEqual(query["returnFormat"], "json")
        self.assertEqual(query["includeEventUuid"], 1)
        self.assertEqual(query["includeEventTags"], 1)
        self.assertNotIn("to_ids", query)
        self.assertIsNone(query["published"])

    def test_error_dictionary_and_to_ids_array(self):
        misp = self.client({"errors":[403,"denied"]})
        with self.assertRaises(TrainingError):
            one_page(misp)
        with self.assertRaises(ValueError):
            misp.search(controller="attributes", to_ids=[0,1])


class BoundedTraversal(unittest.TestCase):
    def test_short_role_capped_pages_continue_to_empty(self):
        a, b = attribute(), attribute()
        misp = Mock()
        misp.search.side_effect = [[a], [b], []]
        self.assertEqual(collect_pages(misp, limit=100), [a,b])
        self.assertEqual([c.kwargs["page"] for c in misp.search.call_args_list], [1,2,3])

    def test_repetition_and_bound_fail_instead_of_claiming_completion(self):
        a = attribute()
        for responses, maximum in [([[a],[a]], 3), ([[a]], 1)]:
            misp = Mock()
            misp.search.side_effect = responses
            with self.assertRaises(TrainingError):
                collect_pages(misp, max_pages=maximum)


if __name__ == "__main__":
    unittest.main()
