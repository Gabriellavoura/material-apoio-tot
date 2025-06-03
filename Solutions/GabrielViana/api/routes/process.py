from datetime import datetime
from flask import current_app
from flask_restx import Resource
from services.aws_service import AWSService


aws_service = AWSService()


def check_worker_status():
    try:
        messages = aws_service.receive_sqs_messages('new-image-input.fifo', max_messages=1)
        if not messages:
            return 'idle'
        else:
            return 'running'
    except Exception as e:
        current_app.logger.error(f"Error checking worker status: {str(e)}")
        return 'error'

def create_process_routes(api, namespace, models):
    @namespace.route('')
    class ProcessStatus(Resource):
        @api.response(200, 'Success', models['process_status_model'])
        def get(self):
            worker_status = check_worker_status()
            """Retorna o status do worker de processamento de imagens"""
            try:
                return {
                    'message': 'Worker is processing images' if worker_status == 'running' else 'Worker is idle',
                    'timestamp': datetime.utcnow().isoformat(),
                    'worker_status': worker_status
                }, 200
            except Exception as e:
                current_app.logger.error(f"Process status error: {str(e)}")
                return {'error': 'Internal server error', 'timestamp': datetime.utcnow().isoformat()}, 500
    
    return namespace