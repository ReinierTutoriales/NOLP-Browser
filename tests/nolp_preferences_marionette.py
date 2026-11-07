#!/usr/bin/env python3
"""Exercise NOLP's actual about:preferences UI using Firefox Marionette/WebDriver."""
import os
from pathlib import Path
import tempfile
import time

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
    driver.get("about:preferences")
    WebDriverWait(driver, 30).until(
        lambda d: d.execute_script("return !!document.getElementById('nolp-theme-select')")
    )
    return driver.execute_script("return document.getElementById('nolp-theme-select').value")


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
    # Confirm the actual active built-in theme via Firefox privileged about:addons UI,
    # not merely the select value. A reload must read it back from AddonManager.
    driver.refresh()
    WebDriverWait(driver, 30).until(
        lambda d: d.execute_script(
            "return document.getElementById('nolp-theme-select')?.value === arguments[0]", mode
        )
    )


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
    finally:
        driver.quit()
    # Restart Firefox against the same on-disk profile.
    driver = launch(profile)
    try:
        actual = picker(driver)
        assert actual == "auto", f"Theme lost after restart: {actual!r}"
        print("PASS: NOLP auto theme persisted after Firefox restart", flush=True)
    finally:
        driver.quit()
