"""Build synthetic models offline; construction and JSON conversion do not call MISP."""
from uuid import uuid4

from pymisp import MISPEvent, MISPObject


def build_event():
    token = uuid4().hex[:12]
    event = MISPEvent()
    event.info = f"PyMISP 2.5 training / {token}"
    event.distribution = 0
    event.threat_level_id = 4  # Undefined; synthetic data is not a threat assessment.
    event.analysis = 0
    event.published = False
    attribute = event.add_attribute(
        "domain", f"observer-{token}.example", to_ids=False,
        comment="Synthetic observation; not a production indicator.",
    )
    domain_ip = MISPObject("domain-ip", strict=True, standalone=False)
    domain_ip.add_attribute("domain", value=f"host-{token}.example", to_ids=False)
    domain_ip.add_attribute("ip", value="192.0.2.10", to_ids=False)
    domain_ip.add_reference(attribute.uuid, "related-to", "Synthetic teaching relation.")
    event.add_object(domain_ip)
    return event


if __name__ == "__main__":
    print(build_event().to_json(indent=2))
