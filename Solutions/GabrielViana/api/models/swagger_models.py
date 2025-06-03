from flask_restx import fields

def create_swagger_models(api):
    """Create and return Swagger models for API documentation"""
    
    upload_model = api.model('ImageUpload', {
        'message': fields.String(description='Response message'),
        'image_id': fields.String(description='Unique identifier for the uploaded image'),
        'filename': fields.String(description='Original filename'),
        'timestamp': fields.String(description='Upload timestamp')
    })

    health_model = api.model('Health', {
        'status': fields.String(description='Service status'),
        'timestamp': fields.String(description='Current timestamp'),
        'services': fields.Raw(description='Service dependencies status')
    })

    error_model = api.model('Error', {
        'error': fields.String(description='Error message'),
        'timestamp': fields.String(description='Error timestamp')
    })

    process_status_model = api.model('ProcessStatus', {
        'message': fields.String(description='Process status message'),
        'timestamp': fields.String(description='Current timestamp'),
        'worker_status': fields.String(description='Worker status')
    })

    return {
        'upload_model': upload_model,
        'health_model': health_model,
        'error_model': error_model,
        'process_status_model': process_status_model
    }
