"""
Script de Inicialização do Banco de Dados

Este script cria as tabelas (User e Movie) no banco de dados MySQL
usando SQLAlchemy. Execute este arquivo antes de rodar o aplicativo
pela primeira vez.

Uso:
    python init_db.py

O script irá:
1. Verificar a conexão com o MySQL
2. Criar o banco de dados (se não existir)
3. Criar as tabelas User e Movie
4. Exibir confirmação do sucesso
"""

import os
from dotenv import load_dotenv
from src.app import create_app
from src.models import db

# Carregar variáveis de ambiente
load_dotenv()


def init_database():
    """Inicializa as tabelas do banco de dados."""
    print("🔧 Inicializando banco de dados...")
    
    # Criar aplicação
    app = create_app()
    
    with app.app_context():
        try:
            print("✓ Conexão com banco de dados estabelecida")
            
            # Criar todas as tabelas
            db.create_all()
            print("✓ Tabelas criadas com sucesso!")
            
            print("\n📊 Tabelas criadas:")
            print("  - users (id, name, email, password_hash, created_at)")
            print("  - movies (id, title, description, user_id, created_at)")
            
            print("\n✅ Banco de dados inicializado com sucesso!")
            print("\nAgora você pode executar:")
            print("  python -m src.app  (para rodar o servidor)")
            
        except Exception as e:
            print(f"\n❌ Erro ao inicializar banco de dados:")
            print(f"   {str(e)}")
            print("\nVerifique:")
            print("  1. Se o MySQL está rodando")
            print("  2. Se as credenciais em .env estão corretas")
            print("  3. Se o banco de dados 'sistema_api' existe")
            return False
    
    return True


if __name__ == '__main__':
    success = init_database()
    exit(0 if success else 1)
