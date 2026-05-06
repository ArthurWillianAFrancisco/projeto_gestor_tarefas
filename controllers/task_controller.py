from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models.task_model import db, Task

# Criamos um Blueprint para organizar as rotas
task_bp = Blueprint('tasks', __name__)

@task_bp.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    data = request.get_json()
    current_user_id = get_jwt_identity() # Pega o ID do usuário do Token[cite: 2]
    
    new_task = Task(
        title=data.get('title'),
        description=data.get('description'),
        user_id=current_user_id # Mantemos o registro de quem criou para fins de auditoria[cite: 2]
    )
    
    db.session.add(new_task)
    db.session.commit()
    
    return jsonify({"msg": "Tarefa criada com sucesso!"}), 201[cite: 2]

@task_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    # MUDANÇA CRÍTICA: Agora buscamos TODAS as tarefas do banco de dados,
    # independente de quem seja o dono (user_id).
    tasks = Task.query.all() 
    
    output = []
    for t in tasks:
        # Tentamos incluir o nome do autor do card para ficar bonito no Front-end
        autor = "Sistema"
        try:
            if t.user:
                autor = t.user.username
        except:
            pass

        output.append({
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "status": t.status,
            "username": autor # Enviamos o nome de quem criou (Arthur ou Robô)
        })
    
    return jsonify(output), 200

@task_bp.route('/tasks/<int:id>', methods=['PUT'])
@jwt_required()
def update_task(id):
    current_user_id = int(get_jwt_identity())[cite: 2]
    user_role = get_jwt().get("role")[cite: 2]
    
    task = Task.query.get_or_404(id)[cite: 2]

    # No modo colaborativo, permitimos que qualquer um edite (mude o status)
    # ou você pode manter a trava de Admin se preferir.
    if user_role != 'admin' and task.user_id != current_user_id:
        # Se quiser que todos possam mover cards uns dos outros, comente as linhas abaixo:
        # return jsonify({"msg": "Acesso negado"}), 403 
        pass

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

    # Para deletar, ainda é bom manter a segurança: apenas o dono ou o admin[cite: 2]
    if user_role != 'admin' and task.user_id != current_user_id:
        return jsonify({"msg": "Acesso negado"}), 403[cite: 2]

    db.session.delete(task)[cite: 2]
    db.session.commit()[cite: 2]
    return jsonify({"msg": "Tarefa excluída com sucesso!"}), 200[cite: 2]