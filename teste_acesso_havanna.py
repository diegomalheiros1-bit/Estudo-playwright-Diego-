import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    # Abre o navegador Chromium no modo visível (headless=False).
    browser = playwright.chromium.launch(headless=False)
    # Cria um contexto isolado (como uma sessão nova do navegador).
    context = browser.new_context()
    # Abre uma nova aba dentro do contexto.
    page = context.new_page()
    # Acessa o site da Havanna.
    page.goto("https://www.havanna.com.br/")
    # Clica no link de login/cadastro.
    page.get_by_role("link", name="Login | Cadastre-se").click()
    # Clica em um item do menu identificado pelo texto.
    page.locator("#main-menu div").filter(has_text="Alfajores Alfajor Havanna 70").click()
    # Clica no campo de e-mail.
    page.get_by_role("textbox", name="E-mail", exact=True).click()
    # Preenche o campo de e-mail.
    page.get_by_role("textbox", name="E-mail", exact=True).fill("diego.malheiros1@gmail.com")
    # Pressiona TAB para sair do campo de e-mail.
    page.get_by_role("textbox", name="E-mail", exact=True).press("Tab")
    # Preenche o campo de senha.
    page.get_by_role("textbox", name="Senha").fill("Diego10")
    # Pressiona Enter para tentar enviar o login.
    page.get_by_role("textbox", name="Senha").press("Enter")
    # Clica no botão Continuar.
    page.get_by_role("button", name="Continuar").click()
    # Clica no link Sair para encerrar a sessão.
    page.get_by_role("link", name="Sair").click()

    # ---------------------
    # Fecha o contexto (sessão da aba/navegação).
    context.close()
    # Fecha o navegador.
    browser.close()


# Inicia o Playwright e garante encerramento automático dos recursos.
with sync_playwright() as playwright:
    # Executa o fluxo principal definido na função run.
    run(playwright)
