from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from src.models.user import User
from src.models import db

users_bp = Blueprint('users', __name__)


def _validate_user_update(data):
    errors = []
    if 'email' in data and not data['email'].strip():
        errors.append('Email não pode ser vazio.')
    if 'name' in data and not data['name'].strip():
        errors.append('Nome não pode ser vazio.')
    if 'password' in data:
        password = data['password']
        if len(password) < 8:
            errors.append('A senha deve ter ao menos 8 caracteres.')
        if password.isalpha():
            errors.append('A senha deve conter letras e números.')
    return errors


@users_bp.route('', methods=['GET'])
@jwt_required()
def list_users():
    users = User.query.all()
    return jsonify({'users': [user.to_dict() for user in users]}), 200


@users_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    current_user_id = int(get_jwt_identity())
    if current_user_id != user_id:
        return jsonify({'message': 'Acesso negado.'}), 403

    user = User.query.get_or_404(user_id)
    return jsonify({'user': user.to_dict()}), 200


@users_bp.route('/<int:user_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_user(user_id):
    current_user_id = int(get_jwt_identity())
    if current_user_id != user_id:
        return jsonify({'message': 'Acesso negado.'}), 403

    user = User.query.get_or_404(user_id)
    payload = request.get_json(force=True, silent=True) or {}
    errors = _validate_user_update(payload)
    if errors:
        return jsonify({'errors': errors}), 400

    if 'email' in payload:
        email = payload['email'].strip().lower()
        if email != user.email and User.query.filter_by(email=email).first():
            return jsonify({'message': 'Email já cadastrado.'}), 409
        user.email = email
    if 'name' in payload:
        user.name = payload['name'].strip()
    if 'password' in payload:
        user.set_password(payload['password'])

    db.session.commit()
    return jsonify({'message': 'Dados atualizados com sucesso.', 'user': user.to_dict()}), 200


@users_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    current_user_id = int(get_jwt_identity())
    if current_user_id != user_id:
        return jsonify({'message': 'Acesso negado.'}), 403

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'Usuário excluído com sucesso.'}), 200
