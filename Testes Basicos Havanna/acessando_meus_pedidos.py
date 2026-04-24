import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.havanna.com.br/login?url=/painel-do-cliente")

    input("Faca o login manualmente (incluindo reCAPTCHA) e pressione Enter para continuar...")

    if page.locator("#mainModal").count() and page.locator("#mainModal").is_visible():
        page.locator("#mainModal").get_by_role("link", name="×").click()

    page.get_by_role("link", name="Meus Pedidos").click()
    page.get_by_role("link", name="Sair").click()
    page.close()

    # ---------------------
    context.close()
    browser.close()
    print("Teste acessando meus pedidos finalizado.")


with sync_playwright() as playwright:
    run(playwright)
