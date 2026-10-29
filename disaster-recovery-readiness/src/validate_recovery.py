import json
from pathlib import Path


def validate_exercise_checks(checks):
    errors = []
    for check in checks:
        for field in ("owner", "evidence", "pass_condition"):
            if not check.get(field):
                errors.append(f"{check['id']}: missing {field}")
    return errors


def readiness_gate(structural_errors, observed_results):
    required = (
        "restore-customer-api",
        "approve-recovery",
        "approve-communications",
        "confirm-insurance-route",
    )
    observed_pass = all(
        observed_results.get(check_id, {}).get("status") == "PASS"
        and observed_results.get(check_id, {}).get("evidence_ref")
        for check_id in required
    )
    return not structural_errors and observed_pass


def main():
    plan_path = Path(__file__).parents[1] / "data" / "recovery_plan.json"
    plan = json.loads(plan_path.read_text())
    errors = validate_exercise_checks(plan["checks"])
    observed_results = {
        "restore-customer-api": {"evidence_ref": "restore-log-001", "status": "PASS"},
        "approve-recovery": {"evidence_ref": "decision-record-001", "status": "PASS"},
        "approve-communications": {"evidence_ref": "message-log-001", "status": "PASS"},
        "confirm-insurance-route": {"evidence_ref": "insurance-route-001", "status": "FAIL"},
    }
    print(f"exercise checks: {len(plan['checks'])}")
    if errors:
        for error in errors:
            print(error)
        print("structural validation: FAILED")
    else:
        print("structural validation: PASSED")
    status = "READY" if readiness_gate(errors, observed_results) else "NOT READY"
    print(f"transition readiness: {status}")
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
