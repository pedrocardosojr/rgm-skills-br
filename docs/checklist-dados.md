# Dados mínimos para rodar o kit na sua empresa

O kit roda com o dado que toda indústria já tem. Comece pelo mínimo; o recomendado melhora a precisão.

| Skill | Mínimo | Grão e histórico | Onde costuma estar | Recomendado |
|---|---|---|---|---|
| `price-waterfall` | Faturamento com preço de lista e desconto na nota; política comercial por canal (rebate, verbas, bonificação, frete, prazo); custo variável | SKU × cliente (ou canal) × mês; 12 meses | ERP (SAP SD, faturamento), contratos comerciais, controladoria | Verbas pagas por cliente (TPM ou contas a pagar) e custo de servir real |
| `retorno-promocao` | Vendas **semanais** por SKU × cliente; cadastro dos eventos (início, fim, mecânica, desconto, verba) | Semana; 52 semanas, pelo menos 6 limpas em volta de cada evento | ERP, TPM, planilha de trade | Sell-out (Scanntech, NIQ) e lojas de controle |
| `elasticidade-preco` | As vendas semanais acima, com o preço pago | Semana; 52 semanas; pelo menos algumas promoções de desconto puro por SKU | ERP e TPM | 2 anos ou mais e preço da concorrência (price index) |
| `price-pack-architecture` | Preço de prateleira (ou markup do canal), conteúdo em kg/L por SKU, volume e margem de bolso | SKU × canal; o último trimestre basta | Coleta em loja, painel, saída do waterfall | Painel de consumidor para origem do volume entre tamanhos |
| `mix-rentabilidade` | Unidades, receita líquida e custo variável em dois períodos comparáveis | SKU × canal (ou cliente) × período; ano contra ano ou real contra orçamento | ERP, controladoria (custo padrão) | Custo real por lote e margem de bolso do waterfall |
| `sortimento` | Sell-out por loja × SKU e cadastro das lojas; datas de entrada e saída de SKU | Loja × SKU × mês; 12 meses, com um teste de descontinuação | Scanntech, NIQ, dados do cliente (portal do varejo) | Teste desenhado com grupo de controle e dados por planograma |
| `preco-cbs-ibs` | Carga **efetiva** atual por categoria (ICMS com benefícios e ST, PIS/Cofins, IPI); NCM; fatia de clientes no Simples por canal | Categoria × UF × canal | Fiscal e tributário, cadastro de clientes | Simulação por NCM com a classificação tributária oficial |

## Antes de começar, confira
- [ ] Preço com ou sem imposto: todas as tabelas na mesma base.
- [ ] Desconto na nota separado de verba fora da nota.
- [ ] Bonificação valorizada (a preço de nota ou a custo, sempre do mesmo jeito).
- [ ] Eventos promocionais com data de início e fim, não só o mês.
- [ ] SKUs substitutos agrupados (mesma categoria e uso).
- [ ] Um dono da regra em cada área (comercial, trade, fiscal) para validar os limites das regras.
