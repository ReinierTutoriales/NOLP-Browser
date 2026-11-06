# NOLP — Estado real, arquitectura del motor y plan de ejecución

**Corte documental:** 2026-11-06. **Rama:** `main`. **Producto ejecutable:** NO. **Motor integrado y probado:** NO.

> Regla de interpretación: «archivo creado» no significa «función implementada»; «workflow definido» no significa «CI aprobada»; «revisión fijada» no significa «última versión estable».

## 1. Qué existe hoy (verificable en el repositorio)

| Área | Archivos | Resultado real | Falta |
| --- | --- | --- | --- |
| Identidad | `assets/brand/nolp-icon.svg`, `nolp-wordmark.svg`, `nolp-logo.webp`, `docs/BRAND.md` | Recursos de marca y guía | Integrarlos en aplicaciones |
| Licencia | `LICENSE`, `docs/LICENSING.md` | MPL-2.0 y política de terceros | Inventario de componentes distribuidos y revisión antes del release |
| Gobernanza | `AGENTS.md`, `docs/ENGINEERING.md` | Reglas para agentes y calidad | Automatizar y demostrar cumplimiento |
| Arquitectura | `docs/ARCHITECTURE.md`, `docs/SECURITY-PRIVACY.md` | Diseño de módulos y amenazas | Implementaciones y pruebas |
| Actualidad | `skills/upstream-currentness/SKILL.md`, `docs/UPSTREAM-STATUS.md` | Guía local y registro | Comprobación oficial de versiones y seguimiento periódico |
| Motor desktop | `engine/upstream-manifest/firefox.toml` | URL upstream y commit de release estable fijado | Validar que es release estable soportada; compilar y ejecutar |
| Descarga | `scripts/bootstrap-firefox.sh` | Script que exige coincidencia con manifiesto | Probar ejecución real y gestionar errores de red/espacio |
| Verificación | `scripts/check-foundation.py`, `scripts/smoke-firefox.sh` | Comprobaciones definidas | Ejecutarlas en CI y verificar logs |
| CI | `.github/workflows/firefox-foundation.yml` | Workflow declarativo: validación y build manual optativo | Evidencia de CI verde, artefactos y smoke de arranque |
| Navegador | Sin aplicación NOLP compilable | No hay binario NOLP | Identidad, empaquetado, perfil, UI, navegación y pruebas |
| Android | GeckoView declarado sin versión | Sin aplicación Android | Selección, proyecto, build, tests y APK |
| Privacidad/bloqueo/vault | Contratos descritos en documentación | No hay módulos funcionales | Código, integración, auditoría y pruebas |

## 2. Decisión técnica del motor

- **Windows, Linux, macOS:** base Firefox Desktop con Gecko/SpiderMonkey/WebRender y parches mínimos. No duplicar todo el árbol upstream en Git. Mantener fuente externa reproducible y un registro de cambios propios.
- **Android y Android TV:** GeckoView, con adaptadores y UI nativos, versiones compatibles verificadas. No asumir que un fork desktop se compila como APK.
- **iOS/iPadOS:** estudiar reglas de distribución y disponibilidad real del motor en cada mercado; no prometer Gecko.
- **Core futuro:** módulos separados de bloqueo, políticas de red/privacidad, bóveda local, actualizaciones, rendimiento. Rust solo donde aporte una interfaz estable y auditable. Ninguno está implementado.
- **Orden de integración:** APIs soportadas > adaptadores > parches mínimos del motor. Preservar sandbox, aislamiento, TLS, decodificación multimedia y actualizaciones de seguridad.

## 3. Revisión Firefox fijada: qué significa

`engine/upstream-manifest/firefox.toml` fija:

- Origen: `https://github.com/mozilla-firefox/firefox`
- Commit candidato: `6181e6b5f28a8fbae1d5c3ef6f6626b5a2180213`
- GeckoView: sin versión.

