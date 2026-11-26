"""Gera os dados de exemplo da Vale Alto Alimentos (empresa fictícia).

Reproduzível: semente fixa, só biblioteca padrão.
Uso: python3 scripts/gerar_dados.py   (escreve em dados/)
"""
import csv
import math
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(42)
SAIDA = Path(__file__).resolve().parent.parent / "dados"
SAIDA.mkdir(exist_ok=True)

INICIO = date(2025, 12, 1)  # segunda-feira
SEMANAS = 52

# --------------------------------------------------------------------------
# Produtos
# --------------------------------------------------------------------------
PRODUTOS = [
    # sku, descricao, categoria, tamanho, unidade, conteudo_base (kg ou L), embalagem, preco_lista, custo, elasticidade, volume_base_semana
    ("CAF250", "Café torrado e moído 250 g", "Café", 250, "g", 0.25, "Almofada", 11.90, 5.80, -1.4, 9000),
    ("CAF500", "Café torrado e moído 500 g", "Café", 500, "g", 0.50, "Almofada", 21.90, 10.40, -1.8, 22000),
    ("CAF1K", "Café torrado e moído 1 kg", "Café", 1000, "g", 1.00, "Almofada", 41.50, 19.60, -2.0, 6000),
    ("BIS090", "Biscoito recheado chocolate 90 g", "Biscoito", 90, "g", 0.09, "Pacote", 2.49, 0.95, -2.2, 40000),
    ("BIS130", "Biscoito recheado chocolate 130 g", "Biscoito", 130, "g", 0.13, "Pacote", 3.29, 1.25, -2.0, 55000),
    ("BIS390", "Biscoito recheado chocolate multipack 3x130 g", "Biscoito", 390, "g", 0.39, "Multipack", 9.49, 3.80, -1.6, 9000),
    ("REF350", "Refrigerante cola lata 350 ml", "Refrigerante", 350, "ml", 0.35, "Lata", 3.19, 1.15, -1.5, 30000),
    ("REF600", "Refrigerante cola PET 600 ml", "Refrigerante", 600, "ml", 0.60, "PET", 4.49, 1.55, -1.8, 26000),
    ("REF2L", "Refrigerante cola PET 2 L", "Refrigerante", 2000, "ml", 2.00, "PET", 7.99, 3.10, -2.4, 38000),
]

# Reajustes de lista no período: categoria -> (data, % de aumento)
REAJUSTES = {
    "Café": (date(2026, 3, 2), 0.06),
    "Refrigerante": (date(2026, 2, 2), 0.05),
    "Biscoito": (date(2026, 5, 4), 0.04),
}

# --------------------------------------------------------------------------
# Canais e condições comerciais
# --------------------------------------------------------------------------
CANAIS = [
    # canal, nome, on_invoice, rebate, verba_contrato, bonificacao, frete, prazo, taxa_mes, markup_revenda, markup_varejo_final, revenda_no_simples
    ("ATC", "Atacarejo", 8.0, 3.0, 2.0, 2.5, 3.0, 42, 1.2, 18.0, 0.0, 0.0),
    ("RNA", "Rede nacional de supermercados", 5.0, 4.0, 5.0, 1.0, 3.5, 60, 1.2, 30.0, 0.0, 0.0),
    ("SRG", "Supermercado regional", 4.0, 1.0, 1.5, 1.0, 5.0, 35, 1.2, 32.0, 0.0, 30.0),
    ("DIS", "Distribuidor (atende o varejo tradicional)", 12.0, 2.0, 1.0, 0.5, 1.5, 28, 1.2, 14.0, 38.0, 85.0),
]

PARTICIPACAO_CANAL = {
    "Café": {"ATC": 0.30, "RNA": 0.25, "SRG": 0.20, "DIS": 0.25},
    "Biscoito": {"ATC": 0.25, "RNA": 0.25, "SRG": 0.20, "DIS": 0.30},
    "Refrigerante": {"ATC": 0.35, "RNA": 0.20, "SRG": 0.20, "DIS": 0.25},
}

