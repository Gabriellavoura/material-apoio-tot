import boto3

BUCKET_ENTRADA = "image-input"


def salvar_imagem(chave: str, conteudo: bytes) -> None:
    """Guarda a imagem enviada no bucket de entrada."""
    boto3.client("s3").put_object(
        Bucket=BUCKET_ENTRADA, Key=chave, Body=conteudo, ContentType="image/png"
    )