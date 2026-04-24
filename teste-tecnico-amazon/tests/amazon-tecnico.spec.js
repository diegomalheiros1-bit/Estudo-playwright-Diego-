// Importa os recursos principais do Playwright Test.
const { test, expect } = require('@playwright/test');

// Funcao utilitaria para fechar popups comuns que podem aparecer na pagina.
async function dismissCommonPopups(page) {
  // Lista de textos de botoes que normalmente fecham avisos/popups.
  const closeTexts = ['Aceitar', 'Continuar comprando', 'Fechar'];
  // Percorre cada possivel texto para tentar fechar o popup correspondente.
  for (const text of closeTexts) {
    // Localiza um botao pela role "button" e nome visivel igual ao texto atual.
    const button = page.getByRole('button', { name: text });
    // Verifica se o primeiro botao encontrado esta visivel; se der erro, considera falso.
    if (await button.first().isVisible().catch(() => false)) {
      // Clica no primeiro botao visivel para fechar o popup.
      await button.first().click();
      // Aguarda meio segundo para a interface estabilizar apos o clique.
      await page.waitForTimeout(500);
    }
  }
}

// Funcao que realiza uma busca e valida se a listagem de resultados apareceu.
async function searchAndAssertResults(page, term) {
  // Localiza o campo principal de busca da Amazon pelo id.
  const searchBox = page.locator('#twotabsearchtextbox');
  // Garante que o campo de busca esta visivel antes de interagir.
  await expect(searchBox).toBeVisible();
  // Clica no campo de busca para focar.
  await searchBox.click();
  // Preenche o campo com o termo recebido por parametro.
  await searchBox.fill(term);
  // Dispara a busca pressionando Enter.
  await searchBox.press('Enter');

  // Localiza os cards de produtos dentro do container principal de resultados.
  const results = page.locator("div.s-main-slot div[data-component-type='s-search-result']");
  // Garante que pelo menos o primeiro resultado esta visivel.
  await expect(results.first()).toBeVisible();
  // Conta quantos resultados foram encontrados na pagina.
  const total = await results.count();
  // Valida programaticamente que existe ao menos um resultado.
  expect(total).toBeGreaterThan(0);
  // Retorna o locator de resultados para reutilizacao no teste principal.
  return results;
}

// Funcao que tenta clicar no primeiro produto usando seletores alternativos.
async function clickFirstProduct(page) {
  // Lista de seletores candidatos para cobrir variacoes de layout da Amazon.
  const candidateSelectors = [
    // Seletor comum: titulo do produto dentro do card de resultado.
    '.s-main-slot .s-search-result h2 a',
    // Fallback por link que contenha padrao de URL de produto (/dp/).
    ".s-main-slot .s-search-result a[href*='/dp/']",
    // Fallback alternativo visto em algumas versoes da pagina.
    '.s-asin a:has(h2)',
  ];

  // Percorre cada seletor candidato ate encontrar um link valido.
  for (const selector of candidateSelectors) {
    // Localiza o primeiro elemento correspondente ao seletor atual.
    const candidate = page.locator(selector).first();
    // Verifica se existe pelo menos um elemento para esse seletor.
    if ((await candidate.count()) > 0) {
      // Tenta rolar ate o elemento; ignora erro caso nao seja necessario.
      await candidate.scrollIntoViewIfNeeded().catch(() => {});
      // Clica no link do produto encontrado.
      await candidate.click();
      // Sai da funcao apos clicar com sucesso.
      return;
    }
  }

  // Lanca erro explicativo se nenhum seletor encontrou produto clicavel.
  throw new Error('Nenhum link de produto encontrado nos resultados.');
}

// Define o caso de teste principal solicitado no teste tecnico.
test('Teste tecnico Amazon: busca, produto e nova busca', async ({ page }) => {
  // Abre a home da Amazon e aguarda o carregamento inicial do DOM.
  await page.goto('https://www.amazon.com.br/', { waitUntil: 'domcontentloaded' });
  // Fecha popups que possam bloquear as interacoes seguintes.
  await dismissCommonPopups(page);

  // Confere se o titulo da pagina contem "Amazon.com.br".
  await expect(page).toHaveTitle(/Amazon\.com\.br/);

  // Executa a primeira busca pelo termo "monitor 4k" e captura os resultados.
  const firstSearchResults = await searchAndAssertResults(page, 'monitor 4k');

  // Garante novamente que o primeiro resultado esta visivel antes do clique.
  await expect(firstSearchResults.first()).toBeVisible();
  // Clica no primeiro produto encontrado usando fallback de seletores.
  await clickFirstProduct(page);

  // Localiza o titulo da pagina de produto.
  const productTitle = page.locator('#productTitle');
  // Valida que o titulo do produto esta visivel.
  await expect(productTitle).toBeVisible();

  // Monta um locator com multiplos seletores de preco para cobrir layouts diferentes.
  const possiblePrice = page.locator([
    // Bloco de preco comum no layout desktop atual.
    '#corePriceDisplay_desktop_feature_div .a-price .a-offscreen',
    // Outro bloco de preco usado em algumas paginas de produto.
    '#corePrice_feature_div .a-price .a-offscreen',
    // Fallback antigo de preco normal.
    '#priceblock_ourprice',
    // Fallback antigo de preco promocional.
    '#priceblock_dealprice',
    // Fallback de preco no box de compra.
    '#price_inside_buybox',
    // Junta os seletores usando virgula para funcionar como "OU".
  ].join(', '));

  // Valida que ao menos um dos seletores de preco esta visivel.
  await expect(possiblePrice.first()).toBeVisible();

  // Tira screenshot da pagina do produto conforme requisito do teste tecnico.
  await page.screenshot({ path: 'screenshot-produto-amazon.png', fullPage: true });

  // Volta para a pagina anterior (lista de resultados).
  await page.goBack({ waitUntil: 'domcontentloaded' });
  // Fecha popups novamente caso reaparecam apos o retorno.
  await dismissCommonPopups(page);

  // Executa a segunda busca pedida: "notebook i7", validando resultados novamente.
  await searchAndAssertResults(page, 'notebook i7');
});
