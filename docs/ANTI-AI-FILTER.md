# NOLP — Filtro anti-IA (especificación)

**Estado:** requisitos aprobados, sin motor de filtrado implementado ni eficacia demostrada.

## Política de producto
- **Activado por defecto**, desactivable y reactivable en Configuración sin afectar el modo de cuenta local o Firefox Account.
- **Elección explícita del usuario:** cuando desactive el filtro, las funciones de IA propias del navegador que sean compatibles podrán habilitarse individualmente, y los asistentes, resúmenes y respuestas de IA de las páginas dejarán de ocultarse o bloquearse por las reglas de NOLP. No se obliga a usar IA ni se instala automáticamente ningún servicio externo.
- **Control granular:** el usuario puede activar o desactivar cada categoría (integraciones del navegador, IA en páginas, endpoints conocidos) y crear excepciones por sitio. Mostrar claramente qué se habilita y si implica conexión o tratamiento de datos por terceros; no atribuir a NOLP control sobre el funcionamiento interno de esos servicios.
- Cobertura deseada: (1) funciones y asistentes de IA integrados en el navegador, (2) asistentes, chatbots, resúmenes y respuestas generadas por IA dentro de páginas web, (3) conexiones conocidas a proveedores de IA, cuando las reglas sean suficientemente precisas.
- **Sin bloqueo universal garantizado**: la identificación de contenido generado por IA puede ser imposible si está mezclado con contenido normal. No usar clasificadores opacos, telemetría ni enviar contenido del usuario a terceros para decidir.
- El filtrado de elementos de páginas debe ser reversible por sitio, documentar reglas y evitar ocultar resultados normales, controles de accesibilidad o contenido editorial legítimo.
- Mantener categorías independientes (integraciones propias, IA en páginas, endpoints de red) bajo un interruptor principal. El estado inicial de todas las categorías es activo, con excepciones precisas por sitio.
- Nunca desactivar sandbox, TLS, aislamiento, actualizaciones de seguridad ni funciones de autenticación para imponer el filtro.

## Implementación propuesta
1. **Bloqueo propio**: deshabilitar componentes de IA opcionales del navegador en las capas soportadas y verificar ausencia de conexiones correspondientes.
2. **Bloqueo de red**: reglas locales versionadas, revisadas y probadas contra falsos positivos; evitar bloqueos de dominios compartidos que rompan servicios completos.
3. **Filtrado cosmético**: selectores y reglas por dominio para ocultar módulos identificables de respuestas/resúmenes de IA en resultados y sitios. Preferir APIs de extensiones soportadas; no ejecutar scripts remotos ni inspeccionar contraseñas.
4. **Excepciones**: controles por sitio y registro de decisiones local, sin historial de contenido sensible ni envíos externos.
5. **Actualizaciones**: listas firmadas/verificadas cuando se distribuyan remotamente, reemplazo atómico, rollback y pruebas de compatibilidad; sin requerir cuentas ni nube.

## Pruebas de aceptación
- Instalación nueva: filtro activo, las tres categorías activas; cambio global persistente tras reiniciar.
- El usuario puede desactivarlo totalmente y volver a activarlo; el cambio no modifica cuenta ni sincronización.
- Con filtro desactivado, los elementos de IA previamente ocultos en sitios de prueba vuelven a mostrarse, siempre que el sitio los ofrezca. Las funciones integradas solo se activan cuando existan y el usuario las elija.
- Con filtros parciales, cada categoría y excepción funciona independientemente, sin cambios ocultos a permisos ni envío automático de datos.
- Sitios de prueba con resúmenes, asistentes y respuestas de IA identificables: las reglas conocidas actúan correctamente; medir falsos positivos y compatibilidad.
- Sitios sin elementos de IA: no ocultar contenido normal; verificar accesibilidad y navegación.
- Evaluar impacto de latencia, CPU, RAM y renderizado con filtro activo/inactivo; no afirmar mejoras sin benchmark.
- Sin tráfico de telemetría propia ni clasificación en nube; pruebas de red reproducibles.

## Riesgos y límites
- Respuestas de IA servidas como HTML normal no son distinguibles de forma fiable sin señales del sitio.
- El bloqueo de endpoints compartidos puede romper autenticación, búsqueda, vídeos u otras funciones.
- Las reglas requieren mantenimiento continuo ante cambios de sitios. Se prioriza precisión y reversibilidad sobre cobertura ficticia.
