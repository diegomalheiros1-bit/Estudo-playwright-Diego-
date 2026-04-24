from playwright.sync_api import sync_playwright, expect

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://meusiteficticio.com")
    page.wait_for_load_state("networkidle")

    page.get_by_role("link", name="Criar conta").click()
    page.wait_for_load_state("networkidle")

    expect(page).to_have_url("https://meusiteficticio.com/cadastro")

    page.get_by_label("Nome").fill("João da Silva")
    page.get_by_label("E-mail").fill("joao@email.com")
    page.get_by_label("CPF").fill("12345678900")
    page.get_by_label("Telefone").fill("11999999999")
    page.get_by_label("Senha").fill("Senha@123")
    page.get_by_label("Confirmar senha").fill("Senha@123")
    page.get_by_label("Aceito os termos").check()

    page.get_by_role("button", name="Cadastrar").click()

    expect(page.get_by_text("Cadastro realizado com sucesso")).to_be_visible()

    page.screenshot(path="evidencia_cadastro.png")

    print("Cadastro validado com sucesso e evidência gerada.")

    browser.close()