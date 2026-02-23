import streamlit as st
from config import ModelConfig
from service import conversational_agent, conversational_agent_multimodal, generate_conversation_title
from save_conversation import save_json, list_conversations, load_json, delete_conversation

# Configurando o título da página
st.set_page_config(page_title="UFS - Chatbot", page_icon="🤖", layout="wide")

# Inicializando variáveis que não podem ser resetadas
if "history" not in st.session_state:
    st.session_state.history = [] # Armazena as mensagens trocadas
if "current_id" not in st.session_state:
    st.session_state.current_id = None
if "chat_title" not in st.session_state:
    st.session_state.chat_title = "Nova Conversa" # Título exibido no topo do chat

# Configurando o modelo
config = ModelConfig(
    provider="gemini",
    model_name="gemini-2.5-flash", 
    temperature=0.7,
    max_tokens=20,
    modality="text"
)

# Gerenciamento das conversas
with st.sidebar:
    st.title("📂 Conversas")
    if st.button("+ Nova Conversa", use_container_width=True):
        st.session_state.history = []
        st.session_state.current_id = None
        st.session_state.chat_title = "Nova Conversa"
        st.rerun() # Recarrega a página para aplicara as mudanças

    st.divider()
    
    # Listando os arquivos .json encontrados
    conversas_salvas = list_conversations()
    for conv in conversas_salvas:
        # Uma coluna é para o link da conversa e outra é para o link de deletar
        col_link, col_del = st.columns([0.8, 0.2])
        
        with col_link:
            # Quando clica no nome da conversa, carrega o JSON
            if st.button(f"💬 {conv['name']}", key=f"btn_{conv['id']}", use_container_width=True):
                st.session_state.current_id = conv['id']
                st.session_state.chat_title = conv['name']
                st.session_state.history = load_json(conv['id'])
                st.rerun()
        
        with col_del:
            # Quando clica no símbolo de lixeira, o arquivo é deletado
            if st.button("🗑️", key=f"del_{conv['id']}", help="Excluir conversa"):
                # Chamando a função de deletar o arquivo
                delete_conversation(conv['id'])
                
                # Se a convesa excluída estiver aberta, reseta a interface
                if st.session_state.current_id == conv['id']:
                    st.session_state.history = []
                    st.session_state.current_id = None
                    st.session_state.chat_title = "Nova Conversa"
                
                # Recarrega a página para atualizar a lista da sidebar
                st.rerun()

# Página principal
st.title(f"🤖 {st.session_state.chat_title}")

# Renderizar mensagens existentes com suporte a multimodalidade
for msg in st.session_state.history:
    with st.chat_message(msg.role):
        # Verifica a mensagem contém múltiplos títulos
        if isinstance(msg.content, list):
            for item in msg.content:
                if item["type"] == "text":
                    st.markdown(item["text"]) # Exibe o texto do usuário 
                elif item["type"] == "image_url":
                    # Converte a string Base64 de volta para imagem visível 
                    st.image(f"data:image/jpeg;base64,{item['url']}", width=300)
        else:
            # Se for texto puro 
            st.markdown(msg.content)

# Siderbar para envio da imagem
with st.sidebar:
    uploaded_file = st.file_uploader("Enviar imagem para análise", type=["jpg", "png", "jpeg"])

# Barra de digitação do usuário
if prompt := st.chat_input("Digite sua mensagem..."):
    # Exibição da mensagem do usuário
    with st.chat_message("user"):
        st.markdown(prompt)
        if uploaded_file:
            st.image(uploaded_file, width=300)

    # Geração de Título (Apenas se for o início da conversa)
    # Verificamos se o histórico está vazio e se o título ainda é o padrão
    if not st.session_state.history and st.session_state.chat_title == "Nova Conversa":
        try:
            # Chama a função do service.py para resumir o input 
            novo_titulo = generate_conversation_title(prompt, config)
            st.session_state.chat_title = novo_titulo
        except Exception:
            st.session_state.chat_title = "Conversa"

    # Processamento da imagem 
    temp_path = None
    if uploaded_file:
        temp_path = f"temp_{uploaded_file.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

    # Resposta do Assistente
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                # Chama o agente multimodal para obter a resposta
                response, updated_history = conversational_agent_multimodal(
                    prompt, 
                    temp_path,
                    st.session_state.history, 
                    config
                )
                st.markdown(response)
                st.session_state.history = updated_history
                
                # Salvamento Final  
                st.session_state.current_id = save_json(
                    st.session_state.history, 
                    config, 
                    st.session_state.current_id, 
                    st.session_state.chat_title
                )
            except Exception as e:
                st.error(f"Erro: {e}")