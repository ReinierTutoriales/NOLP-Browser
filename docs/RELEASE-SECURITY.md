# Release readiness y procedencia

## Estado
Existe una comprobación manual `.github/workflows/release-readiness.yml` que ejecuta `scripts/check-release-readiness.py`. **No publica binarios, no crea releases ni configura protección de ramas.** La integración real con un futuro pipeline de publicación es un requisito pendiente.

## Condiciones obligatorias
Antes de publicar, el commit exacto debe tener resultados `success` de los workflows Security scanning, Security governance, Dependency inventory SBOM, Module boundaries, NOLP governance y Firefox foundation. La comprobación consulta la API de GitHub, filtra por SHA exacto y falla ante ausencia, errores o ejecución pendiente. Un resultado exitoso de otro commit no sirve.

Los seis workflows obligatorios ahora se ejecutan en cada push a `main` y en pull requests, sin filtros `paths`. La compilación completa de Firefox sigue siendo opcional; su workflow valida automáticamente el manifiesto y scripts. Si algún workflow falta o no concluye, el gate falla. La ejecución manual del gate incorpora pruebas unitarias de éxito, ausencia, fallo, ejecución pendiente y éxito obsoleto.

## Alcance de la procedencia
El SBOM de código fuente tiene atestación de GitHub en `main`; no es una atestación del binario Firefox ni de una release NOLP. Los builds de Firefox son upstream y no prueban que NOLP esté integrado.

## Requisitos pendientes
1. Integrar este gate como dependencia estricta de un workflow de publicación que empaquete y ateste el **binario real**.
2. Configurar reglas de protección de `main` y checks requeridos con permisos administrativos del repositorio; actualmente no se ha confirmado acceso a dicha configuración.
3. Ejecutar y validar el gate contra los resultados reales de un commit, además de sus pruebas unitarias.
4. Establecer reglas administrativas de protección y un pipeline de publicación que dependa del gate; no declarar protección completa antes de ello.
