# Contexto de mercado: onde o caso se encaixa

Três fatos situam a Vale Alto contra o mercado. As fontes estão no fim; as de fornecedor de software estão marcadas.

| Fato de mercado | Fonte | Como aparece no kit |
|---|---|---|
| Cerca de **3 em 4 promoções** não se pagam (análise de 39 milhões de eventos nos EUA). Numa pesquisa com executivos, 67% | Nielsen (2014); Strategy& (zero-based trade) | No caso 03, **15 de 27 (56%)** destroem margem com segurança estatística. O modelo é conservador |
| De 2019 a 2024, **mais de 90%** do crescimento de vendas de bens de consumo veio de preço; em 2024 as 50 maiores cresceram 1,2% | Infosys; Bain (2025) | A pauta virou volume com margem: promoção eficiente (caso 03), mix e escada de preço (caso 04) |
| **RGM 2.0** = preço, promoção, mix e condições comerciais num modelo só, em vez de ferramentas separadas | Everest Group (2025); NIQ (2026) | As 5 skills usam a mesma base (preço de bolso do waterfall) e o mesmo formato de recomendação |
| Planejar, prever e otimizar promoção (TPM, TPF e TPO) estão se fundindo; quase todo fornecedor anunciou IA em 2024-2025, mas **74% das empresas** ainda não usam IA generativa em trade | Comparativos de 2026 (POI citado; fornecedor) | O kit usa regras explícitas e estatística auditável, não caixa-preta |
| Elasticidade com pouco dado: o preço muda pouco em bens de consumo; a saída é decompor a sensibilidade por atributo (marca, tamanho, rede) | PepsiCo PricingAI (preprint de 2026) | O caso 05 usa pooling hierárquico: canal dentro do SKU, SKU dentro da categoria |
| Reforma: cerca de **metade dos processos** de linha de receita (marketing, trade, RGM, vendas) muda; a prateleira pode oscilar de −24,7 a +11,6 p.p. conforme o item | EY-Parthenon; EY | O caso 02 mede quem fica com a diferença, por canal e por ano |

## Ferramentas que o mercado usa (para situar o kit)
- **Dados de mercado:** NIQ (Nielsen), Circana, Kantar e, no Brasil, Scanntech, para sell-out, share e price index.
- **Planejamento e otimização de trade:** SAP RGM, TELUS (ex-Exceedra), Kantar XTEL, Visualfabriq, Vividly.
- **Modelagem aberta:** PyMC e PyMC-Marketing (modelos bayesianos).

O kit não substitui essas ferramentas. Ele mostra o raciocínio que fica por trás delas e funciona com o dado que toda indústria já tem (sell-in e condições comerciais).

## Fontes
- Nielsen via FoodNavigator: https://www.foodnavigator.com/Article/2014/10/09/Three-quarters-of-CPG-promotions-don-t-break-even-Nielsen/
- Strategy&, zero-based trade: https://www.strategyand.pwc.com/gx/en/insights/2017/zero-based-trade-for-cpg-leaders/zero-based-trade-for-cpg-leaders.pdf
- Infosys: https://www.infosys.com/iki/perspectives/integrated-revenue-growth-management-platforms.html
- Bain, Consumer Products Report 2025: https://www.bain.com/es-mx/insights/consumer-products-report-2025-reclaiming-relevance-in-the-gen-ai-era/
- Everest Group, RGM 2.0: https://www.everestgrp.com/wp-content/uploads/2025/06/Everest-Group-Revenue-Growth-Management-RGM-2.0-the-Next-Battleground-for-Enterprise-Technology-in-CPG.pdf
- NIQ: https://nielseniq.com/global/en/insights/analysis/2026/from-trade-spend-to-growth-engine-why-disconnected-pricing-tools-are-costing-manufacturers-more-than-time/
- Tellius, comparativo de 2026 (fornecedor): https://www.tellius.com/resources/blog/best-trade-promotion-analytics-platforms-in-2026-11-platforms-compared
- PepsiCo PricingAI (preprint): https://arxiv.org/abs/2606.17941
- EY, reforma e bens de consumo: https://www.ey.com/pt_br/insights/tax/reforma-tributaria-muda-o-varejo-e-bens-de-consumo
- PyMC-Marketing: https://joss.theoj.org/papers/10.21105/joss.10805
