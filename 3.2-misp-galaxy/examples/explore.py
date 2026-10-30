#!/usr/bin/env python3
"""Read a local misp-galaxy checkout; no API key, network calls or modifications."""
import argparse
import json
from pathlib import Path


def collections(repository):
    for path in sorted((repository / "clusters").glob("*.json")):
        yield path, json.loads(path.read_text())


def statistics(repository):
    packages = list(collections(repository))
    values = [v for _, package in packages for v in package.get("values", [])]
    return {
        "galaxy_definition_files": len(list((repository / "galaxies").glob("*.json"))),
        "cluster_collection_files": len(packages),
        "cluster_entries": len(values),
        "unique_cluster_uuids": len({v["uuid"] for v in values if v.get("uuid")}),
        "related_edges": sum(len(v.get("related", [])) for v in values),
    }


def search(repository, term, collection=None, limit=10):
    if not term.strip() or not 1 <= limit <= 1000:
        raise ValueError("Use a nonempty term and a limit from 1 to 1000.")
    matched_collection = collection is None
    results = []
    for path, package in collections(repository):
        if collection is not None and path.stem != collection:
            continue
        matched_collection = True
        for value in package.get("values", []):
            meta = value.get("meta", {})
            fields = [value.get("value", "")]
            for key in ("synonyms", "external_id"):
                item = meta.get(key, [])
                fields.extend(item if isinstance(item, list) else [item])
            if any(term.casefold() in str(item).casefold() for item in fields):
                results.append({
                    "collection": path.stem, "type": package["type"],
                    "collection_version": package["version"],
                    "uuid": value.get("uuid"), "value": value["value"],
                    "meta": meta, "related": value.get("related", []),
                    "revoked": value.get("revoked", False),
                    "description": value.get("description", ""),
                })
                if len(results) == limit:
                    return results
    if not matched_collection:
        raise ValueError("Unknown collection filename stem.")
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", type=Path)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--stats", action="store_true")
    group.add_argument("--search")
    parser.add_argument("--collection", help="Exact filename stem, for example mitre-enterprise-attack-attack-pattern")
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()
    if not (args.repository / "clusters").is_dir():
        parser.error("Supply a misp-galaxy checkout with a clusters directory.")
    try:
        result = statistics(args.repository) if args.stats else search(
            args.repository, args.search, args.collection, args.limit)
    except ValueError as error:
        parser.error(str(error))
    print(json.dumps(result, indent=2, ensure_ascii=False))
