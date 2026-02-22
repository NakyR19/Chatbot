from config import ModelConfig
from service import conversational_agent, generate_conversation_title
from save_conversation import save_json, list_conversations, load_json

history = []
current_conversation_id = None
current_conversation_name = "Nova Conversa"

#se passar de n mensagens ele esquece as antigas, depoisv amos voltar a 20 só está em 100 para teste
config = ModelConfig(
    provider="gemini",
    model_name="gemini-2.5-flash", 
    temperature=0.7,
    max_tokens=100, 
    modality="text"
)

print("CHATBOT\n\n")
conversas_salvas = list_conversations()

if conversas_salvas:
    print("Conversas anteriores encontradas:")
    for i, conv in enumerate(conversas_salvas):
        print(f"[{i}] - {conv['name']} (ID: {conv['id'][:8]}...)")
    
    escolha = input("\nDigite o número da conversa para carregar (ou ENTER para nova): ")
    
    if escolha.strip().isdigit():
        indice = int(escolha.strip())
        if 0 <= indice < len(conversas_salvas):
            current_conversation_id = conversas_salvas[indice]['id']
            current_conversation_name = conversas_salvas[indice]['name']
            history = load_json(current_conversation_id)
            print(f"\nOk. '{current_conversation_name}' carregada! ({len(history)} mensagens)")
        else:
            print("\nError. Índice inválido. Iniciando nova conversa...")
    else:
        print("\n[*] Iniciando nova conversa...")
else:
    print("\nNenhuma conversa salva. Iniciando uma nova...")

print("\n(Digite 'exit' para salvar e sair)")
print("-" * 30)

while True:
    user_input = input("Você: ")

    if user_input.lower() == "exit":
        break

    if not user_input.strip():
        continue

    # titulo da conversa vai ser o conteudo da primeira mensagem
    if len(history) == 0 and current_conversation_id is None:
        print("[Gerando título da conversa...]")
        current_conversation_name = generate_conversation_title(user_input, config)
    try:
        response, history = conversational_agent(
            user_input,
            history,
            config
        )
        print("Bot:", response)
        
    except Exception as e:
       
        print(f"\nErro na chamada: {e}")
        print("Tente novamente.\n")


if history:
    conversation_id = save_json(history, config, current_conversation_id, current_conversation_name)
    print(f"\nConversa '{current_conversation_name}' salva com sucesso!")
else:
    print("\nNenhuma mensagem para salvar.")