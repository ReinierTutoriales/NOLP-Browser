# NOLP UI — Aero contemporáneo

**Estado:** especificación de diseño aprobada como objetivo; **no implementada**. Identidad: Next · Óptima · Local · Privada.

## Dos temas, sin variantes adicionales
1. **Claro — Aero Light:** superficies de cristal translúcido claro, tinte blanco neutro, tipografía oscura, bordes finos y profundidad discreta.
2. **Oscuro — Aero Dark:** cristal translúcido ahumado, tinte negro/gris carbón, tipografía clara, contraste elevado y profundidad discreta.

Solo dos opciones visibles: Claro y Oscuro. No añadir temas de colores, modo automático independiente ni skins heredadas. Mantener un acento visual coherente con la identidad NOLP y no saturar la interfaz.

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
