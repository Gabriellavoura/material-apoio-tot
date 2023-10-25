from flask import Flask, jsonify
from app.env import *
from app.src.handler import *
from app.tools.aws_utility import *
from app.tools.listener import ProcessSQSListener
import multiprocessing
import requests
import json


def process():
    process_listener = ProcessSQSListener("inputQueue",
                                          endpoint_name = ENDPOINT_URL,
                                          aws_access_key= AWS_ACCESS_KEY_ID,
                                          aws_secret_key= AWS_SECRET_ACCESS_KEY,
                                          queue_url= INPUT_QUEUE_URL,
                                          region_name= REGION_NAME,
                                          force_delete= True)
    process_listener.listen()

app = Flask(__name__, instance_relative_config=False)

@app.route('/', methods=['GET'])
def receive_message():
    return jsonify({'main': 'running'}), 200

@app.route("/health")
def health():
    try:
        s3_client = instantiate_aws_client('s3')
        sqs_client = instantiate_aws_client('sqs')
        response = requests.get('http://host.docker.internal:4566/health')
        data = json.loads(response.text)
        services = data['services']
        active_services = {'sqs': services['sqs'], 's3': services['s3']}

        buckets_names = list_buckets_names(s3_client)

        buckets_keys = {}
        for name in buckets_names:
            buckets_keys[name] = list_buckets_content_keys(s3_client, name)

        queues = list_queues(sqs_client)

        return jsonify({'health': active_services, 'buckets': buckets_keys, 'queues': queues}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

sqs_polling_process = multiprocessing.Process(target=process)
sqs_polling_process.start()