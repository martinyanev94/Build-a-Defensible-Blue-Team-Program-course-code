import json
import sys

REQUIRED_LINKS = ("asset", "risk", "monitoring", "control", "decision")

def validate(path):
    with open(path, encoding="utf-8") as stream:
        mission = json.load(stream)
    errors = []
    if not mission.get("organization") or not mission.get("mission"):
        errors.append("organization and mission are required")
    for index, item in enumerate(mission.get("paths", []), start=1):
        missing = [key for key in REQUIRED_LINKS if not item.get(key)]
        if missing:
            errors.append(f"path {index} missing: {', '.join(missing)}")
    return mission, errors

if __name__ == "__main__":
    mission, errors = validate(sys.argv[1])
    print(f"valid: {not errors}")
    print(f"mission_paths: {len(mission.get('paths', []))}")
    if errors:
        for error in errors:
            print(error)
    sys.exit(bool(errors))
