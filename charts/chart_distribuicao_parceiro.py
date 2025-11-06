import os
import matplotlib.pyplot as plt
import numpy as np

# === Paleta de cores Tempo Energia ===
COLOR_FATURA = "#002644"       # azul escuro
COLOR_ASSINATURA = "#FB6922"   # laranja
COLOR_NAO_COMP = "#1B2124"     # grafite
COLOR_25 = "#0074FF"           # azul Tempo Energia
COLOR_TEXTO = "#1B2124"        # cinza escuro para texto

def gerar_distribuicao_parceiro(finder_name, assinatura, assinatura_fechados=0.0):
    """
    Gera gráfico de distribuição mensal de assinaturas por tipo de Finder.
    Mostra apenas um mês sim e um mês não no eixo X para evitar poluição visual.
    """
    meses = [
        "Jan/2026", "Fev/2026", "Mar/2026", "Abr/2026", "Mai/2026", "Jun/2026",
        "Jul/2026", "Ago/2026", "Set/2026", "Out/2026", "Nov/2026", "Dez/2026",
        "Jan/2027", "Fev/2027", "Mar/2027", "Abr/2027", "Mai/2027", "Jun/2027",
        "Jul/2027", "Ago/2027", "Set/2027", "Out/2027", "Nov/2027", "Dez/2027"
    ]

    valores = np.zeros(len(meses))
    base_vals = np.zeros(len(meses))

    finder_lower = finder_name.lower()

    # Preenche arrays de acordo com o tipo de parceiro
    if "gold" in finder_lower:
        for i, mes in enumerate(meses):
            if mes in ["Mar/2026", "Mar/2027"]:
                valores[i] = assinatura
                base_vals[i] = assinatura_fechados * 1.0

    elif "plus" in finder_lower:
        for i, mes in enumerate(meses):
            if mes in ["Mar/2026", "Mar/2027"]:
                valores[i] = assinatura * 0.85
                base_vals[i] = assinatura_fechados * 0.85

    elif "indique" in finder_lower:
        for i, mes in enumerate(meses):
            if mes in ["Mar/2026", "Mar/2027"]:
                valores[i] = assinatura * 0.5
                base_vals[i] = assinatura_fechados * 0.5

    elif "parceiro exsat" in finder_lower or "exsat" in finder_lower:
        for i, mes in enumerate(meses):
            if mes in ["Mar/2026", "Mar/2027"]:
                valores[i] = assinatura * 0.51
                base_vals[i] = assinatura_fechados * 0.51
            elif mes in ["Abr/2026", "Mai/2026", "Jun/2026",
                "Jul/2026", "Ago/2026", "Set/2026", "Out/2026", "Nov/2026", "Dez/2026",
                "Jan/2027", "Fev/2027", "Abr/2027", "Mai/2027", "Jun/2027",
                "Jul/2027", "Ago/2027", "Set/2027", "Out/2027", "Nov/2027", "Dez/2027"]:
                valores[i] = assinatura * 0.01
                base_vals[i] = assinatura_fechados * 0.01
            else:
                valores[i] = 0
                base_vals[i] = 0

    # === Gráfico (colunas clusterizadas por mês) ===
    fig, ax = plt.subplots(figsize=(11, 4))
    x = np.arange(len(meses))
    width = 0.38

    bars_base = ax.bar(x - width / 2, base_vals, width, label="Fechados", color=COLOR_ASSINATURA)
    bars = ax.bar(x + width / 2, valores, width, label="Em Prospecção", color=COLOR_25)

    ax.set_title(f"Previsão de Comissão por Finder ({finder_name})", fontsize=12, color=COLOR_FATURA, fontweight="bold")

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

    # === Rótulos automáticos com ajuste dinâmico (para cada barra individual) ===
    max_val = max(np.max(base_vals) if any(base_vals) else 0, np.max(valores) if any(valores) else 0)

    def _label_bar(bar, val):
        x_center = bar.get_x() + bar.get_width() / 2
        if val <= 0 or max_val <= 0:
            return
        if val >= 0.3 * max_val:
            ax.text(x_center, bar.get_y() + bar.get_height() / 2, f"R$ {val:,.2f}", ha="center", va="center", fontsize=8, rotation=90, color="white", fontweight="bold")
        else:
            ax.text(x_center, bar.get_y() + bar.get_height() + (max_val * 0.02), f"R$ {val:,.2f}", ha="center", va="bottom", fontsize=8, rotation=90, color=COLOR_TEXTO, fontweight="bold")

    for bar, val in zip(bars_base, base_vals):
        _label_bar(bar, val)
    for bar, val in zip(bars, valores):
        _label_bar(bar, val)

    # Legenda e descrição compacta
    ax.legend(loc="upper right", fontsize=9)

    plt.tight_layout()
    distrib_chart_path = os.path.join("chart_distribuicao_parceiro.png")
    plt.savefig(distrib_chart_path, dpi=150, bbox_inches="tight")
    plt.close()

    return distrib_chart_path
