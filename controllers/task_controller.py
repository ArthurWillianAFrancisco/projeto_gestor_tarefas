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
    except:
        db.session.rollback()
        return jsonify({"msg": "erro"}), 500

@task_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    try:
        # Pega as informações extras do token (claims)
        claims = get_jwt()
        user_role = claims.get("role", "user")
        
        all_t = Task.query.all()
        output = []
        for x in all_t:
            # Lógica: Admin vê o nome do autor, User vê "Equipe" ou "Bot"
            autor = x.user.username if x.user else "Sistema"
            
            output.append({
                "id": x.id, 
                "title": x.title, 
                "description": x.description, 
                "status": x.status, 
                "username": autor if user_role == 'admin' else "Equipe"
            })
        return jsonify(output), 200
    except:
        return jsonify([]), 500

@task_bp.route('/tasks/<int:id>', methods=['PUT'])
@jwt_required()
def update_task(id):
    try:
        t = Task.query.get_or_404(id)
        data = request.get_json()
        
        # Qualquer usuário logado pode mover o card de status
        t.status = data.get('status', t.status)
        
        db.session.commit()
        return jsonify({"msg": "ok"}), 200
    except:
        db.session.rollback()
        return jsonify({"msg": "erro"}), 500

@task_bp.route('/tasks/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_task(id):
    try:
        # PEGAR IDENTIDADE E PAPEL (ROLE)
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        user_role = claims.get("role", "user")
        
        t = Task.query.get_or_404(id)
        
        # REGRA DE OURO: Se não for admin E não for o dono do card, bloqueia
        if user_role != 'admin' and t.user_id != current_user_id:
            return jsonify({"msg": "Acesso Negado: Apenas admins podem excluir cards alheios"}), 403
            
        db.session.delete(t)
        db.session.commit()
        return jsonify({"msg": "ok"}), 200
    except:
        db.session.rollback()
        return jsonify({"msg": "erro"}), 500