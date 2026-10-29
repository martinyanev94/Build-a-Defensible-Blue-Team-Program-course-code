import json
from pathlib import Path


def validate_incident(incident):
    errors = []
    if not incident.get("trigger", {}).get("signals"):
        errors.append("missing trigger signals")
    if not incident.get("owner"):
        errors.append("missing accountable owner")
    for step in incident.get("steps", []):
        if not step.get("action"):
            errors.append(f"{step.get('id')}: missing action")
        if not step.get("evidence"):
            errors.append(f"{step.get('id')}: missing evidence")
        if not step.get("exit_criteria"):
            errors.append(f"{step.get('id')}: missing exit criteria")
    closure = incident.get("closure", {})
    if not closure.get("required_evidence"):
        errors.append("missing closure evidence")
    if not closure.get("exit_criteria"):
        errors.append("missing closure exit criteria")
    return errors


def main():
    path = Path(__file__).parents[1] / "data" / "incident.json"
    incident = json.loads(path.read_text())
    errors = validate_incident(incident)
    if errors:
        for error in errors:
            print(error)
        raise SystemExit(1)
    print("incident playbook valid")


if __name__ == "__main__":
    main()
