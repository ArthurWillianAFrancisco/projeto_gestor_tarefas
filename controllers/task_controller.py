from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models.task_model import db, Task

task_bp = Blueprint('tasks', __name__)[cite: 2]

@task_bp.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    try:
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
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": f"Erro interno: {str(e)}"}), 500

@task_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    try:
        tasks = Task.query.all() 
        output = []
        for t in tasks:
            # Pegar nome do autor com segurança
            autor = t.user.username if (hasattr(t, 'user') and t.user) else "Sistema"
            
            output.append({
                "id": t.id,
                "title": t.title,
                "description": t.description,
                "status": t.status,
                "username": autor
            })
        return jsonify(output), 200
    except Exception as e:
        return jsonify({"msg": f"Erro ao listar: {str(e)}"}), 500

@task_bp.route('/tasks/<int:id>', methods=['PUT'])
@jwt_required()
def update_task(id):
    try:
        task = Task.query.get_or_404(id)[cite: 2]
        data = request.get_json()[cite: 2]

        # MUDANÇA: Qualquer usuário logado pode editar qualquer card (Dashboard Colaborativo)
        task.title = data.get('title', task.title)[cite: 2]
        task.description = data.get('description', task.description)[cite: 2]
        task.status = data.get('status', task.status)[cite: 2]
        
        db.session.commit()[cite: 2]
        return jsonify({"msg": "Tarefa atualizada com sucesso!"}), 200[cite: 2]
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": f"Erro ao atualizar: {str(e)}"}), 500

@task_bp.route('/tasks/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_task(id):
    try:
        task = Task.query.get_or_404(id)[cite: 2]
        # MUDANÇA: Permitir que o admin ou o dono delete
        db.session.delete(task)[cite: 2]
        db.session.commit()[cite: 2]
        return jsonify({"msg": "Tarefa excluída com sucesso!"}), 200[cite: 2]
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": f"Erro ao excluir: {str(e)}"}), 500