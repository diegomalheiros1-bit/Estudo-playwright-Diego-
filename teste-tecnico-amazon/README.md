# Teste Tecnico Amazon com Playwright

## Requisitos
- Node.js 18+

## Instalacao
```powershell
cd .\teste-tecnico-amazon
npm install
npx playwright install chromium
```

## Execucao
Headless:
```powershell
npm test
```

Com navegador aberto:
```powershell
npm run test:headed
```

## Cenarios cobertos
- Acessa `https://www.amazon.com.br/`
- Busca por `monitor 4k`
- Valida que existem produtos nos resultados
- Clica no primeiro produto da lista
- Valida titulo visivel e preco
- Gera screenshot da pagina do produto em `screenshot-produto-amazon.png`
- Volta para a busca e pesquisa `notebook i7`
- Valida novamente se ha produtos visiveis
