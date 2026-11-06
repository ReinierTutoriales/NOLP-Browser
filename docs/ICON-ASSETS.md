# Paquete de iconos de aplicación NOLP

Fuente canónica: `assets/brand/nolp-icon.svg` (vectorial, fondo transparente). Esta fuente es una adaptación geométrica del símbolo, **no una conversión exacta** de la imagen 3D suministrada.

## Generación reproducible

```bash
python -m pip install 'CairoSVG==2.7.1' 'Pillow==11.3.0'
python scripts/build-brand-icons.py
```

Salida: `dist/nolp-icons/` (ignorada por Git). El workflow **Brand icon assets** publica un artefacto descargable con PNG transparentes de 16 a 2048 px, ICO multirresolución para Windows, ICNS para macOS, jerarquía hicolor SVG/PNG para Linux, PNG de primer plano para Android y recursos web/PWA.

**Limitaciones:** El primer plano Android no equivale a un icono adaptativo terminado; faltan los recursos monocromáticos y la definición de fondo. El icono vectorial plano es más legible a tamaños pequeños que la ilustración 3D con resplandor. No se ha validado aún visualmente en dispositivos Windows/macOS/Linux reales. La imagen 3D generada en la conversación no se ha incluido como fuente en este PR.

No instalar dependencias de red en tiempo de ejecución del navegador: son herramientas exclusivas del pipeline de diseño.
