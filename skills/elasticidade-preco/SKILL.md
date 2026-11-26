---
name: elasticidade-preco
description: Estima a elasticidade-preço de curto prazo por SKU e canal em bens de consumo, a partir de vendas semanais, com pooling hierárquico (canal dentro do SKU, SKU dentro da categoria) e intervalo de confiança. Diz quanto o volume reage a 1% de desconto, de que SKUs o dado não basta e quanto herdar da categoria. Alimenta as skills de promoção, reforma e escada de preço. Use quando pedirem "elasticidade", "quanto o volume reage ao preço", "sensibilidade a preço", "elasticidade promocional" ou quando outra skill precisar de elasticidade e os dados não a trouxerem.
---

# Elasticidade-preço

Em bens de consumo o preço de lista muda pouco, e quase toda a variação vem de promoção. Por isso o dado de um SKU sozinho costuma ser fraco. A pergunta é: **quanto o volume reage ao preço e quanto disso sai do próprio dado, e não de um palpite?**

## Método (código em `scripts/estimar_elasticidade.py`)
1. **Por SKU × canal:** `ln(unidades) = a + b·ln(preço pago) + efeito do mês`. O preço pago é a lista vigente × (1 − desconto promocional).
2. **Semanas fora**, porque o volume nelas não responde só a preço:
   - promoção de outro SKU da mesma categoria no canal (canibalização);
   - as 2 semanas depois de uma promoção do próprio SKU (pull-forward);
   - eventos com encarte ou ponto extra (a mecânica infla o volume).
3. **Identificação:** só estima quem tem variação de preço própria (promoção com desconto puro). Um reajuste de lista único se confunde com o mês e não identifica nada.
4. **Pooling hierárquico:** os canais do mesmo SKU compartilham a elasticidade; os SKUs se aproximam da média da categoria na proporção da incerteza deles (Bayes empírico, DerSimonian-Laird). SKU sem dado próprio herda a categoria com intervalo mais largo.
5. **Validar:** quando houver um teste de preço ou um parâmetro conhecido, confira quantos intervalos o contêm.

## Saída
- Tabela por SKU com a estimativa, o intervalo de 95% e o **peso do próprio dado** (0 = herdou tudo da categoria).
- Gráfico de pontos com intervalos e o título com a conclusão.
- Leitura de negócio: o lift esperado de um desconto (`(1 − d)^b − 1`) contra o lift necessário para empatar a margem. Isso liga direto à skill `retorno-promocao`.

## Cuidados
- É elasticidade **promocional de curto prazo**. A de um reajuste permanente é menor, porque a concorrência acompanha e o consumidor se acostuma (no caso, perto da metade).
- Com 2 anos ou mais de dados, troque o efeito do mês por sazonalidade de ano a ano e acrescente preço da concorrência. Com PyMC, o mesmo modelo vira bayesiano completo.
- Não decida com o ponto central de um SKU cujo intervalo é largo: use a faixa.
