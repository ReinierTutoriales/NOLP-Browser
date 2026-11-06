/* NOLP theme selection uses Firefox's native theme add-on manager.
 * Automatic mode activates the Firefox default theme, which follows the
 * operating system's appearance without polling or a page-scoped listener.
 */
export const NOLP_THEMES = Object.freeze({
  auto: "default-theme@mozilla.org",
  light: "firefox-compact-light@mozilla.org",
  dark: "firefox-compact-dark@mozilla.org",
});

export async function setNolpTheme(mode, addonManager) {
  if (!Object.hasOwn(NOLP_THEMES, mode)) {
    throw new RangeError("NOLP supports auto, light and dark");
  }
  const addon = await addonManager.getAddonByID(NOLP_THEMES[mode]);
  if (!addon || addon.type !== "theme" || addon.appDisabled) {
    throw new Error("Firefox built-in theme unavailable");
  }
  if (!addon.isActive) {
    await addon.enable();
  }
  return mode;
}

export async function getNolpTheme(addonManager) {
  for (const [mode, id] of Object.entries(NOLP_THEMES)) {
    const addon = await addonManager.getAddonByID(id);
    if (addon?.isActive) return mode;
  }
  return null; // Preserve an existing non-NOLP theme until explicit selection.
}
