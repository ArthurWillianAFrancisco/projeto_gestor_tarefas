from flask import Flask
from flask_jwt_extended import JWTManager
from models.task_model import db
from controllers.task_controller import task_bp
from controllers.auth_controller import auth_bp
from datetime import timedelta
import os

app = Flask(__name__, static_folder='static')

# --- Configurações de Banco de Dados ---
database_url = os.getenv("DATABASE_URL", "sqlite:///gestor.db")

if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY", "sua_chave_secreta_padrao")

# --- AJUSTE PARA O ROBÔ: Token agora dura 24 horas ---
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# --- Inicialização ---
db.init_app(app)
jwt = JWTManager(app)

# Registro de Rotas
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(task_bp)

# --- BLOCO DE LIMPEZA (RODAR APENAS UMA VEZ) ---
with app.app_context():
    print("⚠️ OPERAÇÃO DE LIMPEZA INICIADA")
    db.drop_all()   # APAGA TUDO NO RENDER
    db.create_all() # RECRIA AS TABELAS LIMPAS
    print("✅ BANCO DE DADOS RESETADO COM SUCESSO")

@app.route('/')
def index():
    return {"message": "API de Gestão de Tarefas Ativa!"}, 200

@app.route('/login-page')
def serve_front():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True)