import requests

def obter_mapeamentos_campos(api_token):
    """
    Retorna um dicionário com mapeamentos de opções de campos tipo 'opção única' do Pipedrive:
    - Finder (Origem da Fatura)
    - Plano Assinado
    """
    base_url = "https://tempoenergia.pipedrive.com/v1"
    url = f"{base_url}/dealFields"
    params = {"api_token": api_token}

    mapeamentos = {}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json().get("data", [])

        for field in data:
            key = field.get("key")
            options = field.get("options", [])

            # Finder (Origem da Fatura)
            if key == "93df664878ce08f58067f382e1c134bed803ce53":
                mapeamentos["finder"] = {str(opt["id"]): opt["label"] for opt in options}

            # Plano Assinado
            elif key == "fae8184ad9ee4befb23365ad84e47c76e03c6f71":
                mapeamentos["plano_assinado"] = {str(opt["id"]): opt["label"] for opt in options}

    except requests.exceptions.RequestException as e:
        print(f"⚠️ Erro ao obter mapeamentos de campos: {e}")

    return mapeamentos


def process_finder_field(finder_value, finder_mapping):
    """Processa o campo 'Finder (Origem da Fatura)' para desconsiderar valores com 'interno'."""
    if not finder_value:
        return None

    if isinstance(finder_value, list):
        resolved_parts = [finder_mapping.get(str(part), str(part)) for part in finder_value]
    else:
        parts = [part.strip() for part in str(finder_value).split(",")]
        resolved_parts = [finder_mapping.get(part, part) for part in parts]

    filtered_parts = [part for part in resolved_parts if "interno" not in part.lower()]
    return ", ".join(filtered_parts) if filtered_parts else None
