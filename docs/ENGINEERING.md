# Guía de ingeniería y criterios de aceptación

**Estado:** guía de ejecución para trabajo futuro.

## Secuencia
1. Inventariar versiones oficiales, licencias, plataformas, APIs Gecko/GeckoView y restricciones.
2. Registrar decisiones de arquitectura, amenazas y contratos mínimos.
3. Probar un prototipo de escritorio y otro de GeckoView sin divergencia profunda.
4. Validar bloqueo de red, cosmético y scriptlets con pruebas de compatibilidad.
5. Inventariar y auditar conexiones propias automáticas.
6. Construir el almacenamiento seguro por fases: credenciales, luego persistencia sensible y WebAuthn.
7. Medir rendimiento, memoria, GPU, vídeo y energía antes de optimizar.
8. Implementar UI final por plataforma después de estabilizar las integraciones.

## Política de cambios
Cada PR debe describir alcance, versión de upstream, riesgos de seguridad, pruebas ejecutadas, evidencia y plan de reversión. Los cambios de API, persistencia y criptografía requieren pruebas de compatibilidad y migración. Ningún test no ejecutado se reporta como aprobado.

## Métricas
Medir tiempos de inicio, navegación, respuesta de UI, memoria por proceso, CPU en reposo, consumo energético, latencia de bloqueo, fotogramas perdidos y decodificación hardware. Comparar con línea base en escenarios equivalentes; registrar equipo, SO, motor y configuración.

## Puertas de calidad
- Compilación y pruebas automatizadas por plataforma disponible.
- Auditoría de dependencias y licencias.
- Pruebas de red y de ausencia de telemetría propia no autorizada.
- Pruebas de integridad, recuperación y migración de datos.
- Verificación de sandbox y aislamiento.
- Pruebas de compatibilidad web, multimedia y accesibilidad.
- Documentación actualizada antes de publicar.

## Fuentes técnicas preferidas
Mozilla Firefox Source Docs, documentación GeckoView/Android Components, MDN, estándares WebAuthn/FIDO2, Rust Security Advisories y documentación oficial de seguridad de cada SO. Confirmar versiones y disponibilidad actual en el momento de implementar; no fijar números sin verificarlos.

## Estado de implementación
La presencia de esta documentación no significa que el navegador, el bloqueador, el vault, la CI o los tests estén construidos. Registrar por separado el progreso real de cada módulo.

## Guía técnica: módulos Gecko, Rust y verificación

**Fuente de arquitectura:** `docs/MODULAR-ARCHITECTURE.md`. El manifiesto `modules/manifest.json` es un inventario de contratos propuestos, no una prueba de independencia funcional.

### Selección de mecanismos
1. Para interfaz y comportamiento frontend, evaluar primero APIs soportadas de Firefox y WebExtensions. Utilizar JSActors cuando sea necesaria comunicación documentada entre contextos; no crear IPC por conveniencia.
2. Para integraciones nativas, usar los mecanismos Gecko adecuados (XPCOM, WebIDL o IPDL según límite y proceso). Evitar acoplamiento con internals upstream no soportados.
3. Para bibliotecas Rust propias, definir crates con APIs pequeñas y Cargo Workspaces cuando exista código compilable. Integrar en Gecko mediante `moz.build` y su sistema oficial; no enlazar artefactos manualmente sin contrato.
4. Mantener `contracts` sin dependencias funcionales y componer adaptadores desde `core`. La compatibilidad de los contratos se comprueba con tests, no solo con el inventario.
5. Diferenciar aislamiento de código, de proceso y de seguridad: no afirmar sandbox independiente por separar un crate o paquete.

### Dos rutas de construcción
- **Rápida (Artifact Build):** únicamente cambios compatibles de frontend, recursos y JS. Requiere validar el origen del repositorio y las condiciones oficiales de resolución de artefactos (incluido `git-cinnabar` cuando aplique).
- **Completa (compilación nativa):** obligatoria para cambios Rust, C/C++, WebIDL y cualquier integración no cubierta por Artifact Builds. Sin esta ruta, no declarar validados los módulos nativos.
- Ambas rutas deben registrar versión Gecko, revisión exacta, sistema operativo, toolchain, resultado de compilación y prueba de arranque. `./mach run --version` no demuestra navegación real.

### Matriz de pruebas por modificación
| Tipo de cambio | Verificación mínima |
| --- | --- |
| Contrato de módulo | Pruebas de contrato y consumidores dependientes |
| JS/frontend | xpcshell, mochitest o browser-chrome según superficie |
| Rust | cargo fmt, clippy, test, auditoría de dependencias y build integrado |
| Integración Gecko nativa | Compilación completa, pruebas de integración y sandbox |
| Bloqueo/anti-IA | Falsos positivos, excepciones, compatibilidad y métricas |
| Cuenta/vault | Migración, cifrado, aislamiento, revocación y ausencia de sincronización involuntaria |
| UI | Accesibilidad, foco, composición GPU y rendimiento |
| Actualizaciones | Integridad, firma, rollback y recuperación |

### Procedimiento obligatorio por módulo
1. Identificar responsabilidad, propietario de datos, límites de confianza y APIs upstream soportadas.
2. Revisar documentación oficial y versiones estables actuales, registrar fecha y decisiones.
3. Definir interfaz y pruebas de contrato antes de implementar.
4. Implementar sin importar internals de otro módulo; registrar excepciones justificadas.
5. Ejecutar pruebas unitarias, integración inversa y pruebas de seguridad pertinentes.
6. Medir impacto en CPU, RAM, latencia, GPU y consumo cuando proceda.
7. Actualizar inventario, estado real, compatibilidad, instrucciones de rollback y evidencias.

### Referencias primarias
- [Firefox Source Docs — Gecko](https://firefox-source-docs.mozilla.org/overview/gecko.html)
- [Firefox Source Docs — Build System](https://firefox-source-docs.mozilla.org/build/buildsystem/)
- [Firefox Source Docs — moz.build](https://firefox-source-docs.mozilla.org/build/buildsystem/mozbuild-files.html)
- [Firefox Source Docs — Writing Rust Code](https://firefox-source-docs.mozilla.org/writing-rust-code/index.html)
- [Firefox Source Docs — Artifact Builds](https://firefox-source-docs.mozilla.org/contributing/build/artifact_builds.html)
- [Firefox Source Docs — Modules (MOTS)](https://firefox-source-docs.mozilla.org/mots/)
- [Rust — Cargo Workspaces](https://doc.rust-lang.org/stable/cargo/reference/workspaces.html)

**Actualización:** revisar las páginas oficiales al implementar; las APIs y requisitos pueden cambiar. No se ha demostrado aún una compilación nativa completa ni aislamiento real de los módulos NOLP.

## Guía de red
Antes de modificar la red, seguir `docs/NETWORK-ENGINEERING.md`: Necko/NSS/Neqo upstream, contratos modulares, pruebas de seguridad y mediciones comparables. No presentar especificaciones como funcionalidades implementadas.
