/* Native Firefox preferences integration; no polling or independent theme store. */
const { AddonManager } = ChromeUtils.importESModule("resource://gre/modules/AddonManager.sys.mjs");
const { getNolpTheme, setNolpTheme } = ChromeUtils.importESModule("chrome://browser/content/preferences/nolp/NolpThemeSelector.sys.mjs");

window.__nolpThemeDiagnostics = { loaded: true, attached: false, error: null };

// Preferences scripts can run before the pane is attached: wait for DOM readiness
// instead of silently skipping the selector.
function initNolpThemeSelector() {
  const select = document.getElementById("nolp-theme-select");
  if (select) {
    window.__nolpThemeDiagnostics.attached = true;
    let generation = 0;
    const refresh = async () => {
      const current = ++generation;
      const active = await getNolpTheme(AddonManager);
      if (disposed || current !== generation || !select.isConnected) return;
      if (active) {
        select.value = active;
      } else {
        // Never misrepresent a third-party theme as an active NOLP choice.
        select.selectedIndex = -1;
      }
    };

    let changing = false;
    let disposed = false;
    const listener = {
      onEnabled(addon) {
        if (addon.type === "theme") void refresh();
      },
      onDisabled(addon) {
        if (addon.type === "theme") void refresh();
      },
    };
    AddonManager.addAddonListener(listener);
    window.addEventListener("pagehide", () => {
      disposed = true;
      generation++;
      AddonManager.removeAddonListener(listener);
    }, { once: true });

    select.addEventListener("change", async () => {
      if (changing || disposed) return;
      changing = true;
      const value = select.value;
      select.disabled = true;
      try {
        await setNolpTheme(value, AddonManager);
      } catch (error) {
        window.__nolpThemeDiagnostics.error = String(error);
        console.error("NOLP theme selection failed", error);
      } finally {
        try {
          await refresh();
        } catch (error) {
          console.error("NOLP theme state refresh failed", error);
        } finally {
          changing = false;
          if (!disposed && select.isConnected) select.disabled = false;
        }
      }
    });
    void refresh();
  }
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initNolpThemeSelector, { once: true });
} else {
  initNolpThemeSelector();
}
