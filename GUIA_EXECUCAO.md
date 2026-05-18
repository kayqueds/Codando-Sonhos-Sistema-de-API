% COMO EXECUTAR O PROJETO - GUIA COMPLETO

## 🎯 Visão Geral

Este projeto é um **Sistema de Gerenciamento de Usuários e Filmes** com:
- ✅ API REST com JWT (JSON Web Tokens)
- ✅ Banco de dados MySQL com SQLAlchemy
- ✅ Interface web com HTML, CSS e Tailwind
- ✅ Integração JavaScript com fetch API
- ✅ Autenticação com localStorage

---

## 📋 PRÉ-REQUISITOS

Antes de começar, certifique-se de ter instalado:

### 1. **Python 3.8+**
```bash
python --version
# Deve retornar: Python 3.x.x
```

### 2. **MySQL 5.7+**
```bash
mysql --version
# Deve retornar: mysql  Ver X.X.XX
```

O MySQL **deve estar rodando** na sua máquina.

### 3. **Variáveis de Ambiente (.env)**
O arquivo `.env` já existe com as configurações:
```
DB_USER=root
DB_PASSWORD=99261632
DB_HOST=localhost
DB_PORT=3306
DB_NAME=sistema_api
```

**Ajuste se necessário** (nome de usuário, senha, etc)

---

## 🚀 PASSO A PASSO DE EXECUÇÃO

### **PASSO 1: Criar Banco de Dados (MySQL)**

Abra o MySQL Workbench ou linha de comando e crie o banco:

```sql
CREATE DATABASE IF NOT EXISTS sistema_api;
```

Ou, se preferir via terminal:
```bash
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS sistema_api;"
```

### **PASSO 2: Instalar Dependências Python**

```bash
# Navegar até a pasta do projeto
cd "c:\Users\Henrique\Desktop\PROJETOS FINAIS\Projeto_QA"

# Instalar dependências
pip install -r requirements.txt
```

### **PASSO 3: Criar as Tabelas do Banco de Dados**

Execute o script de inicialização:

```bash
python init_db.py
```

**Esperado:**
```
🔧 Inicializando banco de dados...
✓ Conexão com banco de dados estabelecida
✓ Tabelas criadas com sucesso!

📊 Tabelas criadas:
  - users (id, name, email, password_hash, created_at)
  - movies (id, title, description, user_id, created_at)

✅ Banco de dados inicializado com sucesso!

Agora você pode executar:
  python -m src.app  (para rodar o servidor)
```

Se receber erro, verifique:
- MySQL está rodando?
- Credenciais em `.env` estão corretas?
- Banco `sistema_api` foi criado?

### **PASSO 4: Iniciar o Servidor Flask**

```bash
python -m src.app
```

Ou:
```bash
python -m flask run
```

**Esperado:**
```
 * Serving Flask app 'src.app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

### **PASSO 5: Acessar a Aplicação**

Abra seu navegador e vá para:

```
http://127.0.0.1:5000
```

Você deve ver a página **Home** do sistema.

---

## 📚 ESTRUTURA DE ARQUIVOS

```
Projeto_QA/
├── init_db.py                    # Script para criar as tabelas ⭐
├── requirements.txt              # Dependências Python
├── .env                          # Variáveis de ambiente (não compartilhar)
├── .gitignore                    # Arquivos ignorados pelo Git
│
├── src/
│   ├── app.py                    # Factory da aplicação + rotas web
│   ├── config.py                 # Configuração do banco de dados
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py           # Exporta db (SQLAlchemy)
│   │   ├── user.py               # Modelo User
│   │   └── movie.py              # Modelo Movie
│   ├── routes/
│   │   ├── __init__.py           # Exporta blueprints
│   │   ├── auth.py               # Rotas: /auth/register, /auth/login
│   │   ├── users.py              # Rotas: /users/* (CRUD)
│   │   └── movies.py             # Rotas: /movies/* (CRUD)
│   └── database/                 # Migrações (se usar Alembic)
│
├── templates/                    # Templates HTML
│   ├── base.html                 # Layout base com navegação
│   ├── home.html                 # Página inicial
│   ├── register.html             # Cadastro de usuário
│   ├── login.html                # Login
│   ├── dashboard.html            # Dashboard do usuário
│   └── movies.html               # Gerenciamento de filmes
│
├── static/
│   └── css/
│       └── styles.css            # Estilos (verde, branco, cinza)
│
├── tests/
│   ├── test_app.py               # Testes automatizados
│   └── pytest.ini
│
├── docs/
│   ├── TESTES_MANUAIS.md         # Guia de testes manuais
│   ├── ANALISE_RESULTADOS.md     # Análise dos resultados
│   └── MELHORIAS_SUGERIDAS.md    # 25+ sugestões de features
│
├── postman/
│   └── API_Collection.json       # Coleção Postman para testes
│
└── evidencias/                   # Pasta para screenshots
```

---

## 🧪 TESTANDO O SISTEMA

### **1. Via Interface Web**

1. Acesse `http://127.0.0.1:5000`
2. Clique em **"Cadastro"**
3. Preencha: Nome, Email, Senha (min 8 caracteres)
4. Clique em **"Cadastrar"**
5. Se tudo der certo, você verá mensagem de sucesso
6. Clique em **"Fazer login"**
7. Use o email e senha cadastrados
8. Você será redirecionado ao **Dashboard**

