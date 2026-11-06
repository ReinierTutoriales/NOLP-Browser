# Skill obligatoria — Latest Stable Gate (NOLP)

## Alcance y regla innegociable
Toda dependencia **directa, transitiva, vendorizada o de compilación**, incluido Firefox/Gecko, GeckoView, Rust/toolchains, Kotlin/Gradle, SDK, GitHub Actions, listas de bloqueo, bibliotecas nativas, formatos de base de datos y herramientas de CI, debe evaluarse contra **la última versión estable publicada y soportada** antes de añadirla, modificarla o publicar una release.

**Regla de publicación:** ninguna release se declara actualizada ni se distribuye si una dependencia está desactualizada sin una excepción documentada y aprobada, o si falla la matriz de compatibilidad y seguridad. Nunca se promete que una versión futura no fallará: la garantía exigible es detectar, bloquear, corregir y verificar.

## Procedimiento de cada PR y release
1. Inventariar componentes directos, transitivos, SDK, compiladores, herramientas y dependencias del upstream. Generar SBOM cuando exista soporte.
2. Consultar **fuentes oficiales** y avisos de seguridad con fecha UTC. Registrar versión instalada, última estable, canal, soporte, URL y evidencia. Nunca inventar una versión.
3. Clasificar cada diferencia: actualización compatible, cambio mayor que requiere migración, bloqueo de plataforma, o parche urgente de seguridad. ESR/LTS es excepción explícita, no sustituto automático de latest stable.
4. Actualizar pines, hashes, lockfiles, APIs y documentación. No introducir betas, nightlies, versiones retiradas, paquetes sin mantenimiento ni dependencias innecesarias.
5. Ejecutar compilación y pruebas por plataforma, lint, pruebas funcionales, regresión, seguridad, licencias y rendimiento donde corresponda. No confundir resolución de dependencias con compatibilidad real.
6. Si una actualización rompe algo, corregir la incompatibilidad; **no** desactivar controles, bajar de versión en silencio ni aceptar un estado fallido. Mantener el último estado seguro verificado mientras se resuelve el bloqueo.
7. Si la última estable no es compatible, abrir excepción trazable con dependencia, versión objetivo, evidencia técnica, responsable, fecha de vencimiento, mitigación y plan de migración. Bloquear la release sin excepción aprobada.
8. Antes de fusionar o publicar: revisar alertas Dependabot, informes de CI, lockfiles, versiones upstream y excepciones vencidas. Registrar el resultado en `docs/UPSTREAM-STATUS.md`.

## Automatización
- Dependabot comprueba Cargo y GitHub Actions diariamente y abre propuestas; **no** significa que todas las dependencias estén ya actualizadas.
- La revisión de versiones de Firefox/Gecko, SDK y otras fuentes no cubiertas por Dependabot sigue siendo obligatoria y requiere automatización específica y evidencia.
- No fusionar automáticamente actualizaciones mayores o de seguridad sin las pruebas correspondientes.
- Un fallo de comprobación o falta de evidencia implica estado **no verificado**, nunca «cumple».

## Criterios de aceptación
Última estable verificada o excepción vigente; CVE evaluadas; CI y smoke tests aprobados; licencia compatible; sin regresiones conocidas de sandbox, TLS, aislamiento, privacidad ni rendimiento crítico. La regla se aplica a agentes, personas y automatizaciones por igual.

Leer también `skills/upstream-currentness/SKILL.md` y `skills/security-performance/SKILL.md`.
