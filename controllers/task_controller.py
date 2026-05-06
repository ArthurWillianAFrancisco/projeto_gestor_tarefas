from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models.task_model import db, Task

# Blueprint para organizar as rotas[cite: 2]
task_bp = Blueprint('tasks', __name__)

@task_bp.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    try:
        data = request.get_json()
        user_id = get_jwt_identity() # Pega quem está logado[cite: 2]
        
        new_task = Task(
            title=data.get('title'),
            description=data.get('description'),
            user_id=user_id
        )
        
        db.session.add(new_task)
        db.session.commit()
        return jsonify({"msg": "Tarefa criada com sucesso!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": str(e)}), 500

@task_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    try:
        # Busca absolutamente tudo no banco[cite: 2]
        tasks = Task.query.all() 
        output = []
        for t in tasks:
            # Lógica simples para o nome do autor
            nome = "Sistema"
            if t.user:
                nome = t.user.username
                
            output.append({
                "id": t.id,
                "title": t.title,
                "description": t.description,
                "status": t.status,
                "username": nome
            })
        return jsonify(output), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@task_bp.route('/tasks/<int:id>', methods=['PUT'])
@jwt_required()
def update_task(id):
    try:
        task = Task.query.get_or_404(id)
        data = request.get_json()

        # Atualiza os campos[cite: 2]
        task.title = data.get('title', task.title)
        task.description = data.get('description', task.description)
        task.status = data.get('status', task.status)
        
        db.session.commit()
        return jsonify({"msg": "Atualizado!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": str(e)}), 500

@task_bp.route('/tasks/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_task(id):
    try:
        task = Task.query.get_or_404(id)
        db.session.delete(task)
        db.session.commit()
        return jsonify({"msg": "Excluído!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": str(e)}), 500