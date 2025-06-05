from flask import Flask
from routes import routes  # Só importa as rotas agora

app = Flask(__name__)
app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
