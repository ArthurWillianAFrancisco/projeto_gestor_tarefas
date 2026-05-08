from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from models.task_model import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get('username')).first()
    if user and user.check_password(data.get('password')):
        # O token agora leva o "role" para o front-end saber quem é admin
        token = create_access_token(identity=user.id, additional_claims={"role": user.role})
        return jsonify({"token": token, "role": user.role, "username": user.username}), 200
    return jsonify({"msg": "Credenciais inválidas"}), 401

@auth_bp.route('/register', methods=['POST'])
@jwt_required()
def register():
    claims = get_jwt()
    if claims.get("role") != 'admin':
        return jsonify({"msg": "Acesso negado: Apenas administradores podem criar usuários"}), 403
    
    data = request.get_json()
    if User.query.filter_by(username=data.get('username')).first():
        return jsonify({"msg": "Usuário já existe"}), 400
    
    new_user = User(username=data.get('username'), role=data.get('role', 'comum'))
    new_user.set_password(data.get('password'))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "Usuário criado com sucesso"}), 201

@auth_bp.route('/users', methods=['GET'])
@jwt_required()
def list_users():
    claims = get_jwt()
    if claims.get("role") != 'admin':
        return jsonify({"msg": "Acesso negado"}), 403
    users = User.query.all()
    return jsonify([{"id": u.id, "username": u.username, "role": u.role} for u in users]), 200

@auth_bp.route('/users/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    claims = get_jwt()
    if claims.get("role") != 'admin':
        return jsonify({"msg": "Acesso negado"}), 403
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"msg": "Usuário removido"}), 200