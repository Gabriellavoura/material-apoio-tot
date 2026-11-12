import cv2
import numpy as np


def binarizar(conteudo: bytes) -> bytes:
    """Converte uma imagem PNG para preto e branco (binarização de Otsu)."""
    dados = np.frombuffer(conteudo, dtype=np.uint8)
    imagem = cv2.imdecode(dados, cv2.IMREAD_GRAYSCALE)
    if imagem is None:
        raise ValueError("O conteúdo não é uma imagem válida")

    _, binaria = cv2.threshold(imagem, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    ok, buffer = cv2.imencode(".png", binaria)
    if not ok:
        raise ValueError("Falha ao codificar a imagem processada")
    return buffer.tobytes()