# Estrutura do Projeto

## Visão geral

Este projeto foi montado para automatizar a tela de cadastro da Havanna com Playwright em Python.

A estrutura começou de forma simples, com um único script funcional, e depois foi organizada em uma suíte de cadastro para facilitar crescimento, manutenção e criação de novos cenários.

Hoje a base está organizada assim:

```text
New project/
  cadastro_havanna.py
  requirements.txt
  README.md
  ESTRUTURA_DO_PROJETO.md
  .gitignore
  suites/
    __init__.py
    cadastro/
      __init__.py
      common.py
      preenchimento_basico.py
      validacoes_negativas.py
```

## Como a estrutura foi pensada

A ideia principal foi separar o projeto em camadas simples:

- um ponto de entrada fácil de executar
- uma suíte organizada por funcionalidade
- um arquivo com utilidades compartilhadas
- arquivos separados para cada cenário

Isso evita que toda a lógica fique concentrada em um único script grande e difícil de manter.

## Arquivo de entrada

Arquivo: `cadastro_havanna.py`

Esse arquivo funciona como um atalho para executar o cenário principal da suíte de cadastro.

Ele foi mantido na raiz para facilitar o comando:

```powershell
python .\cadastro_havanna.py
```

Em vez de carregar toda a lógica do teste, ele apenas importa e executa o cenário positivo.

## Arquivo de dependências

Arquivo: `requirements.txt`

Esse arquivo define a dependência principal do projeto, permitindo reinstalar o ambiente de forma consistente.

## Arquivo de documentação principal

Arquivo: `README.md`

Esse arquivo documenta:

- o nome do projeto
- como instalar
- como executar
- a estrutura inicial da suíte

Ele foi pensado para ser a documentação rápida do projeto.

## Arquivo de documentação da estrutura

Arquivo: `ESTRUTURA_DO_PROJETO.md`

Este arquivo foi criado para explicar com mais detalhes como o projeto foi montado, o papel de cada arquivo e a lógica por trás da estrutura.

## Controle de arquivos gerados

Arquivo: `.gitignore`

Esse arquivo impede que artefatos temporários e arquivos gerados automaticamente sejam enviados ao GitHub.

Hoje ele ignora:

- `__pycache__/`
- `*.pyc`
- `screenshots/`

## Pasta de suítes

Pasta: `suites/`

Essa pasta organiza os testes por domínio funcional. Em vez de deixar todos os cenários na raiz, a lógica foi agrupada por assunto.

No momento, a primeira suíte é a de cadastro:

```text
suites/
  cadastro/
```

## Pacotes Python

Arquivos:

- `suites/__init__.py`
- `suites/cadastro/__init__.py`

Esses arquivos servem para o Python reconhecer essas pastas como pacotes, permitindo imports organizados entre os módulos do projeto.

## Arquivo comum da suíte

Arquivo: `suites/cadastro/common.py`

Esse é o arquivo de utilidades compartilhadas da suíte de cadastro.

Ele concentra comportamentos que podem ser reaproveitados por vários cenários, evitando duplicação de código.

### Responsabilidades principais do `common.py`

- abrir a navegação até a tela de cadastro
- fechar pop-ups e overlays
- preencher campos simples
- digitar em campos com máscara
- gerar CPF fictício válido
- formatar CPF
- validar valores preenchidos
- ler e validar mensagens de erro

### Funções principais do `common.py`

`dismiss_overlays(page)`

- fecha pop-ups e mensagens que podem bloquear cliques ou inputs

`fill_visible_field(page, selector, value)`

- preenche campos simples usando `fill()`

`fill_and_blur_visible_field(page, selector, value)`

- preenche o campo e sai dele com `Tab`
- foi criada para campos que só validam corretamente após perder foco

`type_visible_field(page, selector, value, delay=...)`

- digita caractere por caractere
- é útil para campos com máscara, como data, CPF e telefone

