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
    service = Service(str(GECKODRIVER), env={**os.environ, "MOZ_REMOTE_ALLOW_SYSTEM_ACCESS": "1"})
    return webdriver.Firefox(service=service, options=options)


def picker(driver):
    # WebDriver content navigation cannot open privileged about:preferences.
    # Use the browser's trusted-tab API through Marionette chrome context.
    driver.set_context("chrome")
    try:
        # Reuse the existing tab: opening a new tab does not switch the
        # WebDriver browsing context to it automatically.
        driver.execute_script(
            "gBrowser.loadURI(Services.io.newURI('about:preferences'), "
            "{triggeringPrincipal: Services.scriptSecurityManager.getSystemPrincipal()});"
        )
    finally:
        driver.set_context("content")
    try:
        WebDriverWait(driver, 30).until(
            lambda d: d.execute_script(
                "return location.href.startsWith('about:preferences') && "
                "!!document.getElementById('nolp-theme-select')"
            )
        )
    except Exception:
        details = driver.execute_script(
            "return {url: location.href, readyState: document.readyState, "
            "mainPane: !!document.getElementById('mainPrefPane'), "
            "picker: !!document.getElementById('nolp-theme-select')}"
        )
        driver.save_screenshot(str(ARTIFACTS / "preferences-failure.png"))
        raise AssertionError(f"NOLP preferences selector unavailable: {details!r}") from None
    return driver.execute_script("return document.getElementById('nolp-theme-select').value")


THEME_IDS = {
    "auto": "default-theme@mozilla.org",
    "light": "firefox-compact-light@mozilla.org",
    "dark": "firefox-compact-dark@mozilla.org",
}


def active_theme_state(driver, mode):
    """Read Firefox's actual theme state through privileged Marionette."""
    driver.set_context("chrome")
    try:
        return driver.execute_async_script("""
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


def assert_active_theme(driver, mode):
    active = active_theme_state(driver, mode)
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
    # Theme activation is asynchronous: the select's value changes before
    # AddonManager finishes enabling the built-in theme.
    try:
        WebDriverWait(driver, 30).until(
            lambda d: active_theme_state(d, mode) == {"active": True, "type": "theme"}
        )
    except Exception:
        state = active_theme_state(driver, mode)
        ui = driver.execute_script(
            "const s=document.getElementById('nolp-theme-select');"
            "return {value:s?.value, disabled:s?.disabled, url:location.href}"
        )
        raise AssertionError(
            f"Theme {mode} activation failed: AddonManager={state!r}, UI={ui!r}"
        ) from None
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
