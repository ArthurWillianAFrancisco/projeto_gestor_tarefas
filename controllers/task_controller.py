from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models.task_model import db, Task

task_bp = Blueprint('tasks', __name__)[cite: 2]

@task_bp.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    data = request.get_json()[cite: 2]
    current_user_id = get_jwt_identity()[cite: 2]
    
    new_task = Task(
        title=data.get('title'),
        description=data.get('description'),
        user_id=current_user_id[cite: 2]
    )
    
    db.session.add(new_task)[cite: 2]
    db.session.commit()[cite: 2]
    
    return jsonify({"msg": "Tarefa criada com sucesso!"}), 201[cite: 2]

@task_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    # Busca todas as tarefas para o dashboard colaborativo
    tasks = Task.query.all() 
    
    output = []
    for t in tasks:
        # PROTEÇÃO CONTRA ERRO 500:
        # Verificamos se o objeto 'user' existe antes de pedir o 'username'
        autor_nome = "Sistema"
        if hasattr(t, 'user') and t.user is not None:
            autor_nome = t.user.username

        output.append({
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "status": t.status,
            "username": autor_nome
        })
    
    return jsonify(output), 200

@task_bp.route('/tasks/<int:id>', methods=['PUT'])
@jwt_required()
def update_task(id):
    current_user_id = int(get_jwt_identity())[cite: 2]
    user_role = get_jwt().get("role")[cite: 2]
    
    task = Task.query.get_or_404(id)[cite: 2]

    # Permitir que qualquer um logado atualize o status dos alertas
    data = request.get_json()[cite: 2]
    task.title = data.get('title', task.title)[cite: 2]
    task.description = data.get('description', task.description)[cite: 2]
    task.status = data.get('status', task.status)[cite: 2]
    
    db.session.commit()[cite: 2]
    return jsonify({"msg": "Tarefa atualizada com sucesso!"}), 200[cite: 2]

@task_bp.route('/tasks/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_task(id):
    current_user_id = int(get_jwt_identity())[cite: 2]
    user_role = get_jwt().get("role")[cite: 2]
    
    task = Task.query.get_or_404(id)[cite: 2]

    # Segurança: Apenas o dono ou admin pode excluir permanentemente
    if user_role != 'admin' and task.user_id != current_user_id:
        return jsonify({"msg": "Acesso negado"}), 403[cite: 2]

    db.session.delete(task)[cite: 2]
    db.session.commit()[cite: 2]
    return jsonify({"msg": "Tarefa excluída com sucesso!"}), 200[cite: 2]