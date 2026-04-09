# Guia de Arquivos e Linhas

## Objetivo

Este arquivo explica:

- o que faz cada arquivo principal do projeto
- o papel de cada arquivo da suíte de cadastro
- o que faz cada linha dos arquivos principais

Ele foi criado para servir como material de estudo do projeto.

## Arquivos do projeto

### `cadastro_havanna.py`

Função no projeto:

- é o ponto de entrada mais simples
- executa o cenário principal de cadastro
- evita que você precise chamar diretamente o arquivo interno da suíte

### `suites/__init__.py`

Função no projeto:

- marca a pasta `suites` como pacote Python
- permite imports organizados como `from suites.cadastro...`

### `suites/cadastro/__init__.py`

Função no projeto:

- marca a pasta `suites/cadastro` como pacote Python
- permite importar os módulos da suíte de cadastro

### `suites/cadastro/common.py`

Função no projeto:

- concentra funções utilitárias reutilizadas pelos cenários
- centraliza navegação, preenchimento, validações e leitura de mensagens

### `suites/cadastro/preenchimento_basico.py`

Função no projeto:

- contém o cenário positivo
- valida o preenchimento correto da tela
- gera screenshot do fluxo bem-sucedido

### `suites/cadastro/validacoes_negativas.py`

Função no projeto:

- contém o cenário negativo
- valida erros de obrigatoriedade
- valida erros de formato inválido
- gera screenshots dos cenários negativos

## Explicação linha por linha

## 1. `cadastro_havanna.py`

```python
1: from suites.cadastro.preenchimento_basico import run
```

- importa a função `run` do cenário positivo da suíte de cadastro

```python
4: if __name__ == "__main__":
```

- verifica se esse arquivo foi executado diretamente pelo Python

```python
5:     run()
```

- executa o cenário principal de preenchimento básico

## 2. `suites/__init__.py`

```python
1: # Este arquivo marca a pasta `suites` como um pacote Python.
```

- comentário explicando que a pasta `suites` é tratada como pacote Python

## 3. `suites/cadastro/__init__.py`

```python
1: # Este arquivo marca a pasta `suites/cadastro` como um pacote Python.
```

- comentário explicando que a pasta da suíte de cadastro é tratada como pacote Python

## 4. `suites/cadastro/common.py`

```python
1: from __future__ import annotations
```

- habilita comportamento moderno de anotações de tipo

```python
3: from pathlib import Path
```

- importa a classe `Path` para trabalhar com caminhos de arquivos

```python
5: from playwright.sync_api import Page
```

- importa o tipo `Page` da API síncrona do Playwright

```python
8: BASE_DIR = Path(__file__).resolve().parents[2]
```

- identifica a pasta raiz do projeto a partir do arquivo atual

```python
9: SCREENSHOTS_DIR = BASE_DIR / "screenshots"
```

- define a pasta onde screenshots serão salvos

```python
10: HOME_URL = "https://www.havanna.com.br/"
```

- guarda a URL da página inicial da Havanna

```python
11: REGISTER_URL = "https://www.havanna.com.br/cadastro"
```

- guarda a URL esperada da tela de cadastro

### Função `dismiss_overlays`

```python
14: def dismiss_overlays(page: Page) -> None:
```

- cria a função para fechar pop-ups e botões de aviso

```python
15:     for label in ("Fechar", "OK"):
```

- percorre os possíveis textos de botão encontrados nos overlays

```python
16:         button = page.get_by_role("button", name=label)
```

- localiza um botão com o texto correspondente

```python
17:         if button.count() and button.first.is_visible():
```

- verifica se o botão existe e está visível

```python
18:             button.first.click()
```

- clica no botão encontrado

```python
19:             page.wait_for_timeout(500)
```

- espera meio segundo para a tela reagir

### Função `fill_visible_field`

```python
22: def fill_visible_field(page: Page, selector: str, value: str) -> None:
```

- cria uma função genérica para preencher um campo visível

```python
23:     field = page.locator(selector)
```

- localiza o campo pelo seletor CSS

```python
24:     if field.count() and field.first.is_visible():
```

- verifica se o campo existe e está visível

```python
25:         field.first.fill(value)
```

- preenche o campo com o valor informado

### Função `fill_and_blur_visible_field`

```python
28: def fill_and_blur_visible_field(page: Page, selector: str, value: str) -> None:
```

- cria uma função para preencher o campo e depois tirar o foco

```python
29:     field = page.locator(selector)
```

- localiza o campo desejado

```python
30:     if field.count() and field.first.is_visible():
```

- garante que o campo existe e pode ser usado

