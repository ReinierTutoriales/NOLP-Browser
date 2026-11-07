// Exercise the actual NOLP theme module with a persistent mock AddonManager.
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
const source = await readFile(new URL("../integrations/firefox-chrome/NolpThemeSelector.sys.mjs", import.meta.url), "utf8");
const { NOLP_THEMES, getNolpTheme, setNolpTheme } =
  await import("data:text/javascript;base64," + Buffer.from(source).toString("base64"));
const ids = Object.values(NOLP_THEMES);
let persisted = ids[0];
function manager() {
  return {
    async getAddonByID(id) {
      if (!ids.includes(id)) return null;
      return { id, type: "theme", appDisabled: false,
        get isActive() { return persisted === id; },
        async enable() { persisted = id; } };
    }
  };
}
for (const mode of ["auto", "light", "dark", "auto"]) {
  assert.equal(await setNolpTheme(mode, manager()), mode);
  assert.equal(await getNolpTheme(manager()), mode);
  // A new manager instance simulates a new UI session with the saved theme.
  assert.equal(await getNolpTheme(manager()), mode);
}
await assert.rejects(setNolpTheme("invalid", manager()), RangeError);
persisted = "third-party-theme";
assert.equal(await getNolpTheme(manager()), null);
const missing = { getAddonByID: async () => null };
await assert.rejects(setNolpTheme("dark", missing), /unavailable/);
console.log("NOLP theme module: auto/light/dark transitions, reload state, invalid and third-party themes PASS");