**Verificado:** el commit corresponde al tag oficial de Firefox 159.0.1, la versión estable identificada al 2026-11-06. **Sin verificar:** que la compilación y el arranque funcionen. Antes de producción: identificar release estable oficial, relacionarla con el tag/commit upstream, registrar fecha, advisories y cambios, actualizar manifiesto y repetir pruebas. No actualizar automáticamente a la punta de `main` o Nightly.

## 4. Cómo reproducir lo disponible (Linux o entorno compatible)

Requisitos: Git, Bash, Python 3.11+ (para `tomllib`), espacio de disco suficiente y dependencias Mozilla. En la raíz NOLP:

```bash
python3 scripts/check-foundation.py
bash -n scripts/bootstrap-firefox.sh
bash -n scripts/smoke-firefox.sh
bash scripts/bootstrap-firefox.sh
bash scripts/smoke-firefox.sh
```

La descarga va a `.upstream/firefox` (ignorado por Git). El bootstrap rechaza destino existente y revisión que no coincida con el manifiesto. El smoke comprueba el SHA del árbol descargado; **por defecto no compila**. Para solicitar una compilación, solo después de instalar dependencias y configurar `mozconfig` según Mozilla:

```bash
NOLP_RUN_BUILD=1 bash scripts/smoke-firefox.sh
```

La compilación puede fallar por dependencias, recursos o revisión; el script no crea una aplicación NOLP. `./mach run` y las pruebas de interfaz solo tienen sentido después de un build válido.

## 5. CI existente y sus límites

Workflow: `.github/workflows/firefox-foundation.yml`.

- `validate`: revisa sintaxis Bash y forma del manifiesto. **No** confirma la procedencia ni el estado estable del commit.
- `artifact-build`: solo se solicita manualmente con `build_firefox=true`. Intenta bootstrap y `./mach build` de Firefox upstream con Artifact Builds. No genera release NOLP.
- **No existe evidencia registrada de ejecución verde**. Consultar los runs y logs antes de marcar cualquiera de los pasos como aprobado.
- El workflow todavía necesita robustez: permisos mínimos y acciones fijadas a SHA, caché/control de espacio, compatibilidad de bootstrap no interactivo, publicación de evidencias, smoke de arranque y estrategia de rollback.

## 6. Hitos ordenados con criterios de aceptación

### M0 — Asegurar procedencia y versión
- [x] Manifiesto con revisión inmutable candidata.
- [x] Bootstrap que exige coincidencia con manifiesto.
- [x] Comparar con versión estable oficial de Mozilla y avisos de seguridad (159.0.1; MFSA 2026-123; 2026-11-06).
- [x] Fijar revisión de release con procedencia y fecha; **pendiente validar build y estrategia de actualizaciones**.

**Aceptación:** versión/commit oficial identificados y registrados; revisión de seguridad completada.

### M1 — Compilación reproducible del motor (prioridad inmediata)
- [x] Workflow y scripts iniciales.
- [ ] CI `validate` verde verificada.
- [ ] Bootstrap upstream ejecutado sin errores.
- [ ] `./mach build` exitoso en Linux.
- [ ] `./mach run` o prueba de arranque en entorno compatible; registrar versión, logs, commit y plataforma.
- [ ] Documentar requisitos, duración, recursos y fallos.

**Aceptación:** evidencias de build + arranque del Firefox upstream fijado. Aún no es NOLP.

### M2 — Primer ejecutable NOLP desktop
- [ ] Decidir estrategia de identidad/producto sin infringir marcas Mozilla.
- [ ] Perfil de usuario NOLP aislado, migraciones y almacenamiento local.
- [ ] Empaquetado, actualizaciones firmadas y distribución reproducible.
- [ ] Navegación mínima, permisos y compatibilidad web.
- [ ] Pruebas de arranque, cierre, múltiples procesos y regresión.

**Aceptación:** binario NOLP identificable y ejecutable; no solo Firefox upstream renombrado sin cumplimiento.

