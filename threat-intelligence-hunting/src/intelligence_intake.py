"""Small, traceable threat-intelligence intake workflow."""


def collect(indicator, indicator_type, source, observed_at):
    return {
        "indicator": indicator,
        "indicator_type": indicator_type,
        "source": source,
        "observed_at": observed_at,
        "status": "collected",
    }


def validate(record, corroborated):
    supported_types = {"ipv4", "domain", "sha256"}
    if record["indicator_type"] not in supported_types:
        raise ValueError("unsupported indicator type")
    if not record["source"] or not record["observed_at"]:
        raise ValueError("missing provenance")
    record["confidence"] = "high" if corroborated else "medium"
    record["status"] = "validated"
    return record


def enrich_and_prioritize(record, asset, local_alert):
    record["asset"] = asset
    record["local_alert"] = local_alert
    record["local_match"] = bool(local_alert)
    record["relevance"] = "high" if asset == "public-web" else "medium"
    record["priority"] = "high" if record["confidence"] == "high" and record["local_match"] else "medium"
    record["action"] = "block-and-investigate" if record["priority"] == "high" else "investigate"
    record["audience"] = "SOC"
    record["status"] = "ready-to-distribute"
    return record


def build_intelligence():
    record = collect(
        "198.51.100.24",
        "ipv4",
        "ISAC",
        "2026-10-28T18:00:00Z",
    )
    record = validate(record, corroborated=True)
    return enrich_and_prioritize(record, "public-web", "web-443-017")


if __name__ == "__main__":
    result = build_intelligence()
    print(f"{result['status']}: {result['indicator']} priority={result['priority']} action={result['action']} audience={result['audience']}")
