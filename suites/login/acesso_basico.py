from __future__ import annotations

from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from suites.login.common import LOGIN_URL, SCREENSHOTS_DIR, open_login_form, wait_for_input_value
from playwright.sync_api import sync_playwright


SCREENSHOT_PATH = SCREENSHOTS_DIR / "login-havanna-acesso-basico.png"


def run() -> None:
    SCREENSHOTS_DIR.mkdir(exist_ok=True)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 2200})
        open_login_form(page)

        assert page.url == LOGIN_URL
        wait_for_input_value(page, "#widget75-email", "")
        wait_for_input_value(page, "#widget75-password", "")
        page.locator("#widget75-submit").scroll_into_view_if_needed()
        page.wait_for_timeout(1000)
        page.screenshot(path=str(SCREENSHOT_PATH), full_page=True)
        browser.close()

    print(f"Screenshot salvo em: {SCREENSHOT_PATH}")


if __name__ == "__main__":
    run()
