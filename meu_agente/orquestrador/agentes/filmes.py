import os
import requests #faz requisições HTTP
import urllib.parse #URL encoding, transforma caracteres em códigos seguros para a web

def search_tmdb_movie(title: str) -> str:
    """Busca informações oficiais de um filme na API do TMDB usando o Token de Acesso de Leitura (JWT)."""
    
    API_TOKEN = os.getenv("TMDB_API_TOKEN")
    if not API_TOKEN:
        return "Erro: O token TMDB_API_TOKEN não foi encontrado no ambiente."
        
    title_clean = title.strip()
    title_encoded = urllib.parse.quote(title_clean)
    
    # URL padrão sem expor a chave nos parâmetros
    url = f"https://api.themoviedb.org/3/search/movie?query={title_encoded}&language=pt-BR"
    
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {API_TOKEN}"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10) 
        data = response.json()
        
        if response.status_code != 200:
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