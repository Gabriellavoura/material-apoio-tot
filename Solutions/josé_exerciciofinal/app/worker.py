from .services import s3_service
from .image_processor import binarize_image
from app.services.sqs_service import SQSService
import io

sqs_service = SQSService()

def process_message():
    messages = sqs_service.receive_messages(sqs_service.queue_url_input)

    if not messages:
        print("No messages to process.")
        return

    for msg in messages:
        filename = msg['Body']
        print(f"🚀 Processing {filename}")

        try:
            # Baixa a imagem do bucket de input
            image_bytes = s3_service.download_file('image-input', filename)

            # Processa a imagem (espera bytes, retorna bytes)
            processed_image_bytes = binarize_image(image_bytes)

            # Converte bytes para um file-like object
            file_like = io.BytesIO(processed_image_bytes)

            # Upload no bucket output
            s3_service.upload_file('image-processed', filename, file_like)

            # Envia notificação para fila processados
            sqs_service.send_message(sqs_service.queue_url_processed, filename)

            # Deleta mensagem da fila input
            sqs_service.delete_message(sqs_service.queue_url_input, msg['ReceiptHandle'])

            print(f"✅ Processed and uploaded {filename}")

        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")
