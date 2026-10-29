# Incident Response Playbook System

This project stores a structured incident record, validates the response plan, and runs a deterministic tabletop exercise.

## Run the tabletop

From this directory:

```sh
python3 src/run_tabletop.py
```

The command reads `data/tabletop.json`, records unanswered coordination decisions, and writes `data/tabletop_report.json`. The expected report contains four findings: coordination, communication, authorization, and recovery.

The report is an exercise artifact, not evidence that a production incident occurred. Review each finding in a debrief, assign or confirm ownership, and retest the repaired workflow.
