# Estado upstream — NOLP

**Consulta oficial:** 2026-11-06. **Canal:** Firefox Desktop estable (no Nightly/ESR).

| Componente | Versión/revisión en NOLP | Última estable oficial identificada | Validación | Acción |
| --- | --- | --- | --- | --- |
| Firefox Desktop | 159.0.1; commit `6181e6b5f28a8fbae1d5c3ef6f6626b5a2180213`; tag `FIREFOX_159_0_1_RELEASE` | **159.0.1**, publicada 2026-11-03 | Tag y versión verificados mediante GitHub de Mozilla; **compilación y arranque no ejecutados** | Ejecutar CI, corregir fallos y validar arranque |
| GeckoView Android | Sin fijar | Sin verificar | No integrado | Seleccionar versión estable compatible |
| Rust/toolchain | Sin fijar | Sin verificar | Sin proyecto Rust compilable | Elegir versión estable y lockfile |
| Dependencias de módulos | No implementadas | No aplica | No aplica | Inventariar cuando existan |

## Evidencia de procedencia

- Mozilla Firefox releases: https://www.mozilla.org/en-US/firefox/releases/
- Mozilla Security Advisory **MFSA 2026-123** (159.0.1, 2026-11-03): https://www.mozilla.org/en-US/security/advisories/mfsa2026-123/
- Tag oficial de Mozilla: https://github.com/mozilla-firefox/firefox/tree/FIREFOX_159_0_1_RELEASE
- Commit resuelto del tag: https://github.com/mozilla-firefox/firefox/commit/6181e6b5f28a8fbae1d5c3ef6f6626b5a2180213
- Archivo `browser/config/version.txt` en ese tag: `159.0.1`.

La revisión se fijó tras verificar el tag y la versión en la fuente oficial. **No equivale a una compilación aprobada** ni a un producto distribuible.

La política exige revisar nuevas versiones y advisories antes de cada release, sin saltar automáticamente a Nightly. Véase `skills/upstream-currentness/SKILL.md`.
