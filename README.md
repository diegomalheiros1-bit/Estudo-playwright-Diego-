# Projeto Teste Playwright - Cadastro Havanna

## Como instalar

```powershell
pip install -r requirements.txt
python -m playwright install chromium
```

## Como executar

Atalho pela raiz do projeto:

```powershell
python .\cadastro_havanna.py
```

Atalho da suíte de login:

```powershell
python .\login_havanna.py
```

Execução direta da suíte de cadastro:

```powershell
python .\suites\cadastro\preenchimento_basico.py
```

Cenário negativo com validações dos campos:

```powershell
python .\suites\cadastro\validacoes_negativas.py
```

Suíte de login:

```powershell
python .\suites\login\acesso_basico.py
```

## Estrutura inicial

```text
suites/
  cadastro/
    preenchimento_basico.py
    validacoes_negativas.py
  login/
    acesso_basico.py
```

O cenário atual abre a página de cadastro, preenche os campos visíveis do formulário de pessoa física e salva o resultado em `screenshots/cadastro-havanna-preenchido.png`.
