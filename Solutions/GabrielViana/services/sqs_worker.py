from .aws_service import AWSService
from .image_processor import ImageProcessor
import json
import time
import threading
from datetime import datetime
from flask import Flask

aws_service = AWSService()
image_processor = ImageProcessor()



def image_processing_worker(app: Flask):
    """Background worker that processes images from the SQS queue"""
    app.logger.info("🔄 Starting image processing worker...")
    
    while True:
        try:
            # Poll for messages from the input queue
            messages = aws_service.receive_sqs_messages('new-image-input.fifo', max_messages=1)
            
            if not messages:
                time.sleep(2)  # Wait before polling again
                continue
            
            for message in messages:
                try:
                    # Parse message body
                    message_body = json.loads(message['Body'])
                    image_id = message_body['image_id']
                    filename = message_body['filename']
                    
                    app.logger.info(f"📸 Processing image: {image_id}")
                    
                    # Download image from S3
                    image_data = aws_service.download_from_s3('image-input', filename)
                    if not image_data:
                        app.logger.error(f"Failed to download image: {filename}")
                        continue
                    
                    # Process image with OpenCV
                    processed_image_data = image_processor.process_image(image_data)
                    if not processed_image_data:
                        app.logger.error(f"Failed to process image: {filename}")
                        continue
                    
                    # Upload processed image to S3
                    processed_filename = f"processed_{filename}"
                    success = aws_service.upload_to_s3(
                        bucket_name='image-processed',
                        key=processed_filename,
                        file_content=processed_image_data,
                        content_type='image/png'
                    )
                    
                    if not success:
                        app.logger.error(f"Failed to upload processed image: {processed_filename}")
                        continue
                    
                    # Send completion message to output queue
                    completion_message = {
                        'image_id': image_id,
                        'original_filename': filename,
                        'processed_filename': processed_filename,
                        'processed_timestamp': datetime.utcnow().isoformat()
                    }
                    
                    aws_service.send_sqs_message(
                        queue_name='new-image-processed.fifo',
                        message_body=json.dumps(completion_message),
                        message_group_id='image-processing',
                        message_deduplication_id=f"processed_{image_id}"
                    )
                    
                    # Delete processed message from input queue
                    aws_service.delete_sqs_message('new-image-input.fifo', message['ReceiptHandle'])
                    
                    app.logger.info(f"✅ Successfully processed image: {image_id}")
                    
                except Exception as e:
                    app.logger.error(f"Error processing message: {str(e)}")
                    continue
                    
        except Exception as e:
            app.logger.error(f"Worker error: {str(e)}")
            time.sleep(5)  # Wait longer on error

def start_background_worker(app: Flask):
    """Start the background worker in a separate thread"""
    worker_thread = threading.Thread(target=image_processing_worker, daemon=True, args=(app,))
    worker_thread.start()
    app.logger.info("Background worker started")
