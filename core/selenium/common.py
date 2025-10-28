import os
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import platform

def initialize_driver():
    options = webdriver.FirefoxOptions()

    snap_tmp = os.path.expanduser("~/snap/firefox/common/tmp")
    os.makedirs(snap_tmp, exist_ok=True)
    os.environ["TMPDIR"] = snap_tmp

    # Detect system architecture
    arch = platform.machine()
    if arch in ("aarch64", "arm64"):
        # Use system ARM64 geckodriver
        gecko_path = "/usr/local/bin/geckodriver"
    else:
        # Use webdriver-manager on x86/x86_64
        gecko_path = GeckoDriverManager().install()

    service = Service(gecko_path)
    driver = webdriver.Firefox(service=service, options=options)
    return driver

def close_driver(driver):
    driver.quit()