# Condições negociadas fora da política (SKU x canal)
ESPECIAIS = [
    ("ATC", "REF2L", "bonificacao", 6.0, "Acordo de volume de verão renovado sem revisão"),
    ("DIS", "CAF500", "on_invoice", 3.0, "Desconto extra para combater marca regional"),
    ("DIS", "CAF1K", "on_invoice", 3.0, "Desconto extra para combater marca regional"),
    ("RNA", "BIS390", "verba_contrato", 4.0, "Enxoval de lançamento do multipack, nunca encerrado"),
]

# --------------------------------------------------------------------------
# Promoções
# --------------------------------------------------------------------------
# Em promoção o consumidor reage mais do que a um reajuste de lista (efeito de preço de referência)
ELASTICIDADE_PROMO = 1.8
LIFT_MECANICA = {"TPR": 1.00, "Encarte": 1.35, "Ponto extra": 1.40, "Encarte + ponto extra": 1.70, "Leve 3 pague 2": 1.15}
CANIBALIZACAO = {"Café": 0.35, "Biscoito": 0.15, "Refrigerante": 0.25}
PULL_FORWARD = {"CAF250": 0.25, "CAF500": 0.30, "CAF1K": 0.35, "BIS090": 0.05, "BIS130": 0.08,
                "BIS390": 0.20, "REF350": 0.05, "REF600": 0.05, "REF2L": 0.40}

PROMOCOES = [
    # evento, sku, canal, semana (0-51), duracao, mecanica, desconto %, verba fixa R$
    ("E01", "REF2L", "ATC", 2, 2, "TPR", 20, 15000),
    ("E02", "REF350", "RNA", 3, 2, "Encarte", 12, 25000),
    ("E03", "CAF500", "RNA", 6, 1, "Encarte + ponto extra", 15, 40000),
    ("E04", "BIS130", "SRG", 9, 2, "Leve 3 pague 2", 25, 8000),
    ("E05", "BIS390", "ATC", 10, 2, "TPR", 10, 2000),
    ("E06", "CAF250", "DIS", 12, 2, "TPR", 10, 0),
    ("E07", "REF600", "SRG", 13, 1, "Encarte", 15, 3000),
    ("E08", "CAF1K", "ATC", 15, 2, "TPR", 12, 5000),
    ("E09", "BIS090", "DIS", 17, 2, "TPR", 15, 0),
    ("E10", "CAF500", "ATC", 19, 2, "TPR", 18, 20000),
    ("E11", "REF2L", "RNA", 20, 1, "Encarte + ponto extra", 25, 45000),
    ("E12", "BIS130", "RNA", 22, 2, "Encarte", 15, 12000),
    ("E13", "CAF500", "SRG", 24, 1, "Encarte", 15, 15000),
    ("E14", "BIS390", "RNA", 26, 2, "Ponto extra", 8, 3000),
    ("E15", "REF350", "DIS", 27, 2, "TPR", 10, 0),
    ("E16", "CAF250", "RNA", 29, 1, "Encarte", 15, 8000),
    ("E17", "REF2L", "ATC", 31, 2, "TPR", 20, 15000),
    ("E18", "BIS090", "ATC", 33, 2, "TPR", 12, 1500),
    ("E19", "CAF500", "RNA", 35, 1, "Encarte + ponto extra", 15, 40000),
    ("E20", "REF600", "ATC", 36, 2, "TPR", 12, 8000),
    ("E21", "BIS130", "DIS", 38, 2, "TPR", 12, 0),
    ("E22", "CAF1K", "RNA", 40, 1, "Encarte", 10, 8000),
    ("E23", "BIS390", "SRG", 42, 2, "TPR", 10, 2000),
    ("E24", "REF2L", "SRG", 44, 1, "Encarte", 20, 15000),
    ("E25", "CAF500", "ATC", 46, 2, "TPR", 18, 20000),
    ("E26", "REF350", "RNA", 47, 2, "Encarte + ponto extra", 15, 8000),
    ("E27", "BIS130", "ATC", 49, 2, "TPR", 15, 10000),
]

