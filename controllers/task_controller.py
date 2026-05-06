from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.task_model import db, Task

task_bp = Blueprint('tasks', __name__)[cite: 2]

@task_bp.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    try:
        data = request.get_json()
        user_id = get_jwt_identity()[cite: 2]
        new_task = Task(
            title=data.get('title'),
            description=data.get('description'),
            user_id=user_id
        )
        db.session.add(new_task)
        db.session.commit()
        return jsonify({"msg": "Sucesso"}), 201[cite: 2]
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": str(e)}), 500

@task_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    try:
        tasks = Task.query.all()[cite: 2]
        output = []
        for t in tasks:
            # Simplificação máxima para evitar erro 500
            output.append({
                "id": t.id,
                "title": t.title,
                "description": t.description,
                "status": t.status,
                "username": "Operador"
            })
        return jsonify(output), 200[cite: 2]
    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@task_bp.route('/tasks/<int:id>', methods=['PUT'])
@jwt_required()
def update_task(id):
    try:
        task = Task.query.get_or_404(id)[cite: 2]
        data = request.get_json()
        task.title = data.get('title', task.title)
        task.description = data.get('description', task.description)
        task.status = data.get('status', task.status)
        db.session.commit()
        return jsonify({"msg": "Ok"}), 200[cite: 2]
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": str(e)}), 500

@task_bp.route('/tasks/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_task(id):
    try:
        task = Task.query.get_or_404(id)[cite: 2]
        db.session.delete(task)
        db.session.commit()
        return jsonify({"msg": "Ok"}), 200[cite: 2]
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": str(e)}), 500