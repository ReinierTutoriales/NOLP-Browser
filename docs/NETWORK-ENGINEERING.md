# NOLP — Guía de ingeniería de red y seguridad

**Estado:** especificación técnica y plan de trabajo. **Sin implementación funcional ni benchmarks verificados.**
**Fecha de revisión documental:** 2026-11-06. Revisar versiones y documentación oficial antes de codificar.

## Decisión arquitectónica
Conservar **Necko** como stack de red Gecko, **NSS** para TLS y **Neqo** para QUIC/HTTP/3, usando mecanismos soportados por Firefox. No introducir un proxy local residente ni un stack HTTP/TLS paralelo sin necesidad demostrada. El controlador de políticas NOLP decide mediante contratos pequeños; el adaptador Gecko aplica decisiones donde la API lo permita.

## Responsabilidades propuestas
- **network-policy:** configuración de red y evaluación de políticas (contratos, precedencia y excepciones).
- **network-privacy:** opciones de DNS/DoH, ECH, particionamiento, conexiones anticipadas y compatibilidad con VPN/proxy.
- **network-filter:** composición de decisiones del bloqueador y filtro anti-IA antes de enviar solicitudes, donde la plataforma permita intervenir.
- **network-diagnostics:** métricas locales y redacción de información sensible.
- **network-tests:** pruebas de integración, regresión, seguridad y rendimiento.

Los cinco son **submódulos previstos**, no paquetes ejecutables existentes. Integrarlos con el inventario general de módulos y evitar dependencia directa entre módulos funcionales: comunicación mediante `contracts`, composición en `core`. Mantener `engine-gecko` como adaptador.

## Política por defecto y controles
1. **TLS:** conservar validación de certificados, TLS 1.3 y políticas de seguridad de Mozilla; no degradar TLS ni deshabilitar comprobaciones.
2. **HTTP/3/QUIC:** mantener negociación compatible con Firefox, con fallback seguro; no forzar HTTP/3 cuando una red o servidor no lo admite.
3. **DNS/DoH:** ofrecer modo equilibrado inicial y modo estricto opcional. No imponer proveedor público único ni asegurar que DoH impide todo rastreo. Tratar DNS local, VPN, proxy, portales cautivos y redes empresariales.
4. **ECH:** preservar el soporte de Firefox cuando el servidor y DNS lo permitan; no garantizar ECH universal ni equipararlo a anonimato.
5. **Particionamiento:** conservar particionamiento de estado, caché y conexiones de Firefox; no compartir identificadores entre sitios para mejorar benchmarks.
6. **Prefetch/preconnect:** medir antes de desactivar o restringir; balancear privacidad, latencia, consumo y compatibilidad.
7. **Bloqueo:** aplicar decisiones locales de anuncios/rastreadores/IA sin interceptación TLS ni scripts remotos arbitrarios. Evitar bloqueo de dominios compartidos y documentar excepciones.
8. **Observabilidad:** diagnósticos locales y opcionales, con mínimos metadatos; no registrar URLs completas, consultas sensibles, cookies, tokens ni credenciales por defecto.
9. **Seguridad de actualización:** listas y reglas con integridad, procedencia, reemplazo atómico, versionado y rollback.
10. **Fallo seguro:** un fallo de filtrado no puede desactivar el sandbox, alterar TLS ni corromper cuentas/vault. Especificar explícitamente comportamiento ante errores por categoría.

## Contratos mínimos a diseñar
- `NetworkRequestContext`: origen, partición, tipo de recurso y capacidades, minimizando datos.
- `NetworkPolicyDecision`: permitir/bloquear/solicitar decisión, regla, motivo y excepción, sin datos sensibles.
- `ResolverPolicy`: modo DNS, excepciones de red y fallback autorizado.
- `NetworkDiagnostics`: contadores y temporización agregados sin telemetría externa.

No congelar interfaces públicas ni elegir IPC hasta contrastar las APIs realmente disponibles en la versión Gecko fijada.

## Verificación y benchmarks
- Comparar Firefox upstream vs NOLP en igual versión de motor, SO, hardware, DNS, red y conjunto de sitios.
- Medir: resolución DNS, tiempo de conexión, TLS handshake, TTFB, navegación, solicitudes y bytes evitados, CPU, RAM, energía y fallos.
- Probar: TLS/certificados, HTTP/2 y HTTP/3, fallback, DoH estricto/equilibrado, ECH compatible/incompatible, VPN, proxies, portales cautivos, DNS local, IPv4/IPv6 y redes con pérdida.
- Seguridad: fugas DNS según modo, aislamiento entre sitios, excepciones por dominio, protección de credenciales y ausencia de telemetría propia no consentida.
- Regresión: compatibilidad de vídeo, autenticación, pagos, descargas, WebSockets y sitios con CDN compartidas.
- No afirmar mejoras sin mediciones reproducibles y resultados de CI.

## Orden de implementación
1. Validar compilación y arranque del Gecko upstream fijado.
2. Inventariar capacidades y puntos de integración reales de Necko, DNS, ECH y WebExtensions.
3. Definir y probar contratos de `network-policy`; añadir módulos al manifiesto con estado correcto.
4. Integrar adaptador de políticas sin interceptación TLS ni cambios profundos upstream.
5. Integrar filtrado y anti-IA por reglas auditadas, con pruebas de falsos positivos.
6. Añadir diagnósticos locales, benchmark y matriz de compatibilidad.
7. Habilitar opciones avanzadas únicamente después de verificar funcionamiento, seguridad y reversibilidad.

## Referencias primarias a contrastar al implementar
- Mozilla Firefox Source Docs: https://firefox-source-docs.mozilla.org/
- Mozilla Necko: https://firefox-source-docs.mozilla.org/networking/
- Mozilla NSS: https://firefox-source-docs.mozilla.org/security/nss/
- Mozilla Firefox DNS over HTTPS: https://support.mozilla.org/en-US/kb/firefox-dns-over-https
- Mozilla Firefox Total Cookie Protection: https://support.mozilla.org/en-US/kb/introducing-total-cookie-protection-standard-mode
- IETF TLS 1.3: https://www.rfc-editor.org/rfc/rfc8446
- IETF HTTP/3: https://www.rfc-editor.org/rfc/rfc9114
- IETF QUIC: https://www.rfc-editor.org/rfc/rfc9000
- IETF ECH: verificar estado de especificación y soporte vigente antes de implementar.

**Regla de mantenimiento:** actualizar esta guía, `docs/ENGINEERING.md`, `docs/PROJECT-STATUS-AND-ROADMAP.md` y `modules/manifest.json` cuando cambien políticas, módulos o evidencias.
