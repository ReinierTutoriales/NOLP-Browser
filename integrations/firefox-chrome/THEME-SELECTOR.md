# NOLP native theme selector

Use the **Firefox built-in Light and Dark in-app theme add-ons**, not a second theme renderer. The upstream `BuiltInThemeConfig.sys.mjs` defines `firefox-compact-light@mozilla.org` and `firefox-compact-dark@mozilla.org` as `inApp: true`.

`NolpThemeSelector.sys.mjs` is a small, privileged-browser-chrome controller. The caller passes Firefox's `AddonManager`; `setNolpTheme("light" | "dark", AddonManager)` enables the corresponding built-in theme, and `getNolpTheme(AddonManager)` reads its current state. Unknown modes fail closed. A system/third-party theme returns null rather than being silently replaced.

**Integration boundary:** This module is staged in NOLP's repository but is not yet registered as a Firefox resource or wired into the browser's settings screen. No claim is made that an on-screen selector is already functional. Wiring should use Firefox's existing browser chrome/preferences controls and test the supported theme-manager API in a compiled browser. Do not disable Firefox theme security or extension management by overriding global theme behavior.

Official Mozilla references:
- https://firefox-source-docs.mozilla.org/code-quality/coding-style/css_guidelines.html
- https://firefox-source-docs.mozilla.org/toolkit/themes/shared/design-system/docs/README.design-tokens.stories.html
