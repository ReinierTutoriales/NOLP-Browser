# NOLP desktop UI — first interactive prototype

Open `prototypes/desktop/index.html` in a browser. No dependencies, network requests, or build steps. This is an **HTML/CSS/JS design prototype**, not a NOLP native window, Gecko embedding, or browser release.

Implemented: official 3D PNG branding, compact tab bar with add/switch/close, address input with local-only display, dark/light Aero theme, keyboard focus, accessible labels, responsive sizing, and reduced-transparency fallback.

Not implemented: Gecko integration, real navigation, back/forward/reload, downloads, shield, persistence, actual native Aero material, security state, packaging. Disabled controls explicitly indicate absent functionality. The address bar stores the entered text in ephemeral tab state only and does **not** open a URL.

Next: validate UI semantics and convert the approved chrome into a supported Firefox desktop integration, without weakening upstream sandbox or TLS.
