import json
import uuid
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel
from sqlmodel import Session

from pipeline import aws, db
from pipeline.config import get_settings
from pipeline.models import Imagem

ASSINATURA_PNG = b"\x89PNG\r\n\x1a\n"


@asynccontextmanager
async def lifespan(_: FastAPI):
    db.init_db()
    yield


app = FastAPI(
    title="Pipeline de imagens",
    description="Recebe imagens PNG, processa em segundo plano e acompanha cada etapa.",
    version="0.1.0",
    lifespan=lifespan,
)


def get_session():
    with Session(db.get_engine()) as session:
        yield session


class ImagemCriada(BaseModel):
    id: str


class ImagemSaida(BaseModel):
    id: str
    nome_arquivo: str
    status: str
    enviada_em: str
    concluida_em: str | None = None
    erro: str | None = None


def converter(imagem: Imagem) -> ImagemSaida:
    return ImagemSaida(
        id=imagem.id,
        nome_arquivo=imagem.nome_arquivo,
        status=imagem.status,
        enviada_em=imagem.enviada_em.isoformat(),
        concluida_em=imagem.concluida_em.isoformat() if imagem.concluida_em else None,
        erro=imagem.erro,
    )


@app.get(
    "/health",
    summary="Verifica se a API esta no ar",
    responses={200: {"description": "API no ar"}},
)
def health():
    return {"status": "ok"}


@app.post(
    "/images",
    status_code=202,
    response_model=ImagemCriada,
    summary="Envia uma imagem PNG para processamento",
    responses={
        202: {"description": "Imagem aceita; devolve o id"},
        400: {"description": "O arquivo nao e um .png valido"},
    },
)
async def enviar_imagem(
    file: UploadFile = File(...), session: Session = Depends(get_session)
):
    conteudo = await file.read()
    nome = file.filename or ""
    if not nome.lower().endswith(".png") or not conteudo.startswith(ASSINATURA_PNG):
        raise HTTPException(status_code=400, detail="Apenas arquivos .png sao aceitos")

    settings = get_settings()
    image_id = str(uuid.uuid4())
    chave = f"{image_id}.png"

    aws.salvar_objeto(settings.input_bucket, chave, conteudo)
    db.criar_imagem(session, image_id, nome, chave)
    aws.enviar_mensagem(
        settings.input_queue, json.dumps({"image_id": image_id, "chave": chave})
    )
    return ImagemCriada(id=image_id)


@app.get(
    "/images/{image_id}",
    response_model=ImagemSaida,
    summary="Consulta o status de uma imagem",
    responses={
        200: {"description": "Status e datas de envio e conclusao"},
        404: {"description": "Imagem nao encontrada"},
    },
)
def consultar_imagem(image_id: str, session: Session = Depends(get_session)):
    imagem = session.get(Imagem, image_id)
    if imagem is None:
        raise HTTPException(status_code=404, detail="Imagem nao encontrada")
    return converter(imagem)


@app.get(
    "/images",
    response_model=list[ImagemSaida],
    summary="Lista as imagens, com filtro opcional por status",
    responses={200: {"description": "Lista de imagens"}},
)
def listar(status: str | None = None, session: Session = Depends(get_session)):
    return [converter(i) for i in db.listar_imagens(session, status)]
