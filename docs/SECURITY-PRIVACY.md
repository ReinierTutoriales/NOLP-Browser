# Política de seguridad, privacidad y almacenamiento

**Estado:** requisitos de diseño. Las garantías deben demostrarse mediante implementación y pruebas.

## Modelo de amenazas
Considerar robo de archivos de perfil, equipo perdido, extensiones maliciosas, páginas hostiles, rastreo entre sitios, suministro de actualizaciones comprometidas, malware en sesión desbloqueada y fallos de almacenamiento. El cifrado en reposo no protege frente a malware privilegiado que accede a secretos ya desbloqueados.

## Red y telemetría
Separar: (a) telemetría propia — prohibida por defecto; (b) servicios de seguridad y actualizaciones — permitidos solo con propósito documentado y minimización de datos; (c) tráfico web solicitado por el usuario — sujeto a protecciones y permisos. Cada conexión automática debe declarar destino, finalidad, datos enviados, activación y opción de control.

Pruebas de tráfico: inicio, reposo, navegación, privado, cierre, actualización, fallo y recuperación. No declarar «cero telemetría» sin evidencia; no desactivar indiscriminadamente Remote Settings u otros mecanismos de seguridad.

## Secure Local Vault
- Proteger contraseñas, cookies, tokens, sesiones, historial, marcadores, formularios, configuración sensible y claves según su clasificación.
- Separar claves por perfil y propósito mediante derivación adecuada; usar cifrado autenticado, nonces correctos y bibliotecas auditadas.
- Considerar AES-256-GCM o XChaCha20-Poly1305 según soporte; Argon2id para contraseñas maestras y HKDF para derivación de subclaves cuando corresponda.
- Integrar mecanismos seguros de SO: Windows DPAPI/CNG, macOS Keychain, Android Keystore y almacenamiento seguro disponible en Linux, documentando diferencias reales.
- Ofrecer protección reforzada mediante contraseña maestra y bloqueo configurable, sin asumir que una clave de SO equivale a una contraseña independiente.
- Mantener WebAuthn/FIDO2 conforme a estándares. Las claves de hardware pueden ser no exportables.
- Diseñar exportación cifrada, respaldos locales, recuperación, migraciones transaccionales y pruebas de corrupción; no prometer recuperación sin clave o respaldo.
- Revisar persistencia real de Gecko: cookies, SQLite/WAL, caché, archivos temporales, crash dumps y copias. No afirmar cifrado integral del perfil hasta cubrir todas las rutas.
- Evitar secretos en logs, diagnósticos, volcados, portapapeles y procesos no autorizados; minimizar su permanencia en memoria.

## Seguridad del navegador
Conservar sandbox, aislamiento multiproceso, controles de origen, validación TLS, particionamiento de estado y permisos mínimos. Actualizaciones firmadas y con control de versiones. No sacrificar aislamiento para obtener rendimiento.

## Bloqueo
Filtrado de red y cosmético con excepciones explícitas. Scriptlets de catálogo revisado y versionado; nunca código remoto arbitrario. No garantizar bloqueo del 100 % ni imposibilidad de fingerprinting.

## Verificación mínima
Pruebas de extracción de perfil bloqueado, integridad y restauración, migración y caída de energía, permisos, tráfico saliente, regresión de sandbox, vulnerabilidades de dependencias y firmas de actualización.
