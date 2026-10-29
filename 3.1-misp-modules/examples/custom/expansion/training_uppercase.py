"""Local, dependency-free teaching module; not an intelligence source."""

import json

moduleinfo = {
    "version": "1.0",
    "author": "MISP Project training contributors",
    "name": "Training uppercase",
    "description": "Uppercase synthetic training text without network access.",
    "module-type": ["expansion", "hover"],
}
moduleconfig = ["prefix"]
mispattributes = {"input": ["text"], "output": ["text"]}


def introspection():
    return dict(mispattributes)


def version():
    return {**moduleinfo, "config": list(moduleconfig)}


def dict_handler(request):
    if not isinstance(request, dict):
        return {"error": "Expected a request object."}
    value = request.get("text")
    if not isinstance(value, str) or not value.strip():
        return {"error": "A nonempty text value is required."}
    config = request.get("config", {})
    if not isinstance(config, dict):
        return {"error": "config must be an object."}
    prefix = config.get("prefix", "")
    if not isinstance(prefix, str):
        return {"error": "prefix must be a string."}
    return {"results": [{"types": ["text"], "values": [prefix + value.upper()]}]}


def handler(q=False):
    """Compatibility adapter for callers using the legacy JSON interface."""
    if q is False:
        return False
    try:
        request = json.loads(q)
    except (TypeError, ValueError):
        return {"error": "Invalid JSON."}
    return dict_handler(request)
