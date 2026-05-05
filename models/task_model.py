from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Inicializamos o db aqui, mas ele será ligado ao app no app.py
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='comum')  # 'admin' ou 'comum'

    # Relacionamento: Um usuário pode ter várias tarefas
    tasks = db.relationship('Task', backref='owner', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='pendente')  # pendente, fazendo, concluida
    
    # Chave Estrangeira: liga a tarefa a um usuário específico
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)