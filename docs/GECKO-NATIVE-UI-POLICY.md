# NOLP — Política de interfaz Gecko-native e identidad propia

**Estado:** decisión arquitectónica obligatoria. No implica que exista una compilación nativa terminada.

## Principio rector
**Gecko y Firefox determinan la infraestructura de interfaz; NOLP determina la identidad visual, la experiencia y las capacidades diferenciadoras.** Reutilizar primero, personalizar después y crear componentes propios únicamente ante una necesidad comprobada.

## Reutilización prioritaria
- Usar Firefox Desktop Chrome UI y su infraestructura existente: pestañas, Urlbar, navegación, menús, historial, permisos, identidad TLS, accesibilidad, ventanas, GPU y compositor.
- No reconstruir gestores de pestañas, seguridad, historial ni controles de vídeo si Firefox ya proporciona una solución mantenida.
- Evitar frameworks gráficos paralelos (WinUI, Electron, Qt, etc.) solo para decorar Firefox. Evitar usar `userChrome.css` como interfaz de producción.
- Mantener parches mínimos, separados, revisables y fáciles de actualizar frente al upstream estable y soportado.

## Identidad NOLP
- Utilizar el logotipo oficial existente en `assets/brand/nolp-official.png`, sin reemplazarlo por aproximaciones.
- Diseñar una identidad coherente de iconos, proporciones, densidad, tipografía, espaciado, estados, foco, controles y menús, sin copiar íntegramente el aspecto de Windows, macOS ni Firefox.
- **Exactamente dos temas:** NOLP Dark y NOLP Light. Transparencia reducida, alto contraste y superficies opacas son adaptaciones de accesibilidad/rendimiento, no temas adicionales.
- Los tokens semánticos de diseño se comparten; la composición y el comportamiento de ventanas siguen siendo nativos de cada plataforma.

## Materiales y plataformas
- **Windows 11:** reutilizar primero la integración nativa Firefox/DWM. Evaluar Mica Alt para la superficie persistente de ventanas con pestañas; usar Acrylic solo para superficies transitorias cuando haya beneficio medido. La API DWM no garantiza que el fondo sea visible bajo el chrome real de Firefox; demostrarlo en una compilación real.
- **Windows sin soporte:** respetar el chrome nativo y ofrecer superficie opaca.
- **macOS:** reutilizar AppKit, vibrancy y composición existentes en Firefox; evitar un segundo `NSWindow`/renderer.
- **Linux:** reutilizar GTK y composición Wayland/X11; no depender de un protocolo de desenfoque exclusivo de un compositor. Fallback opaco.
- **Android:** usar GeckoView y controles nativos apropiados para Android; no trasladar la composición de escritorio.
- Nunca aplicar desenfoque de chrome sobre contenido web ni vídeo.

## Optimización y mantenimiento
- Evitar reflows síncronos, repintados redundantes, animaciones en el hilo principal, filtros de blur por CSS de gran superficie y procesos residentes innecesarios.
- Aprovechar herramientas de Firefox (Gecko Profiler, pruebas browser-chrome/mochitest y herramientas de rendimiento) antes de añadir instrumentación propia.
- Para cada cambio: hipótesis, versión exacta de Firefox, comparación contra Firefox base, pruebas funcionales, métricas de inicio, memoria, CPU, GPU, latencia, vídeo, accesibilidad y ruta de reversión.
- Conservar sandbox, aislamiento de sitios, TLS, indicadores de seguridad y parches Mozilla. Aplicar las puertas obligatorias Latest Stable y Security Assurance.
- Ningún prototipo HTML ni CI de documentación demuestra una interfaz Gecko nativa operativa.

## Orden de ejecución
1. Compilar y ejecutar una ventana Firefox derivada real y fijar la línea base.
2. Auditar las integraciones upstream por plataforma y definir tokens de los dos temas.
3. Integrar identidad NOLP y estilos en Chrome UI con cambios mínimos.
4. Evaluar adaptadores de materiales nativos solo si Firefox no ofrece ya el mecanismo adecuado.
5. Ejecutar pruebas de seguridad, compatibilidad, accesibilidad y benchmarks comparativos antes de declarar la función terminada.

Documentación relacionada: `AGENTS.md`, `docs/UI-DESIGN-SYSTEM.md`, `docs/ENGINEERING.md`, `docs/NATIVE-AERO-INTEGRATION.md` (propuesta en PR #10).

Referencias oficiales:
- https://firefox-source-docs.mozilla.org/
- https://learn.microsoft.com/en-us/windows/win32/api/dwmapi/ne-dwmapi-dwm_systembackdrop_type
- https://learn.microsoft.com/en-us/windows/apps/develop/ui/system-backdrops
