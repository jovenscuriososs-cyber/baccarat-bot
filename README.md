# 🎰 Bot de Baccarat Completo - TipMiner + Firebase + WhatsApp

Bot profissional que scrapa resultados do TipMiner em tempo real, analisa padrões, faz previsões e notifica via WhatsApp.

## ⚙️ Funcionalidades

- ✅ Web scraping em tempo real (TipMiner)
- ✅ Análise de padrões e previsões com ML
- ✅ Integração Firebase (armazenamento em tempo real)
- ✅ Notificações via WhatsApp (GreenAPI)
- ✅ Gerenciamento de bankroll
- ✅ Dashboard web
- ✅ Histórico completo de apostas
- ✅ Estatísticas e relatórios

## 📋 Pré-requisitos

- Python 3.9+
- Conta no TipMiner (acesso ao histórico)
- Credenciais Firebase
- Credenciais GreenAPI (WhatsApp)
- Navegador com Tampermonkey (para scraping)

## 🚀 Instalação Rápida

```bash
# Clonar repositório
git clone https://github.com/Pezado/baccarat-bot.git
cd baccarat-bot

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com suas credenciais

# Executar bot
python main.py
```

## 🔐 Configuração de Credenciais

Edite `.env` com:

```env
# Firebase
FIREBASE_URL=https://fermagna-9f211-default-rtdb.firebaseio.com
FIREBASE_API_KEY=AIzaSyBY-5S1d28lSinOrDKKpYx2FchE6zTF0n0

# GreenAPI (WhatsApp)
GREENAPI_URL=https://7107.api.greenapi.com
GREENAPI_INSTANCE_ID=7107654572
GREENAPI_TOKEN=499b5912cda643e5a6ec732529f1d2ae1be155aa7f6247a683

# TipMiner
TIPMINER_URL=https://www.tipminer.com/br/historico/jonbet/bac-bo

# Bot Config
STARTING_BANKROLL=1000
MIN_BET=10
MAX_BET=500
```

## 📁 Estrutura do Projeto

```
baccarat-bot/
├── main.py                      # Entry point
├── requirements.txt             # Dependências
├── .env.example                 # Template de env
├── src/
│   ├── core/
│   │   ├── bot_manager.py       # Gerenciador central
│   │   ├── scraper_tipminer.py  # Web scraping
│   │   ├── prediction_engine.py # ML e previsões
│   │   └── bankroll_manager.py  # Gestão de apostas
│   ├── integrations/
│   │   ├── firebase_client.py   # Firebase DB
│   │   ├── greenapi_client.py   # WhatsApp
│   │   └── telegram_notifier.py # Telegram (stub)
│   ├── utils/
│   │   ├── logger_setup.py      # Logging
│   │   ├── config.py            # Configurações
│   │   └── helpers.py           # Funções auxiliares
│   └── web/
│       ├── app.py               # Flask Dashboard
│       └── static/              # Recursos web
├── tests/                       # Testes
├── docs/                        # Documentação
└── logs/                        # Arquivos de log
```

## 🎯 Como Usar

### 1. Scraping Automático
O bot busca automaticamente resultados do TipMiner a cada 10 segundos.

### 2. Análise e Previsão
Gera previsões baseadas em:
- Padrões históricos (streaks, alternância)
- Regressão à média
- Machine Learning
- Análise de séries temporais

### 3. Apostas e Notificações
Cada previsão envia:
- Notificação via WhatsApp
- Registro no Firebase
- Log local
- Dashboard atualizado

### 4. Dashboard
Acesse em: http://localhost:5000

## 🔄 Fluxo de Dados

```
TipMiner (scraping)
    ↓
Prediction Engine (análise)
    ↓
Firebase (armazenamento)
    ↓
WhatsApp + Dashboard (notificações)
```

## ⚠️ Aviso Legal

**Este bot é para fins EDUCACIONAIS e SIMULAÇÃO.**

- Não há garantia de lucro
- Baccarat é um jogo de azar
- Use por sua conta e risco
- Nunca coloque dinheiro real sem compreender riscos

## 📖 Documentação Completa

Veja a pasta `/docs` para:
- [Instalação Detalhada](docs/INSTALACAO.md)
- [Configuração](docs/CONFIGURACAO.md)
- [Arquitetura](docs/ARQUITETURA.md)
- [Estratégias](docs/ESTRATEGIAS.md)
- [API Reference](docs/API.md)

## 🤝 Contribuindo

Pull requests são bem-vindas!

## 📞 Suporte

Abra uma issue no GitHub para reportar bugs ou sugestões.

## 📄 Licença

MIT License - veja LICENSE para detalhes

---

**Desenvolvido com ❤️ para análise de padrões em Baccarat**