# --------------------------------------------------------------------------
# Tributação (ilustrativa)
# --------------------------------------------------------------------------
TRIB_ATUAL = [
    ("Café", 7.0, 0.0, 0.0, "ICMS reduzido de cesta (varia por estado); PIS/Cofins zero (Lei 10.925/2004)"),
    ("Biscoito", 18.0, 9.25, 0.0, "Regime geral, sem substituição tributária"),
    ("Refrigerante", 18.0, 9.25, 4.0, "Simplificado: sem ST e sem regime monofásico"),
]
TRIB_REFORMA = [
    ("Café", "Cesta básica nacional", 100, "não", "LC 214/2025, Anexo I (conferir NCM 0901.2)"),
    ("Biscoito", "Alíquota padrão", 0, "não", "LC 214/2025, regra geral"),
    ("Refrigerante", "Alíquota padrão + Imposto Seletivo", 0, "sim", "LC 214/2025, IS sobre bebidas açucaradas; alíquota em lei ordinária"),
]
CBS_REF, IBS_REF, IS_REFRI = 8.8, 17.7, 10.0
CRONOGRAMA = [
    # ano, cbs, ibs, fator pis/cofins, fator ipi, fator icms, is refri, nota
    (2026, 0.9, 0.1, 1, 1, 1.0, 0.0, "Ano de teste: CBS e IBS destacados e compensados; efeito líquido zero"),
    (2027, CBS_REF, 0.1, 0, 0, 1.0, IS_REFRI, "CBS cheia; PIS/Cofins extintos; IPI zerado (exceto ZFM); IS começa"),
    (2028, CBS_REF, 0.1, 0, 0, 1.0, IS_REFRI, "Igual a 2027"),
    (2029, CBS_REF, round(IBS_REF * 0.1, 2), 0, 0, 0.9, IS_REFRI, "ICMS a 90%; IBS sobe na mesma proporção"),
    (2030, CBS_REF, round(IBS_REF * 0.2, 2), 0, 0, 0.8, IS_REFRI, "ICMS a 80%"),
    (2031, CBS_REF, round(IBS_REF * 0.3, 2), 0, 0, 0.7, IS_REFRI, "ICMS a 70%"),
    (2032, CBS_REF, round(IBS_REF * 0.4, 2), 0, 0, 0.6, IS_REFRI, "ICMS a 60%"),
    (2033, CBS_REF, IBS_REF, 0, 0, 0.0, IS_REFRI, "ICMS e ISS extintos; sistema novo completo"),
]


def mes_fator(categoria, d):
    m = d.month
    if categoria == "Café":
        return {4: 1.08, 5: 1.10, 6: 1.12, 7: 1.12, 8: 1.08, 12: 0.95}.get(m, 1.0)
    if categoria == "Refrigerante":
        return {12: 1.30, 1: 1.35, 2: 1.25, 3: 1.10, 6: 0.85, 7: 0.85, 11: 1.12}.get(m, 1.0)
    return {2: 1.10, 7: 1.05, 10: 1.05, 12: 1.08}.get(m, 1.0)


