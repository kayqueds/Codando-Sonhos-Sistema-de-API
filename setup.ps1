#!/usr/bin/env pwsh
# =====================================================
# Script de Setup Automático - Projeto QA
# =====================================================
# Este script configura e executa o projeto automaticamente
# 
# Uso:
#   .\setup.ps1         # Mostra menu
#   .\setup.ps1 -init   # Inicializa tudo
#   .\setup.ps1 -run    # Apenas roda o servidor
#   .\setup.ps1 -db     # Apenas cria as tabelas
# =====================================================

param(
    [switch]$init = $false,
    [switch]$run = $false,
    [switch]$db = $false,
    [switch]$test = $false
)

$projectPath = Get-Location
$pythonExe = "python"
$pipExe = "pip"

# Cores
$green = [System.ConsoleColor]::Green
$red = [System.ConsoleColor]::Red
$yellow = [System.ConsoleColor]::Yellow
$blue = [System.ConsoleColor]::Cyan

function Write-Success {
    param([string]$message)
    Write-Host "✅ $message" -ForegroundColor $green
}

function Write-Error-Custom {
    param([string]$message)
    Write-Host "❌ $message" -ForegroundColor $red
}

function Write-Info {
    param([string]$message)
    Write-Host "ℹ️  $message" -ForegroundColor $blue
}

function Write-Warning-Custom {
    param([string]$message)
    Write-Host "⚠️  $message" -ForegroundColor $yellow
}

# Verificar Python
function Test-PythonInstalled {
    try {
        $version = & python --version 2>&1
        Write-Success "Python encontrado: $version"
        return $true
    }
    catch {
        Write-Error-Custom "Python não encontrado! Instale Python 3.8+"
        return $false
    }
}

# Instalar dependências
function Install-Dependencies {
    Write-Info "Instalando dependências Python..."
    & pip install -r requirements.txt
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Dependências instaladas com sucesso!"
        return $true
    }
    else {
        Write-Error-Custom "Erro ao instalar dependências"
        return $false
    }
}

# Criar banco de dados
function Initialize-Database {
    Write-Info "Inicializando banco de dados..."
    & python init_db.py
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Banco de dados inicializado com sucesso!"
        return $true
    }
    else {
        Write-Error-Custom "Erro ao inicializar banco de dados"
        return $false
    }
}

# Rodar servidor
function Run-Server {
    Write-Info "Iniciando servidor Flask..."
    Write-Warning-Custom "Servidor rodando em http://127.0.0.1:5000"
    Write-Info "Pressione CTRL+C para parar o servidor"
    & python -m src
}

# Executar testes
function Run-Tests {
    Write-Info "Executando testes..."
    & pytest tests/test_app.py -v
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Todos os testes passaram!"
        return $true
    }
    else {
        Write-Error-Custom "Alguns testes falharam"
        return $false
    }
}

# Menu principal
function Show-Menu {
    Write-Host "`n╔════════════════════════════════════════╗" -ForegroundColor $blue
    Write-Host "║   Sistema de Usuários e Filmes       ║" -ForegroundColor $blue
    Write-Host "║   Setup Automático                   ║" -ForegroundColor $blue
    Write-Host "╚════════════════════════════════════════╝" -ForegroundColor $blue
    Write-Host ""
    Write-Host "1. 🚀 Setup Completo (instalar + DB + rodar)" -ForegroundColor $green
    Write-Host "2. 📦 Instalar Dependências" -ForegroundColor $green
    Write-Host "3. 🗄️  Criar Banco de Dados" -ForegroundColor $green
    Write-Host "4. ▶️  Rodar Servidor" -ForegroundColor $green
    Write-Host "5. 🧪 Executar Testes" -ForegroundColor $green
    Write-Host "6. ❌ Sair" -ForegroundColor $red
    Write-Host ""
}

# Main execution
if ($init) {
    # Setup completo
    Write-Info "Iniciando setup completo..."
    
    if (-not (Test-PythonInstalled)) { exit 1 }
    if (-not (Install-Dependencies)) { exit 1 }
    if (-not (Initialize-Database)) { exit 1 }
    
    Write-Success "Setup completo finalizado!"
    Write-Info "Iniciando servidor..."
    Run-Server
}
elseif ($run) {
    # Apenas rodar servidor
    Run-Server
}
elseif ($db) {
    # Apenas criar DB
    if (-not (Test-PythonInstalled)) { exit 1 }
    Initialize-Database
}
elseif ($test) {
    # Executar testes
    if (-not (Test-PythonInstalled)) { exit 1 }
    Run-Tests
}
else {
    # Menu interativo
    while ($true) {
        Show-Menu
        $choice = Read-Host "Escolha uma opção (1-6)"
        
        switch ($choice) {
            "1" {
                if (-not (Test-PythonInstalled)) { continue }
                if (-not (Install-Dependencies)) { continue }
                if (-not (Initialize-Database)) { continue }
                
                Write-Success "Setup completo! Iniciando servidor..."
                Run-Server
            }
            "2" {
                if (-not (Test-PythonInstalled)) { continue }
                Install-Dependencies
            }
            "3" {
                if (-not (Test-PythonInstalled)) { continue }
                Initialize-Database
            }
            "4" {
                Run-Server
            }
            "5" {
                if (-not (Test-PythonInstalled)) { continue }
                Run-Tests
            }
            "6" {
                Write-Warning-Custom "Encerrando..."
                exit 0
            }
            default {
                Write-Error-Custom "Opção inválida! Digite 1-6"
            }
        }
    }
}
