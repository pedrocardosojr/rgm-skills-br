# Regras de decisão de promoção

| Código | Dispara quando | Decisão padrão |
|---|---|---|
| **PR1** | Resultado negativo e **conclusivo** | Sair do formato atual: cortar ou redesenhar, conforme as regras PR2 a PR5 |
| **PR2** | Pull-forward ≥ 25% do incremental | Item estocável: reduzir profundidade e duração, limitar quantidade por cliente e espaçar os eventos (≥ 8 semanas) |
| **PR3** | Canibalização ≥ 25% do incremental | Promover o SKU que menos canibaliza ou o de maior margem por kg/L; conferir a escada de preço (`price-pack-architecture`) |
| **PR4** | Verba fixa > margem extra do SKU na promoção | Renegociar a verba para pay-for-performance (paga por unidade incremental) ou trocar por TPR sem encarte |
| **PR5** | Lift obtido < lift de equilíbrio | A profundidade não se paga: reduzir o desconto até perto do equilíbrio ou trocar de mecânica |
| **PR6** | Resultado **inconclusivo** | Não cortar nem escalar com esse dado. Repetir como teste com controle (metade das lojas, clientes parecidos) ou somar eventos semelhantes |
| **PR7** | O mesmo SKU × canal × mecânica teve resultado negativo duas vezes ou mais | É padrão, não acaso: tirar do calendário |
| **PR8** | Resultado positivo e **conclusivo** | Repetir e testar escala (mais uma semana, outro canal) |

## Agrupar
Junte eventos com a mesma causa em um achado só ("café 500 g com 15 a 18% de desconto") e some o valor. A ação vem da regra mais específica que disparou.

## Valor do achado
- **Cortar:** o valor é a perda evitada (−resultado).
- **Redesenhar:** use metade da perda evitada como estimativa conservadora até o teste confirmar.
- **Liberar verba:** mostre à parte o investimento liberado; ele não é ganho até ser realocado.

## Próximo passo (roadmap)
Trocar os limites fixos por um modelo calibrado com o histórico (por exemplo, uma árvore de decisão sobre profundidade, mecânica, categoria e estocabilidade), mantendo a mesma saída.
