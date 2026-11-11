from fastapi import FastAPI
from pydantic import BaseModel
from app.fila import enviar_mensagem_livro

app = FastAPI(title="API/Livros", version="0.1.0")
class Livro(BaseModel):
    id: str
    titulo: str
    autor: str
    ano: int
    genero: str
    resumo: str

@app.get("/health", status_code=200)
def health_check():
    return {"status": "ok"}

@app.post("/livros", status_code=202)
def criar_livro(livro: Livro):
    enviar_mensagem_livro(livro.model_dump())
    return {"message": "recebido", "id": livro.id}
