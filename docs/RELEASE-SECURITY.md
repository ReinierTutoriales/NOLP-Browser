# Release readiness y procedencia

## Estado
Existe una comprobación manual `.github/workflows/release-readiness.yml` que ejecuta `scripts/check-release-readiness.py`. **No publica binarios, no crea releases ni configura protección de ramas.** La integración real con un futuro pipeline de publicación es un requisito pendiente.

## Condiciones obligatorias
Antes de publicar, el commit exacto debe tener resultados `success` de los workflows Security scanning, Security governance, Dependency inventory SBOM, Module boundaries, NOLP governance y Firefox foundation. La comprobación consulta la API de GitHub, filtra por SHA exacto y falla ante ausencia, errores o ejecución pendiente. Un resultado exitoso de otro commit no sirve.

**Advertencia operativa:** varios workflows utilizan filtros `paths` y pueden no ejecutarse en el commit seleccionado. En tal caso el gate falla deliberadamente; deben ejecutarse manualmente para ese mismo commit (cuando su workflow permita `workflow_dispatch`) o ajustarse los triggers. No saltar la validación.

## Alcance de la procedencia
El SBOM de código fuente tiene atestación de GitHub en `main`; no es una atestación del binario Firefox ni de una release NOLP. Los builds de Firefox son upstream y no prueban que NOLP esté integrado.

## Requisitos pendientes
1. Integrar este gate como dependencia estricta de un workflow de publicación que empaquete y ateste el **binario real**.
2. Configurar reglas de protección de `main` y checks requeridos con permisos administrativos del repositorio; actualmente no se ha confirmado acceso a dicha configuración.
3. Eliminar filtros que impidan verificar todos los checks por commit o establecer un flujo de ejecución verificable.
4. Probar el gate tanto en caso válido como ante un check ausente/fallido; no declarar protección completa antes de ello.
