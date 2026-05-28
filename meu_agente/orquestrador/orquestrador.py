from agentes.calculadora import python_calculator
from agentes.filmes import search_tmdb_movie


import os #biblioteca padrão do Python para interagir com o SO(genrencia pastas, caminhos de arquivos)
from dotenv import load_dotenv #ler arquivos .env (esconder chaves API e senhas)
from google import genai
from google.genai import types #importa o SDK oficial para interagir com o Gemini
import time  #Serve p/ o sleep

base_dir = os.path.dirname(__file__) #FILE: variável interna do Python que sabe o caminho da pasta
dotenv_path = os.path.join(base_dir, ".env") #Path.dirname: "resume" o caminho dessa pasta
load_dotenv(dotenv_path)

# Inicializa o cliente padrão do Gemini (busca a chave GEMINI_API_KEY automaticamente)
client = genai.Client()

# Dicionário mapeando as funções para execução dinâmica quando o modelo pedir
available_tools = {
    "python_calculator": python_calculator,
    "search_tmdb_movie": search_tmdb_movie
}

# ==========================================
# DIRETRIZES DOS AGENTES ESPECIALISTAS
# ==========================================

SYSTEM_INSTRUCTION = """Você é o Agente Orquestrador (O Chefe) de um sistema multiagentes.
Sua única função é analisar a mensagem do usuário e respondê-la coordenando ou assumindo o papel do especialista correto listado abaixo:

1. AGENTE BIÓLOGO (biologist_agent):
   - Atuação: Ative este agente sempre que o usuário perguntar sobre animais, plantas ou biologia.
   - Comportamento: Você deve agir como um biólogo pesquisador altamente técnico.
   - Formato obrigatório da resposta:
     * Apresente a espécie exata do animal/planta.
     * Detalhe suas características físicas, alimentação, habitat natural, hábitos e comportamento.
     * Informe o status de conservação atual (risco de extinção, preservado, etc.).
     * Conte uma curiosidade científica interessante.
     * Termine fazendo um paralelo com outra espécie semelhante.

2. AGENTE MATEMÁTICO (math_agent):
   - Atuação: Ative sempre que houver contas, equações ou lógica matemática.
   - Comportamento: Você DEVE obrigatoriamente invocar a ferramenta 'python_calculator' para resolver o cálculo com precisão absoluta. Mostre o passo a passo lógico antes de exibir o resultado final da ferramenta.

3. AGENTE CRÍTICO DE CINEMA (movie_agent):
   - Atuação: Ative quando o assunto for filmes, cinema ou diretores.
   - Comportamento: Você DEVE buscar dados reais usando a ferramenta 'search_tmdb_movie'. Em seguida, monte uma resposta misturando os fatos oficiais trazidos pela ferramenta com uma análise crítica profunda e profissional da obra.
   Você deve extrair apenas o TÍTULO PRINCIPAL do filme que o usuário deseja e usar esse título limpo na ferramenta 'search_tmdb_movie' (ex: se o usuário pedir "filme clássico cinderela disney anos 50", busque apenas por "Cinderela").
   Depois, use os dados retornados para contextualizar com o ano ou detalhes que o usuário pediu, montando uma análise crítica profunda.

Se a pergunta for vaga, informal ou totalmente fora desses três escopos, responda cordialmente informando que o assunto foge do limite operacional do sistema."""

# ==========================================
# 1. LOOP DE CONVERSA DIRETO E ESTÁVEL
# ==========================================

def main_chat():
    print("\n" + "="*40)
    print("🤖 SISTEMA MULTIAGENTES INICIALIZADO")
    print("Digite 'sair' para encerrar o chat.")
    print("="*40 + "\n")
    
    chat = client.chats.create(
        model="gemini-2.5-flash", 
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            tools=[python_calculator, search_tmdb_movie],
            temperature=0.3
        )
    )
    
    while True:
        try:
            user_question = input("👤 Você: ")
            if user_question.strip().lower() in ['sair', 'exit', 'quit']:
                print("\n🤖 Orquestrador: Até logo!")
                break
            if not user_question.strip():
                continue
                
            print("\n🤖 Orquestrador: ", end="", flush=True)
            
            # Envia a mensagem inicial
            response = chat.send_message(user_question)
            
            # Loop para lidar com as ferramentas (Calculadora ou TMDB)
            while response and response.function_calls:
                for function_call in response.function_calls:
                    tool_name = function_call.name 
                    tool_args = function_call.args 
                    
                    if tool_name in available_tools:
                        tool_result = available_tools[tool_name](**tool_args)
                        
                        time.sleep(2.5)
                        
                        # Devolve o resultado para o modelo
                        response = chat.send_message(
                            types.Part.from_function_response(
                                name=tool_name,
                                response={"result": tool_result}
                            )
                        )
            
            if response:
                print(response.text)
            print("\n" + "-"*40 + "\n")
            
        except KeyboardInterrupt: #caso use ctrl + C
            print("\n\n🤖 Sistema interrompido pelo usuário. Até logo!")
            break
        except Exception as e:

            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                print("\n⚠️ O Google limitou a velocidade por estarmos no plano gratuito.")
                print("Aguarde 15 segundos antes de enviar a próxima mensagem...")
                time.sleep(15)
            else:
                print(f"\n❌ Erro no processamento: {e}\n")

if __name__ == "__main__": #O orquestrador (Função main) deve ser excutado primeiro
    main_chat()