import cv2
import numpy as np


def binarizar(png: bytes) -> bytes:
    matriz = np.frombuffer(png, dtype=np.uint8)
    imagem = cv2.imdecode(matriz, cv2.IMREAD_GRAYSCALE)
    if imagem is None:
        raise ValueError("Nao foi possivel decodificar a imagem")
    _, binaria = cv2.threshold(imagem, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    ok, codificada = cv2.imencode(".png", binaria)
    if not ok:
        raise ValueError("Falha ao codificar a imagem processada")
    return codificada.tobytes()
