# NOLP — Arquitectura modular y contratos

**Estado:** arquitectura objetivo; no equivale a módulos funcionales implementados.

## Principio rector
El núcleo del navegador no debe importar directamente detalles de UI, bloqueo, cuentas o bóveda. Toda dependencia entre componentes se expresa mediante contratos explícitos y versionados; cada implementación se sustituye o prueba por separado. El aislamiento reduce el radio de impacto, pero los cambios de ABI, protocolos, seguridad y Gecko requieren pruebas de integración.

## Módulos y dependencias permitidas
| Módulo | Responsabilidad | Dependencias permitidas |
| --- | --- | --- |
| `core` | Orquestación y ciclo de vida | `contracts` |
| `contracts` | Tipos, interfaces, eventos y capacidades versionadas | ninguna |
| `engine-gecko` | Adaptador Gecko/Firefox upstream | `contracts` |
| `ui-aero` | Barra superior, pestañas, Aero Light/Dark, accesibilidad | `contracts` |
| `privacy` | Políticas locales, permisos y mitigación de telemetría opcional | `contracts` |
| `content-blocker` | Publicidad, rastreadores, listas y excepciones | `contracts` |
| `anti-ai` | Reglas anti-IA y control reversible por categoría/sitio | `contracts` |
| `identity-local` | Perfiles locales, preferencias y sesiones locales | `contracts` |
| `identity-firefox` | Adaptador opcional a Firefox Account oficial | `contracts` |
| `vault` | Secretos cifrados y llaves protegidas por plataforma | `contracts` |
| `media` | Políticas y diagnósticos de reproducción | `contracts` |
| `updates` | Verificación y aplicación segura de actualizaciones | `contracts` |
| `platform-desktop` | Integración Windows/macOS/Linux | `contracts` |
| `platform-android` | Integración futura GeckoView | `contracts` |

## Reglas obligatorias
1. Dependencias unidireccionales. Ningún módulo funcional importa otro módulo funcional; la composición y el cableado se realizan en `core` mediante interfaces de `contracts`.
2. Sin estados globales mutables compartidos. Los datos persistentes tienen propietario definido, esquema versionado y migraciones.
3. Contratos con versionado semántico, compatibilidad documentada y pruebas de contrato. Cambios incompatibles requieren migración explícita.
4. Fallos contenidos: timeouts, cancelación, degradación controlada y reversión cuando corresponda. Un fallo del bloqueador no debe corromper el vault ni las cuentas.
5. Privilegios mínimos y separación de procesos donde lo justifique el modelo de amenazas; módulos lógicos **no** implican aislamiento de seguridad por sí mismos.
6. Cada módulo declara pruebas unitarias, integración, rendimiento y seguridad apropiadas, junto con límites de memoria y CPU medidos.
7. No bifurcar Gecko innecesariamente: mantener el upstream fijado y adaptadores estrechos, evitando modificaciones internas salvo necesidad demostrada.
8. Características opcionales mediante capacidades y feature flags locales; los valores predeterminados de privacidad no dependen de servicios externos.
9. Cuentas locales predeterminadas, Firefox Account opcional y consentimiento por categoría; anti-IA activado por defecto y reversible.
10. Actualizaciones atómicas, comprobación de integridad y estrategia de rollback; sin saltarse protecciones por compatibilidad.

## Organización inicial
```text
modules/
  manifest.json             # Inventario y grafo de dependencias
  contracts/                # Futuras interfaces públicas versionadas
  core/
  engine-gecko/
  ui-aero/
  privacy/
  content-blocker/
  anti-ai/
  identity-local/
  identity-firefox/
  vault/
  media/
  updates/
  platform-desktop/
  platform-android/
scripts/check-modules.py    # Verificación estructural inicial
```

## Criterios de aceptación por módulo
- Código ejecutable, pruebas unitarias y de contrato, límites claros y documentación.
- Integración en CI con pruebas selectivas según dependencias inversas.
- Benchmark reproducible cuando afecta rendimiento.
- Análisis de seguridad y revisión de permisos para módulos sensibles.
- Capacidad de deshabilitar el módulo opcional sin corrupción de datos.
- Pruebas de compatibilidad en plataformas soportadas antes de publicar.

**Importante:** el manifiesto inicial y su validador verifican solo estructura y dependencias declaradas; no prueban aislamiento de procesos, ausencia de imports indebidos, rendimiento ni implementación funcional. Estas garantías se incorporarán a medida que exista código compilable.

## Contraste con documentación oficial (6 de noviembre de 2026)
Fuentes primarias consultadas:
- Arquitectura Gecko: https://firefox-source-docs.mozilla.org/overview/gecko.html
- Sistema de compilación: https://firefox-source-docs.mozilla.org/build/buildsystem/
- moz.build: https://firefox-source-docs.mozilla.org/build/buildsystem/mozbuild-files.html
- Rust en Firefox: https://firefox-source-docs.mozilla.org/writing-rust-code/index.html
- Artifact Builds y restricciones: https://firefox-source-docs.mozilla.org/contributing/build/artifact_builds.html
- Cargo Workspaces: https://doc.rust-lang.org/stable/cargo/reference/workspaces.html
- Gobernanza de módulos Mozilla: https://firefox-source-docs.mozilla.org/mots/

### Decisiones de integración
1. **Frontend:** preferir APIs frontend, WebExtensions y módulos JS soportados para funciones que no requieren modificar código nativo. Probar con xpcshell, mochitest y browser-chrome según su capa.
2. **Motor:** respetar las interfaces Gecko existentes (XPCOM/WebIDL, JSActors o IPDL solo cuando sea apropiado); evitar introducir nuevas capas IPC sin necesidad medida.
3. **Rust:** cuando existan crates reales, utilizar Cargo Workspaces para compartir lockfile y ejecutar pruebas por paquete. Integrar Rust en Gecko mediante el sistema de compilación documentado de Mozilla, no mediante copias manuales de binarios.
4. **Dos rutas de compilación:** Artifact Builds únicamente para cambios compatibles (principalmente JS, HTML, CSS y recursos). **Compilación nativa completa obligatoria** para C/C++/Rust, WebIDL o modificaciones no soportadas por artifact mode.
5. **Precaución crítica:** Mozilla documenta requisitos de git-cinnabar para artifact builds sobre clones Git; no considerar el flujo actual de GitHub clonando mozilla-firefox como validado hasta demostrar resolución de artefactos y ejecución real.
6. **Contratos:** interfaces estables en el límite de nuestros módulos; dentro de Gecko usar las interfaces soportadas, sin imponer un protocolo universal ni duplicar abstractions upstream.
7. **Seguridad:** el aislamiento lógico por crates no sustituye al sandbox de procesos de Gecko. Revisión de capacidades, secretos, actualizaciones y límites de confianza por separado.
8. **CI:** ejecutar pruebas de cada módulo afectado y pruebas de integración inversa. Publicar resultados verificables y no confundir el manifiesto con validación de dependencias del código.
9. **Actualizaciones:** no adoptar versiones solo por ser las más recientes; preferir versiones estables compatibles, con changelog, CVEs, pruebas y reversión.

### Próximo cambio ejecutable
Validar primero el flujo Artifact Build con fuente compatible y pruebas de arranque. Antes de integrar el primer crate nativo, preparar un job de compilación completa independiente; evitar que la CI rápida declare cobertura nativa inexistente.
