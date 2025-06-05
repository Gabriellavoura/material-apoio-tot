from flask import request, Flask, send_file, jsonify
from flask_restx import Namespace, Resource, fields
from .services import s3_service
from .worker import process_message
from flask import send_from_directory
from app.services.sqs_service import SQSService
import os
import io


api = Namespace('image', description='Operações com imagens')

sqs_service = SQSService()


upload_model = api.model('UploadModel', {
    'file': fields.String(description='Arquivo de imagem (.png)', required=True)
})

@api.route('/processed')
class ProcessedImages(Resource):
    def get(self):
        # Listar arquivos no bucket image-processed
        try:
            response = s3_service.s3.list_objects_v2(Bucket='image-processed')
            files = []
            for obj in response.get('Contents', []):
                files.append(obj['Key'])
            return {'processed_files': files}, 200
        except Exception as e:
            return {'message': f'Erro ao listar arquivos processados: {str(e)}'}, 500


@api.route('/processed/<filename>')
class DownloadProcessed(Resource):
    def get(self, filename):
        try:
            file_bytes = s3_service.download_file('image-processed', filename)
            return send_file(
                io.BytesIO(file_bytes),
                download_name=filename,
                mimetype='image/png'
            )
        except Exception as e:
            return {'message': f'Erro ao baixar arquivo {filename}: {str(e)}'}, 500
@api.route('/')
class Home(Resource):
    def get(self):
        return send_from_directory(os.path.join(os.path.dirname(__file__), 'static'), 'index.html')

@api.route('/upload')
class Upload(Resource):
    def post(self):
        if 'file' not in request.files:
            return {'message': 'Nenhum arquivo enviado'}, 400

        file = request.files['file']
        filename = file.filename

        if not filename:
            return {'message': 'Nome de arquivo inválido'}, 400

        try:
            s3_service.upload_file('image-input', filename, file)
            sqs_service.send_message(sqs_service.queue_url_input, filename)


            return {'message': f'Arquivo {filename} enviado com sucesso'}, 200

        except Exception as e:
            return {'message': f'Erro ao processar o arquivo: {str(e)}'}, 500


@api.route('/healthcheck')
class Health(Resource):
    def get(self):
        return {'status': 'ok'}, 200


@api.route('/process')
class Process(Resource):
    def post(self):
        try:
            process_message()
            return {'message': 'Processamento executado com sucesso'}, 200
        except Exception as e:
            return {'message': f'Erro no processamento: {str(e)}'}, 500

app = Flask(__name__)    

@app.route('/image/processed/<filename>')
def get_processed_image(filename):
    try:
        # Faz download da imagem do bucket S3
        image_bytes = s3_service.download_file('image-processed', filename)

        # Retorna como arquivo de imagem (mimetype image/png)
        return send_file(
            io.BytesIO(image_bytes),
            mimetype='image/png',
            download_name=filename
        )
    except Exception as e:
        return jsonify({'error': f'Erro ao carregar imagem: {str(e)}'}), 404