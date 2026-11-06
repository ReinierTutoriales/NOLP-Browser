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
