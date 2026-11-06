# Skill local — Seguridad, privacidad, rendimiento y arquitectura NOLP

## Precedencia
Aplicar obligatoriamente `skills/security-assurance/SKILL.md` como puerta de seguridad y `skills/latest-stable-gate/SKILL.md` como puerta de dependencias. Esta skill complementa ambas con ingeniería y medición; no permite saltar sus bloqueos.

## Alcance
Obligatorio en cambios de Gecko, GeckoView, UI, bloqueo, red, vault, almacenamiento, actualizador, compilación, CI, filtros y dependencias. Esta skill es una instrucción del repositorio; no modifica habilidades globales de ningún asistente.

## Flujo verificable
1. **Inventario:** leer AGENTS.md y docs normativos; inspeccionar código, dependencias directas/transitivas, lockfiles, permisos, flujos de datos, interfaces y pruebas reales.
2. **Fuentes:** contrastar guías oficiales vigentes, changelogs, advisories y compatibilidad de cada componente afectado. Registrar URL, fecha UTC, versión actual, estable soportada y objetivo.
3. **Amenazas:** identificar entradas no confiables, límites de confianza, privilegios, almacenamiento de secretos, actualizaciones, navegación, extensiones, contenido web y red. Aplicar mínimo privilegio y aislamiento.
4. **Diseño:** preferir APIs públicas soportadas, módulos independientes, interfaces tipadas, contratos versionados y dependencias unidireccionales; evitar singletons globales y procesos adicionales sin necesidad demostrada.
5. **Rendimiento:** definir métricas y escenarios antes de optimizar: cold/warm start, navegación, interacción, scroll, vídeo, CPU, RSS/PSS, energía, I/O y tráfico. Usar perfiles, trazas y benchmarks repetibles con dispositivos/clases de hardware identificados.
6. **Implementación:** cambios pequeños y reversibles, migraciones de datos seguras, pruebas negativas, sin código muerto ni compatibilidad heredada innecesaria. No añadir telemetría ni red oculta.
7. **Validación:** compilar y ejecutar pruebas unitarias, integración, fuzz/property cuando aplique, sanitizers, SAST, análisis de dependencias, licencias, privacidad de tráfico y regresiones de rendimiento. Distinguir claramente pruebas ejecutadas, omitidas y fallidas.
8. **Evidencia:** publicar cambios con resumen técnico, benchmark antes/después, amenazas mitigadas, versiones, licencias, CI, riesgos y rollback; actualizar docs/UPSTREAM-STATUS.md y hoja de ruta.

## Criterios de bloqueo
- No desactivar sandbox, aislamiento de procesos/sitios, TLS, validación de certificados, firma de updates o rollback protection para ganar velocidad.
- No crear criptografía propia ni almacenar claves maestras junto a datos cifrados sin protección adecuada. Usar bibliotecas auditadas y keystore/almacén seguro de plataforma cuando sea viable; documentar amenazas de equipo comprometido.
- No introducir versiones beta/nightly en producción, librerías abandonadas, dependencias sin procedencia ni código copiado sin licencia compatible.
- No afirmar «sin telemetría», «máxima seguridad», «última versión» o «más rápido» sin mediciones, fuente y fecha.
- No ejecutar cambios masivos de dependencias sin matriz de compatibilidad, validación por capas y plan de reversión.
- No falsear autoría, firmas, aprobaciones ni resultados; aplicar AGENTS.md para identidad y commits.

## Prioridad de actualización
1. Vulnerabilidades explotadas activamente o parches críticos.
2. Versiones sin soporte y APIs deprecadas con riesgo.
3. Últimas estables compatibles de motor, toolchains, SDK y librerías.
4. Reducción de deuda técnica y dependencias transitivas.
5. Optimizaciones demostradas con medición, no por intuición.

## Módulos y contratos
- Motor: Gecko/GeckoView upstream con divergencia mínima.
- Red/privacidad: política de conexiones verificable y configurable sin romper actualizaciones de seguridad.
- Bloqueo: reglas versionadas, compilación eficiente, pruebas de compatibilidad y regresión.
- Vault: cifrado autenticado, rotación, derivación de claves, borrado y recuperación documentados.
- UI: estado predecible, accesibilidad, foco de TV, fluidez y límites de memoria.
- Build/updates: artefactos reproducibles donde sea posible, SBOM, procedencia, integridad y firmas autorizadas.

## Fuentes de referencia
Mozilla source docs: https://firefox-source-docs.mozilla.org/
Mozilla security advisories: https://www.mozilla.org/en-US/security/advisories/
Rust security: https://rustsec.org/
OWASP ASVS: https://owasp.org/www-project-application-security-verification-standard/
Android security: https://source.android.com/docs/security
GitHub Actions security: https://docs.github.com/en/actions/security-for-github-actions

## Salida mínima de cada intervención
Estado antes → cambios exactos → pruebas y evidencia → riesgos y limitaciones → siguiente acción concreta.

## Procedimiento adicional: UI y comunicación entre módulos
- Leer `docs/UI-CROSS-PLATFORM-ARCHITECTURE.md`, `docs/UI-DESIGN-SYSTEM.md` y `docs/MODULAR-ARCHITECTURE.md`.
- Clasificar cada comunicación: llamada Rust local, FFI Kotlin/Swift, interfaz Gecko o IPC entre procesos. Elegir la alternativa más simple y segura según el límite real.
- Diseñar contratos versionados, ownership de estado, eventos incrementales, colas acotadas, cancelación y errores tipados. No exponer secretos a UI.
- Verificar threading, memoria, copias FFI, contención y backpressure. Medir latencia input→frame, GPU, CPU, RAM, vídeo y accesibilidad por plataforma.
- Mantener Aero Light/Dark con tokens compartidos, renderer adaptado y fallback opaco. Registrar pruebas ejecutadas y pendientes.
