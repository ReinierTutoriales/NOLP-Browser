# NOLP — Native-first Aero implementation contract

Status: **architecture and acceptance criteria, not a functioning native compositor**. Adopt the native Firefox Desktop chrome rather than shipping the independent HTML prototype as a browser window.

## Shared Firefox chrome
- Reuse `browser.xhtml`, tabbrowser, Urlbar, Places, CustomizableUI, Gecko rendering, accessibility, and native window infrastructure. Keep modifications as a narrow, reviewable patch series against a pinned stable Firefox revision.
- The existing `prototypes/desktop` is a visual experiment only. Do not load it as a privileged browser page or duplicate Firefox's tab/history/permission managers.
- Only two theme selections: Aero Dark and Aero Light. Map semantic tokens (chrome/menu/overlay/text/border/focus) to platform chrome styles. Maintain visible security indicators and keyboard accessibility.
- Keep webpage surfaces opaque/independent: never apply background blur to web content or video.
- Do not use unsupported `userChrome.css` as a production integration mechanism.

## Native adapters, capability-first
| Platform | Preferred native mechanism | Fallback |
|---|---|---|
| Windows 11 build 22621+ | Evaluate DWM `DWMWA_SYSTEMBACKDROP_TYPE` / `DWMSBT_TABBEDWINDOW` (Mica Alt) on the **actual Firefox top-level HWND**. Use transient acrylic only where supported and bounded. | Opaque theme chrome |
| Windows 10 / older Windows 11 | Existing Firefox native window/chrome behavior; do not assume backdrop availability. | Opaque theme chrome |
| macOS | Evaluate Firefox's existing AppKit titlebar/vibrancy integration, without introducing an independent NSWindow or a duplicate browser renderer. | Native opaque theme chrome |
| Linux Wayland/X11 | Reuse Firefox GTK/native decorations and compositor-supported translucency only when reliable; avoid depending on any single compositor blur protocol. | Opaque theme chrome |

**Windows caveat:** DWM backdrop availability does not prove Firefox's current widget/chrome paints transparently enough to expose it. Test with an actual Firefox-derived build. Do not claim that setting a DWM attribute alone delivers visible glass.

## Required implementation sequence
1. Pin and verify a supported stable Firefox upstream revision and build a clean baseline.
2. Inventory Firefox's existing chrome CSS, native window integrations and accessibility paths per OS.
3. Add shared semantic tokens and exactly two themes in Firefox chrome with a small patch; verify tabs, Urlbar, menus, TLS identity and private browsing still work.
4. Implement one minimal Windows DWM adapter **only if** the baseline proves no existing suitable implementation. Gate by OS build, supported attributes, accessibility/energy policies; preserve fallback.
5. macOS and Linux adapters reuse native upstream paths, with platform-specific changes only where justified by profiling.
6. Test on real platforms before calling native Aero complete. Record Firefox revision, OS/build, hardware, feature detection and evidence.

## Acceptance and security gates
- Build and run a real Firefox-derived NOLP window; verify navigation, tabs, downloads, permissions, sandbox and TLS, not just HTML mockups.
- Firefox browser-chrome tests and mochitests for UI changes; native integration tests and visual snapshots on each target OS.
- Profile startup, tab-switch latency, CPU/GPU, memory and video with and without materials; reject measured regressions or offer automatic opaque fallback.
- Test reduced transparency/motion, high contrast, screen readers, DPI scaling, focus and keyboard navigation.
- Run Latest Stable Gate and Security Assurance Gate on every integration PR. Record precise versions and results; CI green on documentation alone is not functional proof.

Official references:
- https://firefox-source-docs.mozilla.org/browser/overview.html
- https://learn.microsoft.com/en-us/windows/win32/api/dwmapi/ne-dwmapi-dwm_systembackdrop_type
- https://learn.microsoft.com/en-us/windows/apps/develop/ui/system-backdrops
