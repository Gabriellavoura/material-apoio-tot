import json
import uuid
from datetime import datetime
from flask import request, current_app
from flask_restx import Resource, fields
from werkzeug.datastructures import FileStorage

from services.aws_service import AWSService
from utils.validators import validate_png_file

def create_upload_routes(api, namespace, models):
    upload_parser = api.parser()
    upload_parser.add_argument('file', location='files', type=FileStorage, required=True, help='PNG image file')
    
    @namespace.route('')
    class ImageUpload(Resource):
        @api.expect(upload_parser)
        @api.response(200, 'Success', models['upload_model'])
        @api.response(400, 'Bad Request', models['error_model'])
        @api.response(500, 'Internal Server Error', models['error_model'])
        def post(self):
            """Faz o upload de uma imagem PNG e a coloca na fila de processamento"""
            try:
                if 'file' not in request.files:
                    return {'error': 'No file provided', 'timestamp': datetime.utcnow().isoformat()}, 400
                
                file = request.files['file']
                
                validation_result = validate_png_file(file)
                if not validation_result['valid']:
                    return {'error': validation_result['error'], 'timestamp': datetime.utcnow().isoformat()}, 400
                
                image_id = str(uuid.uuid4())
                filename = f"{image_id}.png"
                
                file_content = file.read()
                
                aws_service = AWSService()
                
                # Upload  S3
                success = aws_service.upload_to_s3(
                    bucket_name=current_app.config['S3_INPUT_BUCKET'],
                    key=filename,
                    file_content=file_content,
                    content_type='image/png'
                )
                
                if not success:
                    return {'error': 'Failed to upload image to storage', 'timestamp': datetime.utcnow().isoformat()}, 500
                
                # Send message to SQS
                message_body = {
                    'image_id': image_id,
                    'filename': filename,
                    'original_filename': file.filename,
                    'timestamp': datetime.utcnow().isoformat()
                }
                
                success = aws_service.send_sqs_message(
                    queue_name=current_app.config['SQS_QUEUE_NAME'],
                    message_body=json.dumps(message_body),
                    message_group_id=current_app.config['SQS_MESSAGE_GROUP_ID'],
                    message_deduplication_id=image_id
                )
                
                if not success:
                    return {'error': 'Failed to queue image for processing', 'timestamp': datetime.utcnow().isoformat()}, 500
                
                return {
                    'message': 'Image uploaded successfully',
                    'image_id': image_id,
                    'filename': file.filename,
                    'timestamp': datetime.utcnow().isoformat()
                }, 200
                
            except Exception as e:
                current_app.logger.error(f"Upload error: {str(e)}")
                return {'error': 'Internal server error', 'timestamp': datetime.utcnow().isoformat()}, 500
    
    return namespace