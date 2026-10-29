# Blue Team Operating Model

Validate the operating-model decision record with:

```bash
python validate_operating_model.py operating_model.json
```

The validator checks that every responsibility has an accountable role, the red-blue feedback loop has a retest and decision owner, and the staffing assumption has evidence and a review owner.
