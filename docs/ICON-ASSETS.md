# Paquete de iconos de aplicación NOLP

Fuente canónica: `assets/brand/nolp-official.png`, imagen 3D oficial proporcionada por el propietario de NOLP, con transparencia. No sustituirla por el antiguo SVG.

## Generación reproducible

```bash
python -m pip install 'Pillow==11.3.0'
python scripts/build-brand-icons.py
```

Salida: `dist/nolp-icons/` (ignorada por Git). El workflow **Brand icon assets** publica un artefacto descargable con PNG transparentes de 16 a 2048 px, ICO multirresolución para Windows, ICNS para macOS, jerarquía hicolor PNG para Linux, PNG de primer plano para Android y recursos web/PWA.

**Limitaciones:** El primer plano Android no equivale a un icono adaptativo terminado; faltan los recursos monocromáticos y la definición de fondo. El icono vectorial plano es más legible a tamaños pequeños que la ilustración 3D con resplandor. No se ha validado aún visualmente en dispositivos Windows/macOS/Linux reales. La imagen oficial 3D se incorpora mediante el PR #7, requisito para que este generador funcione.

No instalar dependencias de red en tiempo de ejecución del navegador: son herramientas exclusivas del pipeline de diseño.
