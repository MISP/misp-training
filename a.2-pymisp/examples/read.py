"""A read-only JSON query; optional bounded traversal for this fixed SQL-filtered query."""
import argparse
import sys
from uuid import UUID

from pymisp import MISPAttribute

from examples.common import TrainingError, connect


def one_page(misp, *, event_uuid=None, page=1, limit=10):
    if type(page) is not int or page < 1 or type(limit) is not int or not 1 <= limit <= 1000:
        raise ValueError("Use a positive page and a limit from 1 to 1000.")
    filters = {"eventid": str(UUID(event_uuid))} if event_uuid else {}
    rows = misp.search(
        controller="attributes", return_format="json",
        type_attribute="domain", value="%.example",
        include_event_uuid=True, include_event_tags=True,
        order="Attribute.id ASC", limit=limit, page=page,
        pythonify=True, **filters,
    )
    # Omit to_ids and published here to include both states in ordinary JSON.
    if not isinstance(rows, list) or not all(isinstance(row, MISPAttribute) for row in rows):
        raise TrainingError("Expected a list of MISPAttribute objects, not an API error/proposal.")
    for row in rows:
        try:
            UUID(row.uuid)
        except (AttributeError, TypeError, ValueError):
            raise TrainingError("A result has no valid UUID; traversal is incomplete.") from None
    return rows


def collect_pages(misp, *, event_uuid=None, limit=10, max_pages=20):
    """No post-query filters, checkpoint or downstream writes; not a generic sync client."""
    if type(max_pages) is not int or not 1 <= max_pages <= 1000:
        raise ValueError("Use a max_pages bound from 1 to 1000.")
    result, seen = [], set()
    for page in range(1, max_pages + 1):
        rows = one_page(misp, event_uuid=event_uuid, page=page, limit=limit)
        if not rows:
            return result
        ids = [str(UUID(row.uuid)) for row in rows]
        if len(set(ids)) != len(ids) or seen.intersection(ids):
            raise TrainingError("Repeated UUID; concurrent changes may have made traversal incomplete.")
        seen.update(ids)
        result.extend(rows)
        # A role can cap the requested limit: a short page is not completion.
    raise TrainingError("Reached max_pages before an empty page; traversal is incomplete.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--event-uuid", help="Restrict to an event visible to this key.")
    parser.add_argument("--page", type=int, default=1)
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--all-pages", action="store_true", help="Traverse this fixed query until an empty page.")
    parser.add_argument("--max-pages", type=int, default=20)
    args = parser.parse_args()
    if args.all_pages and args.page != 1:
        parser.error("--all-pages starts at page 1; omit --page.")
    try:
        misp = connect()
        if args.all_pages:
            rows = collect_pages(misp, event_uuid=args.event_uuid, limit=args.limit, max_pages=args.max_pages)
            print(f"Completed bounded query: {len(rows)} attributes.")
        else:
            rows = one_page(misp, event_uuid=args.event_uuid, limit=args.limit, page=args.page)
            print(f"One page: {len(rows)} attributes; not a complete export.")
        for row in rows:
            print(row.uuid, row.type)
    except Exception:
        print("Read failed. Check configuration, access and the API response locally. No checkpoint was saved.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
