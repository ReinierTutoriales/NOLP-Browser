# Inicio de desarrollo NOLP

**Estado:** andamiaje de integración; aún no es un navegador ejecutable.

## Primera plataforma: Firefox Desktop
Se mantiene Firefox upstream fuera del repositorio, fijado a un commit inmutable de Firefox 159.0.1 (tag oficial verificado; compilación aún no validada). El script `scripts/bootstrap-firefox.sh` descarga el código sin modificar el repositorio NOLP.

Requisitos: Git, Bash, espacio suficiente, y dependencias de compilación específicas del SO conforme a la documentación vigente de Mozilla.

```bash
python3 scripts/check-foundation.py
bash scripts/bootstrap-firefox.sh
```

El script **no** compila Firefox ni configura automáticamente el producto NOLP. Antes de crear una distribución se debe verificar la revisión fijada, confirmar que el proceso de build upstream funciona y documentar licencias, firma, actualización y pruebas.

## Próximos hitos verificables
1. [Hecho] Seleccionar y fijar Firefox 159.0.1 estable; pendiente verificar compilación y estrategia de parches.
2. [Pendiente] Compilar Firefox upstream en CI para una plataforma piloto.
3. Añadir configuración propia de producto y perfil aislado sin eliminar protecciones.
4. Crear un test de arranque y auditoría de conexiones automáticas.
5. Añadir integración del bloqueador tras validar las APIs disponibles.
6. Integrar GeckoView Android por separado, con su propia matriz de compatibilidad.

No anunciar una versión NOLP hasta que se haya compilado, ejecutado y probado el producto.

## GitHub Actions

El workflow `Firefox foundation` valida el manifiesto en cada cambio relevante. La compilación de Firefox se intenta automáticamente en los pushes a `main` que afectan al motor, scripts o workflow; también puede ejecutarse manualmente (`workflow_dispatch`, opción `build_firefox`). Puede consumir recursos importantes y **no constituye una compilación NOLP**. La CI valida la revisión y la versión upstream, intenta construir en modo artifact y ejecutar `./mach run --version`; **esto no verifica navegación ni inicio gráfico completo**. Ante un fallo se adjuntan diagnósticos básicos de disco y memoria. No hay evidencia de una ejecución satisfactoria hasta consultar los logs del workflow.

## Primera prueba de renderizado Gecko

El workflow `Firefox foundation` ahora ejecuta `scripts/smoke-gecko-navigation.sh` después de compilar Firefox. Abre una página HTML local en modo headless con un perfil temporal aislado, captura una imagen PNG, valida su cabecera y dimensiones y limpia el perfil al finalizar. El comando está limitado a 90 segundos para evitar bloqueos indefinidos.

Esta prueba verifica renderizado real cuando pasa en CI; **no** prueba todavía navegación HTTPS, integración del motor con el código Rust, interfaz NOLP, bloqueo de solicitudes ni distribución de una aplicación propia. Hasta que termine la ejecución correspondiente, la nueva prueba permanece **pendiente de validación**.

## Linux desktop development launcher (upstream Firefox)

After a successful Firefox artifact build on a Linux graphical session:

```bash
bash scripts/run-nolp-desktop.sh https://example.org
```

The launcher validates the pinned Git revision, rejects non-HTTPS user URLs, requires a graphical session and uses a separate profile under `.local/nolp-desktop-profile` (permissions 0700). It delegates to upstream `./mach run` and does **not** integrate the Rust Gecko adapter, add a NOLP UI, or intercept network requests. The profile is persistent for development; delete it manually if isolation reset is required. The CI includes launcher syntax and argument-validation tests. This is a **development harness**, not a distributable NOLP Alpha.
