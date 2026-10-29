"""Local-only reference exercise, not a proposed new upstream integration."""

import ipaddress
import json
import re
from copy import deepcopy
from uuid import UUID

from pymisp import MISPEvent, MISPObject

moduleinfo = {
    "version": "1.0",
    "author": "MISP Project training contributors",
    "name": "Training domain normalization",
    "description": "Demonstrate a MISP-standard, local domain transformation.",
    "module-type": ["expansion"],
    "logo": "",
    "requirements": ["pymisp"],
    "features": (
        "Canonicalize a full DNS name locally; preserve its source attribute and add a referenced domain-ip object."
    ),
    "references": [],
    "input": "A domain or hostname attribute with type, value and uuid.",
    "output": "The source Attribute and a domain-ip Object with a derived-from reference.",
}
moduleconfig = []
mispattributes = {"input": ["domain", "hostname"], "format": "misp_standard"}


def introspection():
    return deepcopy(mispattributes)


def version():
    return deepcopy(dict(moduleinfo, config=moduleconfig))


def canonical_name(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("A nonempty DNS name is required.")
    name = value.strip().removesuffix(".").encode("idna").decode("ascii").lower()
    if len(name) > 253 or len(name.split(".")) < 2:
        raise ValueError("Expected a multi-label DNS name of at most 253 ASCII characters.")
    try:
        ipaddress.ip_address(name)
    except ValueError:
        pass
    else:
        raise ValueError("An IP literal is not a DNS name.")
    if any(not re.fullmatch(r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?", label) for label in name.split(".")):
        raise ValueError("Invalid DNS label.")
    return name


def dict_handler(request):
    if not isinstance(request, dict):
        return {"error": "Expected a request object."}
    attribute = request.get("attribute")
    if not isinstance(attribute, dict) or attribute.get("type") not in mispattributes["input"]:
        return {"error": "A domain or hostname attribute is required."}
    source_uuid = attribute.get("uuid")
    if not isinstance(source_uuid, str):
        return {"error": "A valid source attribute UUID is required."}
    try:
        UUID(source_uuid)
        name = canonical_name(attribute.get("value"))
    except (ValueError, UnicodeError):
        return {"error": "Invalid DNS name or source UUID."}

    event = MISPEvent()
    event.add_attribute(**deepcopy(attribute))
    obj = MISPObject("domain-ip")
    obj.add_attribute("domain", value=name, to_ids=False)
    obj.add_reference(source_uuid, "derived-from")
    event.add_object(obj)
    result = json.loads(event.to_json())
    return {"results": {key: result[key] for key in ("Attribute", "Object")}}


def handler(q=False):
    """Compatibility adapter for the legacy JSON entry point."""
    if q is False:
        return False
    try:
        request = json.loads(q)
    except (TypeError, ValueError):
        return {"error": "Invalid JSON."}
    return dict_handler(request)
