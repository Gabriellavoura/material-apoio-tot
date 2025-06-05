import time
import json
from io import BytesIO
from image_processor import process_image  # Função que processa imagem (retorna BytesIO)
import sqs_service
import s3_service

S3_INPUT_BUCKET = "image-input"
S3_PROCESSED_BUCKET = "image-processed"
SQS_INPUT_QUEUE = sqs_service.SQS_INPUT_QUEUE
SQS_PROCESSED_QUEUE = sqs_service.SQS_PROCESSED_QUEUE

def worker_process():
    print("Worker iniciado. Aguardando mensagens...")

    while True:
        try:
            messages = sqs_service.receive_messages(SQS_INPUT_QUEUE)

            if messages:
                for message in messages:
                    try:
                        body = json.loads(message['Body'])
                        object_key = body['object_key']
                        image_id = body['image_id']

                        print(f"Processando imagem: {object_key}")

                        image_data = s3_service.download_file(S3_INPUT_BUCKET, object_key)

                        processed_image = process_image(image_data)  # Retorna BytesIO

                        processed_key = f"processed_{object_key}"
                        s3_service.upload_fileobj(processed_image, S3_PROCESSED_BUCKET, processed_key)

                        processed_message = {
                            'image_id': image_id,
                            'original_key': object_key,
                            'processed_key': processed_key
                        }
                        sqs_service.send_message(
                            SQS_PROCESSED_QUEUE,
                            processed_message,
                            message_deduplication_id=f"processed_{image_id}"
                        )

                        sqs_service.delete_message(SQS_INPUT_QUEUE, message['ReceiptHandle'])

                        print(f"Imagem {object_key} processada com sucesso")

                    except Exception as e:
                        print(f"Erro ao processar mensagem: {str(e)}")
            else:
                # Sem mensagens, aguarda um pouco
                time.sleep(1)

        except Exception as e:
            print(f"Erro no worker: {str(e)}")
            time.sleep(5)

if __name__ == '__main__':
    worker_process()
