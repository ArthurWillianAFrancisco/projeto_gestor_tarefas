from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models.task_model import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'comum') # Padrão é comum, mas pode ser 'admin'

    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "Usuário já existe"}), 400

    new_user = User(username=username, role=role)
    new_user.set_password(password) # Criptografa a senha usando bcrypt/werkzeug
    
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "Usuário criado com sucesso!"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get('username')).first()

    if user and user.check_password(data.get('password')):
        # O token armazena o ID e a Role do usuário para autorização posterior[cite: 1]
        additional_claims = {"role": user.role}
        access_token = create_access_token(identity=str(user.id), additional_claims=additional_claims)
        return jsonify(access_token=access_token), 200

    return jsonify({"msg": "Usuário ou senha inválidos"}), 401