### M3 — Privacidad verificable
- [ ] Inventariar conexiones automáticas en arranque/reposo/navegación/actualización.
- [ ] Definir políticas locales y excepciones justificadas para seguridad.
- [ ] Tests de red y ausencia de telemetría propia no consentida.
- [ ] Revisar DNS, certificados, permisos y aislamiento.

**Aceptación:** capturas y tests reproducibles, sin afirmaciones absolutas de «cero tráfico».

### M4 — Bloqueador modular
- [ ] Seleccionar APIs realmente disponibles en la versión del motor.
- [ ] Implementar reglas de red y excepciones con pruebas.
- [ ] Añadir filtrado cosmético y scriptlets auditados, sin JS arbitrario remoto.
- [ ] Benchmarks de latencia, RAM, CPU y compatibilidad de sitios.

**Aceptación:** pruebas de eficacia, falsos positivos y rendimiento comparadas con baseline.

### M5 — Bóveda local cifrada
- [ ] Modelo de amenazas, formato versionado, política de recuperación.
- [ ] AEAD y KDF auditados, integración con almacenes seguros del SO.
- [ ] Migraciones, bloqueo, backups cifrados, pruebas de corrupción y recuperación.
- [ ] WebAuthn/passkeys sujeto a APIs y garantías de plataforma.

**Aceptación:** pruebas de seguridad, compatibilidad, pérdida de energía y recuperación.

### M6 — Android/TV y resto de plataformas
- [ ] Fijar GeckoView estable compatible.
- [ ] Proyecto Android y UI móvil/TV con navegación y foco adecuados.
- [ ] Compilación APK, smoke y pruebas de multimedia.
- [ ] Matriz de versiones y limitaciones por dispositivo.
- [ ] Windows/macOS e iOS solo con validación real de distribución.

**Aceptación:** builds y pruebas por plataforma, no paridad supuesta.

### M7 — Release
- [ ] Auditoría de licencias/SBOM/avisos, marca y terceros.
- [ ] Firma, integridad, actualización, rollback y respuesta a CVE.
- [ ] Pruebas de seguridad, privacidad, rendimiento, accesibilidad y multimedia.
- [ ] Artefactos, changelog, instrucciones y reproducibilidad.

**Aceptación:** distribución verificable con trazabilidad y plan de parches.

## 7. Registro de evidencia por cambio

Para cada PR/commit que cambie motor o dependencias, registrar:
1. Versión anterior, versión objetivo, commit/tag y fuente oficial con fecha.
2. Riesgo de seguridad y compatibilidad, licencias, parches locales.
3. Comandos ejecutados, entorno, resultados y enlaces a CI/logs.
4. Métricas antes/después si se afirma optimización.
5. Fallos conocidos, reversión y siguiente paso.

Sin ejecución real, marcar **pendiente/no verificado**. No usar el estado del repositorio como sustituto de pruebas.

## 8. Documentos de referencia

- [README](../README.md) — visión y entrada.
- [Arquitectura](ARCHITECTURE.md) — capas y contratos.
- [Bootstrap](BOOTSTRAP.md) — comandos iniciales.
- [Estado upstream](UPSTREAM-STATUS.md) — versiones y validación.
- [Ingeniería](ENGINEERING.md) — pruebas y métricas.
- [Seguridad y privacidad](SECURITY-PRIVACY.md) — modelo de amenazas.
- [Licencias](LICENSING.md) — MPL y terceros.
- [Skill de actualidad](../skills/upstream-currentness/SKILL.md) — procedimiento de actualización.

**Siguiente acción operativa:** ejecutar CI, corregir errores de compilación y registrar el primer arranque de Firefox upstream 159.0.1. No iniciar el bloqueador o el vault como si el motor ya estuviera integrado.

## Red: estado y secuencia de ejecución (2026-11-06)

