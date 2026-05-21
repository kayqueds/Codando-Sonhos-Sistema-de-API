# Sugestões de Melhorias - Projeto QA

## 🚀 Funcionalidades Futuras

### 1. Paginação
**Descrição**: Listar usuários e filmes com paginação  
**Implementação**: Adicionar parâmetros `page` e `limit`  
**Exemplo**:
```bash
GET /users?page=1&limit=10
GET /movies?page=1&limit=5
```
**Benefício**: Melhor performance com muitos registros

---

### 2. Busca e Filtros
**Descrição**: Buscar filmes por título  
**Implementação**:
```bash
GET /movies/search?q=Inception
GET /movies/filter?year=2010
```
**Benefício**: Facilita localização de filmes

---

### 3. Refresh Token
**Descrição**: Renovar JWT sem fazer login novamente  
**Implementação**:
- POST `/auth/refresh` - Renova o token
- Guardar refresh token em httpOnly cookie
**Benefício**: Melhor UX e segurança

---

### 4. Categorias de Filmes
**Descrição**: Adicionar categorias (Ação, Drama, Ficção, etc)  
**Modelo**:
```python
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    movies = db.relationship('Movie', backref='category')
```
**Benefício**: Melhor organização

---

### 5. Avaliação de Filmes
**Descrição**: Usuário pode avaliar filmes (1-5 estrelas)  
**Modelo**:
```python
class Movie(db.Model):
    rating = db.Column(db.Float, default=0)
    votes = db.Column(db.Integer, default=0)
```
**Benefício**: Interação aumentada

---

### 6. Upload de Capa
**Descrição**: Adicionar capa/poster do filme  
**Implementação**:
- POST `/movies/1/upload-poster` - Upload de imagem
- Salvar em `static/posters/`
**Benefício**: Interface mais visual

---

### 7. Comentários em Filmes
**Descrição**: Usuários comentam sobre filmes  
**Modelo**:
```python
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'))
```
**Benefício**: Comunidade engajada

---

### 8. Favoritos (Likes)
**Descrição**: Usuários podem dar "curtir" em filmes de outros  
**Implementação**:
```python
class Like(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'))
```
**Benefício**: Descobrir filmes populares

---

## 🔒 Melhorias de Segurança

### 1. Rate Limiting
**Descrição**: Limitar requisições por IP para evitar força bruta  
**Implementação**:
```python
from flask_limiter import Limiter
limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/auth/login')
@limiter.limit("5 per minute")
def login():
    ...
```
**Benefício**: Proteção contra ataque de força bruta

---

### 2. CORS Configurado
**Descrição**: Controlar quais domínios podem acessar a API  
**Implementação**:
```python
from flask_cors import CORS
CORS(app, origins=['http://localhost:3000', 'https://example.com'])
```
**Benefício**: Segurança contra requisições não autorizadas

---

### 3. Validação com Regex
**Descrição**: Validar email e outros campos com regex  
**Exemplo**:
```python
import re
email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
if not re.match(email_regex, email):
    return jsonify({'error': 'Email inválido'}), 400
```
**Benefício**: Prevenção de dados inválidos

---

### 4. Soft Delete
**Descrição**: Marcar registros como deletados sem remover dados  
**Implementação**:
```python
class User(db.Model):
    deleted_at = db.Column(db.DateTime, nullable=True)

# Deletar: user.deleted_at = datetime.utcnow()
# Listar: User.query.filter(User.deleted_at == None).all()
```
**Benefício**: Recuperação de dados acidental

---

### 5. Auditoria (Logs)
**Descrição**: Registrar todas as alterações  
**Modelo**:
```python
class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    action = db.Column(db.String(50))  # "CREATE", "UPDATE", "DELETE"
    entity = db.Column(db.String(50))  # "User", "Movie"
    entity_id = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
```
**Benefício**: Rastreamento completo de ações

---

## 📊 Melhorias de Dados

### 1. Genero do Filme
```python
movie.genre = db.Column(db.String(50))  # "Ação", "Drama", etc
```

### 2. Data de Lançamento
```python
movie.release_date = db.Column(db.Date)
```

### 3. Diretor
```python
movie.director = db.Column(db.String(100))
```

### 4. Duração
```python
movie.duration = db.Column(db.Integer)  # em minutos
```

### 5. Imagem de Capa
```python
movie.poster_url = db.Column(db.String(255))
```

---

## 📱 Interface Frontend

### 1. Dashboard Melhorado
- Gráficos de filmes assistidos
- Histórico de atividades
- Recomendações

### 2. Perfil do Usuário
- Foto de perfil
- Bio/descrição
- Filmes favoritos públicos

### 3. Explorador de Filmes
- Busca avançada
- Filtros por categoria
- Ordenação por rating

### 4. Modo Escuro
- Toggle theme claro/escuro
- Salvar preferência em localStorage

---

## 🧪 Melhorias de Testes

### 1. Testes de Performance
```python
import time
start = time.time()
# ... teste
end = time.time()
assert end - start < 1.0  # < 1 segundo
```

### 2. Testes de Carga
```bash
# Usar Apache JMeter ou Locust
locust -f locustfile.py
```

### 3. Testes de Integração Completa
```python
def test_user_lifecycle():
    # Cadastro → Login → Criar Filme → Deletar → Logout
```

### 4. E2E com Selenium
```python
from selenium import webdriver
driver = webdriver.Chrome()
driver.get('http://localhost:5000')
# ... testes de navegação
```

---

## 📚 Documentação

### 1. API Documentation (Swagger/OpenAPI)
```python
from flasgger import Swagger
swagger = Swagger(app)
```

### 2. Vídeo Tutorial
- Como cadastrar
- Como fazer login
- Como gerenciar filmes

### 3. Guia do Desenvolvedor
- Como estender a API
- Como adicionar nova rota
- Padrões de código

---

## ☁️ Deployment

### 1. Deploy em Produção
- Heroku
- AWS Elastic Beanstalk
- DigitalOcean

### 2. Variáveis de Ambiente
```
FLASK_ENV=production
DEBUG=False
JWT_SECRET_KEY=...
DATABASE_URL=...
```

### 3. HTTPS
- Certificado SSL/TLS
- Redirecionamento HTTP → HTTPS

---

## 💰 Priorização de Implementação

| Prioridade | Funcionalidade | Esforço | Impacto |
|---|---|---|---|
| 🔴 Alta | Refresh Token | Médio | Alto |
| 🔴 Alta | Rate Limiting | Baixo | Alto |
| 🟡 Média | Paginação | Baixo | Médio |
| 🟡 Média | Busca | Médio | Médio |
| 🟢 Baixa | Upload Imagem | Alto | Baixo |
| 🟢 Baixa | Comentários | Alto | Baixo |

---

**Última atualização**: 3 de maio de 2026
