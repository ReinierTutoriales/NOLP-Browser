#!/usr/bin/env python3
"""Validate declared NOLP module boundaries (not runtime isolation)."""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
path = ROOT / "modules" / "manifest.json"
data = json.loads(path.read_text(encoding="utf-8"))
assert data["schema_version"] == 1, "Unsupported module manifest"
assert data["architecture"] == "ports-and-adapters"
modules = data["modules"]
ids = [m["id"] for m in modules]
assert len(ids) == len(set(ids)), "Duplicate module IDs"
assert "contracts" in ids and "core" in ids and "engine-gecko" in ids
assert all(re.fullmatch(r"[a-z][a-z0-9-]*", i) for i in ids)
for m in modules:
    assert m["status"] in {"planned", "scaffold", "implemented", "verified"}
    assert re.fullmatch(r"\d+\.\d+\.\d+", m["public_api_version"])
    deps = m["dependencies"]
    assert len(deps) == len(set(deps)), f"Duplicate dependencies: {m['id']}"
    assert all(d in ids and d != m["id"] for d in deps), f"Invalid dependency: {m['id']}"
    if m["id"] == "contracts":
        assert not deps, "Contracts must have no module dependencies"
    else:
        assert deps == ["contracts"], f"{m['id']} must depend only on contracts"
print(f"Validated {len(modules)} declared modules and dependency boundaries")
