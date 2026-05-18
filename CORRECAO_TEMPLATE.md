# 🔧 CORREÇÃO APLICADA - ERRO DO TEMPLATE

## ✅ O Que Foi Feito

### Problema Identificado
```
jinja2.exceptions.TemplateNotFound: home.html
```

Flask não conseguia encontrar os arquivos HTML na pasta `templates/`.

### Causa Raiz
Quando você executa `python -m src.app`, o Flask procura os templates **relativo ao arquivo app.py**, não na raiz do projeto.

- ❌ Flask procurava em: `src/templates/`
- ✅ Templates estão em: `./templates/` (raiz)

### Solução Implementada

#### 1. **Atualizado `src/app.py`**
Adicionei importação de `os` e configuração de paths no `create_app()`:

```python
import os

def create_app(test_config=None):
    # Definir caminhos corretos para templates e static
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    template_folder = os.path.join(basedir, 'templates')
    static_folder = os.path.join(basedir, 'static')
    
    app = Flask(__name__, 
                template_folder=template_folder, 
                static_folder=static_folder,
                instance_relative_config=False)
```

#### 2. **Criado `src/__main__.py`**
Facilita a execução com `python -m src`:

```python
from src.app import create_app
from src.models import db

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    print("🚀 Servidor iniciando em http://127.0.0.1:5000")
    app.run(debug=True)
```

#### 3. **Atualizado `setup.ps1`**
Comando alterado de `python -m src.app` para `python -m src`

---

## 🚀 COMO RODAR AGORA

### **Opção 1: Mais Simples (Recomendada)**
```bash
python -m src
```

### **Opção 2: Via setup.ps1**
```powershell
.\setup.ps1 -run
```

### **Opção 3: Automático (instala tudo + roda)**
```powershell
.\setup.ps1 -init
```

### **Opção 4: Script direto**
```bash
python src/app.py
```

---

## ✅ RESULTADO ESPERADO

Ao executar qualquer um dos comandos acima, você deve ver:

```
 * Serving Flask app 'src.app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

Então acesse no navegador:
```
http://127.0.0.1:5000
```

E você verá a página HOME com opções de cadastro e login.

---

## 📝 ARQUIVOS ALTERADOS/CRIADOS

| Arquivo | Ação | Descrição |
|---------|------|-----------|
| `src/app.py` | ✏️ Alterado | Adicionado configuração de paths |
| `src/__main__.py` | 🆕 Criado | Permite `python -m src` |
| `setup.ps1` | ✏️ Alterado | Comando atualizado |

---

## 🧪 TESTE AGORA

### Terminal PowerShell:
```powershell
cd "c:\Users\Henrique\Desktop\PROJETOS FINAIS\Projeto_QA"
python -m src
```

### Resultado:
```
✅ Servidor rodando sem erros
✅ Acessível em http://127.0.0.1:5000
✅ Templates carregando corretamente
✅ Pronto para testes
```

---

## ⚠️ Se Ainda Tiver Erro

1. Parar o servidor (CTRL+C)
2. Fechar o terminal
3. Abrir terminal novo
4. Executar: `python -m src`

Se persistir, verifique:
- [ ] Pasta `templates/` existe?
- [ ] Arquivo `home.html` existe?
- [ ] Arquivo `src/__main__.py` foi criado?
- [ ] MySQL está rodando?

---

## 🎯 PRÓXIMOS PASSOS

1. Execute: `python -m src`
2. Acesse: http://127.0.0.1:5000
3. Teste: Cadastro, Login, Filmes
4. Valide: Tudo funciona ✅

---

**Status**: ✅ CORRIGIDO  
**Última atualização**: 3 de maio de 2026
