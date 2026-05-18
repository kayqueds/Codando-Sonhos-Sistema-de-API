🚀 COMEÇAR AQUI - Configuração Rápida do Projeto

═══════════════════════════════════════════════════════════

## ⚡ INICIO RÁPIDO (5 MINUTOS)

### Passo 1: Abra o Terminal PowerShell
```
Windows: Win + R → powershell
```

### Passo 2: Navegue para o projeto
```powershell
cd "c:\Users\Henrique\Desktop\PROJETOS FINAIS\Projeto_QA"
```

### Passo 3: Execute o script de setup
```powershell
.\setup.ps1 -init
```

Isso irá:
✅ Verificar se Python está instalado
✅ Instalar todas as dependências
✅ Criar as tabelas no MySQL
✅ Iniciar o servidor

---

## 🎯 ALTERNATIVA: Passos Manuais

Se preferir fazer passo a passo:

### 1️⃣ Criar Banco de Dados MySQL
```bash
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS sistema_api;"
```
(Digite a senha quando solicitado: 99261632)

### 2️⃣ Instalar Dependências
```bash
cd "c:\Users\Henrique\Desktop\PROJETOS FINAIS\Projeto_QA"
pip install -r requirements.txt
```

### 3️⃣ Criar as Tabelas
```bash
python init_db.py
```

### 4️⃣ Rodar o Servidor
```bash
python -m src.app
```

---

## 🌐 Acessar o Sistema

Após o servidor iniciar, abra seu navegador:

```
http://127.0.0.1:5000
```

Você verá a página inicial. Agora você pode:
✅ Cadastrar um novo usuário
✅ Fazer login
✅ Ver o dashboard
✅ Gerenciar filmes favoritos

---

## 📊 ESTRUTURA DO PROJETO

O que foi criado/ajustado:

### Arquivos Principais:
```
init_db.py                  ⭐ Script para criar tabelas
setup.ps1                   ⭐ Script de automação (PowerShell)
GUIA_EXECUCAO.md            ⭐ Documentação completa
src/app.py                  ✅ Aplicação corrigida (sem duplicatas)
```

### Modelos de Dados:
```
src/models/user.py          - Usuário (id, name, email, password_hash, created_at)
src/models/movie.py         - Filme (id, title, description, user_id, created_at)
```

### Rotas API:
```
POST   /auth/register       - Cadastrar usuário
POST   /auth/login          - Fazer login (retorna JWT)
GET    /users               - Listar todos (requer JWT)
GET    /users/<id>          - Obter um usuário
PUT    /users/<id>          - Atualizar usuário
DELETE /users/<id>          - Deletar usuário
POST   /movies              - Criar filme
GET    /movies              - Listar meus filmes
PUT    /movies/<id>         - Atualizar filme
DELETE /movies/<id>         - Deletar filme
```

### Templates Web:
```
templates/base.html         - Layout base com navegação
templates/home.html         - Página inicial
templates/register.html     - Cadastro
templates/login.html        - Login
templates/dashboard.html    - Dashboard (após login)
templates/movies.html       - Gerenciar filmes
```

### Estilos:
```
static/css/styles.css       - CSS com cores (verde, branco, cinza)
```

---

## 🔒 Como Funciona a Autenticação

1. **Cadastro**: POST /auth/register com nome, email, senha
2. **Login**: POST /auth/login com email, senha
3. **Retorno**: API retorna token JWT
4. **Armazenamento**: JavaScript salva token em localStorage
5. **Uso**: Requisições posteriores incluem: `Authorization: Bearer <token>`

---

## ✅ Testes

### Executar testes automatizados:
```bash
pytest tests/test_app.py -v
```

Resultado esperado: **8 testes passando (100%)**

---

## 📝 Exemplo: Cadastro e Login via API

### 1. Cadastrar Usuário
```bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "João Silva",
    "email": "joao@example.com",
    "password": "senha123"
  }'
```

### 2. Fazer Login
```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "joao@example.com",
    "password": "senha123"
  }'
```

**Resposta:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "name": "João Silva",
    "email": "joao@example.com",
    "created_at": "2026-05-03T23:30:00"
  }
}
```

### 3. Usar Token para Listar Usuários
```bash
curl -X GET http://localhost:5000/users \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

---

## ⚠️ Erros Comuns

### Erro: "Connection refused"
**Problema**: MySQL não está rodando  
**Solução**: Inicie o MySQL (Windows Services ou MySQL Workbench)

### Erro: "Database does not exist"
**Problema**: Banco não foi criado  
**Solução**: Execute `python init_db.py`

### Erro: "403 Forbidden" na API
**Problema**: Token JWT não foi enviado  
**Solução**: Faça login primeiro e inclua o token no header

### Erro: "Table already exists"
**Problema**: Tabelas já foram criadas  
**Solução**: Não há problema! Significa que o banco já está pronto

---

## 📚 Documentação Adicional

Para mais detalhes, veja:
- [GUIA_EXECUCAO.md](GUIA_EXECUCAO.md) - Guia completo
- [README.md](README.md) - Visão geral do projeto
- [docs/TESTES_MANUAIS.md](docs/TESTES_MANUAIS.md) - Como fazer testes manuais
- [docs/ANALISE_RESULTADOS.md](docs/ANALISE_RESULTADOS.md) - Análise dos testes
- [docs/MELHORIAS_SUGERIDAS.md](docs/MELHORIAS_SUGERIDAS.md) - 25+ sugestões

---

## 🎬 Próximos Passos

1. ✅ Executar setup.ps1 -init
2. ✅ Acessar http://127.0.0.1:5000
3. ✅ Cadastrar um usuário
4. ✅ Fazer login
5. ✅ Testar as funcionalidades
6. ✅ Executar pytest para validar

---

## 📞 Suporte

Se encontrar problemas:
1. Verifique [GUIA_EXECUCAO.md](GUIA_EXECUCAO.md)
2. Verifique se MySQL está rodando
3. Verifique as credenciais em `.env`
4. Execute novamente: `python init_db.py`

---

**Pronto? Execute agora:**

```powershell
.\setup.ps1 -init
```

🚀 Seu sistema estará rodando em http://127.0.0.1:5000

---

Última atualização: 3 de maio de 2026