def escrever(nome, cabecalho, linhas):
    with open(SAIDA / nome, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(cabecalho)
        w.writerows(linhas)


def main():
    prod = {p[0]: p for p in PRODUTOS}
    canais = {c[0]: c for c in CANAIS}
    semanas = [INICIO + timedelta(weeks=i) for i in range(SEMANAS)]
    especiais = {(c, s, t): v for c, s, t, v, _ in ESPECIAIS}

    # preço de lista por semana (com reajuste)
    def preco_lista(sku, d):
        p = prod[sku]
        data_r, pct = REAJUSTES[p[2]]
        return round(p[7] * (1 + pct), 2) if d >= data_r else p[7]

    # 1) baseline (sem promoção)
    base = {}
    for sku, p in prod.items():
        cat, elast, vol = p[2], p[9], p[10]
        data_r, pct = REAJUSTES[cat]
        for c in canais:
            for i, d in enumerate(semanas):
                efeito_reajuste = (1 + pct) ** (elast * 0.5) if d >= data_r else 1.0  # concorrência acompanha metade
                base[(sku, c, i)] = vol * PARTICIPACAO_CANAL[cat][c] * mes_fator(cat, d) * efeito_reajuste

    unidades = dict(base)
    desc_promo = {}
    evento_de = {}

    # 2) promoções: lift, canibalização dos irmãos, pull-forward
    for ev, sku, c, s0, dur, mec, desc, _verba in PROMOCOES:
        p = prod[sku]
        cat = p[2]
        irmaos = [k for k, q in prod.items() if q[2] == cat and k != sku]
        lift = (1 - desc / 100) ** (p[9] * ELASTICIDADE_PROMO) * LIFT_MECANICA[mec]
        incr_total = 0.0
        for i in range(s0, min(s0 + dur, SEMANAS)):
            incr = base[(sku, c, i)] * (lift - 1)
            unidades[(sku, c, i)] += incr
            desc_promo[(sku, c, i)] = desc
            evento_de[(sku, c, i)] = ev
            incr_total += incr
            # canibalização em conteúdo (kg/L), dividida pelos irmãos conforme a baseline
            conteudo_canib = incr * p[5] * CANIBALIZACAO[cat]
            pesos = {k: base[(k, c, i)] * prod[k][5] for k in irmaos}
            soma = sum(pesos.values())
            for k in irmaos:
                unidades[(k, c, i)] -= conteudo_canib * pesos[k] / soma / prod[k][5]
        pf = incr_total * PULL_FORWARD[sku]
        for j, peso in ((s0 + dur, 0.65), (s0 + dur + 1, 0.35)):
            if j < SEMANAS:
                unidades[(sku, c, j)] -= pf * peso

    # 3) ruído e escrita
    linhas = []
    for sku in prod:
        for c in canais:
            on_inv = canais[c][2] + especiais.get((c, sku, "on_invoice"), 0.0)
            for i, d in enumerate(semanas):
                # piso de 35% da baseline: nem pull-forward nem canibalização zeram a venda de uma semana
                u = max(0.35 * base[(sku, c, i)], unidades[(sku, c, i)]) * math.exp(random.gauss(0, 0.07))
                linhas.append([d.isoformat(), sku, c, int(round(u)), f"{preco_lista(sku, d):.2f}",
                               f"{on_inv:.1f}", f"{desc_promo.get((sku, c, i), 0):.0f}", evento_de.get((sku, c, i), "")])
    escrever("vendas_semanais.csv",
             ["semana", "sku", "canal", "unidades", "preco_lista_unit", "desc_on_invoice_pct", "desc_promo_pct", "evento_id"], linhas)

    escrever("produtos.csv",
             ["sku", "descricao", "categoria", "marca", "tamanho", "unidade", "conteudo_kg_ou_l", "embalagem",
              "preco_lista_inicial", "custo_variavel_unit", "elasticidade_preco"],
             [[p[0], p[1], p[2], "Vale Alto", p[3], p[4], p[5], p[6], f"{p[7]:.2f}", f"{p[8]:.2f}", p[9]] for p in PRODUTOS])

    escrever("reajustes_lista.csv", ["categoria", "vigencia", "reajuste_pct"],
             [[k, v[0].isoformat(), f"{v[1] * 100:.1f}"] for k, v in REAJUSTES.items()])

    escrever("condicoes_canal.csv",
             ["canal", "nome", "desc_on_invoice_pct", "rebate_pct", "verba_contrato_pct", "bonificacao_pct", "frete_pct",
              "prazo_dias", "taxa_financeira_mes_pct", "markup_revenda_pct", "markup_varejo_final_pct", "revenda_no_simples_pct"],
             [list(c) for c in CANAIS])

    escrever("condicoes_especiais.csv", ["canal", "sku", "tipo", "pct_adicional", "motivo"], [list(e) for e in ESPECIAIS])

    escrever("promocoes.csv",
             ["evento_id", "sku", "canal", "semana_inicio", "duracao_semanas", "mecanica", "desc_promo_pct", "verba_fixa_rs"],
             [[e[0], e[1], e[2], semanas[e[3]].isoformat(), e[4], e[5], e[6], e[7]] for e in PROMOCOES])

    escrever("tributacao_atual.csv", ["categoria", "icms_pct", "pis_cofins_pct", "ipi_pct", "observacao"], [list(t) for t in TRIB_ATUAL])
    escrever("tributacao_reforma.csv", ["categoria", "regime", "reducao_aliquota_pct", "imposto_seletivo", "base_legal"],
             [list(t) for t in TRIB_REFORMA])
    escrever("cronograma_transicao.csv",
             ["ano", "cbs_pct", "ibs_pct", "fator_pis_cofins", "fator_ipi", "fator_icms", "is_refrigerante_pct", "nota"],
             [list(t) for t in CRONOGRAMA])
    print(f"ok: {len(linhas)} linhas em vendas_semanais.csv")


if __name__ == "__main__":
    main()
