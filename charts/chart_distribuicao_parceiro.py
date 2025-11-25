import os
import matplotlib.pyplot as plt
import numpy as np
import re

# === Paleta de cores Tempo Energia ===
COLOR_FATURA = "#002644"       # azul escuro
COLOR_ASSINATURA = "#FB6922"   # laranja
COLOR_NAO_COMP = "#1B2124"     # grafite
COLOR_25 = "#0074FF"           # azul Tempo Energia
COLOR_TEXTO = "#1B2124"        # cinza escuro para texto


def gerar_distribuicao_parceiro(finder_name, assinatura, assinatura_fechados=0.0, deals_fechados=None):
    """
    Gera gráfico de distribuição mensal de assinaturas por tipo de Finder.
    Mostra apenas um mês sim e um mês não no eixo X para evitar poluição visual.

    Suporta deals_fechados com:
      - 'assinatura'
      - 'plano_assinado'
      - opcionalmente 'has_interno', 'finder_raw' (ignorados aqui)
    """
    meses = [
        "Jan/2026", "Fev/2026", "Mar/2026", "Abr/2026", "Mai/2026", "Jun/2026",
        "Jul/2026", "Ago/2026", "Set/2026", "Out/2026", "Nov/2026", "Dez/2026",
        "Jan/2027", "Fev/2027", "Mar/2027", "Abr/2027", "Mai/2027", "Jun/2027",
        "Jul/2027", "Ago/2027", "Set/2027", "Out/2027", "Nov/2027", "Dez/2027"
    ]

    valores = np.zeros(len(meses))   # Em prospecção
    base_vals = np.zeros(len(meses)) # Fechados

    finder_lower = (finder_name or "").lower()

    # índices de Abril/2026 e Abril/2027 (datas de pagamento das comissões)
    try:
        idx_abr_2026 = meses.index("Abr/2026")
        idx_abr_2027 = meses.index("Abr/2027")
    except ValueError:
        idx_abr_2026 = idx_abr_2027 = None

    # =========================
    # 1) GOLD
    # =========================
    if "gold" in finder_lower:
        # Regras GOLD por plano (para FECHADOS):
        # - Plano 15% -> 30% em Abr/2026
        # - Plano 20% -> 100% em Abr/2026
        # - Plano 25% -> 100% em Abr/2026 e 100% em Abr/2027

        if deals_fechados:
            assinatura_total = (
                assinatura if assinatura and float(assinatura) > 0
                else sum(float(d.get('assinatura', 0) or 0) for d in deals_fechados)
            )

            # Prospecção: usa 100% em cada Abril (comportamento “cheio”)
            if idx_abr_2026 is not None:
                valores[idx_abr_2026] = assinatura_total
            if idx_abr_2027 is not None:
                valores[idx_abr_2027] = assinatura_total

            for deal in deals_fechados:
                if not isinstance(deal, dict):
                    continue

                deal_assinatura = float(deal.get('assinatura', 0) or 0)

                plano_label = str(deal.get('plano_assinado', '')).lower()
                m = re.search(r"(\d+(?:[\.,]\d+)?)", plano_label)
                perc = float(m.group(1).replace(',', '.')) if m else None

                # --- regra normal Gold, só por plano ---
                if perc == 15.0:
                    if idx_abr_2026 is not None:
                        base_vals[idx_abr_2026] += deal_assinatura * 0.30

                elif perc == 20.0:
                    if idx_abr_2026 is not None:
                        base_vals[idx_abr_2026] += deal_assinatura * 1.00

                elif perc == 25.0:
                    if idx_abr_2026 is not None:
                        base_vals[idx_abr_2026] += deal_assinatura * 1.00
                    if idx_abr_2027 is not None:
                        base_vals[idx_abr_2027] += deal_assinatura * 1.00

                else:
                    # fallback: considera 100% em Abr/2026
                    if idx_abr_2026 is not None:
                        base_vals[idx_abr_2026] += deal_assinatura * 1.00

        else:
            for i, mes in enumerate(meses):
                if mes in ["Abr/2026", "Abr/2027"]:
                    valores[i] = assinatura
                    base_vals[i] = assinatura_fechados * 1.0

    # =========================
    # 2) PLUS
    # =========================
    elif "plus" in finder_lower:
        # Regras PLUS por plano (para FECHADOS):
        # - Plano 15% -> 25% em Abr/2026
        # - Plano 20% -> 85% em Abr/2026
        # - Plano 25% -> 85% em Abr/2026 e 85% em Abr/2027
        # - Plano 30% -> 85% em Abr/2026 e 85% em Abr/2027
        # - "Outro"  -> 85% em Abr/2026 e 85% em Abr/2027

        if deals_fechados:
            assinatura_total = (
                assinatura if assinatura and float(assinatura) > 0
                else sum(float(d.get('assinatura', 0) or 0) for d in deals_fechados)
            )

            # Em prospecção: usa o máximo potencial do Plus (85% + 85%)
            if idx_abr_2026 is not None:
                valores[idx_abr_2026] = assinatura_total * 0.85
            if idx_abr_2027 is not None:
                valores[idx_abr_2027] = assinatura_total * 0.85

            for deal in deals_fechados:
                if not isinstance(deal, dict):
                    continue

                deal_assinatura = float(deal.get('assinatura', 0) or 0)

                plano_label_raw = str(deal.get('plano_assinado', ''))
                plano_label = plano_label_raw.lower()
                m = re.search(r"(\d+(?:[\.,]\d+)?)", plano_label)
                perc = float(m.group(1).replace(',', '.')) if m else None

                is_plano_30 = (
                    (perc is not None and abs(perc - 30.0) < 1e-9)
                    or "30" in plano_label  # segurança extra
                )
                is_outro = "outro" in plano_label

                # --- Plano 30% e "Outro" ---
                if is_plano_30 or is_outro:
                    if idx_abr_2026 is not None:
                        base_vals[idx_abr_2026] += deal_assinatura * 0.85
                    if idx_abr_2027 is not None:
                        base_vals[idx_abr_2027] += deal_assinatura * 0.85
                    continue

                # --- Regras padrão Plus ---
                if perc == 15.0:
                    if idx_abr_2026 is not None:
                        base_vals[idx_abr_2026] += deal_assinatura * 0.25
                elif perc == 20.0:
                    if idx_abr_2026 is not None:
                        base_vals[idx_abr_2026] += deal_assinatura * 0.85
                elif perc == 25.0:
                    if idx_abr_2026 is not None:
                        base_vals[idx_abr_2026] += deal_assinatura * 0.85
                    if idx_abr_2027 is not None:
                        base_vals[idx_abr_2027] += deal_assinatura * 0.85
                else:
                    # fallback: aplica 85% em Abr/2026
                    if idx_abr_2026 is not None:
                        base_vals[idx_abr_2026] += deal_assinatura * 0.85

        else:
            for i, mes in enumerate(meses):
                if mes in ["Abr/2026", "Abr/2027"]:
                    valores[i] = assinatura * 0.85
                    base_vals[i] = assinatura_fechados * 0.85

    # =========================
    # 3) INDIQUE
    # =========================
    elif "indique" in finder_lower:
        # Regras INDIQUE por plano (para FECHADOS):
        # - Plano 15% -> 15% em Abr/2026
        # - Plano 20% -> 50% em Abr/2026
        # - Plano 25% -> 50% em Abr/2026 e 50% em Abr/2027

        if deals_fechados:
            assinatura_total = (
                assinatura if assinatura and float(assinatura) > 0
                else sum(float(d.get('assinatura', 0) or 0) for d in deals_fechados)
            )

            if idx_abr_2026 is not None:
                valores[idx_abr_2026] = assinatura_total * 0.5
            if idx_abr_2027 is not None:
                valores[idx_abr_2027] = assinatura_total * 0.5

            for deal in deals_fechados:
                if not isinstance(deal, dict):
                    continue

                deal_assinatura = float(deal.get('assinatura', 0) or 0)

                plano_label = str(deal.get('plano_assinado', '')).lower()
                m = re.search(r"(\d+(?:[\.,]\d+)?)", plano_label)
                perc = float(m.group(1).replace(',', '.')) if m else None

                if perc == 15.0:
                    if idx_abr_2026 is not None:
                        base_vals[idx_abr_2026] += deal_assinatura * 0.15
                elif perc == 20.0:
                    if idx_abr_2026 is not None:
                        base_vals[idx_abr_2026] += deal_assinatura * 0.50
                elif perc == 25.0:
                    if idx_abr_2026 is not None:
                        base_vals[idx_abr_2026] += deal_assinatura * 0.50
                    if idx_abr_2027 is not None:
                        base_vals[idx_abr_2027] += deal_assinatura * 0.50
                else:
                    if idx_abr_2026 is not None:
                        base_vals[idx_abr_2026] += deal_assinatura * 0.50

        else:
            for i, mes in enumerate(meses):
                if mes in ["Abr/2026", "Abr/2027"]:
                    valores[i] = assinatura * 0.5
                    base_vals[i] = assinatura_fechados * 0.5

    # =========================
    # 4) EXSAT
    # =========================
    elif "parceiro exsat" in finder_lower or "exsat" in finder_lower:
        for i, mes in enumerate(meses):
            if mes in ["Abr/2026", "Abr/2027"]:
                valores[i] = assinatura * 0.51
                base_vals[i] = assinatura_fechados * 0.51
            elif mes in [
                "Abr/2026", "Mai/2026", "Jun/2026",
                "Jul/2026", "Ago/2026", "Set/2026", "Out/2026", "Nov/2026", "Dez/2026",
                "Jan/2027", "Fev/2027", "Abr/2027", "Mai/2027", "Jun/2027",
                "Jul/2027", "Ago/2027", "Set/2027", "Out/2027", "Nov/2027", "Dez/2027"
            ]:
                valores[i] = assinatura * 0.01
                base_vals[i] = assinatura_fechados * 0.01
            else:
                valores[i] = 0
                base_vals[i] = 0

    # =========================
    # === Gráfico (colunas clusterizadas por mês) ===
    # =========================
    fig, ax = plt.subplots(figsize=(11, 4))
    x = np.arange(len(meses))
    width = 0.38

    bars_base = ax.bar(x - width / 2, base_vals, width, label="Fechados", color=COLOR_ASSINATURA)
    bars = ax.bar(x + width / 2, valores, width, label="Em Prospecção", color=COLOR_25)

    ax.set_title(
        f"Previsão de Comissão por Finder ({finder_name})",
        fontsize=12, color=COLOR_FATURA, fontweight="bold"
    )

    ax.set_ylabel("Valor das Comissões (R$)", color=COLOR_TEXTO)
    ax.set_facecolor("#FFFFFF")

    # Aparência
    ax.spines['bottom'].set_color(COLOR_TEXTO)
    ax.spines['left'].set_color(COLOR_TEXTO)
    ax.tick_params(axis='x', rotation=45, labelsize=8, colors=COLOR_TEXTO)
    ax.tick_params(axis='y', colors=COLOR_TEXTO)

    # Exibir apenas meses alternados no eixo X (1 sim, 1 não)
    xtick_labels = [mes if i % 2 == 0 else "" for i, mes in enumerate(meses)]
    ax.set_xticks(x)
    ax.set_xticklabels(xtick_labels)

    # === Rótulos automáticos ===
    max_val = max(
        np.max(base_vals) if any(base_vals) else 0,
        np.max(valores) if any(valores) else 0
    )

    def _label_bar(bar, val):
        x_center = bar.get_x() + bar.get_width() / 2
        if val <= 0 or max_val <= 0:
            return
        if val >= 0.3 * max_val:
            ax.text(
                x_center,
                bar.get_y() + bar.get_height() / 2,
                f"R$ {val:,.2f}",
                ha="center", va="center",
                fontsize=8, rotation=90,
                color="white", fontweight="bold"
            )
        else:
            ax.text(
                x_center,
                bar.get_y() + bar.get_height() + (max_val * 0.02),
                f"R$ {val:,.2f}",
                ha="center", va="bottom",
                fontsize=8, rotation=90,
                color=COLOR_TEXTO, fontweight="bold"
            )

    for bar, val in zip(bars_base, base_vals):
        _label_bar(bar, val)
    for bar, val in zip(bars, valores):
        _label_bar(bar, val)

    ax.legend(loc="upper right", fontsize=9)

    plt.tight_layout()
    distrib_chart_path = os.path.join("chart_distribuicao_parceiro.png")
    plt.savefig(distrib_chart_path, dpi=150, bbox_inches="tight")
    plt.close()

    return distrib_chart_path