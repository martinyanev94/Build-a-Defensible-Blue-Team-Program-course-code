# Blue Team Maturity Roadmap

This project publishes a dependency-aware roadmap from structured maturity milestones.

## Run

From this directory, run:

```bash
python src/main.py
```

The validator requires every milestone to include an owner, evidence target, dependency, and review point. It also checks that dependency IDs exist, dependencies precede the milestone, and the dependency graph contains no cycle. A passing validation confirms structural completeness; the review points still require observed evidence from the responsible team.
