from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from models.task_model import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get('username')).first()
    if user and user.check_password(data.get('password')):
        # Incluímos a role no token para controle de acesso
        token = create_access_token(identity=str(user.id), additional_claims={"role": user.role})
        return jsonify({"access_token": token, "role": user.role, "username": user.username}), 200
    return jsonify({"msg": "Falha na autenticação"}), 401

@auth_bp.route('/register', methods=['POST'])
@jwt_required()
def register():
    claims = get_jwt()
    # TRAVA: Se não for admin, não registra ninguém
    if claims.get("role") != 'admin':
        return jsonify({"msg": "Acesso negado: Apenas administradores podem criar operadores"}), 403
    
    data = request.get_json()
    if User.query.filter_by(username=data.get('username')).first():
        return jsonify({"msg": "Usuário já existe"}), 400
    
    new_user = User(username=data.get('username'), role=data.get('role', 'comum'))
    new_user.set_password(data.get('password'))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "Novo operador registrado com sucesso"}), 201