import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.havanna.com.br/login?url=/painel-do-cliente")

    input("Faca o login manualmente (incluindo reCAPTCHA) e pressione Enter para continuar...")

    # Garante que seguimos do inicio da loja apos o login manual.
    page.goto("https://www.havanna.com.br/")

    page.get_by_role("textbox", name="Busque aqui seu produto").click()
    page.get_by_role("textbox", name="Busque aqui seu produto").fill("Doce de leite")
    page.get_by_role("textbox", name="Busque aqui seu produto").press("Enter")
    page.get_by_role("button", name="Buscar").click()
    page.get_by_role("button", name="Comprar").click()
    page.get_by_role("button", name="Finalizar compraIr para o").click()
    page.get_by_role("textbox", name="Digita o CEP").click()
    page.get_by_role("button", name="Calcular").click()
    page.get_by_role("link", name="Finalizar compra").click()
    page.locator("#AddOrSetAddress_Number").click()
    page.locator("#AddOrSetAddress_Number").fill("507")
    page.locator("#AddOrSetAddress_AddressNotes").click()
    page.locator("#AddOrSetAddress_AddressNotes").fill("apartamento 151 ")
    page.get_by_role("textbox", name="ex: Escritorio, Casa, etc.").click()
    page.get_by_role("textbox", name="ex: Escritorio, Casa, etc.").fill("Casa mae ")
    page.get_by_role("button", name="Enviar para este endereco").click()
    page.get_by_role("radio").first.check()
    page.get_by_role("radio").first.click()
    page.get_by_role("link", name="Continuar").click()
    page.close()

    # ---------------------
    context.close()
    browser.close()
    # Exibe no terminal que o teste terminou com sucesso.
    print("Teste login + carrinho finalizado.")


with sync_playwright() as playwright:
    run(playwright)
