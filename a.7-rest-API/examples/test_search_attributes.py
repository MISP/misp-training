"""Offline client-boundary tests; real HTTP checks are described in the README."""
import copy
import unittest
from unittest.mock import Mock

from search_attributes import APIError, MISPClient, iter_attributes


def row(n):
    return {"uuid": f"00000000-0000-4000-8000-{n:012d}", "value": f"case-{n}.example"}


def response(payload, status=200):
    result = Mock(status_code=status)
    result.json.return_value = payload
    return result


class ClientTests(unittest.TestCase):
    def client(self, *responses):
        session = Mock()
        session.request.side_effect = responses
        return MISPClient("https://misp.example/subdir", "training-placeholder", session)

    def test_url_and_key_validation(self):
        for url in ["http://misp.example", "https://u:p@misp.example", "https://misp.example/?key=x", "", "https://misp.example/#x"]:
            with self.subTest(url=url), self.assertRaises(ValueError):
                MISPClient(url, "placeholder")
        for key in ["", "bad key", "bad\nkey"]:
            with self.subTest(key=repr(key)), self.assertRaises(ValueError):
                MISPClient("https://misp.example", key)

    def test_loopback_lab_http(self):
        self.assertEqual(MISPClient("http://127.0.0.1:18082", "placeholder").base_url,
                         "http://127.0.0.1:18082/")

    def test_request_preserves_subdirectory_and_bounds(self):
        client = self.client(response({"response": {"Attribute": []}}))
        self.assertEqual(client.attributes({"returnFormat": "json"}), [])
        args, kwargs = client.session.request.call_args
        self.assertEqual(args, ("POST", "https://misp.example/subdir/attributes/restSearch"))
        self.assertEqual(kwargs["timeout"], (5, 60))
        self.assertIs(kwargs["allow_redirects"], False)
        # TLS verification remains enabled through Requests defaults/environment.
        self.assertNotIn("verify", kwargs)
        client.session.headers.update.assert_called_once()

    def test_http_errors_and_redirects_do_not_become_empty_results(self):
        for status in [302, 400, 403, 404, 429, 500]:
            with self.subTest(status=status), self.assertRaises(APIError):
                self.client(response({}, status)).attributes({})

    def test_html_response_fails(self):
        bad = response({})
        bad.json.side_effect = ValueError("HTML")
        with self.assertRaises(APIError):
            self.client(bad).attributes({})

    def test_error_and_wrong_scope_envelopes_fail(self):
        for payload in [{"errors": ["invalid"]}, {"response": []}, {"Attribute": []}, [], {"response": {"Attribute": "bad"}}]:
            with self.subTest(payload=payload), self.assertRaises(APIError):
                self.client(response(payload)).attributes({})

    def test_missing_or_invalid_uuid_fails(self):
        for record in [{}, {"uuid": "bad"}, {"uuid": None}, "bad"]:
            with self.subTest(record=record), self.assertRaises(APIError):
                self.client(response({"response": {"Attribute": [record]}})).attributes({})

    def test_unsupported_format_or_post_query_filter_fails_before_http(self):
        client = self.client()
        for query in [{"returnFormat": "text"}, {"enforceWarninglist": True}, {"excludeDecayed": True}, [], None]:
            with self.subTest(query=query), self.assertRaises(ValueError):
                client.attributes(query)
            with self.subTest(paginated=query), self.assertRaises(ValueError):
                list(iter_attributes(client, query))
        client.session.request.assert_not_called()

    def test_short_pages_continue_until_empty(self):
        client = self.client(*[
            response({"response": {"Attribute": rows}})
            for rows in [[row(1)], [row(2)], []]
        ])
        self.assertEqual(list(iter_attributes(client, {}, page_size=100)), [row(1), row(2)])
        self.assertEqual([call.kwargs["json"]["page"] for call in client.session.request.call_args_list], [1, 2, 3])

    def test_max_pages_is_a_failure_even_after_yielding(self):
        client = self.client(response({"response": {"Attribute": [row(1)]}}))
        result = iter_attributes(client, {}, max_pages=1)
        self.assertEqual(next(result), row(1))
        with self.assertRaisesRegex(APIError, "incomplete"):
            next(result)

    def test_duplicate_pages_fail(self):
        client = self.client(*[response({"response": {"Attribute": [row(1)]}})] * 2)
        with self.assertRaisesRegex(APIError, "Repeated UUID"):
            list(iter_attributes(client, {}))

    def test_duplicate_records_in_one_page_fail(self):
        client = self.client(response({"response": {"Attribute": [row(1), row(1)]}}))
        with self.assertRaises(APIError):
            list(iter_attributes(client, {}))

    def test_query_not_mutated_and_sort_is_stable(self):
        query = {"tags": {"AND": ["tlp:clear"]}, "page": 99, "limit": 500}
        original = copy.deepcopy(query)
        client = self.client(response({"response": {"Attribute": []}}))
        list(iter_attributes(client, query, page_size=2))
        self.assertEqual(query, original)
        sent = client.session.request.call_args.kwargs["json"]
        self.assertEqual((sent["page"], sent["limit"], sent["order"]), (1, 2, "Attribute.id ASC"))

    def test_invalid_bounds_fail_before_request(self):
        client = self.client()
        for value in [0, 1001, True, "2"]:
            for field in ["page_size", "max_pages"]:
                with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                    list(iter_attributes(client, {}, **{field: value}))
        client.session.request.assert_not_called()


if __name__ == "__main__":
    unittest.main()
