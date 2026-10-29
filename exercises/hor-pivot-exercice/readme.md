# Human-operated ransomware: pivoting exercise

**Connect two events, investigate overlaps, and assess threat actor attribution.**

Act as a CTI analyst reviewing the incident response report from a ransomware
attack against ACME. Use the available indicators and observed techniques to
identify relevant relationships in MISP and explain your attribution confidence.

[Training home](../../README.md) · [Participant brief](exercice.md) · [Online exercise](https://hdoc.csirt-tooling.org/eneZJU-oSCKhwg_p6AXlcQ)

## Prepare the session

1. Give each participant a separate MISP organisation so correlations between
   participants do not interfere with the exercise.
2. Ensure both events below are encoded in the training instance.
3. Share the [participant brief and incident report](exercice.md).

## Required events

| Event | JSON file |
| --- | --- |
| `2af07707-7a4c-4f15-96bf-5d9d92e17fa6` | [Download event](misp.event.2af07707-7a4c-4f15-96bf-5d9d92e17fa6.json) |
| `daf03b1b-3bbf-4648-980e-a102c865805c` | [Download event](misp.event.daf03b1b-3bbf-4648-980e-a102c865805c.json) |

## Participant workflow

1. Review the incident report and select relevant indicators and techniques.
2. Encode the findings in MISP, including applicable MITRE ATT&CK mappings.
3. Pivot across the events to find overlaps with known campaigns or actors.
4. Explain the proposed attribution, the evidence supporting it, and the
   investigation limits that affect confidence.
