import os
from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from flask_jwt_extended import JWTManager
from src.config import Config
from src.models import db
from src.routes import auth_bp, users_bp, movies_bp


def create_app(test_config=None):
    # Definir caminhos corretos para templates e static
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    template_folder = os.path.join(basedir, 'templates')
    static_folder = os.path.join(basedir, 'static')
    
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder, instance_relative_config=False)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    jwt = JWTManager()
    jwt.init_app(app)

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(movies_bp, url_prefix='/movies')

    # ===== ROTAS WEB (Renderizam HTML) =====
    
    @app.route('/')
    def home():
        """Página inicial do projeto."""
        return render_template('home.html')

    @app.route('/register-page')
    def register_page():
        """Página de cadastro."""
        return render_template('register.html')

    @app.route('/login-page')
    def login_page():
        """Página de login."""
        return render_template('login.html')

    @app.route('/dashboard')
    def dashboard():
        """Dashboard do usuário logado."""
        return render_template('dashboard.html')

    @app.route('/movies-page')
    def movies_page():
        """Página de gerenciamento de filmes."""
        return render_template('movies.html')

    # ===== TRATADORES DE ERRO =====

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

    