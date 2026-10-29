from pathlib import Path
import json


def load_assets(path: str | Path) -> list[dict]:
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)
