import os
import matplotlib.pyplot as plt
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# CORREÇÃO DE IMPORTAÇÃO: Removendo o acento de 'distribuição' para evitar o ImportError
from charts.chart_distribuicao_parceiro import gerar_distribuicao_parceiro


# --- Função Auxiliar de Formatação BR ---
def format_br(value):
    """Formata um número float para o padrão monetário brasileiro (R$ x.xxx,xx)."""
    # 1. Formata para EUA (Ex: 3005.67 -> "3,005.67")
    valor_formatado_eua = f'{value:,.2f}'
    # 2. Converte para BR (Troca ',' de milhar por '#' temporário, depois ',' de milhar por '.', e '#' por ',')
    return valor_formatado_eua.replace('.', '#').replace(',', '.').replace('#', ',')
# ----------------------------------------


def extract_subcontratado(finder_name: str) -> str:
    """
    Extrai o nome do subcontratado a partir do finder_name.
    Retorna tudo após o segundo ' - '.
    """
    try:
        partes = [p.strip() for p in finder_name.split(" - ")]
        if len(partes) >= 3:
            return " - ".join(partes[2:])
        elif len(partes) == 2:
            return partes[1]
        else:
            return finder_name.strip()
    except Exception:
        return finder_name.strip()


def generate_pdf(
    finder_name,
    valor_medio_por_consumo,
    assinatura,
    nao_compensavel,
    vinte_cinco_porcento,
    deals_prospeccao,
    deals_fechados,
    assinatura_fechados,
    pasta_saida
):
    # === DADOS BÁSICOS ===
    sanitized_name = finder_name.replace(" ", "_").replace("/", "_")
    pdf_path = os.path.join(pasta_saida, f"{sanitized_name}.pdf")
    distrib_chart_path = gerar_distribuicao_parceiro(finder_name, assinatura, assinatura_fechados)

    # === PALHETA DE CORES ===
    COLOR_FATURA = "#002644"
    COLOR_ASSINATURA = "#FB6922"
    COLOR_NAO_COMP = "#1B2124"
    COLOR_25 = "#0074FF"

    # === GRÁFICO DE DECOMPOSIÇÃO DA FATURA ===
    fig, ax = plt.subplots(figsize=(8, 4))
    
    # AJUSTE: Inserindo '\n' (quebra de linha) para melhorar a visualização dos rótulos
    categorias = [
        "Valor Médio\nConsumo Sem a TG", 
        "Economia Percebida\n- Plano 25%", 
        "Assinatura", 
        "Não Compensável"
    ]
    x_pos = [0, 1, 2, 3]
    largura = 0.6

    plt.rcParams["hatch.color"] = "white"
    plt.rcParams["hatch.linewidth"] = 1

    # === ESTRUTURA DAS BARRAS ===
    bar_fatura = ax.bar(x_pos[0], valor_medio_por_consumo, color=COLOR_FATURA, width=largura)
    bar_assin = ax.bar(x_pos[2], assinatura, bottom=nao_compensavel, color=COLOR_ASSINATURA, width=largura)
    bar_nao_comp = ax.bar(x_pos[3], nao_compensavel, color=COLOR_NAO_COMP, alpha=0.3, width=largura)
    bar_25 = ax.bar(x_pos[1], vinte_cinco_porcento,
                    bottom=assinatura + nao_compensavel,
                    color=COLOR_25, width=largura, hatch='///')

    ax.axhline(y=valor_medio_por_consumo, color=COLOR_NAO_COMP, linestyle="--", linewidth=1.2)

    ax.set_xticks(x_pos)
    ax.set_xticklabels(categorias, fontsize=9, color=COLOR_NAO_COMP)
    ax.set_ylabel("Valores (R$)", color=COLOR_NAO_COMP)
    ax.set_facecolor("#FFFFFF")
    ax.spines["bottom"].set_color(COLOR_NAO_COMP)
    ax.spines["left"].set_color(COLOR_NAO_COMP)
    ax.tick_params(axis="y", colors=COLOR_NAO_COMP)
    ax.set_ylim(0, valor_medio_por_consumo * 1.25)
    ax.set_title("Comparativo de Valores Médios Com e Sem Benefício TG", fontsize=12, color=COLOR_FATURA, fontweight="bold")

    # === RÓTULOS DE DADOS (USANDO format_br) ===
    # Rótulos dos eixos
    ax.set_ylabel("Valores (R$)", color=COLOR_NAO_COMP)

    # RÓTULO FATURA
    for bar in bar_fatura:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height / 2,
                f"R$ {format_br(height)}", ha="center", va="center",
                color="white", fontsize=9, fontweight="bold")
                
    # RÓTULO ASSINATURA
    for bar in bar_assin:
        height = bar.get_height() + nao_compensavel
        ax.text(bar.get_x() + bar.get_width() / 2, height + (valor_medio_por_consumo * 0.02),
                f"R$ {format_br(assinatura)}", ha="center", va="bottom",
                color=COLOR_ASSINATURA, fontsize=9, fontweight="bold")
                
    # RÓTULO NÃO COMPENSÁVEL
    for bar in bar_nao_comp:
        height = bar.get_height() 
        ax.text(bar.get_x() + bar.get_width() / 2, height + (valor_medio_por_consumo * 0.02),
                f"R$ {format_br(nao_compensavel)}", ha="center", va="bottom",
                color=COLOR_NAO_COMP, fontsize=9, fontweight="bold")
                
    # RÓTULO 25%
    for bar in bar_25:
        height = bar.get_height() + assinatura + nao_compensavel
        ax.text(bar.get_x() + bar.get_width() / 2, height + (valor_medio_por_consumo * 0.02),
                f"R$ {format_br(vinte_cinco_porcento)}",
                ha="center", va="bottom", color=COLOR_25, fontsize=9, fontweight="bold")

    plt.tight_layout()
    chart_path = "chart_main.png"
    plt.savefig(chart_path, dpi=150, bbox_inches="tight")
    plt.close()

    # === CRIAÇÃO DO PDF ===
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, topMargin=36, bottomMargin=36)
    story = []
    styles = getSampleStyleSheet()
    truncate_style = ParagraphStyle(name="Truncate", fontSize=8, leading=10, wordWrap="CJK")

    # === CABEÇALHO COM FAIXA E LOGO ===
    logo_path = r"C:\Users\Matheus\Documents\MeusProgramasPy\data_partners_request\tempo-geracao-logo.png"
    titulo_style = ParagraphStyle(name="TituloCabecalho", fontSize=14,
                                 textColor=colors.white, leftIndent=10, alignment=0, leading=16)
    titulo = Paragraph("<b>Análise de Prospecção e Fechamentos</b>", titulo_style)
    logo = Image(logo_path, width=105, height=35)
    header_data = [[titulo, logo]]
    header_table = Table(header_data, colWidths=[400, 100], hAlign="LEFT")
    header_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#002644")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 12))

    # === INFORMAÇÕES DO PARCEIRO ===
    try:
        partes = finder_name.split(" - ")
        tipo_parceria = partes[1].strip() if len(partes) >= 3 else partes[-1].strip()
        parceiro = partes[2].strip() if len(partes) >= 3 else finder_name
    except Exception:
        tipo_parceria, parceiro = "N/A", finder_name

    data_atual = datetime.now().strftime("%d/%m/%Y")
    info_style = ParagraphStyle(name="Info", fontSize=10, leading=14, textColor=colors.HexColor("#1B2124"))
    story.append(Paragraph(f"<b>Parceiro:</b> {parceiro}", info_style))
    story.append(Paragraph(f"<b>Tipo de Parceria:</b> {tipo_parceria}", info_style))
    story.append(Paragraph(f"<b>Data:</b> {data_atual}", info_style))
    story.append(Spacer(1, 12))

    # === PÁGINA 1: GRÁFICOS ===
    story.append(Image(chart_path, width=400, height=220))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Valor Médio Estimado de Comissão - Simulação de Conversão de LEADS em Fechamentos", styles["Heading2"]))
    story.append(Spacer(1, 6))
    story.append(Image(distrib_chart_path, width=450, height=200))
    story.append(Spacer(1, 8))
    info_text_style = ParagraphStyle(name="InfoText", fontSize=9, textColor=colors.HexColor("#1B2124"),
                                     alignment=1, italic=True)
    info_text = Paragraph("Esta é uma estimativa de comissão, levando em consideração a média de consumo dos clientes em prospecção.", info_text_style)
    story.append(info_text)
    story.append(PageBreak())

    # === IDENTIFICA SE É MOTHER FILE ===
    is_mother = "mother_files" in pasta_saida.lower()

    # === TABELA EM PROSPECÇÃO (Formato BR já estava correto) ===
    if deals_prospeccao:
        story.append(Paragraph("Em Prospecção:", styles["Heading2"]))
        if is_mother:
            col_labels = ["Nome", "Data de Entrada", "Subcontratado", "Valor da Fatura (R$)"]
            col_widths = [150, 100, 150, 120]
        else:
            col_labels = ["Nome", "Data de Entrada", "Valor da Fatura (R$)"]
            col_widths = [200, 160, 120]

        cell_text = []
        for d in deals_prospeccao:
            nome = Paragraph(d["title"][:40], truncate_style)
            data_entrada = Paragraph(d.get("data_entrada", "-"), truncate_style)
            
            # --- LÓGICA DE FORMATO BR (MANTIDA) ---
            valor_formatado_eua = f'{d["value"]:,.2f}'
            valor_formatado_br = valor_formatado_eua.replace('.', '#').replace(',', '.').replace('#', ',')
            valor = Paragraph(f'R$ {valor_formatado_br}', truncate_style)
            # ---------------------------------------------

            if is_mother:
                finder_value = d.get('finder', 'N/A')
                subcontratado_txt = finder_value[:40] + ("..." if len(finder_value) > 40 else "")
                subcontratado_p = Paragraph(subcontratado_txt, truncate_style)
                cell_text.append([nome, data_entrada, subcontratado_p, valor])
            else:
                cell_text.append([nome, data_entrada, valor])

        table_prospec = Table([col_labels] + cell_text, colWidths=col_widths)
        table_prospec.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
            ("ALIGN", (-1, 1), (-1, -1), "RIGHT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        story.append(table_prospec)
        story.append(Spacer(1, 20))

    # === TABELA FECHADOS (Formato BR já estava correto) ===
    if deals_fechados:
        story.append(Paragraph("Fechados:", styles["Heading2"]))
        if is_mother:
            col_labels = ["Nome", "Data de Assinatura", "Subcontratado", "Plano Assinado", "Valor da Fatura (R$)"]
            col_widths = [130, 90, 130, 110, 140]
        else:
            col_labels = ["Nome", "Data de Assinatura", "Plano Assinado", "Valor da Fatura (R$)"]
            col_widths = [200, 120, 100, 140]

        cell_text = []
        for d in deals_fechados:
            nome = Paragraph(d["title"][:40], truncate_style)
            data_ass = Paragraph(d.get("data_assinatura", "-"), truncate_style)
            plano = Paragraph(d.get("plano_assinado", "-"), truncate_style)
            
            # --- LÓGICA DE FORMATO BR (MANTIDA) ---
            valor_formatado_eua = f'{d["value"]:,.2f}'
            valor_formatado_br = valor_formatado_eua.replace('.', '#').replace(',', '.').replace('#', ',')
            valor = Paragraph(f'R$ {valor_formatado_br}', truncate_style)
            # ---------------------------------------------

            if is_mother:
                finder_value = d.get('finder', 'N/A')
                subcontratado_txt = finder_value[:40] + ("..." if len(finder_value) > 40 else "")
                subcontratado_p = Paragraph(subcontratado_txt, truncate_style)
                cell_text.append([nome, data_ass, subcontratado_p, plano, valor])
            else:
                cell_text.append([nome, data_ass, plano, valor])

        table_fechados = Table([col_labels] + cell_text, colWidths=col_widths)
        table_fechados.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
            ("ALIGN", (-1, 1), (-1, -1), "RIGHT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        story.append(table_fechados)

    doc.build(story)
    print(f"✅ PDF gerado com sucesso: {pdf_path}")