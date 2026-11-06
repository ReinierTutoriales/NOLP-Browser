# NOLP Firefox-native theme integration

This integration uses the Firefox Desktop chrome, not the standalone HTML prototype. It does **not** implement Mica, Acrylic or a custom theme settings screen.

## Apply to pinned Firefox source
```sh
bash scripts/bootstrap-firefox.sh
python3 scripts/apply-firefox-chrome.py --firefox-dir .upstream/firefox
python3 scripts/apply-firefox-chrome.py --firefox-dir .upstream/firefox --check
```
The application script registers the stylesheet in Firefox's `browser/themes/shared/jar.inc.mn` and imports it into `browser/themes/shared/browser-shared.css`. It fails closed if the upstream paths change. Do not modify or distribute an upstream build without license and security review.

## Selecting NOLP Dark and NOLP Light
NOLP **reuses Firefox's built-in Light/Dark theme selection** (Add-ons and themes → Themes). No duplicate theme manager, pref observer, or custom process is introduced. The `light-dark()` values follow Firefox's active chrome color scheme. The default/system/third-party themes still exist upstream; restricting them to exactly two choices requires a separate product decision and integration.

Until runtime validation, the NOLP overlay is **off by default**. In a test-only Firefox profile, set the Boolean preference `nolp.theme.enabled` to `true` in `about:config`, then select Firefox Light or Dark. Do not use this as the final NOLP settings UX.

## Remaining acceptance gates
- Verify upstream CSS packaging and CSS feature compatibility in the pinned Firefox source.
- Compile and run a real Firefox-derived build; verify both themes, menus, Urlbar, tab controls, private mode and identity indicators.
- Test forced colors, screen reader, scaling, native macOS/Linux chrome, Windows backdrop capabilities and benchmark versus unchanged Firefox.
- Integrate the final NOLP-only two-theme settings UX after native Firefox theme APIs are audited.
