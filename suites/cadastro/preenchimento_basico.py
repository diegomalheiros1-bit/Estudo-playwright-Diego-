from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys

from playwright.sync_api import sync_playwright

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from suites.cadastro.common import (
    REGISTER_URL,
    SCREENSHOTS_DIR,
    fill_and_blur_visible_field,
    fill_visible_field,
    format_cpf,
    generate_fake_cpf,
    open_registration_form,
    type_visible_field,
    wait_for_input_value,
)


SCREENSHOT_PATH = SCREENSHOTS_DIR / "cadastro-havanna-preenchido.png"


def run() -> None:
    SCREENSHOTS_DIR.mkdir(exist_ok=True)
    unique_suffix = datetime.now().strftime("%Y%m%d%H%M%S")
    fake_cpf = generate_fake_cpf()
    formatted_cpf = format_cpf(fake_cpf)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 2200})
        open_registration_form(page)

        fill_visible_field(page, "#AddOrSetCustomer-Name", "Maria")
        fill_visible_field(page, "#AddOrSetCustomer-Surname", "Teste")
        type_visible_field(page, "#AddOrSetCustomer-BirthDate", "01/01/1990", delay=30)
        if page.locator("#AddOrSetCustomer-Gender").is_visible():
            page.locator("#AddOrSetCustomer-Gender").select_option("F")
        type_visible_field(page, "#AddOrSetCustomer-Cpf", formatted_cpf)
        type_visible_field(page, "#AddOrSetCustomer-Contact-CellPhone", "(11) 98765-4321")
        fill_visible_field(page, "#AddOrSetCustomer-Email", f"maria.teste.{unique_suffix}@example.com")
        fill_visible_field(page, "#AddOrSetCustomer-Password", "Teste@12345")
        fill_visible_field(page, "#AddOrSetCustomer-Password-check", "Teste@12345")

        newsletter = page.locator("#AddOrSetCustomer-ExtendedProperties-0-Value")
        if newsletter.count() and newsletter.is_visible() and not newsletter.is_checked():
            newsletter.check()

        assert page.url == REGISTER_URL
        wait_for_input_value(page, "#AddOrSetCustomer-BirthDate", "01/01/1990")
        wait_for_input_value(page, "#AddOrSetCustomer-Cpf", formatted_cpf)
        wait_for_input_value(page, "#AddOrSetCustomer-Contact-CellPhone", "(11) 98765-4321")

        page.locator("#AddOrSetCustomer-Password-check").scroll_into_view_if_needed()
        page.wait_for_timeout(1000)
        page.screenshot(path=str(SCREENSHOT_PATH), full_page=True)
        browser.close()

    print(f"Screenshot salvo em: {SCREENSHOT_PATH}")


if __name__ == "__main__":
    run()
