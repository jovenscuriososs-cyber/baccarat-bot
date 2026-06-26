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
├── scraper.py                   # Web scraper do Bac Bo
├── example_usage.py             # Exemplos de uso
├── main.py                      # Entry point (em desenvolvimento)
├── requirements.txt             # Dependências
├── .env.example                 # Template de env
├── src/                         # (Em desenvolvimento)
│   ├── core/
│   │   ├── bot_manager.py       # Gerenciador central
│   │   ├── prediction_engine.py # ML e previsões
│   │   └── bankroll_manager.py  # Gestão de apostas
│   ├── integrations/
│   │   ├── firebase_client.py   # Firebase DB
│   │   ├── greenapi_client.py   # WhatsApp
│   │   └── telegram_notifier.py # Telegram
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

### 1. Scraping Básico

```python
from scraper import BacBoScraper

scraper = BacBoScraper(headless=True)
results = scraper.scrape_results_selenium()
print(scraper.format_results(results))
```

### 2. Executar Exemplos

```bash
python example_usage.py
```

Escolha entre:
1. Scraping básico
2. Scraping com BeautifulSoup
3. Salvar dados em JSON/CSV
4. Comparação de métodos
5. **Monitoramento contínuo** (recomendado)
6. Análise e processamento

### 3. Análise e Previsão (em breve)
Gera previsões baseadas em:
- Padrões históricos (streaks, alternância)
- Regressão à média
- Machine Learning
- Análise de séries temporais

### 4. Apostas e Notificações (em breve)
Cada previsão envia:
- Notificação via WhatsApp
- Registro no Firebase
- Log local
- Dashboard atualizado

### 5. Dashboard (em breve)
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

## 📊 Estrutura dos Dados

Cada resultado contém:
- `type`: Tipo de resultado (PLAYER, BANKER, TIE)
- `value`: Valor numérico (0-12)
- `timestamp`: Horário do resultado (HH:MM:SS)

### Exemplo de saída JSON:
```json
{
  "timestamp": "2024-01-15T10:42:30.123456",
  "total": 15,
  "results": [
    {
      "type": "PLAYER",
      "value": 8,
      "timestamp": "10:49"
    },
    {
      "type": "BANKER",
      "value": 9,
      "timestamp": "10:10"
    }
  ]
}
```

## 🔧 Métodos do Scraper

### `scrape_results_selenium()`
- Usa Selenium para aguardar carregamento de JS
- Melhor para páginas dinâmicas
- Mais lento, mas mais confiável

### `scrape_results_requests()`
- Usa requests + BeautifulSoup
- Mais rápido
- Requer que o HTML já tenha sido carregado

### `scrape_with_beautifulsoup()`
- Foca especificamente na tabela "Tabela Bac Bo"
- Melhor precisão
- Otimizado para a estrutura do TipMiner

## 🐛 Troubleshooting

### Erro: "ChromeDriver not found"
Baixe o ChromeDriver correspondente à sua versão do Chrome:
https://chromedriver.chromium.org/

### Erro: "Nenhum resultado encontrado"
1. Verifique se a página está acessível
2. Tente usar `scrape_results_selenium()` em vez de `requests`
3. Verifique se a estrutura do HTML mudou no TipMiner

### Erro: "ImportError: No module named 'selenium'"
```bash
pip install -r requirements.txt
```

## 📚 Referências

- [Selenium Documentation](https://selenium-python.readthedocs.io/)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [TipMiner](https://www.tipminer.com/br/cassinos/evolution/bac-bo-ao-vivo)

## ⚠️ Aviso Legal

**Este bot é para fins EDUCACIONAIS e SIMULAÇÃO.**

- Não há garantia de lucro
- Baccarat é um jogo de azar
- Use por sua conta e risco
- Nunca coloque dinheiro real sem compreender riscos

## 📄 Licença

MIT License

## 👤 Autor

jovenscuriososs-cyber

---

**Desenvolvido com ❤️ para análise de padrões em Baccarat**
