#!/usr/bin/env python3
"""Exercise NOLP's actual about:preferences UI using Firefox Marionette/WebDriver."""
import os
from pathlib import Path
import tempfile

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait

FIREFOX = Path(os.environ["NOLP_FIREFOX_BINARY"]).resolve()
GECKODRIVER = Path(os.environ["NOLP_GECKODRIVER"]).resolve()
ARTIFACTS = Path(os.environ.get("NOLP_UI_ARTIFACTS", "ui-validation")).resolve()
ARTIFACTS.mkdir(parents=True, exist_ok=True)


def launch(profile):
    options = Options()
    options.binary_location = str(FIREFOX)
    options.add_argument("-headless")
    options.add_argument("-profile")
    options.add_argument(str(profile))
    options.set_preference("browser.shell.checkDefaultBrowser", False)
    options.set_preference("datareporting.policy.dataSubmissionEnabled", False)
    return webdriver.Firefox(service=Service(str(GECKODRIVER)), options=options)


def picker(driver):
    # WebDriver content navigation cannot open privileged about:preferences.
    # Use the browser's trusted-tab API through Marionette chrome context.
    driver.set_context("chrome")
    try:
        driver.execute_script(
            "gBrowser.selectedTab = gBrowser.addTrustedTab('about:preferences');"
        )
    finally:
        driver.set_context("content")
    WebDriverWait(driver, 30).until(
        lambda d: d.execute_script("return !!document.getElementById('nolp-theme-select')")
    )
    return driver.execute_script("return document.getElementById('nolp-theme-select').value")


THEME_IDS = {
    "auto": "default-theme@mozilla.org",
    "light": "firefox-compact-light@mozilla.org",
    "dark": "firefox-compact-dark@mozilla.org",
}


def assert_active_theme(driver, mode):
    """Check the active add-on through Firefox's privileged AddonManager."""
    driver.set_context("chrome")
    try:
        active = driver.execute_async_script("""
            const done = arguments[arguments.length - 1];
            (async () => {
              const { AddonManager } = ChromeUtils.importESModule(
                "resource://gre/modules/AddonManager.sys.mjs"
              );
              const addon = await AddonManager.getAddonByID(arguments[0]);
              done({ active: addon?.isActive ?? false, type: addon?.type ?? null });
            })().catch(error => done({ error: String(error) }));
        """, THEME_IDS[mode])
    finally:
        driver.set_context("content")
    assert active == {"active": True, "type": "theme"}, (
        f"Theme {mode} is not active in AddonManager: {active!r}"
    )


def select(driver, mode):
    driver.execute_script("""
        const select = document.getElementById('nolp-theme-select');
        if (!select) throw Error('NOLP theme selector not present');
        select.value = arguments[0];
        select.dispatchEvent(new Event('change', { bubbles: true }));
    """, mode)
    WebDriverWait(driver, 30).until(
        lambda d: d.execute_script(
            "const s=document.getElementById('nolp-theme-select');"
            "return s && !s.disabled && s.value === arguments[0]", mode
        )
    )
    # Verify the real theme in privileged chrome, not only the select element.
    assert_active_theme(driver, mode)
    driver.refresh()
    WebDriverWait(driver, 30).until(
        lambda d: d.execute_script(
            "return document.getElementById('nolp-theme-select')?.value === arguments[0]", mode
        )
    )
    assert_active_theme(driver, mode)


with tempfile.TemporaryDirectory(prefix="nolp-marionette-") as tmp:
    profile = Path(tmp) / "profile"
    profile.mkdir()
    driver = launch(profile)
    try:
        picker(driver)
        driver.save_screenshot(str(ARTIFACTS / "preferences-initial.png"))
        for mode in ("light", "dark", "auto"):
            select(driver, mode)
            driver.save_screenshot(str(ARTIFACTS / f"preferences-{mode}.png"))
            print(f"PASS: NOLP theme {mode} survives preferences reload", flush=True)
            driver.quit()
            driver = None
            # Each theme must survive a full browser restart using the same profile.
            driver = launch(profile)
            actual = picker(driver)
            assert actual == mode, (
                f"Theme {mode} lost after restart: {actual!r}"
            )
            assert_active_theme(driver, mode)
            print(f"PASS: NOLP {mode} theme persisted after Firefox restart", flush=True)
    finally:
        if driver is not None:
            driver.quit()
