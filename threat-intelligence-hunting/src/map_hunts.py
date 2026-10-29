import json
from pathlib import Path


DATA_PATH = Path(__file__).parents[1] / "data" / "hunt_review.json"


def review_result(result):
    expected = set(result["expected_evidence"])
    observed = set(result["observed_evidence"])
    complete = expected.issubset(observed)
    if result["status"] == "supported" and complete:
        decision = "control_change"
    elif result["status"] == "telemetry_gap":
        decision = "monitoring_change"
    else:
        decision = "unresolved"
    return {
        "hunt_id": result["hunt_id"],
        "decision": decision,
        "change": result["change"]
    }


def main():
    results = json.loads(DATA_PATH.read_text())
    for result in results:
        review = review_result(result)
        print(f"{review['hunt_id']}: {review['decision']} — {review['change']}")


if __name__ == "__main__":
    main()
