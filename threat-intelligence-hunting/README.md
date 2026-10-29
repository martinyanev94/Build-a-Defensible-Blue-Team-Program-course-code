# Threat intelligence and hunting review

Run the review from the repository root:

```text
python threat-intelligence-hunting/src/map_hunts.py
```

The script reads `data/hunt_review.json`, compares observed evidence with expected evidence, and prints the defensive decision for each hunt. A supported result produces a control change. A telemetry gap produces a monitoring change.
