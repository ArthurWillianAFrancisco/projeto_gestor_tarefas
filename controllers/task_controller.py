from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.task_model import db, Task

task_bp = Blueprint('tasks', __name__)

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
        return jsonify({"msg": "erro"}), 500

@task_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    try:
        all_t = Task.query.all()
        return jsonify([{"id": x.id, "title": x.title, "description": x.description, "status": x.status, "username": "Admin"} for x in all_t]), 200
    except:
        return jsonify([]), 500

@task_bp.route('/tasks/<int:id>', methods=['PUT'])
@jwt_required()
def update_task(id):
    try:
        t = Task.query.get_or_404(id)
        data = request.get_json()
        t.status = data.get('status', t.status)
        db.session.commit()
        return jsonify({"msg": "ok"}), 200
    except:
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
        return jsonify({"msg": "erro"}), 500