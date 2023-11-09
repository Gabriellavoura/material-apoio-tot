from flask import Flask, jsonify
from tools.listener import ProcessSQSListener
from env import *
import multiprocessing

app = Flask(__name__, instance_relative_config=False)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

@app.route('/', methods=['GET'])
def index():
    return jsonify({"status": "ok"}), 200

def sqs_pooling():
    process_listener = ProcessSQSListener(INPUT_QUEUE_NAME,
                                    endpoint_name=ENDPOINT_URL,
                                    queue_url=INPUT_QUEUE_URL,
                                    region_name=REGION,
                                    aws_access_key=KEY_ID,
                                    aws_secret_key=ACCESS_KEY,
                                    force_delete=True)
    
    process_listener.listen()
    
    return 

sqs_pooling_process = multiprocessing.Process(target=sqs_pooling)
sqs_pooling_process.start()