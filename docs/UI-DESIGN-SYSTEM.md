# NOLP UI — Aero Glass + Acrylic contemporáneo

**Estado:** especificación de diseño aprobada como objetivo; **no implementada**. Identidad: Next · Óptima · Local · Privada.

## Material híbrido oficial: Aero Glass + Acrylic
La identidad NOLP prioriza **Aero Glass** (transparencia real, continuidad visual y profundidad) y utiliza **Acrylic** solo como complemento funcional en menús y paneles. Dirección estética orientativa: 80 % Glass / 20 % Acrylic, no un porcentaje medible de píxeles. Modernizar el material, sin reproducir literalmente versiones antiguas de Windows.

- **Barra de título, pestañas y navegación:** superficie Glass continua y ligera, con transparencia contextual; evitar múltiples capas de blur superpuestas.
- **Menús, cuadros, paneles y overlays:** Acrylic más difuso y tintado para legibilidad; limitar área, frecuencia de recomposición y coste de GPU.
- **Omnibox y controles interactivos:** superficies con contraste estable y delimitación visual clara, sin sacrificar legibilidad por transparencia.
- **Contenido web:** renderizado independiente y sin filtros de cristal sobre las páginas.
- **Composición:** usar APIs nativas soportadas por cada plataforma; no asumir que Windows DWM/Mica/Acrylic, macOS vibrancy y Linux compositors ofrecen exactamente las mismas capacidades. Mica puede ser una alternativa de respaldo, no un equivalente a Acrylic con blur.
- **Fallback:** superficie opaca coherente con el tema si el sistema no soporta transparencia o si accesibilidad, ahorro energético o estabilidad lo requieren.
- **Efectos adaptativos:** evitar blur de pantalla completa, capturas de fondo por fotograma, múltiples passes de desenfoque y sobrecostes de vídeo; perfilar en hardware representativo.
- **Evidencia:** validar materiales y APIs con documentación oficial de la plataforma en el momento de implementarlos; no afirmar que están disponibles o integrados sin pruebas.

## Dos temas, sin variantes adicionales
1. **Claro — Aero Light:** superficies de cristal translúcido claro, tinte blanco neutro, tipografía oscura, bordes finos y profundidad discreta.
2. **Oscuro — Aero Dark:** cristal translúcido ahumado, tinte negro/gris carbón, tipografía clara, contraste elevado y profundidad discreta.

Solo dos opciones visibles: Claro y Oscuro. No añadir temas de colores, modo automático independiente ni skins heredadas. Mantener un acento visual coherente con la identidad NOLP y no saturar la interfaz.

## Geometría — Aero de bordes definidos
- Preferir geometría **rectangular, casi cuadrada**: radio visual orientativo de **2–4 px** en marcos y paneles; evitar esquinas grandes, píldoras y tarjetas redondeadas.
- Pestañas y barra de direcciones compactas, rectangulares y claramente delimitadas; ajustar radio según accesibilidad y convenciones del sistema cuando sea imprescindible.
- Separadores finos, bordes de 1 px donde ayuden a delimitar superficies, sombras mínimas y profundidad aportada por el propio cristal.
- Evitar estéticas Fluent Design, Liquid Glass, neumorfismo, tarjetas sobredimensionadas y decoraciones innecesarias.
- Material principal: vidrio Aero transparente; Acrylic solo en superficies flotantes que requieran mayor difusión y contraste.

## Principios de composición
- Interfaz limpia, compacta y reconocible: barra de pestañas, navegación, omnibox, controles de privacidad, descargas y menús; sin tarjetas decorativas innecesarias.
- Transparencia aplicada a **chrome UI**, no al contenido web; nunca permitir que el fondo interfiera con lectura, formularios, seguridad o señales de origen.
- Cristal con transparencia y desenfoque moderado **solo donde el sistema lo soporte**. Preferir composición nativa de Windows/macOS/Linux y equivalentes de Android cuando estén disponibles; no inventar APIs ni usar CSS costoso por defecto.
- La superficie debe mantener contraste y legibilidad sobre fondos claros, oscuros, vídeos o ventanas ajenas. Emplear tintes opacos de respaldo, bordes sutiles y superficies elevadas cuando la transparencia sea insuficiente.
- Sin sombras excesivas, brillos, gradientes recargados, animaciones largas ni decoraciones que aumenten la latencia.
- Respetar preferencias de accesibilidad: reducción de movimiento, contraste reforzado, escala tipográfica y transparencia reducida cuando la plataforma lo exija. Estas adaptaciones **no constituyen temas adicionales**.
- Navegación por teclado y lector de pantalla en escritorio; foco visible y mando en Android TV; tamaños táctiles adecuados en móvil.

