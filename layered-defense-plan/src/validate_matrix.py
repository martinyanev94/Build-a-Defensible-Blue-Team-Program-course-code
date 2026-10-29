import json
from pathlib import Path


def validate_control(control):
    gaps = []
    if not control.get("owner"):
        gaps.append("missing owner")
    if not control.get("verification_evidence"):
        gaps.append("missing verification evidence")
    priority = "high" if (
        control.get("asset_criticality") == "critical"
        or control.get("failure_mode_risk") == "high"
    ) else "normal"
    return {
        "control_id": control["control_id"],
        "priority": priority,
        "gaps": gaps,
    }


def build_roadmap(matrix):
    validated = [validate_control(control) for control in matrix["controls"]]
    phase_one = ["workload-identity", "managed-device"]
    phase_two = ["network-segmentation", "application-authorization"]
    insider = ["separation-of-duties"]
    return {
        "controls": validated,
        "phase_1": phase_one,
        "phase_2": phase_two,
        "insider_risk_workstream": insider,
        "capability_gaps": matrix["gaps"],
    }


if __name__ == "__main__":
    matrix_path = Path(__file__).parents[1] / "data" / "defense_matrix.json"
    matrix = json.loads(matrix_path.read_text())
    roadmap = build_roadmap(matrix)
    print(json.dumps(roadmap, indent=2))
