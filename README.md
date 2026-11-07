<div align="center">

<img src="assets/brand/nolp-official.png" alt="Logotipo oficial NOLP 3D en violeta, azul y cian" width="220" height="220" />

</div>

# NOLP

**Nex · Óptimo · Local · Privado**

> Un navegador pensado para ofrecer rendimiento, autonomía y privacidad sin depender innecesariamente de servicios en la nube.

**Estado:** proyecto en fase inicial de diseño y desarrollo. Las capacidades descritas a continuación son objetivos de arquitectura, no funcionalidades ya disponibles.

## ¿Qué significa NOLP?

- **N — Nex:** siguiente generación (*next-generation*).
- **O — Óptimo:** rendimiento y eficiencia.
- **L — Local:** tecnología *local-first*.
- **P — Privado:** privacidad desde el diseño (*privacy-first*).

Esta es la interpretación oficial del acrónimo NOLP. No sustituirla por «Navegador Óptimo Local y Privado» ni por otras expansiones.

## Visión

Construir un navegador multiplataforma con una experiencia rápida y consistente, protección frente al rastreo y un modelo *local-first*. La arquitectura buscará separar sus componentes para permitir actualizaciones, auditorías y mantenimiento sin comprometer el resto del sistema.

## Principios de diseño

1. **Local-first:** historial, marcadores, ajustes y credenciales gestionados localmente por defecto.
2. **Privacy-first:** minimizar la recopilación de datos y las conexiones innecesarias; evitar telemetría propia no consentida.
3. **Seguridad por diseño:** aislamiento de procesos y sitios cuando la plataforma lo permita, permisos mínimos, actualizaciones verificables y almacenamiento protegido.
4. **Rendimiento medible:** optimizar arranque, memoria, consumo de CPU, navegación y reproducción multimedia mediante pruebas reproducibles.
5. **Modularidad:** interfaces claras entre motor web, bloqueo de contenido, almacenamiento, identidad, interfaz y servicios de plataforma.
6. **Transparencia:** documentar limitaciones, decisiones técnicas y resultados de pruebas; no atribuir protección absoluta a ningún mecanismo.

## Arquitectura objetivo

| Módulo | Responsabilidad |
| --- | --- |
| Motor web | Renderizado, compatibilidad con estándares web y actualizaciones de seguridad. |
| Protección de contenido | Filtrado de solicitudes y recursos, reglas de bloqueo y mitigaciones antirrastreo. |
| Datos locales | Marcadores, historial, preferencias y perfiles con políticas de retención. |
| Bóveda de credenciales | Cifrado autenticado, gestión de claves y desbloqueo mediante mecanismos seguros de cada sistema. |
| Interfaz | Navegación accesible y adaptable a cada plataforma. |
| Plataforma | Integración con sistemas operativos, sandbox, permisos y actualizaciones. |
| Pruebas | Seguridad, compatibilidad, regresiones y benchmarks de rendimiento. |

**Motor seleccionado:** Firefox/Gecko para escritorio y GeckoView para Android/TV. Actualmente solo existe el andamiaje de integración, con la revisión oficial de Firefox 159.0.1 fijada: no hay motor compilado ni ejecutable NOLP. iOS/iPadOS sigue sujeto a validación específica.

## Privacidad y seguridad

NOLP aspira a mantener los datos personales en el dispositivo, protegidos mediante mecanismos criptográficos modernos y almacenamiento de claves respaldado por el sistema operativo cuando esté disponible. El cifrado local no sustituye al aislamiento de procesos, las actualizaciones de seguridad ni a una estrategia de recuperación de datos.

El bloqueo de anuncios y rastreadores se diseñará como un componente independiente, con reglas mantenibles, actualización verificable de listas y controles comprensibles. **Ningún bloqueador puede garantizar la eliminación total de anuncios, rastreo o telemetría de terceros.**

## Estado técnico y documentación de seguimiento

La referencia central para saber exactamente **qué existe, qué falta y cómo comprobarlo** es [Estado real y hoja de ruta](docs/PROJECT-STATUS-AND-ROADMAP.md). Complementos: [inicio y bootstrap](docs/BOOTSTRAP.md), [versiones upstream](docs/UPSTREAM-STATUS.md), [arquitectura](docs/ARCHITECTURE.md) y [skill de actualización](skills/upstream-currentness/SKILL.md).

## Hoja de ruta

- [ ] Definir plataformas objetivo y matriz de compatibilidad.
- [x] Seleccionar Firefox/Gecko como base y documentar estrategia inicial de actualización (release estable 159.0.1 verificada; build pendiente).
- [x] Documentar el modelo inicial de amenazas y las políticas de privacidad (implementación pendiente).
- [x] Diseñar la arquitectura modular y sus contratos (implementación pendiente).
- [ ] Implementar un prototipo mínimo de navegación.
- [ ] Integrar almacenamiento local y bóveda de credenciales.
- [ ] Desarrollar el motor de filtrado y las protecciones antirrastreo.
- [ ] Incorporar pruebas automatizadas, análisis de dependencias y benchmarks.
- [ ] Publicar versiones reproducibles y documentación de seguridad.

La prioridad será disponer primero de una base verificable y mantenible, antes de añadir funcionalidades avanzadas.

## Política vigente de interfaz

NOLP utiliza únicamente temas **claro** y **oscuro**, con detección automática de la preferencia del sistema y selección manual. **Aero y Acrylic personalizados quedan descartados**: no forman parte de la arquitectura ni del plan de implementación. La interfaz debe priorizar superficies nativas estables, legibilidad, accesibilidad y rendimiento. Los efectos de transparencia o desenfoque no son requisitos y no se introducirán sin una evaluación específica por plataforma y mediciones de rendimiento.

## Identidad visual

El símbolo vectorial oficial se encuentra en [`assets/brand/nolp-icon.svg`](assets/brand/nolp-icon.svg), la marca horizontal en [`assets/brand/nolp-wordmark.svg`](assets/brand/nolp-wordmark.svg) y las reglas de uso en [`docs/BRAND.md`](docs/BRAND.md). Los recursos para aplicaciones se generarán a partir de estos originales al implementar cada plataforma.

## Desarrollo y contribuciones

El proyecto está en fase inicial de implementación. Existen scripts y un workflow de compilación experimental de Firefox upstream, **sin resultado satisfactorio verificado**. Véase [Bootstrap](docs/BOOTSTRAP.md); todavía no existe una compilación ni una aplicación NOLP distribuible.

Las propuestas deben priorizar seguridad, compatibilidad, rendimiento demostrado y mantenimiento a largo plazo. Los cambios de arquitectura deberán acompañarse de justificación técnica y pruebas cuando corresponda.

## Licencia

El código propio de NOLP se distribuye bajo la **Mozilla Public License 2.0 (MPL-2.0)**. Consulta [LICENSE](LICENSE). Los componentes de Firefox/Gecko y las dependencias de terceros conservan sus respectivas licencias y avisos. La licencia del código no concede derechos sobre el nombre ni el logotipo NOLP.

---

**NOLP — Next · Óptima · Local · Privada.**
