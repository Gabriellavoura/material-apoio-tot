import os
import logging
from flask import Flask, request
from flask_restx import Api, Resource, Namespace, fields
import boto3
from botocore.exceptions import BotoCoreError, ClientError

# Flask App and Swagger Setup
app = Flask(__name__)
api = Api(app, version='1.0', title='ToT API', description='Text Of Things API')
ns = api.namespace('images', description='Image operations')

# Logging Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# AWS LocalStack Configuration
AWS_REGION = "us-east-1"
BUCKET_INPUT = "image-input"
QUEUE_URL = "http://localhost:4566/000000000000/new-image-input.fifo"

boto_config = {
    "aws_access_key_id": "test",
    "aws_secret_access_key": "test",
    "region_name": AWS_REGION,
    "endpoint_url": "http://localhost:4566"
}

s3 = boto3.client("s3", **boto_config)
sqs = boto3.client("sqs", **boto_config)

# === Swagger Models ===
upload_response = ns.model('UploadResponse', {
    'message': fields.String(example='example.png uploaded and queued successfully')
})

upload_error = ns.model('UploadError', {
    'error': fields.String(example='No image file provided')
})

health_response = api.model('HealthCheck', {
    'status': fields.String(example='ok')
})

worker_response = api.model('ProcessStatus', {
    'worker': fields.String(example='running')
})

# === Routes ===

@api.route('/healthcheck')
class HealthCheck(Resource):
    """Check if the API is running properly"""
    @api.doc(description="Check if the service is alive")
    @api.response(200, 'Status OK', health_response)
    def get(self):
        return {"status": "ok"}, 200


@ns.route('/upload')
class UploadImage(Resource):
    """Uploads an image to S3 and notifies SQS queue"""
    @api.doc(
        description="Upload a PNG image and notify the processing queue",
        consumes=["multipart/form-data"],
        params={
            'image': {'description': 'PNG image file', 'in': 'formData', 'type': 'file', 'required': True}
        }
    )
    @api.response(201, 'Upload successful', upload_response)
    @api.response(400, 'No file provided', upload_error)
    def post(self):
        if 'image' not in request.files:
            logger.warning("Upload attempt with no file provided.")
            return {"error": "No image file provided"}, 400

        file = request.files['image']
        filename = file.filename

        if not filename.lower().endswith('.png'):
            return {"error": "Only PNG files are supported"}, 400

        upload_path = os.path.join('/tmp', filename)
        file.save(upload_path)
        logger.info(f"Image {filename} saved to {upload_path}")

        try:
            s3.upload_file(upload_path, BUCKET_INPUT, filename)
            logger.info(f"Image {filename} uploaded to S3 bucket {BUCKET_INPUT}")

            sqs.send_message(
                QueueUrl=QUEUE_URL,
                MessageBody=filename,
                MessageGroupId="image-processing"
            )
            logger.info(f"Message for {filename} sent to SQS queue")

            return {"message": f"{filename} uploaded and queued successfully"}, 201

        except (BotoCoreError, ClientError) as e:
            logger.error(f"Error uploading image or sending message: {e}")
            return {"error": str(e)}, 500


@api.route('/process')
class ProcessStatus(Resource):
    """Reports the status of the image worker"""
    @api.doc(description="Indicate that the worker is running")
    @api.response(200, 'Worker is running', worker_response)
    def get(self):
        return {"worker": "running"}, 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
