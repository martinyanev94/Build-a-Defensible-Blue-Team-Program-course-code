import json
from pathlib import Path

REQUIRED_ROLES = {
    "Analyst",
    "Security administrator",
    "Compliance",
    "Red team",
    "Purple team",
    "Threat intelligence",
}


def validate(matrix):
    errors = []
    role_names = {role["name"] for role in matrix["roles"]}
    missing = REQUIRED_ROLES - role_names
    if missing:
        errors.append(f"missing roles: {sorted(missing)}")
    for row in matrix["responsibilities"]:
        if not row.get("owner"):
            errors.append(f"{row['path']}: missing owner")
        if not row.get("escalate_to"):
            errors.append(f"{row['path']}: missing escalation target")
    return errors


def main():
    path = Path(__file__).with_name("responsibility_matrix.json")
    matrix = json.loads(path.read_text())
    errors = validate(matrix)
    print(f"roles: {'PASS' if not (REQUIRED_ROLES - {r['name'] for r in matrix['roles']}) else 'FAIL'} (6 required roles present)")
    print(f"ownership: {'PASS' if all(row.get('owner') for row in matrix['responsibilities']) else 'FAIL'} (6 responsibility rows have one owner)")
    print(f"escalation: {'PASS' if all(row.get('escalate_to') for row in matrix['responsibilities']) else 'FAIL'} (6 responsibility rows have an escalation target)")
    if errors:
        for error in errors:
            print(f"error: {error}")
        print("result: INVALID")
        raise SystemExit(1)
    print("result: VALID")


if __name__ == "__main__":
    main()
