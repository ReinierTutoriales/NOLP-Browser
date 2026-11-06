# Inicio de desarrollo NOLP

**Estado:** andamiaje de integración; aún no es un navegador ejecutable.

## Primera plataforma: Firefox Desktop
Se mantiene Firefox upstream fuera del repositorio, fijado a un commit inmutable revisado. El script `scripts/bootstrap-firefox.sh` descarga el código sin modificar el repositorio NOLP.

Requisitos: Git, Bash, espacio suficiente, y dependencias de compilación específicas del SO conforme a la documentación vigente de Mozilla.

```bash
export FIREFOX_REVISION=<SHA-completo-de-40-caracteres-revisado>
bash scripts/bootstrap-firefox.sh
```

El script **no** compila Firefox ni configura automáticamente el producto NOLP. Antes de crear una distribución se debe fijar una revisión soportada, verificar el proceso de build upstream y documentar licencias, firma, actualización y pruebas.

## Próximos hitos verificables
1. Seleccionar y fijar revisión de Firefox y estrategia de parches.
2. Compilar Firefox upstream en CI para una plataforma piloto.
3. Añadir configuración propia de producto y perfil aislado sin eliminar protecciones.
4. Crear un test de arranque y auditoría de conexiones automáticas.
5. Añadir integración del bloqueador tras validar las APIs disponibles.
6. Integrar GeckoView Android por separado, con su propia matriz de compatibilidad.

No anunciar una versión NOLP hasta que se haya compilado, ejecutado y probado el producto.
