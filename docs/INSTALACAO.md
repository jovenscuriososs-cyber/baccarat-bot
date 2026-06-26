# 🚀 Guia de Instalação

## Pré-requisitos

1. **Python 3.9+**
2. **pip** (gerenciador de pacotes)
3. **Conta Firebase**
4. **Credenciais GreenAPI** (WhatsApp)
5. **Navegador com Tampermonkey** (para scraping extra)

## Passo 1: Clonar Repositório

```bash
git clone https://github.com/Pezado/baccarat-bot.git
cd baccarat-bot
```

## Passo 2: Criar Virtual Environment

```bash
# Windows
python -m venv venv
venv\\Scripts\\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

## Passo 3: Instalar Dependências

```bash
pip install -r requirements.txt
```

## Passo 4: Configurar Credenciais

```bash
cp .env.example .env
```

Edite `.env` com suas credenciais:

### Firebase

1. Acesse https://console.firebase.google.com
2. Crie um novo projeto ou use um existente
3. Ative Realtime Database
4. Copie as credenciais para `.env`

```env
FIREBASE_URL=https://seu-project-rtdb.firebaseio.com
FIREBASE_API_KEY=sua_api_key
FIREBASE_PROJECT_ID=seu_project_id
```

### GreenAPI (WhatsApp)

1. Acesse https://greenapi.com
2. Crie uma conta e obtenha credenciais
3. Copie para `.env`

```env
GREENAPI_URL=https://7107.api.greenapi.com
GREENAPI_INSTANCE_ID=seu_instance_id
GREENAPI_TOKEN=seu_token
```

### TipMiner

A URL padrão funciona, mas você pode customizar:

```env
TIPMINER_URL=https://www.tipminer.com/br/historico/jonbet/bac-bo
```

## Passo 5: Executar Bot

```bash
python main.py
```

Ou via Makefile:

```bash
make run
```

## Troubleshooting

### Erro de conexão Firebase

- Verifique se as credenciais estão corretas
- Confira se o banco de dados está ativo
- Teste a URL: `curl https://seu-url/bacbo/historico.json`

### Erro de WhatsApp

- Verifique se o token é válido
- Confira o número de telefone (com código do país)
- Teste via: `curl -X POST https://api.greenapi.com/...`

### Erro de scraping TipMiner

- O site pode ter mudado a estrutura
- Use Tampermonkey para extrair dados manualmente
- Atualize os seletores em `scraper_tipminer.py`