`generate_fake_cpf()`

- gera um CPF fictício válido para teste

`format_cpf(cpf_digits)`

- converte CPF numérico para o formato visual esperado pela tela

`wait_for_input_value(page, selector, expected_value)`

- espera o campo realmente assumir o valor esperado
- ajuda a estabilizar o teste quando há máscara ou atraso de atualização

`open_registration_form(page)`

- navega desde a home da Havanna até a tela final de cadastro

`read_error_text(page, error_id)`

- lê o texto de uma mensagem de erro específica

`assert_error_text(page, error_id, expected)`

- valida se o texto do erro exibido é o esperado

## Cenário positivo

Arquivo: `suites/cadastro/preenchimento_basico.py`

Esse arquivo representa o primeiro cenário de sucesso do projeto.

Ele usa as funções do `common.py` para:

- abrir o fluxo da home até o cadastro
- preencher os campos principais
- gerar e usar CPF fictício válido
- validar data, CPF e telefone
- salvar um screenshot final

### Objetivo do cenário positivo

Comprovar que o fluxo principal de preenchimento da tela funciona corretamente.

### Papel da função `run()`

A função `run()` é o roteiro completo do cenário positivo.

Ela coordena as etapas do teste, mas reaproveita a maior parte da lógica técnica já centralizada no `common.py`.

## Cenário negativo

Arquivo: `suites/cadastro/validacoes_negativas.py`

Esse arquivo foi criado para validar o comportamento da tela quando o usuário informa dados incorretos ou deixa campos obrigatórios vazios.

Ele foi separado do cenário positivo para manter os objetivos distintos:

- o cenário positivo valida sucesso
- o cenário negativo valida bloqueios e mensagens de erro

### Estrutura do cenário negativo

Esse arquivo foi dividido em dois blocos principais:

`submit_required_fields_scenario(page)`

- valida mensagens de obrigatoriedade com campos vazios

`submit_invalid_format_scenario(page)`

- valida mensagens de formato inválido com dados incorretos

### Validações cobertas no cenário negativo

Obrigatórios:

- Sobrenome
- Data de Nascimento
- Sexo
- CPF
- Telefone
- E-mail
- Senha

Formatos inválidos:

- data inválida
- sexo não selecionado
- CPF inválido
- telefone inválido
- e-mail inválido
- confirmação de senha divergente

### Observações importantes sobre a tela

Durante os testes, foi identificado que o comportamento atual da tela é este:

- o campo `Nome` não dispara validação client-side de obrigatoriedade
- `Nome` e `Sobrenome` não exibem validação client-side específica para caracteres especiais ou números no estado atual da página

Por isso, essas validações não foram forçadas artificialmente no código. O projeto valida o comportamento real observado na aplicação.

## Lógica de organização

A organização do projeto foi pensada para permitir crescimento.

Em vez de continuar adicionando tudo em um único arquivo, a estrutura já aceita novos cenários na pasta:

```text
suites/cadastro/
```

Exemplos de cenários futuros:

- `campos_obrigatorios.py`
- `cadastro_invalido.py`
- `validacao_mascaras.py`
- `cadastro_empresa.py`
- `confirmacao_senha.py`

## Resumo da arquitetura

Você pode pensar no projeto assim:

- `cadastro_havanna.py`: ponto de entrada simples
- `common.py`: caixa de ferramentas da suíte
- `preenchimento_basico.py`: cenário positivo
- `validacoes_negativas.py`: cenário negativo
- `README.md`: documentação rápida
- `ESTRUTURA_DO_PROJETO.md`: documentação detalhada da arquitetura

## Benefício dessa estrutura

O principal ganho é que o projeto deixou de ser apenas um script funcional e passou a ser uma base organizada de automação.

Isso facilita:

- manutenção
- reaproveitamento de código
- inclusão de novos cenários
- leitura do projeto
- evolução futura da suíte
