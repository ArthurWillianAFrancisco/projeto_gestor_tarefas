from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models.task_model import db, Task # Importa do model para evitar o erro circular

task_bp = Blueprint('tasks', __name__)

@task_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    try:
        claims = get_jwt()
        user_role = claims.get("role", "user")
        all_t = Task.query.all()
        output = []
        
        for x in all_t:
            try:
                # Usa 'owner' definido no relacionamento do model
                autor = x.owner.username if x.owner else "Sistema"
                output.append({
                    "id": x.id, 
                    "title": x.title, 
                    "description": x.description, 
                    "status": x.status, 
                    "username": autor if user_role == 'admin' else "Equipe"
                })
            except:
                continue
        return jsonify(output), 200
    except:
        return jsonify([]), 200

@task_bp.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    try:
        data = request.get_json()
        u_id = get_jwt_identity()
        t = Task(title=data.get('title'), description=data.get('description'), user_id=u_id)
        db.session.add(t)
        db.session.commit()
        return jsonify({"msg": "ok"}), 201
    except:
        db.session.rollback()
        return jsonify({"msg": "erro"}), 500

@task_bp.route('/tasks/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_task(id):
    try:
        t = Task.query.get_or_404(id)
        db.session.delete(t)
        db.session.commit()
        return jsonify({"msg": "ok"}), 200
    except:
        db.session.rollback()
        return jsonify({"msg": "erro"}), 500