- Guía normativa publicada: `docs/NETWORK-ENGINEERING.md`.
- Arquitectura elegida: Gecko Necko/NSS/Neqo upstream, con políticas locales y adaptadores mínimos.
- Los submódulos `network-policy`, `network-privacy`, `network-filter`, `network-diagnostics` y `network-tests` son objetivos de arquitectura, no funciones operativas.
- No hay todavía evidencias de compilación del motor, tráfico DNS, compatibilidad HTTP/3 ni benchmarks de red.
- Orden de trabajo: (1) verificar Gecko; (2) contratos de políticas; (3) adaptador; (4) integración de filtros; (5) pruebas de fugas, compatibilidad y rendimiento.
- Criterio para declarar implementado un módulo: código ejecutable, tests y evidencia de integración, no solo inventario.

## UI multiplataforma y Rust: decisión documentada (2026-11-06)

- **Guía normativa:** `docs/UI-CROSS-PLATFORM-ARCHITECTURE.md`, enlazada desde diseño, modularidad, ingeniería, AGENTS y skills.
- **Decisión:** lógica y tokens compartidos; Firefox Chrome UI en escritorio, Compose/GeckoView como propuesta para Android/TV; no añadir un motor WebView paralelo.
- **Comunicación:** Rust local con traits y llamadas tipadas; FFI donde corresponda; IPC únicamente en límites entre procesos; eventos incrementales con control de flujo.
- **Estado real:** arquitectura documentada; sin contratos de UI compilados, integración Rust/Gecko, UI NOLP ejecutable ni benchmarks verificados.
- **Próximo criterio de aceptación:** compilar Gecko upstream, crear contratos de estado con pruebas y validar un recorrido de navegación extremo a extremo.

## Prototipo modular Rust publicado (2026-11-06)
- Existe un workspace Cargo **independiente de Firefox**, con 15 crates de módulos y un crate de pruebas de composición (`integration`).
- Los módulos declaran solo `nolp-contracts` como dependencia directa; `nolp-core` compone políticas mediante traits. El crate `integration` conecta en pruebas `network-policy`, `content-blocker`, `anti-ai`, `core`, `engine-gecko` y `ui-aero`.
- `modules/manifest.json` registra todos los módulos como `scaffold` (API 0.1.0); esto **no significa** integración Gecko ni funcionalidades de navegador completas.
- Implementación parcial: contratos tipados, políticas de host exacto, control anti-IA reversible en memoria, estado local de consentimiento y tema. Son prototipos sin persistencia ni tráfico real.
- Adaptadores Gecko, escritorio, Android, vault, medios y actualizaciones exponen estados no disponibles; no hay integración con APIs Mozilla, FFI, IPC, UI renderizada ni sandbox propio.
- CI configurada para ejecutar tests Rust y Python, además de lint Rust; **resultados pendientes de verificación**. La CI formatea una copia temporal antes de analizar, sin publicar ese formato. Falta fijar Cargo.lock y aplicar el formateo al repositorio.
- Antes de integrar Rust en Firefox: seguir https://firefox-source-docs.mozilla.org/build/buildsystem/rust.html, incluyendo Cargo de Gecko, `gkrust-shared`, vendoring y auditoría. No insertar el workspace externo en libxul sin validar build nativo completo.
- Próximo paso: comprobar CI y corregir fallos, fijar lockfile, normalizar formato, ampliar contratos de entrada/validación y probar adaptador Gecko en build completo.

## Correcciones de base Rust (2026-11-06)
- Añadido `Cargo.lock` para el grafo local de 16 crates; CI usa `--locked` en Clippy y tests. Verificar su consistencia real ejecutando Cargo en CI.
- `scripts/check-modules.py` ahora coteja manifiesto, archivos de crates, versiones, dependencias declaradas en Cargo, miembros del workspace e inventario del lockfile. No inspecciona imports Rust transitivos ni seguridad en ejecución.
- La CI sigue normalizando el formato Rust **solo en el checkout temporal** antes de compilar; su comprobación posterior verifica esa copia, **no** el formato de los archivos versionados. Pendiente aplicar `cargo fmt --all` y publicar los cambios para activar una comprobación estricta directamente sobre Git.
- No hay confirmación de ejecución satisfactoria de CI ni de integración Gecko. No declarar resueltos otros fallos sin logs.
