from __future__ import annotations

from pathlib import Path

from playwright.sync_api import Page


BASE_DIR = Path(__file__).resolve().parents[2]
SCREENSHOTS_DIR = BASE_DIR / "screenshots"
HOME_URL = "https://www.havanna.com.br/"
LOGIN_URL = "https://www.havanna.com.br/login?url=/painel-do-cliente"


def dismiss_overlays(page: Page) -> None:
    for label in ("Fechar", "OK"):
        button = page.get_by_role("button", name=label)
        if button.count() and button.first.is_visible():
            button.first.click()
            page.wait_for_timeout(500)


def open_login_form(page: Page) -> None:
    page.goto(HOME_URL, wait_until="domcontentloaded", timeout=120000)
    page.wait_for_load_state("networkidle")
    dismiss_overlays(page)

    page.get_by_role("link", name="Login | Cadastre-se").click()
    page.wait_for_load_state("networkidle")
    dismiss_overlays(page)


def fill_visible_field(page: Page, selector: str, value: str) -> None:
    field = page.locator(selector)
    if field.count() and field.first.is_visible():
        field.first.fill(value)


def wait_for_input_value(page: Page, selector: str, expected_value: str) -> None:
    field = page.locator(selector)
    for _ in range(40):
        if field.input_value() == expected_value:
            return
        page.wait_for_timeout(250)
    raise AssertionError(f"Valor inesperado para {selector}: {field.input_value()!r}")


def assert_error_text(page: Page, selector: str, expected: str) -> None:
    actual = page.locator(selector).inner_text().strip()
    if actual != expected:
        raise AssertionError(f"Erro inesperado em {selector}: {actual!r}")
