from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models.task_model import db, Task

# Criamos um Blueprint para organizar as rotas
task_bp = Blueprint('tasks', __name__)

@task_bp.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    data = request.get_json()
    current_user_id = get_jwt_identity() # Pega o ID do usuário do Token
    
    new_task = Task(
        title=data.get('title'),
        description=data.get('description'),
        user_id=current_user_id
    )
    
    db.session.add(new_task)
    db.session.commit()
    
    return jsonify({"msg": "Tarefa criada com sucesso!"}), 201

@task_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    current_user_id = get_jwt_identity()
    # Busca apenas as tarefas que pertencem ao usuário logado
    tasks = Task.query.filter_by(user_id=current_user_id).all()
    
    output = []
    for t in tasks:
        output.append({
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "status": t.status
        })
    
    return jsonify(output), 200

@task_bp.route('/tasks/<int:id>', methods=['PUT'])
@jwt_required()
def update_task(id):
    current_user_id = int(get_jwt_identity())
    # Esta é a linha que estava dando erro:
    user_role = get_jwt().get("role") 
    
    task = Task.query.get_or_404(id)

    if user_role != 'admin' and task.user_id != current_user_id:
        return jsonify({"msg": "Acesso negado"}), 403


    data = request.get_json()
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.status = data.get('status', task.status)
    
    db.session.commit()
    return jsonify({"msg": "Tarefa atualizada com sucesso!"}), 200

@task_bp.route('/tasks/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_task(id):
    current_user_id = int(get_jwt_identity())
    user_role = get_jwt().get("role")
    
    task = Task.query.get_or_404(id)

    # Bloqueia se não for o dono nem admin
    if user_role != 'admin' and task.user_id != current_user_id:
        return jsonify({"msg": "Acesso negado"}), 403

    db.session.delete(task)
    db.session.commit()
    return jsonify({"msg": "Tarefa excluída com sucesso!"}), 200