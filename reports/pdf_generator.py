import os
import matplotlib.pyplot as plt
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import re
# CORREÇÃO DE IMPORTAÇÃO: Removendo o acento de 'distribuição' para evitar o ImportError
from charts.chart_distribuicao_parceiro import gerar_distribuicao_parceiro


def calcular_comissao_deal(finder_name, deal):
    finder_lower = (finder_name or "").lower()
    deal_assinatura = float(deal.get('assinatura', 0) or 0)
    plano_label = str(deal.get('plano_assinado', '')).lower()
    m = re.search(r"(\d+(?:[\.,]\d+)?)", plano_label)
    perc = float(m.group(1).replace(',', '.')) if m else None
    comissao = 0.0
    if "gold" in finder_lower:
        if perc == 15.0:
            comissao = deal_assinatura * 0.30
        elif perc == 20.0:
            comissao = deal_assinatura * 1.00
        elif perc == 25.0:
            comissao = deal_assinatura * 1.00
        else:
            comissao = deal_assinatura * 1.00
    elif "plus" in finder_lower:
        if perc == 15.0:
            comissao = deal_assinatura * 0.25
        elif perc == 20.0:
            comissao = deal_assinatura * 0.85
        elif perc == 25.0:
            comissao = deal_assinatura * 0.85
        else:
            comissao = deal_assinatura * 0.85
    elif "indique" in finder_lower:
        if perc == 15.0:
            comissao = deal_assinatura * 0.15
        elif perc == 20.0:
            comissao = deal_assinatura * 0.50
        elif perc == 25.0:
            comissao = deal_assinatura * 0.50
        else:
            comissao = deal_assinatura * 0.50
    elif "parceiro exsat" in finder_lower:
        if perc == 15.0:
            comissao = deal_assinatura * 0.16
        elif perc == 20.0:
            comissao = deal_assinatura * 0.51
        elif perc == 25.0:
            comissao = deal_assinatura * 0.51
        else:
            comissao = deal_assinatura * 0.51
    elif "exsat" in finder_lower:
        if perc == 15.0:
            comissao = deal_assinatura * 0.32
        elif perc == 20.0:
            comissao = deal_assinatura * 1.02
        elif perc == 25.0:
            comissao = deal_assinatura * 1.02
        else:
            comissao = deal_assinatura * 1.02
    elif "provedor" in finder_lower:
        if perc == 15.0:
            comissao = deal_assinatura * 0.025
        elif perc == 20.0:
            comissao = deal_assinatura * 0.030
        elif perc == 25.0:
            comissao = deal_assinatura * 0.035
        elif perc == 28.0:
            comissao = deal_assinatura * 0.035
        elif perc == 30.0:
            comissao = deal_assinatura * 0.035
        else:
            # Para plano "Outro", buscar 'Beneficio Estimado'
            if plano_label == "Outro":
                beneficio_estimado = deal.get('Beneficio Estimado')
                if beneficio_estimado:
                    try:
                        perc_beneficio = float(str(beneficio_estimado).replace(',', '.')) / 100
                        comissao = deal_assinatura * perc_beneficio
                    except ValueError:
                        comissao = 0.0
                else:
                    comissao = 0.0
            else:
                comissao = deal_assinatura * 0.035  # default
    return comissao


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
    finder_id,
    pasta_saida
):
    # === DADOS BÁSICOS ===
    sanitized_name = finder_name.replace(" ", "_").replace("/", "_")
    pdf_path = os.path.join(pasta_saida, f"{sanitized_name}.pdf")
    
    # assinatura_display é usado apenas para exibição na tabela de dados
    # Para o gráfico, usamos o assinatura original (0 se não houver em PROSPECCAO)
    try:
        assinatura_display = float(assinatura) if assinatura and float(assinatura) > 0 else sum(float(d.get('assinatura', 0) or 0) for d in (deals_fechados or []))
    except Exception:
        assinatura_display = assinatura

    # Para passar ao gráfico, usa o valor original de assinatura (sem fallback para deals_fechados)
    assinatura_para_grafico = float(assinatura) if assinatura and float(assinatura) > 0 else 0

    distrib_chart_path = gerar_distribuicao_parceiro(finder_name, assinatura_para_grafico, assinatura_fechados, deals_fechados)

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
    bar_assin = ax.bar(x_pos[2], assinatura_display, bottom=nao_compensavel, color=COLOR_ASSINATURA, width=largura)
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
    # Salva sem bbox_inches="tight" para evitar cálculo errado de dimensões com rótulos
    plt.savefig(chart_path, dpi=150, pad_inches=0.3)
    plt.close()

    # === CRIAÇÃO DO PDF ===
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, topMargin=36, bottomMargin=36)
    story = []
    styles = getSampleStyleSheet()
    truncate_style = ParagraphStyle(name="Truncate", fontSize=6, leading=8, wordWrap="CJK")
    header_style = ParagraphStyle(name="Header", fontSize=6, leading=8, textColor=colors.whitesmoke)

    # === INFORMAÇÕES DO PARCEIRO (Precisa ser antes do título) ===
    try:
        partes = finder_name.split(" - ")
        tipo_parceria = partes[1].strip() if len(partes) >= 3 else partes[-1].strip()
        parceiro = partes[2].strip() if len(partes) >= 3 else finder_name
    except Exception:
        tipo_parceria, parceiro = "N/A", finder_name

    # === CABEÇALHO COM FAIXA E LOGO ===
    logo_path = r"C:\Users\Matheus\Documents\MeusProgramasPy\data_partners_request\tempo-geracao-logo.png"
    titulo_style = ParagraphStyle(name="TituloCabecalho", fontSize=14,
                                 textColor=colors.white, leftIndent=10, alignment=0, leading=16)
    titulo = Paragraph(f"<b>Relatório de Estimativa de Retribuição - {parceiro}</b>", titulo_style)
    logo = Image(logo_path, width=105, height=35)
    header_data = [[titulo, logo]]
    header_table = Table(header_data, colWidths=[374, 94], hAlign="LEFT")
    header_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#002644")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 20))

    # === SEÇÃO 1: INTRODUÇÃO ===
    intro_heading = ParagraphStyle(name="IntroHeading", fontSize=11, fontName="Helvetica-Bold", 
                                   textColor=colors.HexColor("#002644"), leading=14)
    intro_text = ParagraphStyle(name="IntroText", fontSize=10, leading=14, 
                               textColor=colors.HexColor("#1B2124"), alignment=4)
    
    story.append(Paragraph("<b>1. INTRODUÇÃO</b>", intro_heading))
    story.append(Spacer(1, 6))
    story.append(Paragraph(f"Este relatório apresenta o acompanhamento das métricas referentes a <b>{parceiro}</b>, no que se refere a prospecções e fechamentos.", intro_text))
    story.append(Spacer(1, 20))

    # === SEÇÃO 2: DADOS GERAIS ===
    story.append(Paragraph("<b>2. DADOS GERAIS</b>", intro_heading))
    story.append(Spacer(1, 6))
    
    # Usa o finder_id passado como parâmetro, que é o ID original no Pipedrive
    codigo_finder = finder_id if finder_id and finder_id != "N/A" else "N/A"
    
    # Formata a data por extenso
    data_atual_extenso = datetime.now().strftime("%d de %B de %Y")
    meses_pt = {
        "January": "janeiro", "February": "fevereiro", "March": "março", "April": "abril",
        "May": "maio", "June": "junho", "July": "julho", "August": "agosto",
        "September": "setembro", "October": "outubro", "November": "novembro", "December": "dezembro"
    }
    for mes_en, mes_pt in meses_pt.items():
        data_atual_extenso = data_atual_extenso.replace(mes_en, mes_pt)
    
    dados_gerais_style = ParagraphStyle(name="DadosGerais", fontSize=10, leading=16, 
                                       textColor=colors.HexColor("#1B2124"))
    
    story.append(Paragraph(f"<b>•&nbsp;&nbsp;NOME:</b> {parceiro}", dados_gerais_style))
    story.append(Paragraph(f"<b>•&nbsp;&nbsp;CÓDIGO DO PARCEIRO:</b> {codigo_finder}", dados_gerais_style))
    story.append(Paragraph(f"<b>•&nbsp;&nbsp;MODALIDADE DE PARCERIA:</b> {tipo_parceria}", dados_gerais_style))
    story.append(Paragraph(f"<b>•&nbsp;&nbsp;DATA DA ANÁLISE:</b> {data_atual_extenso}", dados_gerais_style))
    story.append(Spacer(1, 20))

    # === SEÇÃO 3: METRICAS DE FECHAMENTO === #
    story.append(Paragraph("<b>3. MÉTRICAS DE FECHAMENTO</b>", intro_heading))
    story.append(Spacer(1, 6))
    story.append(Paragraph(f"Referente as métricas presentes em nossa base, segue a relação de fechamentos realizados pelo parceiro  {parceiro}:"))
    story.append(Spacer(1, 6))
    story.append(Paragraph("A relação de consorciados, com suas respectivas datas de assinatura, subcontratados (se houver), valores de fatura e estimativas de retribuição encontra-se descrita abaixo:"))

    # === IDENTIFICA SE É MOTHER FILE ===
    is_mother = "mother_files" in pasta_saida.lower()

    # === TABELA FECHADOS (Formato BR já estava correto) ===
    if deals_fechados:
        story.append(Paragraph("Fechados:", styles["Heading2"]))
        if is_mother:
            col_labels = ["Nome", "Data de Assinatura", "Subcontratado", "Plano Assinado", "Estimativa da 1° Retribuição", "Valor da Fatura (R$)"]
            col_widths = [76, 65, 84, 68, 99, 76]
        else:
            col_labels = ["Nome", "Data de Assinatura", "Plano Assinado", "Estimativa da 1° Retribuição", "Valor da Fatura (R$)"]
            col_widths = [129, 81, 73, 105, 81]
        col_labels = [Paragraph(label, header_style) for label in col_labels]

        cell_text = []
        for d in deals_fechados:
            nome = Paragraph(d["title"][:40], truncate_style)
            data_ass = Paragraph(d.get("data_assinatura", "-"), truncate_style)
            plano = Paragraph(d.get("plano_assinado", "-"), truncate_style)
            
            # Calcula comissão (estimativa de retribuição com descontos por plano)
            comissao_value = calcular_comissao_deal(finder_name, d)
            try:
                comissao_formatado_eua = f'{comissao_value:,.2f}'
                comissao_formatado = f'R$ {comissao_formatado_eua.replace(".", "#").replace(",", ".").replace("#", ",")}'
            except:
                comissao_formatado = "-"
            comissao_p = Paragraph(comissao_formatado, truncate_style)
            
            # --- LÓGICA DE FORMATO BR (MANTIDA) ---
            valor_formatado_eua = f'{d["value"]:,.2f}'
            valor_formatado_br = valor_formatado_eua.replace('.', '#').replace(',', '.').replace('#', ',')
            valor = Paragraph(f'R$ {valor_formatado_br}', truncate_style)
            # ---------------------------------------------

            if is_mother:
                finder_value = d.get('finder', 'N/A')
                subcontratado_txt = finder_value[:40] + ("..." if len(finder_value) > 40 else "")
                subcontratado_p = Paragraph(subcontratado_txt, truncate_style)
                cell_text.append([nome, data_ass, subcontratado_p, plano, comissao_p, valor])
            else:
                cell_text.append([nome, data_ass, plano, comissao_p, valor])

        # Calcula o total
        total_fechados = sum(float(d["value"]) for d in deals_fechados)
        valor_total_formatado_eua = f'{total_fechados:,.2f}'
        valor_total_formatado_br = valor_total_formatado_eua.replace('.', '#').replace(',', '.').replace('#', ',')
        
        # Calcula o total de comissão
        total_comissao = sum(calcular_comissao_deal(finder_name, d) for d in deals_fechados)
        total_comissao_formatado_eua = f'{total_comissao:,.2f}'
        total_comissao_formatado_br = f'R$ {total_comissao_formatado_eua.replace(".", "#").replace(",", ".").replace("#", ",")}'
        
        # Cria a linha de total
        if is_mother:
            total_row = [
                Paragraph("<b>TOTAL</b>", truncate_style),
                Paragraph("", truncate_style),
                Paragraph("", truncate_style),
                Paragraph("", truncate_style),
                Paragraph(f"<b>{total_comissao_formatado_br}</b>", truncate_style),
                Paragraph(f"<b>R$ {valor_total_formatado_br}</b>", truncate_style)
            ]
        else:
            total_row = [
                Paragraph("<b>TOTAL</b>", truncate_style),
                Paragraph("", truncate_style),
                Paragraph("", truncate_style),
                Paragraph(f"<b>{total_comissao_formatado_br}</b>", truncate_style),
                Paragraph(f"<b>R$ {valor_total_formatado_br}</b>", truncate_style)
            ]
        
        # Monta os dados da tabela com a linha de total
        table_data = [col_labels] + cell_text + [total_row]
        num_rows = len(table_data)
        
        # Cria a tabela com todos os dados
        table_fechados = Table(table_data, colWidths=col_widths)
        table_fechados.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
            ("ALIGN", (-1, 1), (-1, -1), "RIGHT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            # Estilo para a última linha (total)
            ("BACKGROUND", (0, num_rows-1), (-1, num_rows-1), colors.HexColor("#E0E0E0")),
            ("FONTNAME", (0, num_rows-1), (-1, num_rows-1), "Helvetica-Bold"),
        ]))
        
        story.append(table_fechados)
    
    story.append(Spacer(1, 20))

    # === SEÇÃO 4: METRICAS DE PROSPECÇÃO === #
    story.append(Paragraph("<b>4. MÉTRICAS DE PROSPECÇÃO</b>", intro_heading))
    story.append(Spacer(1, 6))
    story.append(Paragraph(f"Referente as métricas presentes em nossa base, segue a relação de prospecções que ainda não foram convertidas em fechamentos, realizadas pelo parceiro: {parceiro}:"))
    story.append(Spacer(1, 6))
    story.append(Paragraph("A relação de leads, com suas respectivas datas de entradas, encontram-se descritas abaixo:"))

    # === TABELA EM PROSPECÇÃO (Formato BR já estava correto) ===
    if deals_prospeccao:
        story.append(Paragraph("Em Prospecção:", styles["Heading2"]))
        if is_mother:
            col_labels = ["Nome", "Data de Entrada", "Subcontratado", "Valor da Fatura (R$)"]
            col_widths = [135, 90, 135, 108]
        else:
            col_labels = ["Nome", "Data de Entrada", "Valor da Fatura (R$)"]
            col_widths = [195, 156, 117]
        col_labels = [Paragraph(label, header_style) for label in col_labels]

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

        # Calcula o total
        total_prospeccao = sum(float(d["value"]) for d in deals_prospeccao)
        valor_total_formatado_eua = f'{total_prospeccao:,.2f}'
        valor_total_formatado_br = valor_total_formatado_eua.replace('.', '#').replace(',', '.').replace('#', ',')
        
        # Cria a linha de total
        if is_mother:
            total_row = [
                Paragraph("<b>TOTAL</b>", truncate_style),
                Paragraph("", truncate_style),
                Paragraph("", truncate_style),
                Paragraph(f"<b>R$ {valor_total_formatado_br}</b>", truncate_style)
            ]
        else:
            total_row = [
                Paragraph("<b>TOTAL</b>", truncate_style),
                Paragraph("", truncate_style),
                Paragraph(f"<b>R$ {valor_total_formatado_br}</b>", truncate_style)
            ]
        
        # Monta os dados da tabela com a linha de total
        table_data = [col_labels] + cell_text + [total_row]
        num_rows = len(table_data)
        
        # Cria a tabela com todos os dados
        table_prospec = Table(table_data, colWidths=col_widths)
        table_prospec.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
            ("ALIGN", (-1, 1), (-1, -1), "RIGHT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            # Estilo para a última linha (total)
            ("BACKGROUND", (0, num_rows-1), (-1, num_rows-1), colors.HexColor("#E0E0E0")),
            ("FONTNAME", (0, num_rows-1), (-1, num_rows-1), "Helvetica-Bold"),
        ]))
        
        story.append(table_prospec)
        story.append(Spacer(1, 20))

    # === SEÇÃO 5: AVALIAÇÃO DE ESTIMATIVA DE RETRIBUIÇÃO === #
    story.append(Paragraph("<b>5. Avaliação de Estimativa de Retribuição - Consorciados e Leads em Prospecção</b>", intro_heading))
    story.append(Spacer(1, 12))
    
    # Define percentual máximo de benefício e fidelidade máxima por parceiro
    if "GF CAPITAL" in parceiro.upper() and "ANDERSON" in parceiro.upper():
        percentual_beneficio = "22%"
        fidelidade_maxima = "3 anos"
    elif "LINKNET" in parceiro.upper():
        percentual_beneficio = "18%"
        fidelidade_maxima = "1 ano"
    else:
        percentual_beneficio = "25%"
        fidelidade_maxima = "3 anos"  # Valor padrão caso não seja especificado
    
    story.append(Paragraph(f"Com o objetivo de apresentar uma estimativa de retribuição referente aos leads atualmente em prospecção, foi considerada, para fins de simulação, a média de consumo declarada durante o processo de prospecção e a adoção do plano de benefício de {percentual_beneficio} com fidelidade de {fidelidade_maxima}.", intro_text))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Dessa forma, ao consolidar os potenciais leads, obtém-se a visão geral apresentada na abaixo, que demonstra o comparativo dos somatórios dos valores médios com e sem o benefício TG, destacando a economia percebida e o valor médio de assinatura.", intro_text))

    # === Gráfico 1 Estimativas para Fechamento ===#
    story.append(Paragraph("Valor Médio Estimado de Comissão - Simulação de Conversão de LEADS em Fechamentos", styles["Heading2"]))
    story.append(Spacer(1, 6))
    story.append(Image(chart_path, width=400, height=220))
    story.append(Spacer(1, 10))

    story.append(Paragraph("A estimativa de retribuição é calculada com base no valor líquido pago pelo cliente, correspondente ao valor da assinatura. A seguir, apresentamos a projeção elaborada considerando a hipótese de conversão integral dos leads prospectados, oferecendo uma visão do potencial estimado de retribuição e também dos consorciados que realizaram a adesão.", intro_text))
    story.append(Spacer(1, 16))
    story.append(Paragraph("Importante:Trata-se de uma estimativa, sujeita a variações conforme a taxa real de conversão, plano escolhido, consumo compensado e outros fatores operacionais.", intro_heading))

    #=== Gráfico 2 de distribuição de parceiros ===#
    story.append(Image(distrib_chart_path, width=450, height=200))
    story.append(Spacer(1, 8))
    info_text_style = ParagraphStyle(name="InfoText", fontSize=9, textColor=colors.HexColor("#1B2124"),alignment=1, italic=True)
    info_text = Paragraph("Esta é uma estimativa de retribuição, levando em consideração a média de consumo dos clientes em prospecção.", info_text_style)

    doc.build(story)
    print(f"PDF gerado com sucesso: {pdf_path}")