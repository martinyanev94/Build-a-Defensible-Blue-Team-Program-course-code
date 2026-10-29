# Security Metrics Automation

Run the sample management report with:

```bash
python3 src/report_metrics.py
```

The report calculates each percentage from its numerator and denominator, applies the metric-specific threshold operator, validates result-to-metric pairing, and adds risk, action, owner, and decision details for exceptions.
