# Modular foundation implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the NOLP scaffold verifiable and fail closed while preserving independent Rust crates; defer a Gecko browser build until reproducible infrastructure is available.

**Architecture:** Ports-and-adapters, typed Rust interfaces, no dynamic plugin loader. The standalone workspace is a test harness, not a Gecko binary.

**Tech Stack:** Rust 2021, Cargo, Python 3.11, GitHub Actions, Mozilla Firefox upstream.

**Spec:** `docs/MODULAR-ARCHITECTURE.md`, `docs/MODULE-LIFECYCLE.md`, `docs/BOOTSTRAP.md`.

## Global constraints
- Keep all 15 modules declared scaffold and disabled.
- No AI-authored signatures, fabricated ownership, or AI-named branches.
- No new external dependencies unless justified.
- Never claim an upstream Firefox artifact build is a NOLP product.

## Review focus
- A scaffold must not be admitted to an operational registry.
- Duplicate module identifiers must be rejected.
- A missing Gecko adapter must fail browser startup.
- Unavailable optional modules must not prevent isolated policy tests.
- CI failures must remain visible; never suppress or mark green without logs.

---

### Task 1: Verify and enforce module activation

**Files:** `modules/contracts/src/lib.rs`, `modules/core/src/lib.rs`, `integration/src/lib.rs`.

- [ ] Write tests for disabled modules, duplicates, and missing engine.
- [ ] Run tests and observe RED.
- [ ] Add a typed registry that rejects non-ready modules and duplicate IDs.
- [ ] Run Cargo tests and observe GREEN.
- [ ] Commit.

### Task 2: Reconcile manifest and runtime expectations

**Files:** `modules/manifest.json`, `scripts/check-modules.py`, `docs/MODULE-LIFECYCLE.md`.

- [ ] Test scaffold flags and dependency graph consistency.
- [ ] Reject unexpected enabled scaffold modules.
- [ ] Run Python validator and Cargo metadata.
- [ ] Commit.

### Task 3: Establish verifiable upstream smoke test

**Files:** `.github/workflows/firefox-foundation.yml`, `docs/BOOTSTRAP.md`.

- [ ] Separate fast foundation checks from resource-intensive upstream build.
- [ ] Execute upstream build and record exit codes and logs.
- [ ] Only then proceed to branded profile and page-navigation smoke tests.
- [ ] Commit.

### Task 4: End-to-end acceptance

- [ ] `cargo fmt --all -- --check`
- [ ] `cargo clippy --workspace --all-targets --locked --offline -- -D warnings`
- [ ] `cargo test --workspace --locked --offline`
- [ ] `python3 scripts/check-modules.py`
- [ ] Gecko executable opens a local page and exits cleanly.
- [ ] Record evidence and remaining blockers without claiming unverified completion.

## Execution ledger

- Plan authored 2026-11-06. Do not mark unchecked items as completed without observed results.
