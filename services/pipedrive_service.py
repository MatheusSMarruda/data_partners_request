import requests
from datetime import datetime
from .finder_utils import obter_mapeamentos_campos, process_finder_field
from config import PIPELINE_FECHADOS


def _parse_plano_label_to_decimal(label):
    """Converte labels como 'Plano 25%' ou '25%' em 0.25. Retorna 0.25 por padrão se não conseguir parsear."""
    try:
        if not label or label == "-":
            return 0.25
        s = str(label)
        # procura por número seguido de %, ex: 'Plano 25%'
        import re
        m = re.search(r"(\d+(?:[\.,]\d+)?)\s*%", s)
        if m:
            val = m.group(1).replace(',', '.')
            return float(val) / 100.0
        # tenta encontrar número isolado e assumir porcentagem
        m2 = re.search(r"(\d+(?:[\.,]\d+)?)", s)
        if m2:
            val = m2.group(1).replace(',', '.')
            # se valor > 1, assume percentual
            if float(val) > 1:
                return float(val) / 100.0
            return float(val)
    except Exception:
        pass
    return 0.25


def analyze_deals_in_pipeline(api_token, pipeline_id, filter_id, custom_field_keys, calcular_totais=True):
    base_url = "https://tempoenergia.pipedrive.com/v1"
    deals_by_finder = {}
    deals_details = {}
    start = 0
    limit = 100

    # === Mapeamentos ===
    mapeamentos = obter_mapeamentos_campos(api_token)
    finder_mapping = mapeamentos.get("finder", {})
    plano_mapping = mapeamentos.get("plano_assinado", {})

    # === Função auxiliar de formatação ===
    def formatar_data(data_str):
        """Converte qualquer formato de data válido em dd/mm/yyyy"""
        if not data_str or str(data_str).strip() in ["", "0000-00-00", "None"]:
            return ""
        try:
            data_str = str(data_str).strip()

            # Corta hora se houver (ex: "2025-07-24 20:48:49" → "2025-07-24")
            if " " in data_str:
                data_str = data_str.split(" ")[0]
            if "T" in data_str:
                data_str = data_str.split("T")[0]

            # Tenta converter no formato ISO
            data_obj = datetime.strptime(data_str, "%Y-%m-%d")
            return data_obj.strftime("%d/%m/%Y")
        except Exception:
            try:
                # fallback para dd/mm/yyyy
                data_obj = datetime.strptime(data_str[:10], "%d/%m/%Y")
                return data_obj.strftime("%d/%m/%Y")
            except Exception:
                return ""

    while True:
        url = f"{base_url}/deals?pipeline_id={pipeline_id}&filter_id={filter_id}&start={start}&limit={limit}&api_token={api_token}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            deals = data.get("data", [])
            if not deals:
                break

            for deal in deals:
                try:
                    # Ignora negócios perdidos
                    status = deal.get("status") or deal.get(custom_field_keys.get("status"))
                    if status and str(status).strip().lower() == "lost":
                        continue
                        
                    # === FIELDS ===
                    finder = deal.get(custom_field_keys["finder"])
                    if finder is None:
                        custom_fields = deal.get("custom_fields", {})
                        finder = custom_fields.get(custom_field_keys["finder"])

                    processed_finder = process_finder_field(finder, finder_mapping)
                    if not processed_finder:
                        continue

                    if processed_finder not in deals_details:
                        deals_details[processed_finder] = []
                    if calcular_totais and processed_finder not in deals_by_finder:
                        deals_by_finder[processed_finder] = {
                            "fatura_cheia": 0.0,
                            "assinatura": 0.0,
                            "nao_compensavel": 0.0,
                            "vinte_cinco_porcento": 0.0,
                            "assinatura_fechados": 0.0
                        }

                    nome = deal.get("title", "Sem Nome")
                    valor = float(deal.get("value") or 0.0)

                    # === DATA DE ENTRADA (ajuste completo) ===
                    data_alteracao_funil = (
                        deal.get(custom_field_keys["Data de Alteração de Funil"])
                        or deal.get("custom_fields", {}).get(custom_field_keys["Data de Alteração de Funil"])
                    )

                    negocio_criado_em = (
                        deal.get("add_time")
                        or deal.get(custom_field_keys["Negócio Criado em"])
                        or deal.get("custom_fields", {}).get(custom_field_keys["Negócio Criado em"])
                    )

                    # Prioriza Data de Alteração de Funil; fallback -> Negócio Criado em
                    data_entrada = formatar_data(data_alteracao_funil)
                    if not data_entrada:
                        data_entrada = formatar_data(negocio_criado_em)

                    # === PLANO ASSINADO ===
                    plano_assinado = (
                        deal.get(custom_field_keys["Plano Assinado"])
                        or deal.get("custom_fields", {}).get(custom_field_keys["Plano Assinado"])
                    )
                    plano_assinado_label = plano_mapping.get(str(plano_assinado), "-")

                    # === DATA DE ASSINATURA ===
                    data_assinatura = (
                        deal.get(custom_field_keys.get("Data de Assinatura"))
                        or deal.get("custom_fields", {}).get(custom_field_keys.get("Data de Assinatura"))
                    )
                    data_assinatura_formatada = formatar_data(data_assinatura)

                    # === Nome Finder formatado ===
                    finder_formatado = processed_finder
                    if finder_formatado and " - " in finder_formatado:
                        partes = finder_formatado.split(" - ", 2)
                        if len(partes) == 3:
                            finder_formatado = partes[2]

                    # === REGISTRO FINAL ===
                    deals_details[processed_finder].append({
                        "title": nome,
                        "finder": finder_formatado,
                        "value": valor,
                        "data_entrada": data_entrada,
                        "plano_assinado": plano_assinado_label,
                        "data_assinatura": data_assinatura_formatada,
                    })

                    # === CÁLCULOS DE TOTAIS ===
                    if calcular_totais:
                        consumo = deal.get(custom_field_keys["consumo"])
                        if consumo is None:
                            custom_fields = deal.get("custom_fields", {})
                            consumo = custom_fields.get(custom_field_keys["consumo"])
                        if consumo is not None and str(consumo).strip():
                            consumo = float(consumo)
                            deals_by_finder[processed_finder]["fatura_cheia"] += consumo * 1.1150643

                        kwh_contratado = deal.get(custom_field_keys["kwh_contratado"])
                        if kwh_contratado is None:
                            custom_fields = deal.get("custom_fields", {})
                            kwh_contratado = custom_fields.get(custom_field_keys["kwh_contratado"])
                        if kwh_contratado is not None and str(kwh_contratado).strip():
                            kwh_contratado = float(kwh_contratado)
                            total_contratado = kwh_contratado * 1.1150643
                            # Se for pipeline de fechados, usar o Plano Assinado para calcular o percentual
                            if pipeline_id == PIPELINE_FECHADOS:
                                plano_decimal = _parse_plano_label_to_decimal(plano_assinado_label)
                                assinatura_valor = total_contratado * (1 - plano_decimal)
                                # acumula em campo específico para fechados
                                deals_by_finder[processed_finder].setdefault("assinatura_fechados", 0.0)
                                deals_by_finder[processed_finder]["assinatura_fechados"] += assinatura_valor
                                # Guarda valor de assinatura por negócio para uso em relatórios
                                try:
                                    if processed_finder in deals_details and deals_details[processed_finder]:
                                        deals_details[processed_finder][-1]['assinatura'] = assinatura_valor
                                except Exception:
                                    pass
                            else:
                                assinatura_valor = total_contratado * (1 - 0.25)
                                vinte_cinco_valor = total_contratado - assinatura_valor
                                deals_by_finder[processed_finder]["assinatura"] += assinatura_valor
                                deals_by_finder[processed_finder]["vinte_cinco_porcento"] += vinte_cinco_valor
                                # Guarda valor de assinatura por negócio para uso em relatórios
                                try:
                                    if processed_finder in deals_details and deals_details[processed_finder]:
                                        deals_details[processed_finder][-1]['assinatura'] = assinatura_valor
                                except Exception:
                                    pass

                        kwh_nao_comp = deal.get(custom_field_keys["kwh_nao_compensavel"])
                        if kwh_nao_comp is None:
                            custom_fields = deal.get("custom_fields", {})
                            kwh_nao_comp = custom_fields.get(custom_field_keys["kwh_nao_compensavel"])
                        if kwh_nao_comp is not None and str(kwh_nao_comp).strip():
                            deals_by_finder[processed_finder]["nao_compensavel"] += float(kwh_nao_comp) * 1.1150643

                except (ValueError, TypeError):
                    pass

            start += limit

        except requests.exceptions.RequestException as e:
            print(f"⚠️ Erro ao acessar a API: {e}")
            return None, None

    return deals_by_finder, deals_details
