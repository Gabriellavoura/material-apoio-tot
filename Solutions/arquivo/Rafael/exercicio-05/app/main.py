from fastapi import Depends, FastAPI, HTTPException, Query, status
from pydantic import BaseModel
from sqlmodel import Session, select

from app.exercicio_05 import Livro as LivroDB, obter_sessao
from app.fila import enviar_mensagem_livro

app = FastAPI(title="API/Livros", version="0.1.0")


class LivroSchema(BaseModel):
    id: str
    titulo: str
    autor: str
    ano: int
    genero: str
    resumo: str


@app.get("/health", status_code=200)
def health_check():
    return {"status": "ok"}


@app.post("/livros", status_code=status.HTTP_202_ACCEPTED)
def criar_livro(livro_in: LivroSchema, session: Session = Depends(obter_sessao)):
    livro_existente = session.get(LivroDB, livro_in.id)
    if livro_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Livro com o ID '{livro_in.id}' já existe.",
        )

    db_livro = LivroDB(
        id=livro_in.id,
        titulo=livro_in.titulo,
        genero=livro_in.genero,
        status="recebido",
    )
    session.add(db_livro)
    session.commit()
    session.refresh(db_livro)

    enviar_mensagem_livro(livro_in.model_dump())

    return {"message": "recebido e registado na base de dados", "id": livro_in.id}


@app.get("/livros/{livro_id}", response_model=LivroDB)
def obter_livro(livro_id: str, session: Session = Depends(obter_sessao)):
    livro = session.get(LivroDB, livro_id)
    if not livro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Livro não encontrado."
        )
    return livro


@app.get("/livros", response_model=list[LivroDB])
def listar_livros(
    status: str | None = Query(None, description="Filtrar livros por status"),
    session: Session = Depends(obter_sessao),
):
    query = select(LivroDB)
    if status:
        query = query.where(LivroDB.status == status)
    return session.exec(query).all()
