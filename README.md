# Testes Basicos Havanna

Projeto simples para estudo de automacao com **Playwright + Python**.

## Objetivo

Este projeto contem testes iniciais para aprender os fundamentos:
- abrir o site da Havanna
- navegar ate login
- preencher dados basicos de acesso

## Estrutura

```text
Testes Basicos Havanna/
  teste_acesso_havanna.py
  acessando_meus_pedidos.py
```

## Pre-requisitos

- Python instalado
- Playwright instalado no ambiente

## Instalacao (primeira vez)

```powershell
pip install playwright
python -m playwright install chromium
```

## Como executar

Teste 1 - acesso basico:

```powershell
python ".\Testes Basicos Havanna\teste_acesso_havanna.py"
```

Teste 2 - fluxo ate login para continuar evoluindo:

```powershell
python ".\Testes Basicos Havanna\acessando_meus_pedidos.py"
```

## Observacoes

- Os testes estao em modo visivel (`headless=False`) para facilitar o estudo.
- A ideia do projeto e manter tudo o mais simples possivel.
