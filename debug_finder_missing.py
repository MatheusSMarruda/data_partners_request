"""
Script de debug para investigar por que o finder "03 - Plus - MONTTEREY (Bruno Ribeiro)"
não aparece nos relatórios.

Hipótese: Ele existe apenas no PIPELINE_FECHADOS, não no PIPELINE_PROSPECCAO.
O main.py itera apenas sobre os finders de PIPELINE_PROSPECCAO, ignorando finders que
só existem em PIPELINE_FECHADOS.
"""

from services.pipedrive_service import analyze_deals_in_pipeline
from config import API_TOKEN, PIPELINE_PROSPECCAO, FILTER_PROSPECCAO, PIPELINE_FECHADOS, FILTER_FECHADOS, CUSTOM_FIELD_KEYS

def debug_finder_coverage():
    print("=" * 80)
    print("DEBUG: Investigando cobertura de Finders nos dois pipelines")
    print("=" * 80)

    # Extrai deals do PIPELINE_PROSPECCAO
    print("\n[1] Extraindo deals do PIPELINE_PROSPECCAO (36)...")
    deals_by_finder_prosp, deals_prospeccao = analyze_deals_in_pipeline(
        API_TOKEN, PIPELINE_PROSPECCAO, FILTER_PROSPECCAO, CUSTOM_FIELD_KEYS, calcular_totais=True
    )
    
    finders_prospeccao = set(deals_by_finder_prosp.keys()) if deals_by_finder_prosp else set()
    print(f"    Total de finders em PROSPECCAO: {len(finders_prospeccao)}")
    print(f"    Finders encontrados:")
    for finder in sorted(finders_prospeccao):
        print(f"      - {finder}")

    # Extrai deals do PIPELINE_FECHADOS
    print("\n[2] Extraindo deals do PIPELINE_FECHADOS (37)...")
    deals_by_finder_fechados, deals_fechados = analyze_deals_in_pipeline(
        API_TOKEN, PIPELINE_FECHADOS, FILTER_FECHADOS, CUSTOM_FIELD_KEYS, calcular_totais=True
    )
    
    finders_fechados = set(deals_by_finder_fechados.keys()) if deals_by_finder_fechados else set()
    print(f"    Total de finders em FECHADOS: {len(finders_fechados)}")
    print(f"    Finders encontrados:")
    for finder in sorted(finders_fechados):
        print(f"      - {finder}")

    # Compara finders
    print("\n[3] Análise comparativa:")
    print("-" * 80)
    
    apenas_prospeccao = finders_prospeccao - finders_fechados
    apenas_fechados = finders_fechados - finders_prospeccao
    em_ambos = finders_prospeccao & finders_fechados
    
    print(f"\n    Finders APENAS em PROSPECCAO ({len(apenas_prospeccao)}):")
    for finder in sorted(apenas_prospeccao):
        print(f"      - {finder}")
    
    print(f"\n    Finders APENAS em FECHADOS ({len(apenas_fechados)}):")
    for finder in sorted(apenas_fechados):
        print(f"      - {finder}")
    
    print(f"\n    Finders em AMBOS os pipelines ({len(em_ambos)}):")
    for finder in sorted(em_ambos):
        print(f"      - {finder}")
    
    # Procura especificamente por "MONTTEREY"
    print("\n[4] Procurando por 'MONTTEREY (Bruno Ribeiro)':")
    print("-" * 80)
    
    target = "MONTTEREY (Bruno Ribeiro)"
    found = False
    
    for finder in finders_prospeccao:
        if target in finder:
            print(f"    ✓ Encontrado em PROSPECCAO: {finder}")
            found = True
    
    for finder in finders_fechados:
        if target in finder:
            print(f"    ✓ Encontrado em FECHADOS: {finder}")
            found = True
    
    if not found:
        print(f"    ✗ NÃO ENCONTRADO em nenhum pipeline")
    
    # Verifica o problema de geração de PDFs
    print("\n[5] Problema no main.py:")
    print("-" * 80)
    print("""
    LINHA 24-31 do main.py (loop de geração de PDFs):
    
        for finder_name, totals in deals_by_finder.items():
            assinatura_fechados_val = deals_by_finder_fechados.get(finder_name, {}).get(...)
            generate_pdf(
                finder_name,
                ...
                deals_fechados.get(finder_name, []),  # <-- AQUI!
            )
    
    O problema: O loop itera APENAS sobre finders de 'deals_by_finder' (PROSPECCAO).
    Se um finder existe APENAS em FECHADOS, ele nunca será processado.
    
    Finders que SERÃO ignorados na geração de PDFs:
    """)
    
    for finder in sorted(apenas_fechados):
        print(f"      - {finder}")
    
    print(f"\n    Total de PDFs gerados: {len(deals_by_finder_prosp)} (apenas de PROSPECCAO)")
    print(f"    Total de finders únicos (PROSPECCAO + FECHADOS): {len(em_ambos | apenas_prospeccao | apenas_fechados)}")
    print(f"    Finders perdidos: {len(apenas_fechados)}")

if __name__ == "__main__":
    debug_finder_coverage()
