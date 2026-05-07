from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models.task_model import db, Task

task_bp = Blueprint('tasks', __name__)

@task_bp.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    try:
        data = request.get_json()
        u_id = get_jwt_identity()
        t = Task(
            title=data.get('title'), 
            description=data.get('description'), 
            user_id=u_id
        )
        db.session.add(t)
        db.session.commit()
        return jsonify({"msg": "ok"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": str(e)}), 500

@task_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    try:
        claims = get_jwt()
        user_role = claims.get("role", "user")
        
        all_t = Task.query.all()
        output = []
        for x in all_t:
            # BLINDAGEM: Se o card não tiver dono (user_id nulo), define como 'Sistema'
            # Isso evita o Erro 500 que você está vendo
            autor = "Sistema"
            if x.user and x.user.username:
                autor = x.user.username
            
            output.append({
                "id": x.id, 
                "title": x.title, 
                "description": x.description, 
                "status": x.status, 
                "username": autor if user_role == 'admin' else "Equipe"
            })
        return jsonify(output), 200
    except Exception as e:
        # Se der erro, ele vai imprimir no log do Render o motivo exato
        print(f"Erro no GET tasks: {e}")
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
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": str(e)}), 500

@task_bp.route('/tasks/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_task(id):
    try:
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        user_role = claims.get("role", "user")
        
        t = Task.query.get_or_404(id)
        
        if user_role != 'admin' and t.user_id != current_user_id:
            return jsonify({"msg": "Acesso Negado"}), 403
            
        db.session.delete(t)
        db.session.commit()
        return jsonify({"msg": "ok"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": str(e)}), 500