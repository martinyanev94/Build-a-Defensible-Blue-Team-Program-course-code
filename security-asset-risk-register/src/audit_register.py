from pathlib import Path
import sys

from inventory import load_assets


def audit_register(assets: list[dict]) -> dict:
    asset_ids = {asset["id"] for asset in assets}
    missing_dependencies = sorted(
        f'{asset["id"]} -> {dependency}'
        for asset in assets
        for dependency in asset.get("dependencies", [])
        if dependency not in asset_ids
    )
    score_mismatches = []
    unsupported_assumptions = []
    unowned_actions = []
    for asset in assets:
        expected_score = asset["likelihood"] * asset["impact"]
        if asset["score"] != expected_score:
            score_mismatches.append(
                f'{asset["id"]}: stored={asset["score"]} expected={expected_score}'
            )
        if not asset.get("evidence"):
            unsupported_assumptions.append(asset["id"])
        if asset.get("treatment") in {"remediate", "mitigate"} and not asset.get("owner"):
            unowned_actions.append(asset["id"])
    return {
        "missing_dependencies": missing_dependencies,
        "score_mismatches": score_mismatches,
        "unsupported_assumptions": unsupported_assumptions,
        "unowned_actions": unowned_actions,
    }


def print_report(report: dict) -> None:
    print("AUDIT: FAIL" if any(report.values()) else "AUDIT: PASS")
    for category, findings in report.items():
        print(f"{category}: {', '.join(findings) or 'none'}")


if __name__ == "__main__":
    register_path = Path(__file__).parents[1] / "data" / "assets.json"
    report = audit_register(load_assets(register_path))
    print_report(report)
