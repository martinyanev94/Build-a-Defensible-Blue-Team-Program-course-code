import json
import sys

def validate(model):
    errors = []
    for item in model["responsibilities"]:
        if not item.get("accountable"):
            errors.append(f"missing owner: {item['outcome']}")
    loop = model["feedback_loop"]
    if not loop.get("retest") or not loop.get("decision_owner"):
        errors.append("incomplete red-blue feedback loop")
    staffing = model["staffing_assumption"]
    if not staffing.get("evidence") or not staffing.get("review_owner"):
        errors.append("unsupported staffing assumption")
    return errors

model = json.load(open(sys.argv[1]))
errors = validate(model)
print("operating model valid" if not errors else "\n".join(errors))
