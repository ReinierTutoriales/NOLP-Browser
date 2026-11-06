# NOLP — Module lifecycle and activation contract

**Scope:** Initial scaffolding only. No browser feature is production-ready.

## Canonical inventory

`modules/manifest.json` is the source of truth for the 15 modules. Each module has a Rust crate, a declared public API version, a dependency boundary and an explicit `enabled` flag. All 15 are currently `status: scaffold` and `enabled: false`.

The separate `integration` crate is an offline composition harness, not a sixteenth browser feature. `contracts` defines shared interfaces and `core` composes policy implementations. Other crates may depend only on `contracts`; `integration` may depend on concrete adapters.

## State machine

1. `planned`: declared only.
2. `scaffold`: crate and contract exist; **must be disabled**.
3. `implemented`: behavior exists; **must be disabled** until verification.
4. `verified`: tests and integration evidence are recorded; eligible for explicit enablement.

`enabled` is independent of `status`: verified does not imply enabled. The validator rejects any enabled module unless it is verified. This is a repository consistency guard, **not** a runtime capability manager.

Rust `ModuleState::Scaffold` is non-operational. `ModuleState::Ready` is reserved for genuinely working adapters. `start_browser()` currently returns `EngineUnavailable` because Gecko is not connected.

## Current prototype limits

`network-policy`, `content-blocker` and `anti-ai` contain offline exact-host evaluators for isolated testing. They are **not** connected to Gecko, cannot block actual network requests, and must not be advertised as active privacy features. `ui-aero` contains only theme values; it is not a renderer. Identity and vault persistence, update signatures, media playback, desktop and Android adapters are not implemented.

## Verification gates

Run:
```sh
python3 scripts/check-modules.py
python3 -m unittest discover -s tests -p 'test_network_policy.py' -v
cargo fmt --all -- --check
cargo metadata --locked --offline --format-version 1 --no-deps
cargo check --workspace --all-targets --locked --offline
cargo clippy --workspace --all-targets --locked --offline -- -D warnings
cargo test --workspace --locked --offline
```

A successful module graph check does not prove Cargo builds or Gecko integration. Do not mark any module `verified` or `enabled` without fresh evidence for the specific implementation and its runtime adapter.

## Development order

First stabilize the manifest, contracts, core and build. Then implement one independent module at a time with tests, integration and an explicit activation gate. Never turn scaffolds into live features merely to make CI green. No unverified claims, AI author signatures, or fabricated owner signatures.
