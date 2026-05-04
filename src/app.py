from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from src.config import Config
from src.models import db
from src.routes import auth_bp, users_bp


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    jwt = JWTManager()
    jwt.init_app(app)

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(users_bp, url_prefix='/users')

    @app.route('/')
    def principal():
        return jsonify({'message': 'API de usuários em Flask'}), 200

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'message': 'Recurso não encontrado.'}), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'message': 'Requisição inválida.'}), 400

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'message': 'Erro interno do servidor.'}), 500

    return app


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)

    