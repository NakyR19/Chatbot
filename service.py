from message import Message
import requests

api_key = 'api do google studio'

def TRUNCATE_HISTORY(history, limit):
    return history[-limit:] if len(history) > limit else history

def CALL_LLM_API(config, payload):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{config.model_name}:generateContent?key={api_key}"

    contents = [
        {
            "role": "model" if msg["role"] == "assistant" else "user",
            "parts": [{"text": msg["content"]}]
        }
        for msg in payload
    ]

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

def conversational_agent(user_input, history, config):
    
    current_msg = Message(role="user", content=user_input)
    history.append(current_msg)

    
    payload_msgs = TRUNCATE_HISTORY(history, limit=config.max_tokens)
    payload = [msg.to_dict() for msg in payload_msgs]

    
    api_response = CALL_LLM_API(config, payload)

    
    reply_text = EXTRACT_CONTENT(api_response)
    reply_msg = Message(role="assistant", content=reply_text)
    
    updated_history = history
    updated_history.append(reply_msg)

    return reply_text, updated_history