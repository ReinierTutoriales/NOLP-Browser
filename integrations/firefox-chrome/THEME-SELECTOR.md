# NOLP native theme selector

Use the **Firefox built-in Light and Dark in-app theme add-ons**, not a second theme renderer. The upstream `BuiltInThemeConfig.sys.mjs` defines `firefox-compact-light@mozilla.org` and `firefox-compact-dark@mozilla.org` as `inApp: true`.

`NolpThemeSelector.sys.mjs` is a small, privileged-browser-chrome controller. The caller passes Firefox's `AddonManager`; `setNolpTheme("auto" | "light" | "dark", AddonManager)` enables the corresponding built-in theme, and `getNolpTheme(AddonManager)` reads its current state. Unknown modes fail closed. A system/third-party theme returns null rather than being silently replaced.

**Integration boundary:** `scripts/apply-nolp-theme-selector.py` patches the pinned Firefox preferences page and `jar.mn` during the optional source-build workflow. This is source-level integration only; the selector has not been verified in a running Firefox build. Do not disable Firefox theme security or extension management by overriding global theme behavior.

Official Mozilla references:
- https://firefox-source-docs.mozilla.org/code-quality/coding-style/css_guidelines.html
- https://firefox-source-docs.mozilla.org/toolkit/themes/shared/design-system/docs/README.design-tokens.stories.html

## Automatic system appearance

The default choice **Automático (sistema)** activates Firefox's built-in `default-theme@mozilla.org`. Firefox handles OS color-scheme changes natively even when the preferences tab is closed. The two actual NOLP appearances remain Light and Dark; Automatic is a selection policy, not a third palette. Explicit Light/Dark selections persist through Firefox's add-on manager. The existing page integration does not yet force the initial choice to Automatic when a different theme is active; that requires a product migration policy and runtime testing.