```python
31:         field.first.click()
```

- coloca foco no campo

```python
32:         field.first.press("Control+A")
```

- seleciona todo o conteúdo atual

```python
33:         field.first.press("Delete")
```

- apaga o conteúdo anterior

```python
34:         field.first.fill(value)
```

- preenche o novo valor

```python
35:         field.first.press("Tab")
```

- sai do campo usando Tab, disparando validações de blur

### Função `type_visible_field`

```python
38: def type_visible_field(page: Page, selector: str, value: str, delay: int = 120) -> None:
```

- cria uma função para digitar caractere por caractere

```python
39:     field = page.locator(selector)
```

- localiza o campo

```python
40:     if field.count() and field.first.is_visible():
```

- valida se o campo existe e está visível

```python
41:         field.first.click()
```

- foca no campo

```python
42:         field.first.press("Control+A")
```

- seleciona todo o conteúdo existente

```python
43:         field.first.press("Delete")
```

- apaga o conteúdo anterior

```python
44:         field.first.type(value, delay=delay)
```

- digita o valor com o atraso configurado, útil para campos mascarados

### Função `generate_fake_cpf`

```python
47: def generate_fake_cpf() -> str:
```

- cria a função que gera um CPF fictício válido

```python
48:     base_digits = [1, 6, 8, 9, 9, 5, 3, 5, 0]
```

- define os 9 primeiros dígitos do CPF usado no cálculo

```python
49:     first_verifier_sum = sum(digit * weight for digit, weight in zip(base_digits, range(10, 1, -1)))
```

- calcula a soma ponderada do primeiro dígito verificador

```python
50:     first_verifier_remainder = (first_verifier_sum * 10) % 11
```

- aplica a regra matemática do CPF para obter o primeiro verificador

```python
51:     first_verifier = 0 if first_verifier_remainder == 10 else first_verifier_remainder
```

- ajusta o resultado para zero quando necessário

```python
53:     cpf_digits = base_digits + [first_verifier]
```

- junta os 9 dígitos base com o primeiro dígito verificador

```python
54:     second_verifier_sum = sum(digit * weight for digit, weight in zip(cpf_digits, range(11, 1, -1)))
```

- calcula a soma ponderada do segundo dígito verificador

```python
55:     second_verifier_remainder = (second_verifier_sum * 10) % 11
```

- aplica a regra matemática para o segundo verificador

```python
56:     second_verifier = 0 if second_verifier_remainder == 10 else second_verifier_remainder
```

- ajusta o valor final do segundo dígito verificador

```python
57:     return "".join(str(digit) for digit in cpf_digits + [second_verifier])
```

- retorna o CPF completo como texto

### Função `format_cpf`

```python
60: def format_cpf(cpf_digits: str) -> str:
```

- cria a função que formata um CPF numérico

```python
61:     return f"{cpf_digits[:3]}.{cpf_digits[3:6]}.{cpf_digits[6:9]}-{cpf_digits[9:]}"
```

- insere pontos e hífen no formato padrão brasileiro

### Função `wait_for_input_value`

```python
64: def wait_for_input_value(page: Page, selector: str, expected_value: str) -> None:
```

- cria a função que espera um campo assumir o valor esperado

```python
65:     field = page.locator(selector)
```

- localiza o campo

```python
66:     for _ in range(40):
```

- tenta várias vezes por um período limitado

```python
67:         if field.input_value() == expected_value:
```

- compara o valor atual do campo com o valor esperado

```python
68:             return
```

- encerra se o valor estiver correto

```python
69:         page.wait_for_timeout(250)
```

- espera um pouco antes de tentar novamente

```python
70:     raise AssertionError(f"Valor inesperado para {selector}: {field.input_value()!r}")
```

- dispara erro se o valor final não for o esperado

### Função `open_registration_form`

```python
73: def open_registration_form(page: Page) -> None:
```

- cria a função que navega até a tela de cadastro

```python
74:     page.goto(HOME_URL, wait_until="domcontentloaded", timeout=120000)
```

- abre a home da Havanna

```python
75:     page.wait_for_load_state("networkidle")
```

- espera a página estabilizar

```python
76:     dismiss_overlays(page)
```

- fecha eventuais pop-ups da home

```python
78:     page.get_by_role("link", name="Login | Cadastre-se").click()
```

- clica no link de login/cadastro

```python
79:     page.wait_for_load_state("networkidle")
```

- espera a página de login carregar

```python
80:     dismiss_overlays(page)
```

- fecha overlays da página de login

```python
82:     register_link = page.locator("a[href='/cadastro']")
```

