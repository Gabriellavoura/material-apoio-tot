from datetime import datetime
from flask import current_app
from flask_restx import Resource

from services.aws_service import AWSService

def create_health_routes(api, namespace, models):
    @namespace.route('')
    class HealthCheck(Resource):
        @api.response(200, 'Success', models['health_model'])
        def get(self):
            """
            Checa o estado de saúde do serviço e suas dependências, como S3 e SQS.
            """
            try:
                aws_service = AWSService()
                
                s3_status = aws_service.check_s3_health()
                sqs_status = aws_service.check_sqs_health()
                
                overall_status = 'healthy' if (s3_status and sqs_status) else 'unhealthy'
                
                return {
                    'status': overall_status,
                    'timestamp': datetime.utcnow().isoformat(),
                    'services': {
                        's3': 'healthy' if s3_status else 'unhealthy',
                        'sqs': 'healthy' if sqs_status else 'unhealthy'
                    }
                }, 200
                
            except Exception as e:
                current_app.logger.error(f"Health check error: {str(e)}")
                return {
                    'status': 'unhealthy',
                    'timestamp': datetime.utcnow().isoformat(),
                    'services': {
                        's3': 'unknown',
                        'sqs': 'unknown'
                    }
                }, 500
    
    return namespace