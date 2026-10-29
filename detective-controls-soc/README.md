# Detective Controls and SOC Workflow

This project reviews sample SOC alerts and produces an evidence-backed improvement backlog.

## Run

From the repository root:

```bash
python detective-controls-soc/src/main.py
```

The reviewer checks four workflow boundaries:

- triage ownership
- required telemetry
- escalation timing
- remediation ownership

A finding remains actionable because the output preserves its alert ID, failure category, evidence, and remediation owner or unassigned state.
