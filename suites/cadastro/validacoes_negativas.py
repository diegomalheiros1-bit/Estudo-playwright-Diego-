from __future__ import annotations

from pathlib import Path
import sys

from playwright.sync_api import sync_playwright

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from suites.cadastro.common import (
    REGISTER_URL,
    SCREENSHOTS_DIR,
    assert_error_text,
    fill_visible_field,
    open_registration_form,
    type_visible_field,
)


REQUIRED_SCREENSHOT_PATH = SCREENSHOTS_DIR / "cadastro-havanna-negativo-obrigatorios.png"
INVALID_SCREENSHOT_PATH = SCREENSHOTS_DIR / "cadastro-havanna-negativo-invalidos.png"


def submit_required_fields_scenario(page) -> None:
    open_registration_form(page)
    page.get_by_role("button", name="Criar seu cadastro").click()
    page.wait_for_timeout(1500)

    assert page.url == REGISTER_URL
    assert_error_text(page, "AddOrSetCustomer-Surname-error", "Preencha o campo Sobrenome")
    assert_error_text(page, "AddOrSetCustomer-BirthDate-error", "Preencha o campo data de Nascimento")
    assert_error_text(page, "AddOrSetCustomer-Gender-error", "Selecione o Sexo")
    assert_error_text(page, "AddOrSetCustomer-Cpf-error", "Preencha o campo CPF")
    assert_error_text(page, "AddOrSetCustomer-Contact-CellPhone-error", "O campo não pode estar em branco")
    assert_error_text(page, "AddOrSetCustomer-Email-error", "Preencha o campo de email")
    assert_error_text(page, "AddOrSetCustomer-Password-error", "Preencha o campo senha")

    # A tela não exibe validação client-side de obrigatoriedade para o campo Nome.
    page.screenshot(path=str(REQUIRED_SCREENSHOT_PATH), full_page=True)


def submit_invalid_format_scenario(page) -> None:
    open_registration_form(page)

    fill_visible_field(page, "#AddOrSetCustomer-Name", "@@@###")
    fill_visible_field(page, "#AddOrSetCustomer-Surname", "123")
    type_visible_field(page, "#AddOrSetCustomer-BirthDate", "29/02/2023", delay=30)
    page.locator("#AddOrSetCustomer-BirthDate").press("Tab")
    page.locator("#AddOrSetCustomer-Gender").select_option("")
    type_visible_field(page, "#AddOrSetCustomer-Cpf", "111.111.111-11")
    type_visible_field(page, "#AddOrSetCustomer-Contact-CellPhone", "(00) 00000-0000")
    fill_visible_field(page, "#AddOrSetCustomer-Email", "email-invalido")
    fill_visible_field(page, "#AddOrSetCustomer-Password", "Teste@12345")
    fill_visible_field(page, "#AddOrSetCustomer-Password-check", "Senha@99999")

    page.get_by_role("button", name="Criar seu cadastro").click()
    page.wait_for_timeout(1500)

    assert page.url == REGISTER_URL
    assert_error_text(page, "AddOrSetCustomer-BirthDate-error", "Informe uma data válida.")
    assert_error_text(page, "AddOrSetCustomer-Gender-error", "Selecione o Sexo")
    assert_error_text(page, "AddOrSetCustomer-Cpf-error", "Informe um CPF válido.")
    assert_error_text(page, "AddOrSetCustomer-Contact-CellPhone-error", "Informe um telefone celular válido.")
    assert_error_text(page, "AddOrSetCustomer-Email-error", "Informe um e-mail válido.")
    assert_error_text(page, "AddOrSetCustomer-Password-check-error", "Repita corretamente a senha informada.")

    # Nome e Sobrenome aceitam esses caracteres no client-side atual; por isso não há alerta específico para eles.
    page.screenshot(path=str(INVALID_SCREENSHOT_PATH), full_page=True)


def run() -> None:
    SCREENSHOTS_DIR.mkdir(exist_ok=True)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)

        required_page = browser.new_page(viewport={"width": 1440, "height": 2600})
        submit_required_fields_scenario(required_page)
        required_page.close()

        invalid_page = browser.new_page(viewport={"width": 1440, "height": 2600})
        submit_invalid_format_scenario(invalid_page)
        invalid_page.close()

        browser.close()

    print(f"Screenshot obrigatorios salvo em: {REQUIRED_SCREENSHOT_PATH}")
    print(f"Screenshot invalidos salvo em: {INVALID_SCREENSHOT_PATH}")


if __name__ == "__main__":
    run()
