import json
from pathlib import Path

ESCALATION_LIMIT_MINUTES = 15


def review_alert(alert):
    findings = []
    if not alert["triage_owner"]:
        findings.append("triage owner missing")
    missing = sorted(set(alert["telemetry_required"]) - set(alert["telemetry_present"]))
    if missing:
        findings.append(f"missing telemetry: {', '.join(missing)}")
    if alert["escalation_minutes"] > ESCALATION_LIMIT_MINUTES:
        findings.append("escalation delay")
    if not alert["remediation_owner"]:
        findings.append("remediation handoff missing")
    return findings


def build_backlog(alerts):
    backlog = []
    for alert in alerts:
        for finding in review_alert(alert):
            category = finding.split(":", 1)[0]
            backlog.append({
                "alert_id": alert["alert_id"],
                "category": category,
                "evidence": finding,
                "owner": alert["remediation_owner"] or "assign owner",
            })
    return backlog


def main():
    path = Path(__file__).parents[1] / "data" / "tabletop_alerts.json"
    alerts = json.loads(path.read_text())
    backlog = build_backlog(alerts)
    print(f"Alerts reviewed: {len(alerts)}")
    print(f"Findings: {len(backlog)}")
    for item in backlog:
        print(f"{item['alert_id']} | {item['category']} | {item['owner']}")


if __name__ == "__main__":
    main()
