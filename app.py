from flask import Flask
from flask_jwt_extended import JWTManager
from models.task_model import db, User
from controllers.task_controller import task_bp
from controllers.auth_controller import auth_bp
from datetime import timedelta
import os

# 1. CRIAR O APP PRIMEIRO (Resolve o NameError)
app = Flask(__name__, static_folder='static')

# 2. CONFIGURAÇÕES
database_url = os.getenv("DATABASE_URL", "sqlite:///gestor.db")
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY", "chave-aegis-soc")
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# 3. INICIALIZAÇÃO
db.init_app(app)
jwt = JWTManager(app)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(task_bp)

# 4. CONTEXTO DO APP (Agora o 'app' já existe!)
with app.app_context():
    db.create_all()
    # Criar Admin Root se o banco estiver vazio
    if not User.query.filter_by(role='admin').first():
        admin = User(username="admin", role="admin")
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin Root criado: admin / admin123")

@app.route('/')
def index():
    return {"status": "Aegis SOC Online"}, 200

@app.route('/login-page')
def serve_front():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True)