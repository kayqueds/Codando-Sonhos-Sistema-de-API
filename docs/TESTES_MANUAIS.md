# Guia de Testes Manuais - QA

## 🎯 Objetivo
Demonstrar funcionalidade completa da API através de testes manuais no Postman e navegador.

---

## 📋 Checklist de Testes

### 1. TELA INICIAL (Home)
- [ ] Acessar `http://127.0.0.1:5000/`
- [ ] Verificar se página carrega com design verde/branco
- [ ] Clicar em "Cadastrar-se" → deve redirecionar para `/register-page`
- [ ] Clicar em "Fazer Login" → deve redirecionar para `/login-page`

---

## 2. CADASTRO DE USUÁRIO

### Teste Positivo - Cadastro Válido
1. Acessar `http://127.0.0.1:5000/register-page`
2. Preencher:
   - Nome: `João Silva`
   - Email: `joao@example.com`
   - Senha: `Senha123`
3. Clicar em "Cadastrar"
4. **Resultado Esperado**: Mensagem de sucesso + link para login

### Teste Negativo - Senha Fraca
1. Preencher:
   - Nome: `Maria`
   - Email: `maria@example.com`
   - Senha: `123` (muito curta)
2. Clicar em "Cadastrar"
3. **Resultado Esperado**: Mensagem de erro "A senha deve ter ao menos 8 caracteres."

### Teste Negativo - Email Duplicado
1. Cadastrar usuário com `joao@example.com`
2. Tentar cadastrar novamente com mesmo email
3. **Resultado Esperado**: Erro `409` - "Email já cadastrado."

---

## 3. LOGIN

### Teste Positivo - Login Correto
1. Acessar `http://127.0.0.1:5000/login-page`
2. Preencher:
   - Email: `joao@example.com`
   - Senha: `Senha123`
3. Clicar em "Entrar"
4. **Resultado Esperado**: Redireciona para `/dashboard`

### Teste Negativo - Senha Incorreta
1. Preencher:
   - Email: `joao@example.com`
   - Senha: `SenhaErrada`
2. Clicar em "Entrar"
3. **Resultado Esperado**: Mensagem de erro "Email ou senha inválidos."

### Teste Negativo - Email Inexistente
1. Preencher:
   - Email: `inexistente@example.com`
   - Senha: `qualquer`
2. Clicar em "Entrar"
3. **Resultado Esperado**: Erro "Email ou senha inválidos."

---

## 4. DASHBOARD

### Após Login
1. Usuário deve ver: "Bem-vindo! Aqui você pode gerenciar sua conta e filmes favoritos."
2. Dois cards: "Minha Conta" e "Meus Filmes Favoritos"
3. Menu no topo deve exibir links de logout

---

## 5. GERENCIAMENTO DE FILMES

### Adicionar Filme
1. Acessar `http://127.0.0.1:5000/movies-page` (ou clique em "Ver Filmes")
2. Preencher:
   - Título: `Inception`
   - Descrição: `Filme de ficção científica`
3. Clicar em "Adicionar Filme"
4. **Resultado Esperado**: Filme aparece na lista abaixo

### Visualizar Filmes
1. Após adicionar, filme deve aparecer com título e descrição
2. Clicar em "Excluir" → deve aparecer aviso de confirmação

### Deletar Filme
1. Clicar em "Excluir" em um filme
2. Confirmar exclusão
3. **Resultado Esperado**: Filme desaparece da lista

---

## 🔧 Testes via Postman

### Preparação
1. Importar `postman/API_Collection.json` no Postman
2. Configurar variável `base_url` = `http://127.0.0.1:5000`

### Teste 1: Cadastro
```
POST /auth/register
Body:
{
  "name": "Teste QA",
  "email": "qa@example.com",
  "password": "TesteSenha123"
}

Status Esperado: 201
Resposta: {"message": "Usuário criado com sucesso.", "user": {...}}
```

### Teste 2: Login
```
POST /auth/login
Body:
{
  "email": "qa@example.com",
  "password": "TesteSenha123"
}

Status Esperado: 200
Resposta: {"access_token": "eyJ...", "user": {...}}
```
**Importante**: Copie o `access_token` para os próximos testes

### Teste 3: Criar Filme
```
POST /movies
Headers: Authorization: Bearer {access_token}
Body:
{
  "title": "The Matrix",
  "description": "Clássico de ficção científica"
}

Status Esperado: 201
Resposta: {"message": "Filme criado com sucesso.", "movie": {...}}
```

### Teste 4: Listar Filmes
```
GET /movies
Headers: Authorization: Bearer {access_token}

Status Esperado: 200
Resposta: {"movies": [{...}, {...}]}
```

### Teste 5: Atualizar Filme
```
PUT /movies/1
Headers: Authorization: Bearer {access_token}
Body:
{
  "title": "The Matrix Reloaded",
  "description": "Sequência"
}

Status Esperado: 200
```

### Teste 6: Deletar Filme
```
DELETE /movies/1
Headers: Authorization: Bearer {access_token}

Status Esperado: 200
```

---

## ✅ Critérios de Sucesso

### Interface Visual
- [ ] Todas as telas carregam corretamente
- [ ] Formulários aceitam entrada
- [ ] Mensagens de erro aparecem
- [ ] Mensagens de sucesso aparecem
- [ ] Design é responsivo

### API
- [ ] Status HTTP corretos (200, 201, 400, 401, 404)
- [ ] Respostas JSON válidas
- [ ] JWT funciona em rotas protegidas
- [ ] Controle de acesso funciona (usuário A não vê dados de B)
- [ ] Validações funcionam

### Fluxo Completo
- [ ] Cadastro → Login → Dashboard → Filmes → Logout
- [ ] Criar filme → Listar → Atualizar → Deletar
- [ ] Erro de validação trata corretamente
- [ ] Sessão persiste após login

---

## 📸 Evidências

Tire screenshots de:
1. Tela home
2. Cadastro com sucesso
3. Login com sucesso
4. Dashboard
5. Lista de filmes
6. Erro de validação
7. Resposta do Postman (status 201, 200, 400, etc)

Salve em `evidencias/` com nomes descritivos.

---

## 🐛 Problemas Encontrados

Se encontrar erros, documente:
- **O que foi testado**: Descrição da ação
- **Resultado esperado**: O que deveria acontecer
- **Resultado obtido**: O que realmente aconteceu
- **Status HTTP/Erro**: Se aplicável
- **Screenshot**: Do erro ou resultado

Salve em `docs/BUGS_ENCONTRADOS.md`
