# main.py
# Este arquivo contém o código FastAPI para a interface do tabuleiro de xadrez.

from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles # Importa StaticFiles
import uvicorn
import os # Importa o módulo os para lidar com caminhos de arquivo

# Inicializa a aplicação FastAPI
app = FastAPI(
    title="Chess Game API",
    description="API de backend para um jogo de xadrez, permitindo interações com o tabuleiro.",
    version="1.0.0"
)

# Adiciona middleware CORS para permitir requisições do frontend HTML
# No ambiente de desenvolvimento, * permite acesso de qualquer origem.
# Em produção, você deve restringir 'allow_origins' aos seus seus domínios específicos.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens para desenvolvimento
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# --- Configuração para servir arquivos estáticos (HTML, CSS, JS) ---
# Define o diretório onde os arquivos estáticos (como index.html) estão localizados.
# Certifique-se de que uma pasta 'static' exista no mesmo diretório que 'main.py'
# e que seu arquivo HTML principal esteja dentro dela (e.g., static/index.html).
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

# Monta o diretório estático.
# Isso significa que qualquer requisição para "/static/..." será servida a partir de STATIC_DIR.
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# --- Exemplo de Estado do Tabuleiro (simples, para demonstração) ---
# Em um jogo real, este estado seria muito mais complexo e gerenciaria
# a posição de cada peça, o turno, etc.
current_board_state = {
    "status": "game_active",
    "turn": "player1",
    "message": "Welcome to the Chess API! Make your moves."
}

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """
    Endpoint raiz da API.
    Serve o arquivo 'index.html' da pasta 'static'.
    Quando alguém acessa a URL base (e.g., http://127.0.0.1:8000/),
    este HTML será retornado.
    """
    # Construir o caminho completo para o arquivo index.html
    html_file_path = os.path.join(STATIC_DIR, "dama.html")
    # Tenta ler o conteúdo do arquivo HTML
    try:
        with open(html_file_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    except FileNotFoundError:
        # Retorna uma mensagem de erro se o arquivo não for encontrado
        return HTMLResponse(content="<h1>Erro: Arquivo index.html não encontrado na pasta 'static'.</h1>", status_code=404)


@app.get("/board_state")
async def get_board_state():
    """
    Retorna o estado atual do tabuleiro.
    Este endpoint pode ser usado pelo frontend para sincronizar o estado do jogo.
    """
    print("Requisição recebida para /board_state")
    return JSONResponse(content=current_board_state)

@app.post("/make_move")
async def make_move(move_data: dict):
    """
    Recebe dados de um movimento e simula uma atualização do tabuleiro.
    Em um jogo real, esta função conteria a lógica de validação do movimento,
    atualização do estado do jogo e verificação de xeque-mate, etc.

    Args:
        move_data (dict): Dicionário contendo informações do movimento,
                          por exemplo: {"from_cell": "cell-7-4", "to_cell": "cell-5-4"}
    """
    from_cell = move_data.get("from_cell")
    to_cell = move_data.get("to_cell")
    print(f"Movimento recebido: da célula '{from_cell}' para a célula '{to_cell}'")

    # Lógica de validação e atualização do tabuleiro seria adicionada aqui.
    # Por enquanto, apenas um log e uma resposta de sucesso.
    current_board_state["message"] = f"Movimento de {from_cell} para {to_cell} processado."
    # Simula a troca de turno
    current_board_state["turn"] = "player2" if current_board_state["turn"] == "player1" else "player1"

    return JSONResponse(content={
        "status": "success",
        "message": "Movimento recebido e processado (sem validação de jogo completa).",
        "new_board_state": current_board_state
    })

# Para rodar a aplicação diretamente a partir deste script (para teste local)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
