# Regras de diagnóstico do waterfall

As regras são explícitas para que a recomendação seja auditável: cada achado diz qual regra disparou. Os limites são pontos de partida para bens de consumo no Brasil e devem ser ajustados à realidade da empresa, dizendo isso na saída.

| Código | Dispara quando | Leitura | Ação padrão |
|---|---|---|---|
| **R1** | Existe condição fora da política (especial) no par SKU × canal | Desconto ou verba sem regra, que tende a virar permanente | Sem contrapartida medível: encerrar na renovação. Com contrapartida: converter em pay-for-performance, com meta e prazo de fim |
| **R2** | O vazamento do par fica ≥ 3 p.p. acima da média do canal | O par custa mais do que o canal justifica | Decompor e apontar a rubrica que explica ≥ 50% do desvio; a ação vem da regra dessa rubrica |
| **R3** | A margem de bolso % do par fica ≥ 5 p.p. abaixo da média da empresa | O item vende, mas paga pouco | Rever preço ou condição antes de buscar volume; cruzar com `price-pack-architecture` |
| **R4** | Bonificação > 2% do preço de nota | Produto grátis sem controle de destino | Converter em desconto condicionado (mesmo custo, com controle e visibilidade) |
| **R5** | Frete > 4% do preço de nota | Cost-to-serve alto (drop pequeno, rota longa) | Pedido mínimo, janela de entrega, roteirização ou FOB |
| **R6** | Custo financeiro > 2% do preço de nota (prazo de mais de ~50 dias) | Prazo financiando o cliente | Desconto por antecipação ou troca de prazo por outra contrapartida |
| **R7** | Verba de promoção > 2% da lista do par | Investimento promocional concentrado | Medir o retorno na skill `retorno-promocao` antes de cortar |

## Como valorar
- **R1:** valor = a condição especial inteira no período, anualizada.
- **R2 e R3:** valor = o desvio em p.p. × a receita a preço de lista do par, limitado ao valor da rubrica causadora.
- **R5 e R6:** valor = (rubrica atual − referência) × preço de nota. A referência é o melhor canal comparável ou o limite da regra.
- **R7:** não valorar aqui; encaminhar para o retorno de promoção.

## Prioridade
- **1:** valor ≥ 0,5% da margem de bolso total **e** decisão interna (política, pedido mínimo).
- **2:** valor alto, mas depende de negociação com o cliente.
- **3:** o resto.

Se a mesma rubrica dispara em vários pares, junte em um achado só ("bonificação no Atacarejo"), em vez de listar SKU por SKU.

## Próximo passo (roadmap)
Uma camada de decisão mais formal (árvore de decisão ou modelo estatístico sobre o histórico de negociações) pode substituir os limites fixos. O formato de saída da seção 4 da SKILL.md continua o mesmo.
