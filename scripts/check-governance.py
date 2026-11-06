#!/usr/bin/env python3
"""Validate NOLP repository governance docs and local skill contracts."""
from pathlib import Path

root = Path(__file__).resolve().parents[1]
required = {
    "AGENTS.md": ("ReinierTutoriales", "Firma criptográfica", "skills/security-performance/SKILL.md"),
    "skills/upstream-currentness/SKILL.md": ("última", "seguridad", "skills/security-performance/SKILL.md"),
    "skills/security-performance/SKILL.md": ("benchmark", "rollback", "AGENTS.md"),
}
for name, terms in required.items():
    content = (root / name).read_text(encoding="utf-8")
    for term in terms:
        if term not in content:
            raise SystemExit(f"Missing required governance term {term!r} in {name}")
print("NOLP governance and local skill contract checks passed")
