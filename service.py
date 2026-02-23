from message import Message
import requests
import base64

# API_KEY deve ser inserida pelo usuário
api_key = 'INSIRA_A_API_KEY'

def TRUNCATE_HISTORY(history, limit):
    return history[-limit:] if len(history) > limit else history

def CALL_LLM_API(config, payload):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{config.model_name}:generateContent?key={api_key}"
    
    contents = []
    for msg in payload:
        role = "model" if msg["role"] == "assistant" else "user"
        parts = []
        
        # Lógica para detectar conteúdo multimodal
        if isinstance(msg["content"], list):
            for item in msg["content"]:
                if item["type"] == "text":
                    parts.append({"text": item["text"]})
                elif item["type"] == "image_url":
                    # Assume-se que a URL aqui é a string Base64
                    parts.append({
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": item["url"]
                        }
                    })
        else:
            parts.append({"text": msg["content"]})
            
        contents.append({"role": role, "parts": parts})

    body = {
        "contents": contents,
        "generationConfig": {
            "temperature": config.temperature,
            "maxOutputTokens": 4096 
        }
    }

    response = requests.post(url, json=body)
    if response.status_code != 200:
        raise Exception(f"API Error: {response.text}")
    return response.json()

def EXTRACT_CONTENT(api_response):
    if "candidates" in api_response and api_response["candidates"]:
        parts = api_response["candidates"][0].get("content", {}).get("parts", [])
        return "".join([p.get("text", "") for p in parts])
    return "Erro: A api não retornou conteúdo válido."

def generate_conversation_title(first_input, config):
    prompt = f"Crie um título máximo 4 palavras que resuma o seguinte texto. Responda apenas com o título, sem aspas ou pontuação: '{first_input}'"
    payload = [{"role": "user", "content": prompt}]
    
    try:
        api_response = CALL_LLM_API(config, payload)
        return EXTRACT_CONTENT(api_response).strip().strip('"\'')
    except Exception:
        return "Nova Conversa"


# Função para orquestrar a análise de imagem
def conversational_agent_multimodal(user_input, image_path, history, config):
    # Se houver imagem, cria conteúdo multimodal 
    if image_path:
        base64_img = ENCODE_IMAGE(image_path)
        content = [
            {"type": "text", "text": user_input},
            {"type": "image_url", "url": base64_img}
        ]
    else:
        content = user_input

    current_msg = Message(role="user", content=content)
    history.append(current_msg)
    
    # Gestão de contexto
    payload_msgs = TRUNCATE_HISTORY(history, limit=config.max_tokens)
    payload = [msg.to_dict() for msg in payload_msgs]
    
    api_response = CALL_LLM_API(config, payload)
    
    reply_text = EXTRACT_CONTENT(api_response)
    history.append(Message(role="assistant", content=reply_text))
    
    return reply_text, history

# Função para converter imagem em Base64
def ENCODE_IMAGE(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Implementação da análise de imagem
def ANALYZE_IMAGE(image_path, user_query, config):
    base64_img = ENCODE_IMAGE(image_path)
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{config.model_name}:generateContent?key={api_key}"

    # Montagem do Payload Multimodal
    body = {
        "contents": [{
            "parts": [
                {"text": user_query},
                {
                    "inline_data": {
                        "mime_type": "image/jpeg", 
                        "data": base64_img
                    }
                }
            ]
        }],
        "generationConfig": {
            "temperature": config.temperature,
            "maxOutputTokens": 4096 
        }
    }

    response = requests.post(url, json=body)
    if response.status_code != 200:
        raise Exception(f"API Error: {response.text}")

    return EXTRACT_CONTENT(response.json())

def conversational_agent(user_input, history, config):
    """Versão simplificada para manter compatibilidade com código antigo"""
    return conversational_agent_multimodal(user_input, None, history, config)