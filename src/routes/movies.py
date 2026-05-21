from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from src.models.movie import Movie
from src.models import db

movies_bp = Blueprint('movies', __name__)


def _validate_movie_data(data):
    errors = []
    title = data.get('title', '').strip()
    if not title:
        errors.append('Título é obrigatório.')
    if len(title) > 255:
        errors.append('Título deve ter no máximo 255 caracteres.')
    description = data.get('description', '')
    if description and len(description) > 1000:
        errors.append('Descrição deve ter no máximo 1000 caracteres.')
    return errors


@movies_bp.route('', methods=['POST'])
@jwt_required()
def create_movie():
    current_user_id = int(get_jwt_identity())
    payload = request.get_json(force=True, silent=True) or {}
    errors = _validate_movie_data(payload)
    if errors:
        return jsonify({'errors': errors}), 400

    movie = Movie(
        title=payload['title'].strip(),
        description=payload.get('description', '').strip(),
        user_id=current_user_id
    )
    db.session.add(movie)
    db.session.commit()

    return jsonify({'message': 'Filme criado com sucesso.', 'movie': movie.to_dict()}), 201


@movies_bp.route('', methods=['GET'])
@jwt_required()
def list_movies():
    current_user_id = int(get_jwt_identity())
    movies = Movie.query.filter_by(user_id=current_user_id).all()
    return jsonify({'movies': [movie.to_dict() for movie in movies]}), 200


@movies_bp.route('/<int:movie_id>', methods=['GET'])
@jwt_required()
def get_movie(movie_id):
    current_user_id = int(get_jwt_identity())
    movie = Movie.query.filter_by(id=movie_id, user_id=current_user_id).first_or_404()
    return jsonify({'movie': movie.to_dict()}), 200


@movies_bp.route('/<int:movie_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_movie(movie_id):
    current_user_id = int(get_jwt_identity())
    movie = Movie.query.filter_by(id=movie_id, user_id=current_user_id).first_or_404()
    payload = request.get_json(force=True, silent=True) or {}
    errors = _validate_movie_data(payload)
    if errors:
        return jsonify({'errors': errors}), 400

    movie.title = payload['title'].strip()
    movie.description = payload.get('description', '').strip()
    db.session.commit()

    return jsonify({'message': 'Filme atualizado com sucesso.', 'movie': movie.to_dict()}), 200


@movies_bp.route('/<int:movie_id>', methods=['DELETE'])
@jwt_required()
def delete_movie(movie_id):
    current_user_id = int(get_jwt_identity())
    movie = Movie.query.filter_by(id=movie_id, user_id=current_user_id).first_or_404()
    db.session.delete(movie)
    db.session.commit()

    return jsonify({'message': 'Filme excluído com sucesso.'}), 200