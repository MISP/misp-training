#!/usr/bin/env python3
"""One read-only page with current PyMISP; not a complete export."""
import os

from pymisp import MISPAttribute, PyMISP

from search_attributes import MISPClient


def search_page():
    config = MISPClient.from_env()  # Same base-URL and key checks as the raw client.
    misp = PyMISP(config.base_url, config.api_key,
                  ssl=os.environ.get("REQUESTS_CA_BUNDLE") or True, timeout=(5, 60))
    rows = misp.search(
        controller="attributes", return_format="json",
        type_attribute="domain", value="%.example",
        include_event_uuid=True, include_event_tags=True,
        limit=100, page=1, order="Attribute.id ASC", pythonify=True,
    )
    # PyMISP can return an error dictionary instead of raising an exception.
    if not isinstance(rows, list) or not all(isinstance(row, MISPAttribute) for row in rows):
        raise RuntimeError("Expected a list of MISPAttribute objects; inspect the API error locally.")
    return rows


if __name__ == "__main__":
    rows = search_page()
    print(f"First page: {len(rows)} attributes (not a complete export).")
    for row in rows:
        print(row.uuid, row.type)