## Arquitectura
- Tokens semánticos: `surface.chrome`, `surface.menu`, `surface.overlay`, `text.primary`, `text.secondary`, `border.subtle`, `focus.visible`, `accent`, `blur.chrome`, `opacity.chrome`.
- Un único sistema de tokens y dos conjuntos de valores (light/dark), con adaptadores por plataforma; evitar duplicación de componentes.
- Separar tema, estado de UI y motor Gecko. Ninguna dependencia del motor respecto a los tokens visuales.
- Aplicar fallback opaco cuando compositor, energía, accesibilidad, hardware o drivers no permitan blur/transparencia fiables.
- Mantener señales de seguridad (TLS, permisos, descargas peligrosas, modo privado) distinguibles sin depender exclusivamente del color.

## Rendimiento y validación
- Medir CPU/GPU, memoria, fotogramas perdidos, tiempo de respuesta de pestañas/omnibox/menús, reproducción de vídeo y consumo energético con/sin efectos de cristal.
- No usar blur dinámico sobre grandes áreas del contenido web ni forzar capturas del fondo por fotograma.
- Evitar recomposición o repintado global por cambios de foco o animación; usar regiones y superficies pequeñas.
- Verificar sobre equipos con GPU y sin aceleración adecuada; respetar batería y reducir efectos si degradan la experiencia.
- Probar ambos temas en alto contraste, escalado, lector de pantalla, teclado, TV y fondos extremos.
- Registrar benchmarks antes/después y pruebas de regresión. No afirmar que el diseño es más rápido hasta medirlo.

## Implementación por fases
1. Definir tokens y prototipo funcional de chrome UI en escritorio con navegación real.
2. Integrar superficies Aero con capacidades reales de composición de cada SO.
3. Implementar menús, pestañas, omnibox y paneles de privacidad; validar accesibilidad.
4. Adaptar componentes a GeckoView Android y Android TV sin arrastrar el diseño de escritorio de forma literal.
5. Medir y optimizar en hardware representativo; mantener fallback seguro y sin efectos.

**Criterio de aceptación:** dos temas coherentes, translucidez segura con fallback, navegación accesible, rendimiento sin regresiones relevantes y tests documentados.

## Barra superior, anti-IA y cuentas (requisitos de producto)
- Barra de menú y navegación **arriba**, compacta, rectangular y con material Aero Glass; accesible por teclado y con indicadores claros de seguridad.
- **Filtro anti-IA habilitado por defecto**, con interruptor visible en Ajustes para desactivarlo y reactivarlo. Su alcance debe desglosarse en: integraciones de IA del navegador, endpoints conocidos y elementos identificables mediante reglas. Evitar promesas de detección total, bloqueo indiscriminado y roturas silenciosas; mostrar excepciones y diagnósticos locales.
- **Cuentas locales por defecto:** perfil, marcadores, historial, preferencias y vault local protegido; sin cuenta en línea ni sincronización automática. No presentar el perfil local como una cuenta remota.
- **Firefox Account opcional:** el usuario puede elegir explícitamente iniciar sesión y habilitar funciones oficiales de Mozilla, si la integración upstream es soportada y cumple requisitos de privacidad. No implementar credenciales propias para imitar Mozilla ni afirmar compatibilidad sin pruebas.
- Cambiar de local a online requiere consentimiento granular por categoría de datos; **nunca subir contraseñas, historial, marcadores ni claves automáticamente**. Cambiar a local deshabilita sincronización y revoca sesiones/tokens según capacidades oficiales, sin borrar datos locales sin confirmación.
- Ambos controles son reversibles, con estado persistido localmente, migraciones seguras y pruebas de privacidad/red. El filtro anti-IA no debe interferir con la autenticación oficial por defecto; documentar excepciones mínimas.
- **Estado:** requisitos documentados, sin implementación funcional ni validación.

## Implementación multiplataforma normativa
Consultar `docs/UI-CROSS-PLATFORM-ARCHITECTURE.md`. Compartir tokens semánticos, estado y comportamiento, pero adaptar el renderer a cada plataforma. Desktop conserva Firefox Chrome UI; Android/TV evalúa Compose con GeckoView. El compositor y las animaciones no deben bloquear navegación ni vídeo. Contratos tipados, eventos incrementales y accesibilidad son requisitos, no funcionalidades ya implementadas.