- localiza o link final que leva para a tela de cadastro

```python
83:     register_link.evaluate("(element) => element.click()")
```

- executa o clique por JavaScript para evitar interferência visual do cabeçalho

```python
84:     page.wait_for_url("**/cadastro", timeout=120000)
```

- espera a URL final de cadastro

```python
85:     page.wait_for_load_state("networkidle")
```

- espera a tela estabilizar

```python
86:     dismiss_overlays(page)
```

- fecha qualquer pop-up restante antes do preenchimento

### Função `read_error_text`

```python
89: def read_error_text(page: Page, error_id: str) -> str:
```

- cria a função que lê o texto de um erro pelo ID

```python
90:     locator = page.locator(f"#{error_id}")
```

- localiza o elemento de erro

```python
91:     return locator.inner_text().strip() if locator.count() else ""
```

- retorna o texto do erro se existir; caso contrário retorna string vazia

### Função `assert_error_text`

```python
94: def assert_error_text(page: Page, error_id: str, expected: str) -> None:
```

- cria a função que compara o erro encontrado com o esperado

```python
95:     actual = read_error_text(page, error_id)
```

- lê o texto atual do erro

```python
96:     if actual != expected:
```

- verifica se o texto difere do esperado

```python
97:         raise AssertionError(f"Erro inesperado em {error_id}: {actual!r}")
```

- dispara erro se a mensagem não corresponder

## 5. `suites/cadastro/preenchimento_basico.py`

```python
1: from __future__ import annotations
```

- ativa comportamento moderno de anotações de tipo

```python
3: from datetime import datetime
```

- importa data e hora para criar e-mail único

```python
4: from pathlib import Path
```

- importa `Path` para resolver a raiz do projeto

```python
5: import sys
```

- importa `sys` para manipular o caminho de imports

```python
7: from playwright.sync_api import sync_playwright
```

- importa a API síncrona principal do Playwright

```python
9: ROOT_DIR = Path(__file__).resolve().parents[2]
```

- identifica a raiz do projeto a partir do arquivo atual

```python
10: if str(ROOT_DIR) not in sys.path:
```

- verifica se a raiz já está no caminho de imports do Python

```python
11:     sys.path.insert(0, str(ROOT_DIR))
```

- adiciona a raiz ao começo do `sys.path`

```python
13-23: from suites.cadastro.common import (...)
```

- importa do `common.py` tudo o que o cenário positivo precisa

```python
26: SCREENSHOT_PATH = SCREENSHOTS_DIR / "cadastro-havanna-preenchido.png"
```

- define o caminho do screenshot do cenário positivo

### Função `run`

```python
29: def run() -> None:
```

- cria a função principal do cenário positivo

```python
30:     SCREENSHOTS_DIR.mkdir(exist_ok=True)
```

- cria a pasta de screenshots se ela ainda não existir

```python
31:     unique_suffix = datetime.now().strftime("%Y%m%d%H%M%S")
```

- gera um identificador único para o e-mail do teste

```python
32:     fake_cpf = generate_fake_cpf()
```

- gera um CPF fictício válido

```python
33:     formatted_cpf = format_cpf(fake_cpf)
```

- formata o CPF para o padrão da tela

```python
35:     with sync_playwright() as playwright:
```

- inicia o contexto do Playwright

```python
36:         browser = playwright.chromium.launch(headless=True)
```

- abre o navegador Chromium em modo invisível

```python
37:         page = browser.new_page(viewport={"width": 1440, "height": 2200})
```

- abre uma nova página com viewport definida

```python
38:         open_registration_form(page)
```

- navega até a tela final de cadastro

```python
40:         fill_visible_field(page, "#AddOrSetCustomer-Name", "Maria")
```

- preenche o campo nome

```python
41:         fill_visible_field(page, "#AddOrSetCustomer-Surname", "Teste")
```

- preenche o sobrenome

```python
42:         type_visible_field(page, "#AddOrSetCustomer-BirthDate", "01/01/1990", delay=30)
```

- digita a data de nascimento em formato válido

```python
43:         if page.locator("#AddOrSetCustomer-Gender").is_visible():
```

- confere se o seletor de sexo está visível

```python
44:             page.locator("#AddOrSetCustomer-Gender").select_option("F")
```

- seleciona a opção Feminino

```python
45:         type_visible_field(page, "#AddOrSetCustomer-Cpf", formatted_cpf)
```

- digita o CPF válido formatado

```python
46:         type_visible_field(page, "#AddOrSetCustomer-Contact-CellPhone", "(11) 98765-4321")
```

- digita o telefone válido

