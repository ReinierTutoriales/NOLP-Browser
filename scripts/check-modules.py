#!/usr/bin/env python3
"""Validate declared NOLP module boundaries (not runtime isolation)."""
import json
import pathlib
import re
import tomllib

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
    crate_path = ROOT / "modules" / m["id"] / "Cargo.toml"
    source_path = ROOT / "modules" / m["id"] / "src" / "lib.rs"
    assert crate_path.is_file() and source_path.is_file(), f"Missing Rust crate: {m['id']}"
    crate = tomllib.loads(crate_path.read_text(encoding="utf-8"))
    assert crate["package"]["name"] == "nolp-" + m["id"], f"Crate name mismatch: {m['id']}"
    assert crate["package"]["version"] == m["public_api_version"], f"Version mismatch: {m['id']}"
    actual = crate.get("dependencies", {})
    expected = {"nolp-" + dep for dep in deps}
    assert set(actual) == expected, f"Dependency boundary violation: {m['id']}"
    for dep in deps:
        assert actual["nolp-" + dep]["path"] == "../" + dep, f"Wrong dependency path: {m['id']}"
workspace = tomllib.loads((ROOT / "Cargo.toml").read_text(encoding="utf-8"))
assert set(workspace["workspace"]["members"]) == {"integration"} | {"modules/" + i for i in ids}, "Workspace members differ from module manifest"
lock = tomllib.loads((ROOT / "Cargo.lock").read_text(encoding="utf-8"))
assert lock["version"] == 4, "Expected Cargo.lock format 4"
assert {p["name"] for p in lock["package"]} == {"nolp-integration"} | {"nolp-" + i for i in ids}, "Lockfile package set mismatch"
print(f"Validated {len(modules)} Rust crates, declared dependencies, workspace and lockfile inventory")
