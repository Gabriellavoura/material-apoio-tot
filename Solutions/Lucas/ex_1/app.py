from flask    import Flask, request
from handlers import healthcheck_handler
from handlers import pooling_handler
from handlers import input_sqs

# Flask app
app = Flask(__name__)

# Pooling URL
@app.route('/', methods=['POST'])
def pooling():
    return pooling_handler.handle()

# Input in list URL
@app.route('/input', methods=['POST'])
def input():
    return input_sqs.handle()

# Healthcheck URL
@app.route('/health', methods=['GET'])
def healthcheck():
    return healthcheck_handler.handle()

# Flask server in debug mode
""" if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) """
