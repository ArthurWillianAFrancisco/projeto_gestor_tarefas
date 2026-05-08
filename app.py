from flask import Flask
from flask_jwt_extended import JWTManager
from models.task_model import db
from controllers.task_controller import task_bp
from controllers.auth_controller import auth_bp
from datetime import timedelta
import os

app = Flask(__name__, static_folder='static')

database_url = os.getenv("DATABASE_URL", "sqlite:///gestor.db")
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY", "sua_chave_secreta_padrao")
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

db.init_app(app)
jwt = JWTManager(app)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(task_bp)

# Cria as tabelas no banco novo assim que o site ligar
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return {"message": "Aegis SOC Online - Banco Novo"}, 200

@app.route('/login-page')
def serve_front():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True)