```python
47:         fill_visible_field(page, "#AddOrSetCustomer-Email", f"maria.teste.{unique_suffix}@example.com")
```

- preenche um e-mail único

```python
48:         fill_visible_field(page, "#AddOrSetCustomer-Password", "Teste@12345")
```

- preenche a senha

```python
49:         fill_visible_field(page, "#AddOrSetCustomer-Password-check", "Teste@12345")
```

- repete a senha para confirmação

```python
51:         newsletter = page.locator("#AddOrSetCustomer-ExtendedProperties-0-Value")
```

- localiza o checkbox de newsletter

```python
52:         if newsletter.count() and newsletter.is_visible() and not newsletter.is_checked():
```

- verifica se o checkbox existe, está visível e ainda não está marcado

```python
53:             newsletter.check()
```

- marca o checkbox

```python
55:         assert page.url == REGISTER_URL
```

- garante que a navegação terminou na URL correta

```python
56:         wait_for_input_value(page, "#AddOrSetCustomer-BirthDate", "01/01/1990")
```

- valida o valor final da data

```python
57:         wait_for_input_value(page, "#AddOrSetCustomer-Cpf", formatted_cpf)
```

- valida o valor final do CPF

```python
58:         wait_for_input_value(page, "#AddOrSetCustomer-Contact-CellPhone", "(11) 98765-4321")
```

- valida o valor final do telefone

```python
60:         page.locator("#AddOrSetCustomer-Password-check").scroll_into_view_if_needed()
```

- rola a tela até a região final do formulário

```python
61:         page.wait_for_timeout(1000)
```

- espera um segundo antes do print

```python
62:         page.screenshot(path=str(SCREENSHOT_PATH), full_page=True)
```

- gera o screenshot final do cenário positivo

```python
63:         browser.close()
```

- fecha o navegador

```python
65:     print(f"Screenshot salvo em: {SCREENSHOT_PATH}")
```

- exibe no terminal onde o screenshot foi salvo

```python
68: if __name__ == "__main__":
69:     run()
```

- executa o cenário diretamente quando o arquivo é chamado pelo Python

## 6. `suites/cadastro/validacoes_negativas.py`

```python
1: from __future__ import annotations
```

- ativa comportamento moderno de anotações de tipo

```python
3: from pathlib import Path
```

- importa `Path` para calcular a raiz do projeto

```python
4: import sys
```

- importa `sys` para ajustar imports

```python
6: from playwright.sync_api import sync_playwright
```

- importa a API síncrona do Playwright

```python
8: ROOT_DIR = Path(__file__).resolve().parents[2]
```

- encontra a raiz do projeto

```python
9: if str(ROOT_DIR) not in sys.path:
```

- verifica se a raiz já está no `sys.path`

```python
10:     sys.path.insert(0, str(ROOT_DIR))
```

- adiciona a raiz ao caminho de imports se necessário

```python
12-19: from suites.cadastro.common import (...)
```

- importa do `common.py` os utilitários necessários para o cenário negativo

```python
22: REQUIRED_SCREENSHOT_PATH = SCREENSHOTS_DIR / "cadastro-havanna-negativo-obrigatorios.png"
```

- define o caminho do screenshot do cenário de obrigatórios

```python
23: INVALID_SCREENSHOT_PATH = SCREENSHOTS_DIR / "cadastro-havanna-negativo-invalidos.png"
```

- define o caminho do screenshot do cenário de inválidos

### Função `submit_required_fields_scenario`

```python
26: def submit_required_fields_scenario(page) -> None:
```

- cria o cenário de validação de campos obrigatórios vazios

```python
27:     open_registration_form(page)
```

- abre o fluxo até a tela de cadastro

```python
28:     page.get_by_role("button", name="Criar seu cadastro").click()
```

- tenta enviar o formulário sem preencher os campos

```python
29:     page.wait_for_timeout(1500)
```

- espera a interface reagir e mostrar os erros

```python
31:     assert page.url == REGISTER_URL
```

- confirma que a página continua na tela de cadastro

```python
32-38:     assert_error_text(...)
```

- valida as mensagens obrigatórias exibidas para cada campo esperado

```python
40:     # A tela não exibe validação client-side de obrigatoriedade para o campo Nome.
```

- documenta o comportamento real observado da aplicação

```python
41:     page.screenshot(path=str(REQUIRED_SCREENSHOT_PATH), full_page=True)
```

- gera o screenshot do cenário com obrigatórios vazios

### Função `submit_invalid_format_scenario`

```python
44: def submit_invalid_format_scenario(page) -> None:
```

