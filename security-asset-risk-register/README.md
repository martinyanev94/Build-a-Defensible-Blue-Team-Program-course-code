# Security Asset and Risk Register

This project audits a JSON risk register before publication.

Run it from this directory with:

```bash
PYTHONPATH=src python src/audit_register.py
```

The audit reports unresolved dependencies, score mismatches, missing assessment evidence, and remediation actions without an owner.
