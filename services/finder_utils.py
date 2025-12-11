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

    #Fazemos a extração do finder se obtiver "Interno" em tipos de finder
def process_finder_field(finder_value, finder_mapping, return_meta=False):
    """
    Processa o campo 'Finder (Origem da Fatura)'.

    - Remove partes com 'interno' para formar o finder_clean.
    - Detecta se havia 'interno' antes de remover (has_interno).
    - Rastreia o ID original antes da resolução do mapeamento (finder_id).

    Se return_meta=True retorna:
        (finder_clean, has_interno, finder_resolved_raw, finder_id)
    Caso contrário, retorna apenas finder_clean (como hoje).
    """
    if not finder_value:
        return (None, False, None, None) if return_meta else None

    # Preserva o ID original antes da resolução
    if isinstance(finder_value, list):
        finder_ids = [str(part) for part in finder_value]
    else:
        finder_ids = [str(part).strip() for part in str(finder_value).split(",")]
    
    # Usa o primeiro ID como identificador principal
    finder_id = finder_ids[0] if finder_ids else None

    # Resolve ids -> labels
    if isinstance(finder_value, list):
        resolved_parts = [finder_mapping.get(str(part), str(part)) for part in finder_value]
    else:
        parts = [part.strip() for part in str(finder_value).split(",")]
        resolved_parts = [finder_mapping.get(part, part) for part in parts]

    # flag de interno olhando as partes resolvidas
    has_interno = any("interno" in str(part).lower() for part in resolved_parts)

    # remove internos do texto final
    filtered_parts = [part for part in resolved_parts if "interno" not in str(part).lower()]
    finder_clean = ", ".join(filtered_parts) if filtered_parts else None

    if return_meta:
        finder_resolved_raw = ", ".join(resolved_parts) if resolved_parts else None
        return finder_clean, has_interno, finder_resolved_raw, finder_id

    return finder_clean

