#!/usr/bin/env python3
"""Bounded, read-only JSON attribute export for the training workshop."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
from urllib.parse import urlsplit
from uuid import UUID

import requests


class APIError(RuntimeError):
    """A failed or incomplete export; do not advance a checkpoint."""


class MISPClient:
    # These filters do not deliberately remove rows after SQL pagination.
    FILTERS = {
        "returnFormat", "value", "type", "category", "tags", "eventid", "uuid",
        "timestamp", "attribute_timestamp", "event_timestamp", "publish_timestamp",
        "published", "to_ids", "includeEventUuid", "includeEventTags",
        "includeWarninglistHits", "order", "limit", "page",
    }

    def __init__(self, base_url: str, api_key: str, session=None):
        parsed = urlsplit(base_url)
        if (not parsed.hostname or parsed.username or parsed.password
                or parsed.query or parsed.fragment):
            raise ValueError("Use an instance base URL without credentials, query or fragment.")
        if parsed.scheme != "https" and not (
            parsed.scheme == "http" and parsed.hostname in {"localhost", "127.0.0.1", "::1"}
        ):
            raise ValueError("Use HTTPS; HTTP is allowed only for an isolated loopback lab.")
        if not api_key or any(c.isspace() for c in api_key):
            raise ValueError("Set a nonempty MISP_API_KEY without whitespace.")
        self.base_url = base_url.rstrip("/") + "/"
        self.api_key = api_key
        self.session = session if session is not None else requests.Session()
        self.session.headers.update({
            "Authorization": api_key, "Accept": "application/json",
            "Content-Type": "application/json",
        })

    @classmethod
    def from_env(cls):
        return cls(os.environ.get("MISP_URL", ""), os.environ.get("MISP_API_KEY", ""))

    def _json(self, method, path, body=None):
        response = self.session.request(
            method, self.base_url + path, json=body,
            timeout=(5, 60), allow_redirects=False,
        )
        if not 200 <= response.status_code < 300:
            raise APIError(f"HTTP {response.status_code}; check URL, key, role and request. Redirects are not followed.")
        try:
            payload = response.json()
        except ValueError:
            raise APIError("Expected JSON; check the URL, proxy and authentication.") from None
        if not isinstance(payload, dict) or "errors" in payload:
            raise APIError("Unexpected JSON or an API error envelope.")
        return payload

    def version(self):
        return self._json("GET", "servers/getVersion")

    def attributes(self, query):
        if not isinstance(query, dict) or set(query) - self.FILTERS:
            raise ValueError("Use the documented JSON SQL filters; post-query filters are outside this sample.")
        if query.get("returnFormat", "json") != "json":
            raise ValueError("This parser supports returnFormat=json only.")
        payload = self._json("POST", "attributes/restSearch", query)
        response = payload.get("response")
        if not isinstance(response, dict) or not isinstance(response.get("Attribute"), list):
            raise APIError("Expected response.Attribute as an array; export is incomplete.")
        rows = response["Attribute"]
        for row in rows:
            if not isinstance(row, dict) or not isinstance(row.get("uuid"), str):
                raise APIError("An attribute has no UUID; export is incomplete.")
            try:
                UUID(row["uuid"])
            except ValueError:
                raise APIError("An attribute UUID is invalid; export is incomplete.") from None
        return rows


def iter_attributes(client, query, page_size=100, max_pages=20):
    """Stable ordering reduces drift; it does not create a database snapshot."""
    if not isinstance(query, dict) or query.get("returnFormat", "json") != "json":
        raise ValueError("query must be a JSON object with returnFormat=json.")
    if type(page_size) is not int or not 1 <= page_size <= 1000:
        raise ValueError("page_size must be an integer from 1 to 1000.")
    if type(max_pages) is not int or not 1 <= max_pages <= 1000:
        raise ValueError("max_pages must be an integer from 1 to 1000.")
    seen = set()
    for page in range(1, max_pages + 1):
        request = dict(query, returnFormat="json", limit=page_size, page=page,
                       order="Attribute.id ASC")
        rows = client.attributes(request)
        if not rows:
            return
        ids = [str(UUID(row["uuid"])) for row in rows]
        if len(ids) != len(set(ids)) or seen.intersection(ids):
            raise APIError("Repeated UUID across pages; data may have changed. Export is incomplete.")
        seen.update(ids)
        yield from rows
        # A role can cap limit below page_size: a short page is not the end.
    raise APIError("Reached max_pages before an empty page; export is incomplete.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", type=Path, default=Path(__file__).with_name("attribute-search.json"))
    parser.add_argument("--page-size", type=int, default=100)
    parser.add_argument("--max-pages", type=int, default=20)
    args = parser.parse_args()
    try:
        client = MISPClient.from_env()
        query = json.loads(args.query.read_text())
        for row in iter_attributes(client, query, args.page_size, args.max_pages):
            print(json.dumps(row, ensure_ascii=False))
    except (APIError, ValueError, OSError, requests.RequestException) as exc:
        # Avoid dumping request headers, keys or server response bodies.
        detail = str(exc) if isinstance(exc, APIError) else "Check local configuration, query and connection."
        print(f"Export failed: {detail} Output may be partial. No checkpoint was saved.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
