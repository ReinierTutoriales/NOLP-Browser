/* Native Firefox preferences integration; no polling or independent theme store. */
import { AddonManager } from "resource://gre/modules/AddonManager.sys.mjs";
import { getNolpTheme, setNolpTheme } from "chrome://browser/content/preferences/nolp/NolpThemeSelector.sys.mjs";

const select = document.getElementById("nolp-theme-select");
if (select) {
  const refresh = async () => {
    const active = await getNolpTheme(AddonManager);
    if (active) {
      select.value = active;
    } else {
      // Never misrepresent a third-party theme as an active NOLP choice.
      select.selectedIndex = -1;
    }
  };

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
    const value = select.value;
    select.disabled = true;
    try {
      await setNolpTheme(value, AddonManager);
    } catch (error) {
      console.error("NOLP theme selection failed", error);
    } finally {
      await refresh();
      select.disabled = false;
    }
  });
  await refresh();
}
