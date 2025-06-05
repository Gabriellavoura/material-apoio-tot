from app.utils.aws_helpers import s3, sqs, ensure_bucket_exists, ensure_queue_exists, process_image
import time

BUCKET_INPUT = "image-input"
BUCKET_OUTPUT = "image-processed"
SQS_QUEUE_URL = "http://localhost:4566/000000000000/new-image-input.fifo"
SQS_PROCESSED_URL = "http://localhost:4566/000000000000/new-image-processed.fifo"

def worker_loop():
    print("🔁 Worker started. Listening for messages...")

    while True:
        print(f"🕵️‍♂️ Checking for messages in queue: {SQS_QUEUE_URL}")
        response = sqs.receive_message(
            QueueUrl=SQS_QUEUE_URL,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=5
        )

        messages = response.get("Messages", [])
        if not messages:
            continue

        for msg in messages:
            receipt = msg["ReceiptHandle"]
            body = msg["Body"]
            filename = body.strip()

            print(f"📦 Message received: {filename}")

            obj = s3.get_object(Bucket=BUCKET_INPUT, Key=filename)
            original_bytes = obj["Body"].read()

            processed_bytes = process_image(original_bytes)

            s3.put_object(Bucket=BUCKET_OUTPUT, Key=filename, Body=processed_bytes)
            print(f"✅ Image processed and saved: {filename}")

            sqs.send_message(
                QueueUrl=SQS_PROCESSED_URL,
                MessageBody=filename,
                MessageGroupId="image-processing"
            )
            print(f"📨 Message sent to processed queue: {filename}")

            sqs.delete_message(QueueUrl=SQS_QUEUE_URL, ReceiptHandle=receipt)

        time.sleep(2)


if __name__ == "__main__":
    ensure_bucket_exists(BUCKET_INPUT)
    ensure_bucket_exists(BUCKET_OUTPUT)
    ensure_queue_exists(SQS_QUEUE_URL)
    ensure_queue_exists(SQS_PROCESSED_URL)
    worker_loop()
