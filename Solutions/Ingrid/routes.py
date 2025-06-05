from flask import Blueprint, request, render_template, jsonify
from werkzeug.utils import secure_filename
import uuid
import sqs_service
import boto3
from botocore.exceptions import ClientError

routes = Blueprint('routes', __name__)

ENDPOINT_URL = "http://localhost:4566"
S3_INPUT_BUCKET = "image-input"
S3_PROCESSED_BUCKET = "image-processed"

s3_client = boto3.client('s3', endpoint_url=ENDPOINT_URL)

@routes.route('/', methods=['GET', 'POST'])
def home():
    status_message = '✅ API rodando com sucesso!'
    original_url = None
    processed_url = None
    image_id = None
    saved_images = []

    if request.method == 'POST':
        if 'image' not in request.files:
            status_message = '❌ Nenhuma imagem enviada.'
            return render_template('upload.html', status_message=status_message, show_form=True)

        file = request.files['image']
        if file.filename == '':
            status_message = '❌ Nome de arquivo vazio.'
            return render_template('upload.html', status_message=status_message, show_form=True)

        if not file.filename.lower().endswith('.png'):
            status_message = '❌ Apenas imagens PNG são permitidas.'
            return render_template('upload.html', status_message=status_message, show_form=True)

        try:
            image_id = str(uuid.uuid4())
            filename = secure_filename(file.filename)
            object_key = f"{image_id}_{filename}"

            # Upload da imagem original
            s3_client.upload_fileobj(file, S3_INPUT_BUCKET, object_key)

            # Envia mensagem para fila
            message_body = {
                'image_id': image_id,
                'object_key': object_key
            }
            sqs_service.send_message(
                sqs_service.SQS_INPUT_QUEUE,
                message_body,
                message_group_id='image_processing',
                message_deduplication_id=image_id
                )

            original_url = f"http://localhost:4566/{S3_INPUT_BUCKET}/{object_key}"
            processed_key = f"processed_{object_key}"

            # Verifica se a imagem processada já está no bucket
            try:
                s3_client.head_object(Bucket=S3_PROCESSED_BUCKET, Key=processed_key)
                processed_url = f"http://localhost:4566/{S3_PROCESSED_BUCKET}/{processed_key}"
            except ClientError as e:
                if e.response['Error']['Code'] != '404':
                    raise

            status_message = "✅ Imagem enviada com sucesso e armazenada."

        except Exception as e:
            status_message = f"❌ Erro ao enviar imagem: {str(e)}"
            return render_template('upload.html', status_message=status_message, show_form=True)

    # Lista de imagens do bucket
    try:
        response = s3_client.list_objects_v2(Bucket=S3_INPUT_BUCKET)
        if 'Contents' in response:
            saved_images = [obj['Key'] for obj in response['Contents']]
    except Exception as e:
        print(f"Erro ao listar imagens: {e}")

    return render_template(
        'upload.html',
        status_message=status_message,
        original_url=original_url,
        processed_url=processed_url,
        s3_input_bucket=S3_INPUT_BUCKET,
        s3_processed_bucket=S3_PROCESSED_BUCKET,
        show_form=(request.method == 'GET'),
        image_id=image_id,
        saved_images=saved_images
    )


@routes.route('/check_processed/<image_id>')
def check_processed(image_id):
    try:
        # Buscar chave que começa com o UUID
        response = s3_client.list_objects_v2(Bucket=S3_INPUT_BUCKET, Prefix=image_id)
        if 'Contents' not in response:
            return jsonify({'processed': False})

        original_key = response['Contents'][0]['Key']
        processed_key = f"processed_{original_key}"

        # Verifica se a imagem processada já está no bucket
        try:
            s3_client.head_object(Bucket=S3_PROCESSED_BUCKET, Key=processed_key)
            processed_url = f"http://localhost:4566/{S3_PROCESSED_BUCKET}/{processed_key}"
            return jsonify({'processed': True, 'processed_url': processed_url})
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return jsonify({'processed': False})
            else:
                raise

    except Exception as e:
        return jsonify({'processed': False, 'error': str(e)})
