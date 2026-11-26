# Regras de decisão de PPA

| Código | Dispara quando | Leitura | Jogada padrão |
|---|---|---|---|
| **PP1** | O preço por kg/L **sobe** com o tamanho (inversão) | O shopper paga mais para levar mais | Corrigir já: repreçar o maior ou o menor |
| **PP2** | Desconto por kg/L entre degraus **< 5%** | O tamanho maior não premia; o shopper fica no menor ou o multipack não gira | Abrir o degrau subindo o tamanho **vizinho de margem maior**, antes de pensar em baixar o maior |
| **PP3** | Desconto por kg/L entre degraus **> 25%** | Margem cedida no tamanho grande; o volume desce para ele | Avaliar um tamanho intermediário ou um ajuste de preço no maior |
| **PP4** | Razão de conteúdo **> 2,5×** entre degraus (dobrar o tamanho é normal; triplicar deixa buraco) | Lacuna: falta um price point no meio | Simular o tamanho intermediário (origem do volume em 3 cenários) |
| **PP5** | Um tamanho tem **> 50% do volume** e margem por kg/L **abaixo da média** da categoria | Dependência de um item que paga pouco | Criar o degrau que permite repreçá-lo (PP4) e mover o mix |
| **PP6** | O preço de prateleira passa de um price point relevante (R$ 4,99 → R$ 5,0x; R$ 9,99 → R$ 10,x) | Perda de conversão acima do limiar | Avaliar conteúdo ou embalagem para segurar o price point, com aviso ao consumidor |
| **PP7** | O produto tem Imposto Seletivo acima do equilíbrio (skill `preco-cbs-ibs`) | A prateleira vai subir | Ter tamanhos menores e price points de entrada prontos antes de o IS entrar |

Se a escada não dispara nenhuma regra, diga que está **saudável** e use isso: em promoção, prefira o tamanho que menos canibaliza (ligação com `retorno-promocao`).

## Próximo passo (roadmap)
Estimar a matriz de substituição entre tamanhos com dados de painel ou de sell-out, em vez das faixas fixas de origem do volume.
