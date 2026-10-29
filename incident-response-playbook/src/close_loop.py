from __future__

import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "data" / "tabletop_report.json"
OUTPUT_PATH = ROOT / "data" / "corrective_actions.json"


def load_report() -> dict:
    return json.loads(REPORT_PATH.read_text())


def build_action(finding: dict) -> dict:
    required = ("finding_id", "proposed_change", "owner", "due_date", "change_type", "evidence_required")
    missing = [field for field in required if not finding.get(field)]
    if missing:
        raise ValueError(f"finding {finding.get('finding_id', '?')} missing {', '.join(missing)}")
    return {
        "action_id": f"CA-{finding['finding_id']}",
        "finding_id": finding["finding_id"],
        "change": finding["proposed_change"],
        "change_type": finding["change_type"],
        "owner": finding["owner"],
        "due_date": finding["due_date"],
        "evidence_required": finding["evidence_required"],
        "status": "open",
    }


def publish_actions(report: dict) -> dict:
    findings = report["findings"]
    finding_ids = [finding.get("finding_id") for finding in findings]
    if len(finding_ids) != len(set(finding_ids)):
        raise ValueError("finding IDs must be unique")
    actions = [build_action(finding) for finding in findings]
    result = {
        "published_on": date.today().isoformat(),
        "exercise_id": report["exercise_id"],
        "actions": actions,
    }
    OUTPUT_PATH.write_text(json.dumps(result, indent=2) + "\n")
    return result


if __name__ == "__main__":
    published = publish_actions(load_report())
    print(f"published {len(published['actions'])} corrective actions")
    for action in published["actions"]:
        print(f"{action['action_id']}: {action['change_type']} -> {action['owner']} by {action['due_date']}")
