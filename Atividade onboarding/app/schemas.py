from pydantic import BaseModel


class LivroEntrada(BaseModel):
    id: str
    titulo: str
    autor: str
    ano: int
    genero: str
    resumo: str
