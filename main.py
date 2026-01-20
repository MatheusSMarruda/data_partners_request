import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend

from services.pipedrive_service import analyze_deals_in_pipeline
from reports.pdf_generator import generate_pdf
from config import API_TOKEN, PIPELINE_PROSPECCAO, FILTER_PROSPECCAO, PIPELINE_FECHADOS, FILTER_FECHADOS, CUSTOM_FIELD_KEYS
from collections import defaultdict
import os

def main():
    deals_by_finder, deals_prospeccao = analyze_deals_in_pipeline(
        API_TOKEN, PIPELINE_PROSPECCAO, FILTER_PROSPECCAO, CUSTOM_FIELD_KEYS, calcular_totais=True
    )
    deals_by_finder_fechados, deals_fechados = analyze_deals_in_pipeline(
        API_TOKEN, PIPELINE_FECHADOS, FILTER_FECHADOS, CUSTOM_FIELD_KEYS, calcular_totais=True
    )

    if not deals_by_finder:
        print("Nenhum negócio encontrado.")
        return

    os.makedirs(r'C:\Users\Matheus\Documents\MeusProgramasPy\data_partners_request\child_files', exist_ok=True)
    os.makedirs(r'C:\Users\Matheus\Documents\MeusProgramasPy\data_partners_request\mother_files', exist_ok=True)

    # --- PDFs por Finder (child_files) ---
    # Itera sobre a UNIÃO de finders de ambos os pipelines (PROSPECCAO + FECHADOS)
    # Assim garante que finders que existem APENAS em FECHADOS também geram PDFs
    all_finders = set(deals_by_finder.keys()) | set(deals_by_finder_fechados.keys())

    for finder_name in sorted(all_finders):
        totals = deals_by_finder.get(finder_name, {
            "fatura_cheia": 0.0,
            "assinatura": 0.0,
            "nao_compensavel": 0.0,
            "vinte_cinco_porcento": 0.0,
            "finder_id": "N/A"
        })
        assinatura_fechados_val = deals_by_finder_fechados.get(finder_name, {}).get("assinatura_fechados", 0.0)
        
        # Tenta obter finder_id de PROSPECCAO, senão tenta de FECHADOS
        finder_id = totals.get("finder_id", "N/A")
        if finder_id == "N/A":
            finder_id = deals_by_finder_fechados.get(finder_name, {}).get("finder_id", "N/A")
        
        generate_pdf(
            finder_name,
            totals["fatura_cheia"],
            totals["assinatura"],
            totals["nao_compensavel"],
            totals["vinte_cinco_porcento"],
            deals_prospeccao.get(finder_name, []),
            deals_fechados.get(finder_name, []),
            assinatura_fechados_val,
            finder_id,
            pasta_saida=r'C:\Users\Matheus\Documents\MeusProgramasPy\data_partners_request\child_files'
        )

    # --- Agregação por Categoria (mother_files) ---
    categoria_totais = defaultdict(lambda: {
        "fatura_cheia": 0,
        "assinatura": 0,
        "nao_compensavel": 0,
        "vinte_cinco_porcento": 0
    })
    categoria_prospeccao = defaultdict(list)
    categoria_fechados = defaultdict(list)

    for finder_name, totals in deals_by_finder.items():
        partes = finder_name.split(" - ")
        categoria = partes[1].strip() if len(partes) >= 2 else finder_name

        for k in categoria_totais[categoria]:
            categoria_totais[categoria][k] += totals[k]

        categoria_prospeccao[categoria].extend(deals_prospeccao.get(finder_name, []))
        categoria_fechados[categoria].extend(deals_fechados.get(finder_name, []))

    for categoria, totals in categoria_totais.items():
        assinatura_fechados_val = deals_by_finder_fechados.get(categoria, {}).get("assinatura_fechados", 0.0)
        generate_pdf(
            categoria,
            totals["fatura_cheia"],
            totals["assinatura"],
            totals["nao_compensavel"],
            totals["vinte_cinco_porcento"],
            categoria_prospeccao[categoria],
            categoria_fechados[categoria],
            assinatura_fechados_val,
            "N/A",
            pasta_saida=r'C:\Users\Matheus\Documents\MeusProgramasPy\data_partners_request\mother_files'
        )

if __name__ == "__main__":
    main()