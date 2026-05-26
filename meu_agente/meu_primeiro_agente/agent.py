import os #biblioteca padrão do Python para interagir com o SO(genrencia pastas, caminhos de arquivos)
import requests #faz requisições HTTP
import dotenv 
from dotenv import load_dotenv #ler arquivos .env (esconder chaves API e senhas)
from google import genai
from google.genai import types #importa o SDK oficial para interagir com o Gemini
import time  #Serve p/ o sleep
import urllib.parse #URL encoding, transforma caracteres em códigos seguros para a web

base_dir = os.path.dirname(__file__) #FILE: variável interna do Python que sabe o caminho da pasta
dotenv_path = os.path.join(base_dir, ".env") #Path.dirname: "resume" o caminho dessa pasta
dotenv.load_dotenv()

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

# ==========================================
# 2. Calculadora
# ==========================================

def python_calculator(expression: str) -> str:
    """Executa uma expressão matemática em Python de forma segura e retorna o resultado."""
    import math #o Dict ignora tudo que começa com __ (config. interna do python)
    allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
    allowed_names.update({"abs": abs, "round": round}) #Inclui funções absolutas do Python que são úteis em matemática
    try: #eval = a string é executada como código python puro
        result = eval(expression, {"__builtins__": None}, allowed_names) #builtins: torna indisponíveis as funções padrões do python
        return f"Resultado exato: {result}" #allowed_names: torna disponíveis as funções/constates permitidas que foram filtradas do Math
    except Exception as e:
        return f"Erro ao calcular a expressão: {str(e)}" #Se digitar algo errado, retorna mensagem de erro


# ==========================================
# 3. Filmes - TMDB
# ==========================================

def search_tmdb_movie(title: str) -> str:
    """Busca informações oficiais de um filme na API do TMDB usando o Token de Acesso de Leitura (JWT)."""
    # Lendo o token longo que configuramos no .env
    API_TOKEN = os.getenv("TMDB_API_TOKEN") #Pega o token do TMDB
    if not API_TOKEN:
        return "Erro: O token TMDB_API_TOKEN não foi encontrado no ambiente."
        
    title_clean = title.strip()
    title_encoded = urllib.parse.quote(title_clean)
    
    # URL padrão sem expor a chave nos parâmetros
    url = f"https://api.themoviedb.org/3/search/movie?query={title_encoded}&language=pt-BR"
    
    # Configuração dos cabeçalhos de autorização exigidos para o Token Longo
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {API_TOKEN}" #O token é escondido dentro do header, e não exposto diretamente no link URL
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10) #urllib codifica o título do filme e vaia té o server TMDB // se estiver fora do ar por 10 segundos, o código desiste
        data = response.json()
        
        if response.status_code != 200: #Verifica se a busca deu certo (Status 200), pega oprimeiro resultado e extrai as suas informações
            return f"Erro na API do TMDB (Status {response.status_code}): {data.get('status_message', 'Sem mensagem')}"
            
        if not data.get('results'):
            return f"Nenhum filme encontrado com o título: '{title_clean}'."
            
        movie = data['results'][0]
        
        titulo_br = movie.get('title', 'Não informado')
        titulo_orig = movie.get('original_title', 'Não informado')
        data_lanc = movie.get('release_date', 'Data desconhecida')
        nota = movie.get('vote_average', 'Sem nota')
        sinopse = movie.get('overview', 'Sinopse não disponível em português.')
        
        if not sinopse.strip():
            sinopse = "Sinopse não disponível em português."

        return (
            f"Título no Brasil: {titulo_br}\n"
            f"Título Original: {titulo_orig}\n"
            f"Data de Lançamento: {data_lanc}\n"
            f"Nota Média: {nota}/10\n"
            f"Sinopse Oficial: {sinopse}"
        )
    except Exception as e:
        return f"Falha ao conectar ou processar os dados da API do TMDB: {str(e)}"