# Common Exercise Format (CEXF)

**Describe an exercise once: its scenario, injects, flow, and evaluation.**

CEXF is a proposed format for reusable training exercises. It brings exercise
metadata, participant actions, payloads, and scoring into one structured
definition. The format is still a proposal; the sample illustrates the current
structure rather than a finalized schema.

[Training home](../../README.md) · [Full JSON example](samples/misp-01.json) · [All exercises](../)

## Why a common format?

- **Completeness:** make required exercise elements explicit.
- **Validation:** identify missing or inconsistent definitions.
- **Automation:** describe planning, inject delivery, and evaluation.
- **Traceability:** review changes through Git history and diffs.
- **Collaboration:** share exercises in a format others can extend.

## Anatomy of an exercise

| Section | Purpose |
| --- | --- |
| `exercise` | Identify the scenario, version, tags, audience level, and validity period. |
| `inject_flow` | Define triggers, requirements, and the order of injects. |
| `injects` | Describe participant-facing actions, target tools, evaluation criteria, and scores. |
| `inject_payloads` | Supply the files or actions referenced by the injects. |

UUID references connect injects, flow entries, and payloads. Evaluation criteria
in the sample cover event creation, captured attributes, MISP objects, ATT&CK
tagging, publication, and a Suricata alert.

## Explore the phishing example

The [complete sample](samples/misp-01.json) follows two injects: a phishing email
to participants and a malicious network flow. Here is a short metadata excerpt:

```json
{
  "exercise": {
    "name": "Phishing e-mail",
    "tags": ["exercise:software-scope=\"misp\"", "state:production"],
    "version": "20210611",
    "level": "beginner",
    "namespace": "phishing"
  }
}
```

Read the full sample to follow `inject_uuid` and
`action_payload_resource_uuid` references through the flow, actions, and payloads.
Keeping the full example in a JSON file makes it easier to inspect and reuse.

## Draft repository conventions

The original proposal suggests a separate `misp-training-xxx` repository for
each training, based on a shared template. The template, setup conventions, and
license choice still need to be defined.
