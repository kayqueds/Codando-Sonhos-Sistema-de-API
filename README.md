# Codando Sonhos - Sistema de Gestão de Usuários e Filmes Favoritos

## 📋 Projeto Acadêmico - Quality Assurance (QA)

**Disciplina**: Quality Assurance  
**Objetivo**: Demonstrar testes de API, testes automatizados, validações e controle de qualidade

**Desenvolvedores:**
- André de Queiroz Cenaque - 86717
- Kayque Estevão de Queiroga - 89632
- Luís Henrique do Carmo Santos - 7722
- Marina Duarte Cabral - 94306

---

## 🎯 Funcionalidades Principais

### ✅ Autenticação
- Cadastro de usuário com validação
- Login com JWT
- Criptografia de senha com Werkzeug
- Token de acesso para requisições protegidas

### ✅ Gerenciamento de Usuários
- Criar, ler, atualizar e deletar usuários
- Controle de acesso (usuários veem apenas seus dados)
- Validação de email único
- Status HTTP adequados

### ✅ Filmes Favoritos
- Adicionar filmes favoritos vinculados ao usuário
- Listar filmes do usuário logado
- Atualizar e deletar filmes
- Isolamento completo por usuário

### ✅ Interface Visual
- Tela inicial com apresentação
- Cadastro responsivo
- Login com armazenamento de JWT
- Dashboard personalizado
- Gerenciador de filmes favoritos

---

## 🚀 Como Rodar o Projeto

### Pré-requisitos
- Python 3.14+
- MySQL instalado
- Git

### Instalação Rápida

```bash
# 1. Clonar repositório
git clone https://github.com/kayqueds/Codando-Sonhos-Sistema-de-API.git
cd Codando-Sonhos-Sistema-de-API

# 2. Criar ambiente virtual
python -m venv venv
venv\Scripts\activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Configurar .env (copiar src/.env.example)
DB_USER=root
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=3306
DB_NAME=sistema_api

# 5. Executar script SQL no Workbench
# Abra MySQL Workbench e execute: src/database/sistema_api.sql

# 6. Rodar a aplicação
python -m src.app

# Acesse: http://127.0.0.1:5000
```

---

## 🧪 Testes e QA

### Testes Automatizados (Pytest)
```bash
# Rodar todos os testes
python -m pytest tests/test_app.py -v

# Rodar teste específico
python -m pytest tests/test_app.py::test_register_and_login -v
```

**Cobertura de Testes:**
- ✅ Cadastro e login
- ✅ Autenticação obrigatória
- ✅ Controle de acesso
- ✅ CRUD de usuários
- ✅ CRUD de filmes
- ✅ Isolamento de dados

### Testes de API (Postman)
1. Importe: `postman/API_Collection.json`
2. Siga os exemplos de requisição
3. Verifique respostas JSON e status HTTP

### Testes Manuais
Veja `docs/TESTES_MANUAIS.md` para guia completo

---

## 📊 Estrutura do Projeto

```
Projeto_QA/
├── src/
│   ├── app.py              # Factory pattern Flask
│   ├── config.py           # Config BD
│   ├── models/
│   │   ├── user.py         # Model User + relacionamento
│   │   └── movie.py        # Model Movie
│   ├── routes/
│   │   ├── auth.py         # POST /auth/register, /auth/login
│   │   ├── users.py        # CRUD usuários
│   │   └── movies.py       # CRUD filmes
│   └── database/
│       └── sistema_api.sql # Script SQL
├── templates/              # HTML (Tailwind + CSS)
├── static/css/             # Estilos customizados
├── tests/test_app.py       # Pytest (8 testes)
├── postman/                # Coleção Postman
├── docs/                   # Documentação completa
├── evidencias/             # Screenshots e logs
├── .env                    # Variáveis ambiente
├── requirements.txt        # Dependências
└── README.md              # Este arquivo
```

---

## 📝 Rotas da API

### Autenticação
- `POST /auth/register` - Criar usuário
- `POST /auth/login` - Fazer login (retorna token JWT)

### Usuários (requer JWT)
- `GET /users` - Listar usuários
- `GET /users/<id>` - Detalhes do usuário
- `PUT /users/<id>` - Atualizar usuário
- `DELETE /users/<id>` - Deletar usuário

### Filmes (requer JWT)
- `POST /movies` - Criar filme favorito
- `GET /movies` - Listar filmes do usuário
- `GET /movies/<id>` - Detalhes do filme
- `PUT /movies/<id>` - Atualizar filme
- `DELETE /movies/<id>` - Deletar filme

### Web (Frontend)
- `GET /` - Home
- `GET /register-page` - Tela de cadastro
- `GET /login-page` - Tela de login
- `GET /dashboard` - Dashboard (após login)
- `GET /movies-page` - Gerenciar filmes

---

## 🔐 Segurança

### Validações Implementadas
- ✅ Email único
- ✅ Senha mínima 8 caracteres + letras + números
- ✅ Título de filme obrigatório
- ✅ JWT obrigatório em rotas protegidas

### Controle de Acesso
- ✅ Usuário A não vê dados do usuário B
- ✅ Usuário A não pode editar/deletar dados de B
- ✅ Isolamento completo de filmes

---

## 📖 Documentação Completa

Veja a pasta `docs/` para:
- **TESTES_MANUAIS.md** - Como testar manualmente
- **ANALISE_RESULTADOS.md** - Resultados dos testes
- **MELHORIAS_SUGERIDAS.md** - Possíveis melhorias
- **BUGS_ENCONTRADOS.md** - Bugs corrigidos

---

## ✨ Exemplos de Requisições

### Cadastro
```bash
curl -X POST http://127.0.0.1:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "João",
    "email": "joao@example.com",
    "password": "Senha123"
  }'
```

### Login
```bash
curl -X POST http://127.0.0.1:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "joao@example.com",
    "password": "Senha123"
  }'
# Resposta: {"access_token": "eyJ...", "user": {...}}
```

### Listar Filmes
```bash
curl -X GET http://127.0.0.1:5000/movies \
  -H "Authorization: Bearer {access_token}"
```

---

## 🐛 Bugs Encontrados e Resolvidos

1. **JWT Identity Type** - Integer vs String ✅
2. **Imports de Blueprints** - Factory pattern ✅

Veja `docs/BUGS_ENCONTRADOS.md` para detalhes

---

**Status**: ✅ Projeto Completo  
**Data**: 3 de maio de 2026  
**Repositório**: https://github.com/kayqueds/Codando-Sonhos-Sistema-de-API

















