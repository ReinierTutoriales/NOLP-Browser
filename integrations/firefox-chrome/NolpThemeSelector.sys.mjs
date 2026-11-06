/* NOLP theme selector backend: reuse Firefox's built-in theme add-ons.
 * Intended for privileged Firefox browser chrome only, not web content.
 * No custom theme engine, storage, observer or extension.
 */
export const NOLP_THEMES = Object.freeze({
  light: "firefox-compact-light@mozilla.org",
  dark: "firefox-compact-dark@mozilla.org",
});

export async function setNolpTheme(mode, addonManager) {
  if (!Object.hasOwn(NOLP_THEMES, mode)) {
    throw new RangeError("NOLP supports only light and dark");
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
  const dark = await addonManager.getAddonByID(NOLP_THEMES.dark);
  if (dark?.isActive) return "dark";
  const light = await addonManager.getAddonByID(NOLP_THEMES.light);
  if (light?.isActive) return "light";
  return null; // Existing system/extension theme: do not silently overwrite.
}

