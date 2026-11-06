# Protección de main: configuración administrativa pendiente

## Estado verificado

- El workflow `Release readiness gate` ya se ejecuta automáticamente en cada push a `main`.
- Su job se llama `Verify all mandatory checks on exact commit`.
- Los seis controles del commit `7aca8ae8` y el gate terminaron correctamente.
- La API de rulesets devolvió `[]`: no hay rulesets visibles configurados.
- La conexión GitHub disponible no tiene permiso de administración para activar protección de ramas. **Este archivo no aplica protección por sí solo.**

## Aplicación por propietario con permisos de administración

En el repositorio, abrir **Settings → Rules → Rulesets → New branch ruleset**. Crear la regla `NOLP main protection` con alcance a la rama predeterminada `main` y estado **Active**.

1. Activar **Require a pull request before merging** (al menos una aprobación humana independiente cuando haya colaboradores).
2. Activar **Require status checks to pass**. Seleccionar el contexto exacto `Verify all mandatory checks on exact commit` del workflow `Release readiness gate`. Si GitHub muestra contextos ambiguos, comprobar el origen GitHub Actions.
3. Activar **Require branches to be up to date before merging**, si está disponible y es compatible con la estrategia de integración.
4. Activar **Block force pushes** y **Restrict deletions**.
5. No habilitar bypass para bots o herramientas de IA. Revisar cualquier bypass administrativo según las necesidades reales de mantenimiento.
6. Guardar y verificar que el ruleset aparezca **Active** y que un PR con CI fallida no pueda fusionarse.

**Importante:** un status check obligatorio bloquea fusiones de PR, pero no constituye por sí solo una prohibición absoluta de publicar releases o de hacer push directo si las reglas no restringen esas operaciones. Para impedir publicación directa, se necesita un workflow de publicación único, permisos de escritura limitados y un entorno de release protegido. El navegador NOLP aún no produce binarios propios publicables; no crear una release ficticia.

## Verificación posterior

- Consultar `GET /repos/ReinierTutoriales/NOLP-Browser/rulesets` y confirmar regla activa.
- Probar un PR con un check fallido y otro con todos los checks aprobados.
- Verificar que no se permite push directo no autorizado, force push o borrado de `main`.
- Documentar excepciones administrativas explícitas sin simular identidad, firmas ni aprobaciones del propietario.
