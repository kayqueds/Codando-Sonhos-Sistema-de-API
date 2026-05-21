from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from src.models.user import User
from src.models import db

auth_bp = Blueprint('auth', __name__)


def _validate_registration(data):
    errors = []
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    name = data.get('name', '').strip()

    if not name:
        errors.append('Nome é obrigatório.')
    if not email:
        errors.append('Email é obrigatório.')
    if not password:
        errors.append('Senha é obrigatória.')
    if password and len(password) < 8:
        errors.append('A senha deve ter ao menos 8 caracteres.')
    if password and password.isalpha():
        errors.append('A senha deve conter letras e números.')
    return errors


@auth_bp.route('/register', methods=['POST'])
def register():
    payload = request.get_json(force=True, silent=True) or {}
    errors = _validate_registration(payload)
    if errors:
        return jsonify({'errors': errors}), 400

    email = payload['email'].strip().lower()
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email já cadastrado.'}), 409

    user = User(name=payload['name'].strip(), email=email)
    user.set_password(payload['password'])
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'Usuário criado com sucesso.', 'user': user.to_dict()}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    payload = request.get_json(force=True, silent=True) or {}
    email = payload.get('email', '').strip().lower()
    password = payload.get('password', '')

    if not email or not password:
        return jsonify({'message': 'Email e senha são obrigatórios.'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'message': 'Email ou senha inválidos.'}), 401

    token = create_access_token(identity=str(user.id))
    return jsonify({'access_token': token, 'user': user.to_dict()}), 200
