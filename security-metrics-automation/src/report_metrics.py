from __future__ import annotations

import json
from pathlib import Path


def load_metrics(path: Path) -> list[dict]:
    return json.loads(path.read_text())


def evaluate_metric(metric: dict) -> dict:
    current = metric["numerator"] / metric["denominator"] * 100
    previous = metric["previous_value"]
    delta = current - previous
    threshold = metric["threshold"]
    operator = metric["threshold_operator"]
    if operator == "lt":
        exception = current < threshold
    elif operator == "gt":
        exception = current > threshold
    else:
        raise ValueError(f"Unsupported threshold operator: {operator}")
    return {
        "name": metric["name"],
        "current": current,
        "delta": delta,
        "threshold": threshold,
        "exception": exception,
    }


def render_report(results: list[dict], metrics: list[dict]) -> str:
    if len(results) != len(metrics):
        raise ValueError("Results and metrics must have the same length")
    lines = ["Management security report"]
    for result, metric in zip(results, metrics):
        if result["name"] != metric["name"]:
            raise ValueError("Result and metric names must match")
        status = "EXCEPTION" if result["exception"] else "OK"
        change = f"{result['delta']:+.0f} points"
        lines.append(f"- {result['name']}: {result['current']:.0f}% ({change}) [{status}]")
        if result["exception"]:
            lines.append(f"  Risk: {metric['risk']}")
            lines.append(f"  Action: {metric['action']}")
            lines.append(f"  Owner: {metric['owner']}")
            lines.append(f"  Decision: {metric['decision']}")
    return "\n".join(lines)


def main() -> None:
    path = Path(__file__).parents[1] / "data" / "metrics.json"
    metrics = load_metrics(path)
    results = [evaluate_metric(metric) for metric in metrics]
    print(render_report(results, metrics))


if __name__ == "__main__":
    main()
