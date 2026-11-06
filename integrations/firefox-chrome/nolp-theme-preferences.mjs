/* NOLP theme selector in Firefox's privileged about:preferences page. */
import { AddonManager } from "resource://gre/modules/AddonManager.sys.mjs";
import { getNolpTheme, setNolpTheme } from "chrome://browser/content/preferences/nolp/NolpThemeSelector.sys.mjs";

const select = document.getElementById("nolp-theme-select");
if (select) {
  const refresh = async () => {
    const active = await getNolpTheme(AddonManager);
    if (active) select.value = active;
  };
  select.addEventListener("change", async () => {
    const value = select.value;
    select.disabled = true;
    try {
      await setNolpTheme(value, AddonManager);
    } catch (error) {
      console.error("NOLP theme selection failed", error);
      await refresh();
    } finally {
      select.disabled = false;
    }
  });
  await refresh();
}
