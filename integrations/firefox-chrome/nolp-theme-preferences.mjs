/* Native Firefox preferences integration; no polling or independent theme store. */
import { AddonManager } from "resource://gre/modules/AddonManager.sys.mjs";
import { getNolpTheme, setNolpTheme } from "chrome://browser/content/preferences/nolp/NolpThemeSelector.sys.mjs";

const select = document.getElementById("nolp-theme-select");
if (select) {
  let generation = 0;
  const refresh = async () => {
    const current = ++generation;
    const active = await getNolpTheme(AddonManager);
    if (current !== generation || !select.isConnected) return;
    if (active) {
      select.value = active;
    } else {
      // Never misrepresent a third-party theme as an active NOLP choice.
      select.selectedIndex = -1;
    }
  };

  let changing = false;
  const listener = {
    onEnabled(addon) {
      if (addon.type === "theme") void refresh();
    },
    onDisabled(addon) {
      if (addon.type === "theme") void refresh();
    },
  };
  AddonManager.addAddonListener(listener);
  window.addEventListener("pagehide", () => AddonManager.removeAddonListener(listener), { once: true });

  select.addEventListener("change", async () => {
    if (changing) return;
    changing = true;
    const value = select.value;
    select.disabled = true;
    try {
      await setNolpTheme(value, AddonManager);
    } catch (error) {
      console.error("NOLP theme selection failed", error);
    } finally {
      await refresh();
      select.disabled = false;
      changing = false;
    }
  });
  await refresh();
}
