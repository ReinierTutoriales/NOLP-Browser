# Skill obligatoria — Security Assurance Gate

## Objetivo
Seguridad moderna **verificable**, no promesas de invulnerabilidad. Aplicar a todos los PR, actualizaciones de dependencias, builds y releases, junto a `skills/latest-stable-gate/SKILL.md`.

## Modelo de amenazas y prioridades
1. **Explotación del motor:** conservar sandbox Gecko, aislamiento de sitios/procesos, mitigaciones de memoria, validación TLS, protecciones anti-phishing y actualizaciones de seguridad upstream.
2. **Cadena de suministro:** lockfiles, procedencia y hashes verificables, SBOM, revisión de advisories, mínimo privilegio en CI, acciones fijadas a commit SHA completo y revisión de scripts externos.
3. **Datos locales:** secretos con criptografía autenticada auditada, Argon2id cuando haya contraseña maestra, claves separadas, almacén seguro de SO, permisos mínimos, protección frente a rollback y migraciones seguras. No inventar cifrado ni declarar perfil cifrado mientras Gecko genere datos en claro.
4. **Límites de confianza:** origen de mensajes verificado, validación de entradas, IPC/FFI tipado, separación UI/contenido privilegiado, ausencia de ejecución de código remoto arbitrario.
5. **Privacidad:** conexiones automáticas inventariadas; telemetría propia desactivada por defecto; no desactivar servicios de protección upstream sin evaluación y sustituto seguro.
6. **Disponibilidad:** límites de tiempo/memoria, recuperación segura, pruebas negativas y fuzzing en parsers, reglas y formatos no confiables.

## Procedimiento exigido
- Inventariar superficies, permisos, secretos, dependencias directas/transitivas y fronteras de confianza; actualizar el modelo de amenazas.
- Consultar advisories oficiales (Mozilla MFSA, RustSec, GitHub Advisory Database, Android) y versiones estables **con fecha UTC**. Priorizar CVE explotadas activamente.
- Aplicar mínimo privilegio, defensa en profundidad y *secure by default*. Preferir mecanismos nativos y mantenidos; no añadir un framework de seguridad redundante.
- Ejecutar: formato/lint/tests, auditoría de dependencias, escaneo de secretos, análisis estático, comprobación de permisos de workflows y pruebas de integración. Añadir fuzzing, sanitizers y análisis dinámico en superficies de riesgo.
- Validar en ejecutables reales: aislamiento del perfil, sandbox, TLS, permisos, tráfico de red, integridad de actualizaciones, cierre limpio y regresiones. No extrapolar resultados de tests de Rust a Gecko.
- Para cada fallo: bloquear la release, corregir raíz, añadir test de regresión, registrar CVE/advisory y evidencia. Excepción temporal solo si está aprobada, con mitigación, responsable y caducidad.
- Publicar informe: qué se probó, CI exacta, riesgos pendientes, versiones y fecha; sin términos como «100 % seguro».

## Controles mínimos CI
- Permisos `contents: read` por defecto; tokens con permisos mínimos, sin secretos en PR externos.
- Acciones de terceros fijadas a SHA completo tras revisión; actualizaciones mediante PR auditables.
- Auditoría de RustSec cuando haya dependencias Rust externas, y escáner de secretos; análisis de código y SBOM por plataforma cuando exista build real.
- No permitir que fallos de seguridad se conviertan en éxito mediante `continue-on-error` o `|| true` sin excepción explícita.
- Gates de publicación separados de CI de desarrollo; sin firma de release si no existe clave autorizada.

## Criterios de bloqueo
Vulnerabilidades críticas no mitigadas, pérdida de sandbox/TLS, filtración de secretos, procedencia no verificable, test de seguridad fallido, dependencia vulnerable sin excepción o actualización no verificada. Si una herramienta no puede ejecutarse, estado **pendiente**, nunca aprobado.

## Referencias oficiales
- Mozilla: https://www.mozilla.org/en-US/security/advisories/
- Mozilla security architecture: https://firefox-source-docs.mozilla.org/
- RustSec: https://rustsec.org/
- GitHub Actions hardening: https://docs.github.com/en/actions/security-for-github-actions
- OWASP ASVS: https://owasp.org/www-project-application-security-verification-standard/
- NIST SSDF: https://csrc.nist.gov/projects/ssdf

Esta skill es local al repositorio; no modifica las capacidades globales de ChatGPT.
