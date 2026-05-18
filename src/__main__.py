"""
Executar: python -m src
ou: python -m src.app (ambos funcionam)
"""

from src.app import create_app
from src.models import db

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    print("🚀 Servidor iniciando em http://127.0.0.1:5000")
    app.run(debug=True)
