from __future__ import annotations

from pathlib import Path

from playwright.sync_api import Page


BASE_DIR = Path(__file__).resolve().parents[2]
SCREENSHOTS_DIR = BASE_DIR / "screenshots"
HOME_URL = "https://www.havanna.com.br/"
REGISTER_URL = "https://www.havanna.com.br/cadastro"


def dismiss_overlays(page: Page) -> None:
    for label in ("Fechar", "OK"):
        button = page.get_by_role("button", name=label)
        if button.count() and button.first.is_visible():
            button.first.click()
            page.wait_for_timeout(500)


def fill_visible_field(page: Page, selector: str, value: str) -> None:
    field = page.locator(selector)
    if field.count() and field.first.is_visible():
        field.first.fill(value)


def fill_and_blur_visible_field(page: Page, selector: str, value: str) -> None:
    field = page.locator(selector)
    if field.count() and field.first.is_visible():
        field.first.click()
        field.first.press("Control+A")
        field.first.press("Delete")
        field.first.fill(value)
        field.first.press("Tab")


def type_visible_field(page: Page, selector: str, value: str, delay: int = 120) -> None:
    field = page.locator(selector)
    if field.count() and field.first.is_visible():
        field.first.click()
        field.first.press("Control+A")
        field.first.press("Delete")
        field.first.type(value, delay=delay)


def generate_fake_cpf() -> str:
    base_digits = [1, 6, 8, 9, 9, 5, 3, 5, 0]
    first_verifier_sum = sum(digit * weight for digit, weight in zip(base_digits, range(10, 1, -1)))
    first_verifier_remainder = (first_verifier_sum * 10) % 11
    first_verifier = 0 if first_verifier_remainder == 10 else first_verifier_remainder

    cpf_digits = base_digits + [first_verifier]
    second_verifier_sum = sum(digit * weight for digit, weight in zip(cpf_digits, range(11, 1, -1)))
    second_verifier_remainder = (second_verifier_sum * 10) % 11
    second_verifier = 0 if second_verifier_remainder == 10 else second_verifier_remainder
    return "".join(str(digit) for digit in cpf_digits + [second_verifier])


def format_cpf(cpf_digits: str) -> str:
    return f"{cpf_digits[:3]}.{cpf_digits[3:6]}.{cpf_digits[6:9]}-{cpf_digits[9:]}"


def wait_for_input_value(page: Page, selector: str, expected_value: str) -> None:
    field = page.locator(selector)
    for _ in range(40):
        if field.input_value() == expected_value:
            return
        page.wait_for_timeout(250)
    raise AssertionError(f"Valor inesperado para {selector}: {field.input_value()!r}")


def open_registration_form(page: Page) -> None:
    page.goto(HOME_URL, wait_until="domcontentloaded", timeout=120000)
    page.wait_for_load_state("networkidle")
    dismiss_overlays(page)

    page.get_by_role("link", name="Login | Cadastre-se").click()
    page.wait_for_load_state("networkidle")
    dismiss_overlays(page)

    register_link = page.locator("a[href='/cadastro']")
    register_link.evaluate("(element) => element.click()")
    page.wait_for_url("**/cadastro", timeout=120000)
    page.wait_for_load_state("networkidle")
    dismiss_overlays(page)


def read_error_text(page: Page, error_id: str) -> str:
    locator = page.locator(f"#{error_id}")
    return locator.inner_text().strip() if locator.count() else ""


def assert_error_text(page: Page, error_id: str, expected: str) -> None:
    actual = read_error_text(page, error_id)
    if actual != expected:
        raise AssertionError(f"Erro inesperado em {error_id}: {actual!r}")
