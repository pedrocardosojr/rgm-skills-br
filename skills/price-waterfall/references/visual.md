# Padrão visual (vale para as 4 skills do rgm-br)

O gestor lê em 30 segundos. O visual não é acabamento: ele é a análise.

## Regras
1. **O título diz a conclusão**, com o número: "R$ 15,6 mi (19,8%) da lista não chegam ao bolso", e não "Waterfall total".
2. **Um número-chave por bloco**, grande, com a unidade e a base de comparação.
3. **Cor só para o que importa.** Totais em azul; degraus em cinza; o degrau ou item que é o achado em vermelho. Nunca um arco-íris por categoria.
4. **Escala divergente para desvio** (acima ou abaixo da média): azul ↔ cinza ↔ vermelho, com o cinza no zero.
5. **Rótulos diretos** nos valores que sustentam a conclusão; nem todo ponto precisa de número.
6. **Um eixo só.** Duas grandezas diferentes viram dois gráficos.
7. **Texto em preto ou cinza**, nunca na cor da série.
8. **Fonte e premissa** em uma linha, pequena, no rodapé do gráfico.

## Paleta (tema claro)
| Papel | Hex |
|---|---|
| Fundo | `#fcfcfb` |
| Texto principal / secundário | `#0b0b0b` / `#52514e` |
| Total (azul) | `#2a78d6` |
| Degrau neutro (cinza) | `#b9b8b2` |
| Achado (vermelho) | `#e34948` |
| Divergente: azul ↔ neutro ↔ vermelho | `#2a78d6` · `#86b6ef` · `#f0efec` · `#f0a3a2` · `#e34948` |

## Formato
- **Para relatório ou README:** SVG ou PNG com fundo claro explícito, legível em tema escuro.
- **Para uso interativo:** HTML com tooltip por barra ou célula e uma tabela com os mesmos números logo abaixo.
- **Waterfall:** barras flutuantes com 2 px de espaço entre elas, os totais ancorados na base e o valor em R$ e em % da lista sobre cada barra.
