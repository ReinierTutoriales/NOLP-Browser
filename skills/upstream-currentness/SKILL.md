# Skill local — Actualización tecnológica de NOLP

## Objetivo
Mantener el navegador y todos sus módulos en versiones **estables, soportadas y seguras** lo más recientes posible, sin degradar seguridad, compatibilidad, rendimiento ni privacidad. Este archivo es una guía para agentes que trabajen en el repositorio; no instala ni modifica skills globales de ChatGPT.

## Activación
Aplicar al actualizar Gecko/Firefox, GeckoView, Rust, Android, UI, librerías, compiladores, filtros, mecanismos criptográficos, formatos de datos, CI y herramientas.

## Procedimiento obligatorio
1. Leer `AGENTS.md`, `docs/ARCHITECTURE.md`, `docs/SECURITY-PRIVACY.md`, `docs/LICENSING.md` y este archivo.
2. Inspeccionar versiones reales del repositorio; no deducirlas de conversaciones o planes.
3. Consultar las páginas **oficiales** de versiones, avisos de seguridad, migración y soporte, registrando fecha UTC y URL.
4. Separar latest stable, ESR/LTS, beta y nightly. Seleccionar estable reciente para producción; justificar ESR/LTS cuando reduzca riesgo y preserve soporte.
5. Construir matriz actual → disponible → objetivo, requisitos, cambios incompatibles, CVE, licencias, riesgo y reversión.
6. Aplicar actualizaciones pequeñas y verificables, con pines reproducibles y mínima divergencia respecto a upstream.
7. Ejecutar tests, compilación, smoke tests, seguridad, privacidad, rendimiento y revisión de licencias según el componente. No atribuir resultados a pruebas no ejecutadas.
8. Registrar evidencia, commit, estado de CI, riesgos residuales y fecha del siguiente control.

## Condiciones de aceptación
- Sin desactivar sandbox, TLS, aislamiento, actualizaciones de seguridad ni controles de firma.
- Sin telemetría nueva no justificada ni dependencia de nube obligatoria.
- Sin introducir versiones prerelease en el canal estable.
- Sin declarar «última versión» sin fuente, fecha y comparación.
- Si una actualización falla, documentar el bloqueo, conservar la última versión segura validada y abrir tarea de seguimiento.

## Fuentes prioritarias
- Firefox releases y avisos: https://www.mozilla.org/en-US/firefox/releases/ y https://www.mozilla.org/en-US/security/advisories/
- Firefox build docs: https://firefox-source-docs.mozilla.org/
- GeckoView: https://mozilla.github.io/geckoview/
- Rust releases: https://blog.rust-lang.org/ y https://releases.rs/
- Android releases: https://developer.android.com/about/versions
- Dependencias: repositorios upstream, changelogs oficiales, advisories y SBOM del proyecto.

## Evidencia
Actualizar `docs/UPSTREAM-STATUS.md` con la versión exacta, referencia upstream, fecha de consulta, estado de compilación, resultado y pendiente. Si no hay acceso a fuentes o CI, registrar **sin verificar** en vez de afirmar actualidad.
