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
