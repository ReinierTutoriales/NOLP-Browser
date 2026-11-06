# Arquitectura objetivo de NOLP

**Estado:** diseño propuesto, no implementación verificada.

## Plataformas
- Windows, Linux y macOS: fork controlado de Firefox Desktop, con divergencia mínima.
- Android móvil y Android TV: GeckoView con adaptadores y UI específicos; evaluar Android Components donde aporte valor.
- iOS/iPadOS: sujeto a restricciones técnicas y regulatorias de distribución; no prometer compatibilidad Gecko.

## Capas
1. Aplicaciones: UI escritorio, táctil y TV, con accesibilidad y controles nativos.
2. Núcleo compartido: políticas de privacidad, filtrado, seguridad, configuración local, vault, red, actualizaciones y rendimiento.
3. Adaptadores: Firefox Desktop, GeckoView y servicios del sistema operativo.
4. Motor: Gecko, SpiderMonkey, WebRender y mecanismos de seguridad upstream.

Los módulos son límites de responsabilidad, no procesos obligatorios.

## Contratos previstos
- `filter-core`: reglas compiladas, excepciones y evaluación determinista; evitar I/O en ruta crítica.
- `filter-lists`: obtención, autenticidad, validación, versionado y reemplazo atómico de listas.
- `filter-content`: reglas cosméticas y catálogo auditado de scriptlets; nunca ejecutar JavaScript arbitrario procedente de listas.
- `filter-adapter`: integración mediante capacidades reales de WebExtensions y GeckoView; evaluar webRequest y declarativeNetRequest por plataforma y versión.
- `privacy-policy`: política única de conexiones automáticas, permisos y persistencia.
- `network-policy`: decisiones de conexiones del navegador, DNS, excepciones y auditoría.
- `secure-local-vault`: operaciones restringidas de cifrado, desbloqueo y credenciales; no exponer claves a la UI web.
- `update-manager`: actualizaciones verificadas, rollback controlado y trazabilidad.
- `performance`: métricas locales y pruebas reproducibles, sin envío automático.

## Estrategia de integración
Prioridad: APIs públicas y extensiones integradas > bibliotecas nativas con interfaces tipadas > parches internos mínimos a Gecko. Cualquier parche upstream requiere propietario, pruebas, documentación de rebase y revisión en cada actualización.

## Organización objetivo
```text
apps/{desktop,android,android-tv}/
core/{adblock,privacy,security,network-policy,local-vault,updates,performance}/
integrations/{firefox-desktop,geckoview,operating-systems}/
engine/{upstream-manifest,patches}/
tests/{privacy-network,security,adblock-compat,media-performance,cross-platform}/
policies/
docs/
```
Esta estructura es un mapa futuro: no crear directorios vacíos ni afirmar que existen implementaciones.

## Dependencias y actualizaciones
Registrar versión de Gecko/GeckoView, APIs utilizadas, licencias, parches y compatibilidad por plataforma. Actualizar con pruebas de regresión completas. Mantener un manifiesto de componentes y dependencias verificable.