- cria o cenário de dados preenchidos com formato inválido

```python
45:     open_registration_form(page)
```

- abre o fluxo até a tela de cadastro

```python
47:     fill_visible_field(page, "#AddOrSetCustomer-Name", "@@@###")
```

- preenche nome com caracteres especiais

```python
48:     fill_visible_field(page, "#AddOrSetCustomer-Surname", "123")
```

- preenche sobrenome com números

```python
49:     type_visible_field(page, "#AddOrSetCustomer-BirthDate", "29/02/2023", delay=30)
```

- digita uma data inválida

```python
50:     page.locator("#AddOrSetCustomer-BirthDate").press("Tab")
```

- tira o foco do campo para disparar a validação da data

```python
51:     page.locator("#AddOrSetCustomer-Gender").select_option("")
```

- deixa o campo sexo sem seleção válida

```python
52:     type_visible_field(page, "#AddOrSetCustomer-Cpf", "111.111.111-11")
```

- digita um CPF inválido

```python
53:     type_visible_field(page, "#AddOrSetCustomer-Contact-CellPhone", "(00) 00000-0000")
```

- digita um telefone inválido

```python
54:     fill_visible_field(page, "#AddOrSetCustomer-Email", "email-invalido")
```

- informa um e-mail inválido

```python
55:     fill_visible_field(page, "#AddOrSetCustomer-Password", "Teste@12345")
```

- preenche a senha principal

```python
56:     fill_visible_field(page, "#AddOrSetCustomer-Password-check", "Senha@99999")
```

- preenche uma confirmação diferente da senha principal

```python
58:     page.get_by_role("button", name="Criar seu cadastro").click()
```

- tenta enviar o formulário com dados inválidos

```python
59:     page.wait_for_timeout(1500)
```

- espera as mensagens de erro aparecerem

```python
61:     assert page.url == REGISTER_URL
```

- garante que a página permaneceu no cadastro

```python
62-67:     assert_error_text(...)
```

- valida as mensagens de erro esperadas para os campos inválidos

```python
69:     # Nome e Sobrenome aceitam esses caracteres no client-side atual; por isso não há alerta específico para eles.
```

- documenta o comportamento real da aplicação para nome e sobrenome

```python
70:     page.screenshot(path=str(INVALID_SCREENSHOT_PATH), full_page=True)
```

- gera o screenshot do cenário com dados inválidos

### Função `run`

```python
73: def run() -> None:
```

- cria a função principal da suíte negativa

```python
74:     SCREENSHOTS_DIR.mkdir(exist_ok=True)
```

- cria a pasta de screenshots se necessário

```python
76:     with sync_playwright() as playwright:
```

- inicia o contexto do Playwright

```python
77:         browser = playwright.chromium.launch(headless=True)
```

- abre o navegador Chromium em modo invisível

```python
79:         required_page = browser.new_page(viewport={"width": 1440, "height": 2600})
```

- cria uma página para o cenário de obrigatórios

```python
80:         submit_required_fields_scenario(required_page)
```

- executa o cenário de campos obrigatórios

```python
81:         required_page.close()
```

- fecha a página usada nesse cenário

```python
83:         invalid_page = browser.new_page(viewport={"width": 1440, "height": 2600})
```

- cria uma página para o cenário de inválidos

```python
84:         submit_invalid_format_scenario(invalid_page)
```

- executa o cenário de formatos inválidos

```python
85:         invalid_page.close()
```

- fecha a página usada nesse cenário

```python
87:         browser.close()
```

- fecha o navegador ao final

```python
89:     print(f"Screenshot obrigatorios salvo em: {REQUIRED_SCREENSHOT_PATH}")
```

- informa o caminho do screenshot dos obrigatórios

```python
90:     print(f"Screenshot invalidos salvo em: {INVALID_SCREENSHOT_PATH}")
```

- informa o caminho do screenshot dos inválidos

```python
93: if __name__ == "__main__":
94:     run()
```

- executa a suíte negativa diretamente quando esse arquivo é rodado

## Resumo final

Se você quiser memorizar a função de cada arquivo de forma rápida:

- `cadastro_havanna.py`: atalho de execução
- `suites/__init__.py`: pacote Python da pasta `suites`
- `suites/cadastro/__init__.py`: pacote Python da suíte de cadastro
- `common.py`: funções compartilhadas
- `preenchimento_basico.py`: cenário positivo
- `validacoes_negativas.py`: cenário negativo

Se quiser, no próximo passo eu posso transformar esse guia em uma versão ainda mais visual, com tabela por arquivo e fluxograma de execução. 
