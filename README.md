<div align="center">

<img src="assets/brand/nolp-wordmark.svg" alt="NOLP — Nexo Óptimo Local y Privado" width="520" />

</div>

# NOLP

**Nexo Óptimo Local y Privado**

> Un navegador pensado para ofrecer rendimiento, autonomía y privacidad sin depender innecesariamente de servicios en la nube.

**Estado:** proyecto en fase inicial de diseño y desarrollo. Las capacidades descritas a continuación son objetivos de arquitectura, no funcionalidades ya disponibles.

## ¿Qué significa NOLP?

- **N — Nexo:** conexión y acceso a la web.
- **O — Óptimo:** eficiencia, fluidez y uso responsable de recursos.
- **L — Local:** datos y preferencias bajo control del usuario, prioritariamente en su dispositivo.
- **P — Privado:** privacidad y seguridad integradas desde el diseño.

NOLP también puede leerse como **Navegador Óptimo Local y Privado**.

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

**Motor previsto:** evaluar la familia tecnológica Firefox/Gecko y sus opciones reales de integración por plataforma antes de fijar una implementación. No se presupone que un mismo motor pueda distribuirse de forma idéntica en todos los sistemas.

## Privacidad y seguridad

NOLP aspira a mantener los datos personales en el dispositivo, protegidos mediante mecanismos criptográficos modernos y almacenamiento de claves respaldado por el sistema operativo cuando esté disponible. El cifrado local no sustituye al aislamiento de procesos, las actualizaciones de seguridad ni a una estrategia de recuperación de datos.

El bloqueo de anuncios y rastreadores se diseñará como un componente independiente, con reglas mantenibles, actualización verificable de listas y controles comprensibles. **Ningún bloqueador puede garantizar la eliminación total de anuncios, rastreo o telemetría de terceros.**

## Hoja de ruta

- [ ] Definir plataformas objetivo y matriz de compatibilidad.
- [ ] Seleccionar y justificar el motor web y su estrategia de actualización.
- [ ] Establecer el modelo de amenazas y las políticas de privacidad.
- [ ] Diseñar la arquitectura modular y sus contratos.
- [ ] Implementar un prototipo mínimo de navegación.
- [ ] Integrar almacenamiento local y bóveda de credenciales.
- [ ] Desarrollar el motor de filtrado y las protecciones antirrastreo.
- [ ] Incorporar pruebas automatizadas, análisis de dependencias y benchmarks.
- [ ] Publicar versiones reproducibles y documentación de seguridad.

La prioridad será disponer primero de una base verificable y mantenible, antes de añadir funcionalidades avanzadas.

## Identidad visual

El símbolo vectorial oficial se encuentra en [`assets/brand/nolp-icon.svg`](assets/brand/nolp-icon.svg), la marca horizontal en [`assets/brand/nolp-wordmark.svg`](assets/brand/nolp-wordmark.svg) y las reglas de uso en [`docs/BRAND.md`](docs/BRAND.md). Los recursos para aplicaciones se generarán a partir de estos originales al implementar cada plataforma.

## Desarrollo y contribuciones

El proyecto está en fase de definición. Aún no se publican instrucciones de compilación porque no existe una configuración de construcción verificada en este repositorio.

Las propuestas deben priorizar seguridad, compatibilidad, rendimiento demostrado y mantenimiento a largo plazo. Los cambios de arquitectura deberán acompañarse de justificación técnica y pruebas cuando corresponda.

## Licencia

El código propio de NOLP se distribuye bajo la **Mozilla Public License 2.0 (MPL-2.0)**. Consulta [LICENSE](LICENSE). Los componentes de Firefox/Gecko y las dependencias de terceros conservan sus respectivas licencias y avisos. La licencia del código no concede derechos sobre el nombre ni el logotipo NOLP.

---

**NOLP — Nexo Óptimo Local y Privado.**
