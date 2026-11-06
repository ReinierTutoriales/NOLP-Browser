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
