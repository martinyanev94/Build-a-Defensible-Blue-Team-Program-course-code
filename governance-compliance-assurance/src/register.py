import json
from pathlib import Path

PLAN = Path(__file__).parents[1] / "data" / "evidence_plan.json"

def load_plan():
    return json.loads(PLAN.read_text())

def validate(record):
    required = ["control_id", "operation_evidence", "exception", "remediation", "oversight"]
    missing = [field for field in required if field not in record]
    if missing:
        return [f"missing: {', '.join(missing)}"]
    if record["exception"]["status"] == "open" and not record["remediation"].get("due_date"):
        return ["open exception needs a remediation due date"]
    return []

def report():
    records = load_plan()["evidence_plan"]
    for record in records:
        errors = validate(record)
        status = "valid" if not errors else "invalid"
        print(f"{record['control_id']}: {status}; exception={record['exception']['status']}")
        for error in errors:
            print(f"  {error}")

if __name__ == "__main__":
    report()