### **2. Via Postman**

1. Abra o Postman
2. Importe o arquivo: `postman/API_Collection.json`
3. Teste os endpoints:
   - `POST /auth/register` - Criar usuário
   - `POST /auth/login` - Fazer login
   - `GET /users` - Listar usuários (requer token)
   - `POST /movies` - Criar filme (requer token)

### **3. Via Testes Automatizados**

```bash
# Executar todos os testes
pytest tests/test_app.py -v

# Executar teste específico
pytest tests/test_app.py::test_register_and_login -v

# Executar com cobertura
pytest tests/test_app.py --cov=src
```

---

## 🔐 COMO FUNCIONA A AUTENTICAÇÃO

### **Fluxo de Login:**

```
1. Usuário preenche email e senha
   ↓
2. Fetch POST /auth/login com credenciais
   ↓
3. Servidor retorna: { "access_token": "jwt...", "user": {...} }
   ↓
4. JavaScript salva token em localStorage
   ↓
5. localStorage.getItem('token') recupera o token
   ↓
6. Requisições autenticadas enviam: Authorization: Bearer <token>
```

### **Exemplo no JavaScript:**

```javascript
// Login
const response = await fetch('/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email: 'user@example.com', password: '12345678' })
});
const result = await response.json();
localStorage.setItem('token', result.access_token);  // Salva token

// Requisição autenticada
const token = localStorage.getItem('token');
const response = await fetch('/users', {
    headers: { 'Authorization': `Bearer ${token}` }
});
```

---

## 📊 ROTAS DISPONÍVEIS

### **Rotas WEB (Renderizam HTML):**
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/` | Página inicial |
| GET | `/register-page` | Formulário de cadastro |
| GET | `/login-page` | Formulário de login |
| GET | `/dashboard` | Dashboard do usuário (requer token) |
| GET | `/movies-page` | Gerenciamento de filmes (requer token) |

### **Rotas API (Retornam JSON):**
| Método | Rota | Descrição | Auth |
|--------|------|-----------|------|
| POST | `/auth/register` | Cadastrar usuário | ❌ |
| POST | `/auth/login` | Fazer login | ❌ |
| GET | `/users` | Listar todos os usuários | ✅ |
| GET | `/users/<id>` | Obter usuário específico | ✅ |
| PUT | `/users/<id>` | Atualizar usuário | ✅ |
| DELETE | `/users/<id>` | Deletar usuário | ✅ |
| POST | `/movies` | Criar filme favorito | ✅ |
| GET | `/movies` | Listar filmes do usuário | ✅ |
| GET | `/movies/<id>` | Obter filme específico | ✅ |
| PUT | `/movies/<id>` | Atualizar filme | ✅ |
| DELETE | `/movies/<id>` | Deletar filme | ✅ |

---

## ⚠️ ERROS COMUNS

### **Erro: "Connection refused"**
```
Problema: MySQL não está rodando
Solução: Inicie o MySQL:
  - Windows: Services > MySQL80 > Start
  - Ou use MySQL Workbench
```

### **Erro: "Database 'sistema_api' does not exist"**
```
Problema: Banco de dados não foi criado
Solução: Execute init_db.py ou crie via MySQL
  mysql -u root -p -e "CREATE DATABASE sistema_api;"
```

### **Erro: "404 Not Found"**
```
Problema: Rota não existe
Verificação: 
  - Verifique a URL (http vs https)
  - Verifique se o servidor está rodando
  - Veja as rotas disponíveis acima
```

### **Erro: "Unauthorized" na API**
```
Problema: Token JWT não foi enviado
Solução: 
  - Faça login para obter token
  - Inclua header: Authorization: Bearer <token>
  - Verifique se token está no localStorage
```

---

## 📝 COMANDOS ÚTEIS

```bash
# Instalar dependências
pip install -r requirements.txt

# Criar banco de dados
python init_db.py

# Rodar servidor
python -m src.app

# Executar testes
pytest tests/test_app.py -v

# Executar teste específico
pytest tests/test_app.py::test_register_and_login -v

# Limpar cache
rm -r .pytest_cache __pycache__ src/__pycache__ tests/__pycache__

# Parar o servidor
CTRL + C (Windows/Linux/Mac)
```

---

## ✅ CHECKLIST DE CONFIGURAÇÃO

- [ ] Python 3.8+ instalado
- [ ] MySQL rodando
- [ ] Arquivo `.env` configurado
- [ ] Banco `sistema_api` criado
- [ ] `pip install -r requirements.txt` executado
- [ ] `python init_db.py` executado com sucesso
- [ ] `python -m src.app` rodando sem erros
- [ ] Navegador abre `http://127.0.0.1:5000` sem erros
- [ ] Cadastro de usuário funciona
- [ ] Login funciona
- [ ] Dashboard acessível após login

---

## 🔗 RECURSOS

- **Flask Documentation**: https://flask.palletsprojects.com/
- **SQLAlchemy**: https://www.sqlalchemy.org/
- **Flask-JWT-Extended**: https://flask-jwt-extended.readthedocs.io/
- **Tailwind CSS**: https://tailwindcss.com/

---

**Última atualização:** 3 de maio de 2026  
**Status:** ✅ Pronto para QA
