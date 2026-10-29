from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
scenario = json.loads((ROOT / "data" / "tabletop.json").read_text())
findings = []

for prompt in scenario["prompts"]:
    if not prompt["answer"].strip():
        findings.append({
            "finding_id": prompt["finding_id"],
            "category": prompt["category"],
            "observation": prompt["observation"],
            "action": prompt["action"],
            "owner": prompt["owner"]
        })

report = {
    "exercise_id": scenario["exercise_id"],
    "scenario": scenario["title"],
    "finding_count": len(findings),
    "findings": findings
}
output = ROOT / "data" / "tabletop_report.json"
output.write_text(json.dumps(report, indent=2) + "\n")
print(f"{len(findings)} findings recorded")
for finding in findings:
    print(f"{finding['category']}: {finding['action']}")
