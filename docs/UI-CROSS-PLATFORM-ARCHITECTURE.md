# NOLP — UI multiplataforma y comunicación eficiente entre módulos

**Estado:** decisión arquitectónica y criterios de implementación; no es una UI ni un runtime Rust operativo.
**Revisión:** 2026-11-06. Contrastar versiones y soporte en cada implementación.

## Decisión
Compartir **lógica, estado, contratos y tokens**; no imponer un único renderer gráfico ni un framework webview adicional. En escritorio, evolucionar la interfaz Firefox Chrome UI sin sustituir Gecko. En Android/TV, evaluar Jetpack Compose y Compose for TV con GeckoView, sujeto a compatibilidad y benchmarks. No utilizar Tauri como base del navegador Gecko: su UI se apoya en WebViews del sistema y añadiría otra dependencia de motor.

## Matriz de plataforma
| Plataforma | Superficie de UI propuesta | Integración |
| --- | --- | --- |
| Windows | Firefox Chrome UI + composición del SO cuando sea viable | Adaptador Gecko y DWM |
| Linux | Firefox Chrome UI + GTK/Wayland/compositor según disponibilidad | Adaptador Gecko |
| macOS | Firefox Chrome UI + AppKit/compositor cuando corresponda | Adaptador Gecko |
| Android | Compose nativo + GeckoView | Adaptador Kotlin ↔ Rust/GeckoView |
| Android TV | Compose for TV, foco y mando + GeckoView | Adaptador Kotlin ↔ Rust/GeckoView |

No prometer paridad exacta de materiales, API, rendimiento ni soporte sin pruebas.

## Contratos y flujos
- **Mismo proceso Rust:** traits y llamadas tipadas directas; no usar JSON, IPC ni buses globales para operaciones triviales.
- **Rust ↔ Kotlin/Swift:** evaluar UniFFI para contratos compartidos donde las APIs, costes FFI y empaquetado lo permitan. No forzar UniFFI en interfaces Gecko ya existentes.
- **Frontend Firefox ↔ Gecko:** usar mecanismos documentados y adecuados al límite real (módulos JS, XPCOM, JSActors, WebIDL, IPDL según contexto); respetar aislamiento de procesos.
- **Procesos distintos:** IPC oficial de Gecko o transporte de plataforma con mensajes tipados/versionados, validación, límites de tamaño, timeout y cancelación.
- **Eventos de estado:** emitir deltas con secuencia y generación; snapshot inicial + actualizaciones; cola acotada, coalescencia de cambios visuales y backpressure explícita.
- **Secretos:** referencias opacas y operaciones autorizadas, nunca claves ni tokens en el estado de UI, eventos, logs o contenido web.

## Modelo de estado
1. Propiedad única del estado por dominio (tabs, permisos, privacidad, descargas, perfiles); sin duplicar fuentes de verdad.
2. Comandos explícitos UI → core; respuestas tipadas con errores recuperables; eventos core → UI únicamente cuando hay cambio observable.
3. Ordenar eventos por ámbito, versionar contratos, detectar eventos obsoletos y recuperar snapshot si se pierde sincronización.
4. No bloquear hilo UI, hilo de renderizado ni main thread de Gecko con I/O o trabajo Rust pesado.
5. Cancelar operaciones cuando la ventana o pantalla desaparezca; respetar ciclo de vida Android y procesos Firefox.
6. Evitar `Arc<Mutex<...>>` como arquitectura universal: minimizar estado mutable, bloquear brevemente y medir contención. Evitar procesos adicionales sin amenaza o beneficio medido.
7. No convertir el núcleo Rust en un singleton privilegiado: permisos mínimos y acceso segmentado por capacidad.

## Aero multiplataforma
Seguir `docs/UI-DESIGN-SYSTEM.md`: solo Aero Light y Aero Dark, geometría de 2–4 px, vidrio predominante, Acrylic puntual, chrome UI separado del contenido web, fallback opaco. Tokens semánticos versionados compartidos; cada plataforma aplica su compositor nativo y ajustes de accesibilidad. No usar blur de página completa ni repintar todo por eventos locales.

## Calidad y medición
- Contratos: pruebas unitarias, compatibilidad semántica, casos de error, cancelación, eventos fuera de orden y recuperación.
- FFI: verificar propiedad de memoria, ciclo de vida, threading, costes de copia y errores; fuzz/property tests donde corresponda.
- UI: latencia input→frame, dropped frames, CPU, RAM, GPU, batería, cold/warm start, accesibilidad, teclado/táctil/mando.
- Gecko: pruebas xpcshell, mochitest y browser-chrome según capa; build nativo para Rust/C++/WebIDL, no solo Artifact Builds.
- Benchmark: misma revisión de Gecko, dispositivo, configuración y escenarios; no afirmar mejoras sin datos.

## Plan por hitos
1. Confirmar build y arranque de Firefox upstream.
2. Diseñar `contracts` mínimo para acciones, snapshot, eventos y errores, con pruebas.
3. Prototipar un recorrido real pestaña → comando → core → adaptador Gecko → evento → UI desktop.
4. Medir overhead, threading y aislamiento; no adoptar IPC adicional sin justificación.
5. Prototipar Android/TV con GeckoView y adaptadores Kotlin; evaluar UniFFI con mediciones.
6. Introducir tokens Aero compartidos y componentes por plataforma; probar accesibilidad y vídeo.
7. Extender módulos y CI con pruebas de consumidores, compatibilidad y regresiones.

## Referencias primarias
- Mozilla Firefox Source Docs: https://firefox-source-docs.mozilla.org/
- Mozilla UniFFI: https://mozilla.github.io/uniffi-rs/
- UniFFI source: https://github.com/mozilla/uniffi-rs
- Rust Cargo Workspaces: https://doc.rust-lang.org/cargo/reference/workspaces.html
- Android Jetpack Compose: https://developer.android.com/develop/ui/compose
- Android TV Compose: https://developer.android.com/training/tv/playback/compose
- GeckoView: https://mozilla.github.io/geckoview/
- Tauri process model (WebView limitation): https://v2.tauri.app/concept/process-model/

**Actualización normativa:** al cambiar esta decisión, revisar `docs/MODULAR-ARCHITECTURE.md`, `docs/UI-DESIGN-SYSTEM.md`, `docs/ENGINEERING.md`, skills y roadmap. No confundir guía con implementación.
