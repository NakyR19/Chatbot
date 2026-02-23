import json
import os
import glob
import uuid
from message import Message

# Define a pasta onde os arquivos JSON serão armazenados
CONVERSATION_DIR = "conversations"

def list_conversations():
    # Verifica se a pasta existe
    if not os.path.exists(CONVERSATION_DIR):
        return []
    
    conversations = []
    # Busca todos os arquivos que terminam com .json na pasta definida
    files = glob.glob(os.path.join(CONVERSATION_DIR, "*.json"))
    
    for f in files:
        # Extrai o nome do arquivo sem a extensão para usar como ID
        cid = os.path.splitext(os.path.basename(f))[0]
        try:
            with open(f, "r", encoding="utf-8") as file:
                data = json.load(file)
                # se for um arquivo antigo sem nome usa um padrão se nao 
                name = data.get("name", "Conversa antiga (sem título)")
                conversations.append({"id": cid, "name": name})
        except Exception:
            # teste do tamanho do json (nao foi testado ainda)
            conversations.append({"id": cid, "name": "Erro ao ler arquivo"})
            
    return conversations

def delete_conversation(conversation_id):
    # Remove o arquivo JSON da conversa do diretório
    filename = os.path.join(CONVERSATION_DIR, f"{conversation_id}.json")
    if os.path.exists(filename):
        os.remove(filename)
        return True
    return False

def load_json(conversation_id):
    filename = os.path.join(CONVERSATION_DIR, f"{conversation_id}.json")
    if not os.path.exists(filename):
        return []
    
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    history = []
    for msg_data in data.get("messages", []):
        history.append(Message(role=msg_data["role"], content=msg_data["content"]))
        
    return history

def save_json(history, config, conversation_id=None, conversation_name="Conversa sem título"):
    if not os.path.exists(CONVERSATION_DIR):
        os.makedirs(CONVERSATION_DIR)

    if conversation_id is None:
        conversation_id = str(uuid.uuid4())

    filename = os.path.join(CONVERSATION_DIR, f"{conversation_id}.json")
    messages = [msg.to_dict() for msg in history]

    data = {
        "name": conversation_name, # Agora salva a chave 'name' corretamente na raiz
        "config": {
            "provider": config.provider,
            "model_name": config.model_name,
            "temperature": config.temperature,
            "max_tokens": config.max_tokens,
            "modality": config.modality
        },
        "messages": messages
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return conversation_id