#!/bin/bash
# Setup automático para Termux - Baccarat Bot
# Use: bash setup.sh

set -e

echo "================================"
echo "🎰 Baccarat Bot - Setup Termux"
echo "================================"
echo ""

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Função para imprimir status
status() {
    echo -e "${GREEN}✓${NC} $1"
}

warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

error() {
    echo -e "${RED}✗${NC} $1"
}

# Atualizar sistema
echo "📦 Atualizando sistema..."
pkg update -y > /dev/null 2>&1
pkg upgrade -y > /dev/null 2>&1
status "Sistema atualizado"

# Instalar Python
echo ""
echo "🐍 Instalando Python..."
if command -v python &> /dev/null; then
    status "Python já instalado: $(python --version)"
else
    pkg install python -y > /dev/null 2>&1
    status "Python instalado"
fi

# Instalar Git
echo ""
echo "🔧 Instalando Git..."
if command -v git &> /dev/null; then
    status "Git já instalado"
else
    pkg install git -y > /dev/null 2>&1
    status "Git instalado"
fi

# Atualizar pip
echo ""
echo "📥 Atualizando pip..."
pip install --upgrade pip > /dev/null 2>&1
status "pip atualizado"

# Instalar dependências
echo ""
echo "📚 Instalando dependências..."
pip install -r requirements-termux.txt > /dev/null 2>&1
status "Dependências instaladas"

# Fazer teste
echo ""
echo "🧪 Testando conexão..."
if python scraper_termux.py check > /dev/null 2>&1; then
    status "Conexão OK"
else
    warning "Verifique sua conexão com internet"
fi

# Criar diretórios necessários
echo ""
echo "📁 Criando diretórios..."
mkdir -p logs data
status "Diretórios criados"

# Resumo final
echo ""
echo "================================"
echo "✅ Setup concluído com sucesso!"
echo "================================"
echo ""
echo "📖 Próximos passos:"
echo ""
echo "1. Testar scraper:"
echo "   python scraper_termux.py test"
echo ""
echo "2. Rodar monitoramento contínuo:"
echo "   python scraper_termux.py"
echo ""
echo "3. Ver estatísticas:"
echo "   python scraper_termux.py stats"
echo ""
echo "Mais informações: cat ANDROID_SETUP.md"
echo ""
