# 🎰 Guia Completo: Baccarat Bot no Android com Termux

## 📱 O que você vai precisar

- Android 7+ (qualquer celular)
- Termux instalado
- ~200MB de espaço livre
- Conexão com internet

---

## 🚀 PASSO 1: Instalar Termux

### No Android:

1. **Abra a Play Store** (ou F-Droid para versão sem rastreamento)
2. **Procure por:** `Termux`
3. **Instale** a versão oficial (ícone preto/roxo)
4. **Abra o app**

Você verá a tela preta com prompt: `~$`

---

## 📦 PASSO 2: Setup Inicial

### Execute estes comandos um por um:

```bash
# Atualizar sistema
pkg update && pkg upgrade -y

# Instalar Python
pkg install python -y

# Instalar Git
pkg install git -y

# Instalar dependências extras
pkg install curl wget -y
```

**Leva ~5-10 minutos dependendo da internet**

---

## 📥 PASSO 3: Clonar o Repositório

```bash
# Vá para o diretório home
cd ~

# Clone o repositório
git clone https://github.com/jovenscuriososs-cyber/baccarat-bot.git

# Entre no diretório
cd baccarat-bot
```

---

## 🔧 PASSO 4: Instalar Dependências Python

```bash
# Instalar pip (gerenciador de pacotes)
pip install --upgrade pip

# Instalar bibliotecas necessárias
pip install requests beautifulsoup4
```

**Se demorar muito, tente:**
```bash
pip install requests beautifulsoup4 --no-cache-dir
```

---

## ✅ PASSO 5: Testar o Scraper

### Primeiro, verifique a conexão:

```bash
python scraper_termux.py check
```

**Esperado:**
```
🧪 Testando conexão...

✓ Conexão bem-sucedida!
  Status: 200
  Content-Length: 45230 bytes
  Encoding: utf-8
✓ Página contém 'Tabela Bac Bo'
```

---

## 🔍 Se não funcionar (Modo Debug):

```bash
python scraper_termux.py debug
```

Isso vai:
- Salvar o HTML em `debug_html.txt`
- Tentar 3 estratégias diferentes
- Mostrar erros detalhados

**Visualizar o HTML:**
```bash
cat debug_html.txt | head -50
```

---

## 🎯 PASSO 6: Rodar o Scraper

### Opção A: Monitoramento Contínuo (Recomendado)

```bash
python scraper_termux.py
```

**Vai:**
- Coletar dados a cada 30 segundos
- Salvar em `bac_bo_results.json`
- Mostrar em tempo real

**Para para:**
- Pressione `CTRL + C`

### Opção B: Teste Rápido

```bash
python scraper_termux.py test
```

Faz um scraping único e salva.

### Opção C: Ver Estatísticas

```bash
python scraper_termux.py stats
```

Mostra:
- Total de resultados coletados
- Distribuição por tipo (PLAYER/BANKER/TIE)
- Valores mais frequentes

---

## 💾 PASSO 7: Acessar os Dados

### Ver arquivo de dados:

```bash
cat bac_bo_results.json
```

### Ver primeiras linhas:

```bash
head -20 bac_bo_results.json
```

### Ver estatísticas de dados:

```bash
python scraper_termux.py stats
```

---

## 🔄 PASSO 8: Manter Rodando em Background

### Opção A: Usar `nohup` (continua mesmo fechando Termux)

```bash
nohup python scraper_termux.py > scraper.log 2>&1 &
```

**Para:**
```bash
pkill -f scraper_termux.py
```

**Ver logs:**
```bash
tail -f scraper.log
```

### Opção B: Usar screen (gerenciador de sessões)

```bash
# Instalar
pkg install screen -y

# Criar sessão
screen -S scraper

# Dentro da sessão, rode:
python scraper_termux.py

# Desconectar (deixando rodar): CTRL + A, depois D

# Reconectar depois:
screen -r scraper

# Listar sessões:
screen -ls
```

---

## 📊 Dashboard de Dados

### Ver estrutura dos dados salvos:

```bash
python -c "import json; data=json.load(open('bac_bo_results.json')); print(json.dumps(data[0], indent=2))"
```

### Exemplo de saída:

```json
{
  "timestamp": "2024-01-15T11:47:01.123456",
  "total": 15,
  "database": "scrapp/bacbo",
  "results": [
    {
      "type": "PLAYER",
      "value": 8,
      "timestamp": "10:49",
      "scraped_at": "2024-01-15T11:47:01.456789"
    }
  ]
}
```

---

## 🛠️ Troubleshooting

### ❌ "Nenhum resultado encontrado"

**Solução 1:** Teste a conexão
```bash
curl https://www.tipminer.com/br/cassinos/evolution/bac-bo-ao-vivo
```

**Solução 2:** Modo debug
```bash
python scraper_termux.py debug
```

**Solução 3:** Verifique internet
```bash
ping 8.8.8.8
```

---

### ❌ "ModuleNotFoundError: No module named 'requests'"

**Solução:**
```bash
pip install requests beautifulsoup4
```

---

### ❌ "python: command not found"

**Solução:**
```bash
pkg install python -y
```

---

### ❌ "Permission denied"

**Solução:**
```bash
chmod +x scraper_termux.py
```

---

## 📱 Dicas de Use no Android

### 1. **Manter tela ligada:**
   - Settings > Display > Screen timeout = Nunca

### 2. **Evitar hibernação:**
   - Settings > Battery > Battery saver = Off

### 3. **Usar WiFi:**
   - Mais estável que dados móveis
   - Não consome bateria rápido

### 4. **Monitorar consumo:**
```bash
# Ver tamanho do arquivo
ls -lh bac_bo_results.json

# Limpar dados antigos (manter últimas 100 coletas)
python -c "import json; data=json.load(open('bac_bo_results.json')); json.dump(data[-100:], open('bac_bo_results.json','w'))"
```

---

## 🔄 Atualizar o Projeto

```bash
cd ~/baccarat-bot

# Baixar atualizações
git pull origin main

# Atualizar dependências Python
pip install --upgrade requests beautifulsoup4
```

---

## 📋 Checklist Final

- [ ] Termux instalado
- [ ] Python instalado (`python --version`)
- [ ] Repositório clonado (`ls baccarat-bot`)
- [ ] Dependências instaladas (`pip list | grep requests`)
- [ ] Conexão testada (`python scraper_termux.py check`)
- [ ] Scraper rodando (`python scraper_termux.py test`)
- [ ] Dados salvos (`cat bac_bo_results.json`)
- [ ] Monitoramento rodando (CTRL+C para parar)

---

## ⚡ Próximos Passos

1. **Testar agora:**
   ```bash
   python scraper_termux.py check
   ```

2. **Rodar monitoramento:**
   ```bash
   python scraper_termux.py
   ```

3. **Deixar rodando:**
   ```bash
   nohup python scraper_termux.py > scraper.log 2>&1 &
   ```

4. **Ver dados depois:**
   ```bash
   python scraper_termux.py stats
   ```

---

## 🆘 Precisa de Ajuda?

Se der erro:

1. **Copie o erro exato**
2. **Execute em modo debug:**
   ```bash
   python scraper_termux.py debug
   ```
3. **Mande a saída do debug**

---

## 📞 Contato & Suporte

- **GitHub:** https://github.com/jovenscuriososs-cyber/baccarat-bot
- **Issues:** Abra uma issue se tiver problema

---

**Desenvolvido com ❤️ para rodar em qualquer Android** 🚀
