import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(storage_state="estado_login_havanna.json")
    page = context.new_page()
    page.goto("https://www.havanna.com.br/login?url=/painel-do-cliente")
    page.get_by_role("textbox", name="E-mail", exact=True).click()
    page.get_by_role("textbox", name="E-mail", exact=True).fill("diego.malheiros1@gmail.com")
    page.get_by_role("textbox", name="E-mail", exact=True).press("Tab")
    page.get_by_role("textbox", name="Senha").fill("Diego10")
    page.get_by_role("textbox", name="Senha").press("Enter")
    page.get_by_role("button", name="Continuar").click()
    page.locator("#mainModal").get_by_role("link", name="×").click()
    page.get_by_role("button", name="Continuar").click()
    page.get_by_role("link", name="Meus Pedidos").click()
    page.get_by_role("link", name="Sair").click()
    page.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
