import json
from pathlib import Path


def dependency_ids(item):
    raw = item.get("dependency", "")
    if raw == "None":
        return []
    return [part.strip() for part in raw.replace(" and ", ",").split(",") if part.strip()]


def validate_milestone(item, items):
    required = ("owner", "evidence", "dependency", "review_point")
    missing = [field for field in required if not item.get(field)]
    if missing:
        return f"{item['id']}: missing {', '.join(missing)}"
    known = {candidate["id"]: candidate for candidate in items}
    dependencies = dependency_ids(item)
    unknown = [dep for dep in dependencies if dep not in known]
    if unknown:
        return f"{item['id']}: unknown dependency {', '.join(unknown)}"
    later = [
        dep for dep in dependencies
        if known[dep]["stage_order"] >= item["stage_order"]
    ]
    if later:
        return f"{item['id']}: dependency must be earlier: {', '.join(later)}"
    return ""


def has_cycle(items):
    graph = {item["id"]: dependency_ids(item) for item in items}
    visiting = set()
    visited = set()

    def visit(milestone_id):
        if milestone_id in visiting:
            return True
        if milestone_id in visited:
            return False
        visiting.add(milestone_id)
        if any(visit(dep) for dep in graph[milestone_id]):
            return True
        visiting.remove(milestone_id)
        visited.add(milestone_id)
        return False

    return any(visit(milestone_id) for milestone_id in graph)


def build_roadmap(items):
    errors = [
        error for item in items
        if (error := validate_milestone(item, items))
    ]
    if has_cycle(items):
        errors.append("roadmap contains a dependency cycle")
    if errors:
        raise ValueError("Roadmap validation failed: " + "; ".join(errors))
    return sorted(items, key=lambda item: (item["stage_order"], item["id"]))


def main():
    data_path = Path(__file__).parents[1] / "data" / "maturity.json"
    items = json.loads(data_path.read_text())
    roadmap = build_roadmap(items)
    print(f"Roadmap validation passed: {len(roadmap)} milestones")
    stages = {}
    for item in roadmap:
        stages.setdefault(item["stage"], []).append(item["id"])
    for stage, milestone_ids in stages.items():
        print(f"{stage}: {', '.join(milestone_ids)}")


if __name__ == "__main__":
    main()
