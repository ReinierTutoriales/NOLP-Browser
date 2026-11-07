# NOLP — Sistema visual vigente

**Estado:** especificación de diseño; implementación y rendimiento por validar.
**Identidad:** Nex · Óptimo · Local · Privado.

## Decisión arquitectónica

NOLP utiliza **solo dos temas: claro y oscuro**. Aero Glass, Acrylic personalizado, desenfoque dinámico y transparencia obligatoria están **descartados**. No se desarrollará un compositor propio ni se incorporarán efectos visuales que requieran parches adicionales al motor Gecko.

La interfaz usa superficies opacas, controles soportados por Firefox o el sistema operativo, y colores semánticos. La preferencia del sistema se sigue por defecto; una elección manual de claro u oscuro tiene prioridad. El seguimiento automático del sistema no constituye un tercer tema visual.

## Diseño

- Geometría compacta y mayormente rectangular, con bordes discretos y controles accesibles.
- Barra superior, pestañas y omnibox coherentes, sin tarjetas decorativas.
- Dos conjuntos de tokens semánticos: superficie, texto, borde, foco y acento.
- Indicadores de privacidad y seguridad distinguibles por texto o icono, no solo por color.
- Alto contraste, reducción de movimiento y tamaños de texto respetan las preferencias del sistema.
- El contenido web permanece independiente de la apariencia del chrome del navegador.

## Rendimiento y mantenimiento

- No usar blur, captura de fondo, shaders personalizados ni repintado continuo para decoración.
- Preferir componentes existentes y APIs estables a nuevos parches internos de Firefox.
- Medir arranque, latencia de interacción, memoria, CPU/GPU y reproducción multimedia antes de afirmar mejoras.
- Mantener dos temas y un solo conjunto de tokens, con adaptadores mínimos por plataforma.
- Cualquier nueva propuesta visual debe justificar coste de mantenimiento y demostrar que no introduce regresiones.

## Implementación por fases

1. Consolidar tokens claro/oscuro y seguimiento del sistema en Firefox Desktop.
2. Completar barra, pestañas, menús, omnibox y ajustes con controles accesibles.
3. Adaptar la experiencia a GeckoView y UI nativa Android/TV sin replicar código de escritorio.
4. Validar rendimiento y accesibilidad con métricas reproducibles.

**Aceptación:** navegación funcional, dos temas consistentes, ninguna dependencia de Aero/Acrylic, accesibilidad y rendimiento medidos.

## Barra superior, anti-IA y cuentas (requisitos de producto)
- Barra de menú y navegación **arriba**, compacta, rectangular y con superficie opaca nativa; accesible por teclado y con indicadores claros de seguridad.
- **Filtro anti-IA habilitado por defecto**, con interruptor visible en Ajustes para desactivarlo y reactivarlo. Su alcance debe desglosarse en: integraciones de IA del navegador, endpoints conocidos y elementos identificables mediante reglas. Evitar promesas de detección total, bloqueo indiscriminado y roturas silenciosas; mostrar excepciones y diagnósticos locales.
- **Cuentas locales por defecto:** perfil, marcadores, historial, preferencias y vault local protegido; sin cuenta en línea ni sincronización automática. No presentar el perfil local como una cuenta remota.
- **Firefox Account opcional:** el usuario puede elegir explícitamente iniciar sesión y habilitar funciones oficiales de Mozilla, si la integración upstream es soportada y cumple requisitos de privacidad. No implementar credenciales propias para imitar Mozilla ni afirmar compatibilidad sin pruebas.
- Cambiar de local a online requiere consentimiento granular por categoría de datos; **nunca subir contraseñas, historial, marcadores ni claves automáticamente**. Cambiar a local deshabilita sincronización y revoca sesiones/tokens según capacidades oficiales, sin borrar datos locales sin confirmación.
- Ambos controles son reversibles, con estado persistido localmente, migraciones seguras y pruebas de privacidad/red. El filtro anti-IA no debe interferir con la autenticación oficial por defecto; documentar excepciones mínimas.
- **Estado:** requisitos documentados, sin implementación funcional ni validación.

## Implementación multiplataforma normativa
Consultar `docs/UI-CROSS-PLATFORM-ARCHITECTURE.md`. Compartir tokens semánticos, estado y comportamiento, pero adaptar el renderer a cada plataforma. Desktop conserva Firefox Chrome UI; Android/TV evalúa Compose con GeckoView. El compositor y las animaciones no deben bloquear navegación ni vídeo. Contratos tipados, eventos incrementales y accesibilidad son requisitos, no funcionalidades ya implementadas.
