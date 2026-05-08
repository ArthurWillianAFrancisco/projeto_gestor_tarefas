from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models.task_model import db, Task

task_bp = Blueprint('tasks', __name__)

@task_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    try:
        # A MÁGICA ESTÁ AQUI: .order_by(Task.id.asc()) 
        # Garante que o card 1 venha antes do 2, sempre.
        all_t = Task.query.order_by(Task.id.asc()).all()
        
        return jsonify([{
            "id": x.id, 
            "title": x.title, 
            "description": x.description,
            "status": x.status, 
            "username": x.owner.username if x.owner else "Sistema"
        } for x in all_t]), 200
    except:
        return jsonify([]), 200

@task_bp.route('/tasks/<int:id>', methods=['PUT'])
@jwt_required()
def update_task(id):
    try:
        t = Task.query.get_or_404(id)
        data = request.get_json()
        
        if 'status' in data: t.status = data['status']
        if 'description' in data: t.description = data['description']
        if 'title' in data: t.title = data['title']
        
        db.session.commit()
        return jsonify({"msg": "Atualizado"}), 200
    except:
        db.session.rollback()
        return jsonify({"msg": "Erro ao atualizar"}), 500

@task_bp.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    try:
        data = request.get_json()
        u_id = get_jwt_identity()
        t = Task(title=data.get('title'), description=data.get('description'), 
                 status=data.get('status', 'pendente'), user_id=u_id)
        db.session.add(t)
        db.session.commit()
        return jsonify({"msg": "Criado"}), 201
    except:
        db.session.rollback()
        return jsonify({"msg": "Erro"}), 500

@task_bp.route('/tasks/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_task(id):
    try:
        t = Task.query.get_or_404(id)
        db.session.delete(t)
        db.session.commit()
        return jsonify({"msg": "Removido"}), 200
    except:
        return jsonify({"msg": "Erro"}), 500