# Identidad visual de NOLP

## Archivos oficiales
- `assets/brand/nolp-icon.svg`: símbolo principal, cuadrado, escalable, sin fondo. Preferido para iconos, accesos y aplicaciones.
- `assets/brand/nolp-wordmark.svg`: marca horizontal para documentación y cabeceras de fondo oscuro.

## Significado oficial del nombre

- **N — Nex:** conexión.
- **O — Óptima:** rendimiento y eficiencia.
- **L — Local:** tecnología *local-first*.
- **P — Privada:** *privacy-first*.

Esta definición es la referencia oficial para el nombre NOLP en documentación, interfaz y publicaciones. No usar expansiones alternativas del acrónimo.

## Concepto
Monograma «N» como cinta continua, que representa conexión y autonomía. Arco abierto como metáfora de navegación sin encierro. Diseño sin dependencia de fuentes externas ni imágenes remotas.

## Paleta
- Violeta: `#BD4CFF`
- Índigo: `#6748F5`
- Cian: `#00D9F5`
- Texto sobre oscuro: `#F4F6FF`
- Fondo de presentación recomendado: `#080B14`

## Reglas de implementación
1. Conservar SVG como fuente de referencia versionada y editable; no rasterizarlo para el README.
2. Para iconos de aplicación generar PNG/ICO/ICNS/adaptive icons a partir del SVG mediante una herramienta reproducible, con tamaños y máscaras específicos por plataforma. No considerar esos artefactos creados hasta generar y validar sus archivos.
3. El icono es transparente y no requiere servicios externos; comprobar legibilidad a 16, 24, 32 y 48 px antes de empaquetar.
4. No agregar sombras, brillos animados ni fondos fijos al icono de sistema; adaptar el fondo según los requisitos de la plataforma.
5. La marca horizontal usa tipografía de sistema como referencia; si se exige apariencia idéntica en todas las plataformas, convertir el texto a contornos con una fuente de licencia compatible.
6. No afirmar que esta versión vectorial reproduce píxel a píxel el primer concepto rasterizado: es una adaptación geométrica optimizada para producción.
7. Mantener espacio de seguridad alrededor del símbolo y contrastar sobre temas claros y oscuros.

## Estado
Activos vectoriales fuente disponibles. Exportaciones por plataforma, favicon, paquete de iconos, accesibilidad y pruebas visuales quedan pendientes de la fase de aplicación.
