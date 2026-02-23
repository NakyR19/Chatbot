# Chatbot de texto com persistência

Este projeto implementa um Agente Conversacional em Python, capaz de interagir com Grandes Modelos de Linguagem (LLMs). Ele possui uma arquitetura modular que permite a troca de motores de Inteligência Artificial em tempo de execução, suportando atualmente o **Google Gemini** e o **Meta LLaMA** (via Groq). 

O sistema destaca-se por implementar persistência de dados em JSON e gerenciamento inteligente de contexto através da técnica de **Janela Deslizante (Sliding Window)**, o que previne o esgotamento de tokens da API durante conversas longas.

## 📁 Estrutura do Projeto

O código foi construído seguindo princípios de responsabilidade única e separação de conceitos. Abaixo está a descrição de cada componente:

* **`main.py`**: O orquestrador do sistema. É o ponto de entrada da aplicação, responsável por exibir o menu interativo, capturar a escolha do motor da IA pelo usuário e rodar o loop principal da conversa.
* **`service.py`**: O núcleo de processamento do Agente Conversacional. Contém as regras de negócio para truncar o histórico (Sliding Window), adaptar o formato das mensagens dependendo da IA escolhida (Strategy Pattern) e realizar as requisições HTTP para as APIs externas.
* **`config.py`**: Define a classe `ModelConfig`, que centraliza os parâmetros de configuração da IA, como o nome do modelo, a temperatura (nível de criatividade) e o limite de tokens da janela de contexto.
* **`message.py`**: Contém a classe `Message`, responsável por estruturar a entidade da mensagem, padronizando os papéis (`user` e `assistant`) e o conteúdo do texto.
* **`save_conversation.py`**: Módulo de persistência. Contém as lógicas para ler, listar e salvar o histórico de mensagens em arquivos físicos, superando a volatilidade da memória RAM.
* **`conversations/`**: Diretório gerado automaticamente pelo sistema. É aqui que todas as conversas são salvas isoladamente em formato `.json`, utilizando UUIDs como identificadores únicos e armazenando o título gerado pela IA.

---

## 🔑 Configuração das APIs (Chaves de Acesso)

Para que o chatbot consiga se comunicar com a inteligência artificial, você precisará inserir as suas próprias chaves de API.

### 1. Onde alterar no código
Abra o arquivo **`service.py`** e localize as seguintes variáveis nas primeiras linhas do código:

api_key = 'COLOQUE_SUA_CHAVE_DO_GEMINI_AQUI'
groq_key = 'COLOQUE_SUA_CHAVE_DA_GROQ_AQUI'

Substitua os valores de exemplo pelas suas chaves reais. *(Nota: Em ambientes de produção, recomenda-se o uso de variáveis de ambiente .env para maior segurança).*

### 2. Como obter as chaves 
* **Google Gemini:** Acesse o Google AI Studio, faça login com sua conta Google e clique em "Get API key" para gerar a sua chave.
* **Meta LLaMA (Groq):** Acesse o Groq, crie sua conta de desenvolvedor e clique em "Create API Key" para gerar a sua chave de acesso ultrarrápido.

---

## 🚀 Como Executar o Projeto

Certifique-se de ter o Python instalado na sua máquina. O único pacote externo necessário para rodar o projeto é o `requests`.

1. **Instale a dependência:**
   No terminal, execute o comando:
   pip install requests

2. **Inicie a aplicação:**
   Estando no diretório raiz do projeto, rode:
   python main.py

3. **Uso CLI:**
   * O terminal exibirá um menu perguntando qual IA você deseja usar (0 para Gemini, 1 para LLaMA).
   * Em seguida, listará as conversas anteriores salvas na pasta `conversations/`. Você pode digitar o número de uma conversa antiga para retomá-la ou pressionar ENTER para começar uma nova.
   * Para encerrar e salvar o progresso atual, digite `exit`.

   **Uso Interface:**