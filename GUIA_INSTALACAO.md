# 🚀 GUIA COMPLETO - Do ZERO ao Lucro

## O que é isso que criamos?

Um **sistema automático** que:
- 📄 Lê PDFs de seguros automaticamente (com IA)
- 📊 Salva os dados em planilha Google Sheets
- 💬 Avisa você no Telegram quando seguro vence
- 📧 Manda email de lembrete pros clientes
- 💰 Você pode vender como serviço ou produto

---

## ✅ PASSO 1: Preparar sua máquina (15 min)

### Windows, Mac ou Linux:

1. **Baixe Python** (versão 3.10+)
   - Acesse: https://www.python.org/downloads/
   - Clique em "Download Python 3.11" (ou mais novo)
   - **IMPORTANTE**: Na instalação, marque "Add Python to PATH"

2. **Abra o terminal/prompt** (Winkey + R, digita `cmd`)
   ```bash
   python --version
   ```
   Deve aparecer algo como `Python 3.11.x`

3. **Instale Poetry** (gerenciador de dependências)
   ```bash
   pip install poetry
   ```

4. **Clone seu repositório** (copie seu código do GitHub)
   ```bash
   git clone https://github.com/fm24logos-star/insurance-manager.git
   cd insurance-manager
   ```

5. **Instale as dependências**
   ```bash
   poetry install
   ```
   Isso vai demorar um pouco... espere terminar

---

## 🔑 PASSO 2: Criar Credenciais (MUITO IMPORTANTE!)

Você precisa de 3 coisas:

### A) Chave do Google Gemini (para ler PDFs)

1. Acesse: https://aistudio.google.com/app/apikey
2. Clique "Create API Key"
3. Clique "Create API Key in new project"
4. Copia a chave (algo como: `AIzaSy...`)

### B) Token do Telegram Bot (para avisos)

1. Abra Telegram
2. Procure por `@BotFather`
3. Mande mensagem: `/start`
4. Mande: `/newbot`
5. Escolha um nome (ex: "SeguroBot")
6. Escolha um username (ex: "meu_seguro_bot")
7. Copia o TOKEN (algo como: `123456:ABCD...`)

### C) Seu Chat ID no Telegram (para receber avisos)

1. Procure por `@userinfobot`
2. Mande `/start`
3. Ele vai te mostrar seu ID (número com 8-10 dígitos)
4. Copia esse número

### D) Google Sheets + Drive (para guardar dados)

Isso é mais complexo, vou simplificar:

1. Acesse: https://console.cloud.google.com
2. Clique "Criar Projeto"
3. Escreva "Insurance Manager"
4. Aguarde criar
5. Na barra de busca, procure por "Google Sheets API"
6. Clique e depois "Ativar"
7. Faça o mesmo com "Google Drive API"

**Agora criar Service Account:**
1. Clique em "Credenciais" (esquerda)
2. Clique "+ CRIAR CREDENCIAIS"
3. Escolha "Conta de Serviço"
4. Escreva "insurance-manager" como nome
5. Clique "Criar e Continuar"
6. Clique "Continuar" nas próximas telas
7. Clique na conta que criou
8. Vá em "Chaves"
9. Clique "+ ADICIONAR CHAVE" > "Criar nova chave"
10. Escolha "JSON"
11. Clique "Criar"
12. Um arquivo vai baixar (service-account.json)
13. **Salve esse arquivo na pasta do projeto**

**Criar Planilha Google Sheets:**
1. Acesse: https://sheets.google.com
2. Clique "Criar nova planilha"
3. Copia a URL (algo como: `https://docs.google.com/spreadsheets/d/ABC123XYZ...`)
4. A parte ABC123XYZ é seu ID (guarda isso)

**Compartilhar com a Service Account:**
1. Abra o arquivo service-account.json que baixou
2. Procura por `"client_email"` (algo como: `xxx@xxx.iam.gserviceaccount.com`)
3. Copia esse email
4. Volta na planilha Google Sheets
5. Clique "Compartilhar" (canto superior)
6. Cola o email e clica "Compartilhar"

---

## ⚙️ PASSO 3: Configurar o .env (15 min)

1. Abra a pasta do projeto
2. Procura por `.env.example`
3. Clica direito > "Abrir com" > Bloco de Notas
4. Muda para isso:

```env
# Cole suas credenciais aqui
GOOGLE_SHEETS_CREDENTIALS_JSON=service-account.json
GOOGLE_SPREADSHEET_ID=ABC123XYZ_aqui_cola_seu_ID_da_planilha
GOOGLE_DRIVE_FOLDER_ID=XYZ789_qualquer_ID_de_pasta

TELEGRAM_TOKEN=123456:ABCD_aqui_cola_seu_token
TELEGRAM_CHAT_IDS=1234567890_aqui_cola_seu_chat_ID

GEMINI_API_KEY=AIzaSy_aqui_cola_sua_chave_gemini

API_HOST=0.0.0.0
API_PORT=8000
DEBUG=False

SMTP_USERNAME=seu_email@gmail.com
SMTP_PASSWORD=sua_senha_de_app
```

5. Salva o arquivo como `.env` (sem o .example)
6. Coloca `service-account.json` na mesma pasta

---

## 🧪 PASSO 4: Testar (5 min)

1. Abra terminal na pasta do projeto
2. Rode:
   ```bash
   poetry run python -m insurance_manager.api.main
   ```

3. Você deve ver algo como:
   ```
   INFO:     Uvicorn running on http://0.0.0.0:8000
   ```

4. Abra browser: http://localhost:8000

5. Você deve ver: `{"status":"ok","message":"Insurance Manager API is running"}`

✅ **Funcionando!**

---

## 🚀 PASSO 5: Testar com PDF

1. Pegue um PDF de seguro (qualquer um)
2. Abra Postman (ou use online: https://www.postman.com/downloads/)
3. Cria nova requisição:
   - Tipo: POST
   - URL: `http://localhost:8000/upload-policy`
   - Clica em "Body" > "form-data"
   - Adiciona campo: `file` (tipo File)
   - Seleciona seu PDF
   - Clica "Send"

4. Se funcionar, você vai ver:
   ```json
   {
     "status": "success",
     "data": {
       "n_apolice": "123456",
       "nome": "João Silva",
       ...
     }
   }
   ```

✅ **Sistema funcionando!**

---

## 💰 PASSO 6: Vender (O mais importante!)

### Opção 1: SaaS (MELHOR) - Lucro infinito
- Você monta um servidor na nuvem
- Cliente acessa um painel
- Você cobra $99-999/mês
- Cliente nunca se preocupa com instalação

### Opção 2: Template - Venda única
- Vende o código pronto
- Cliente instala no servidor dele
- Você cobra $500-2000 (uma vez)
- Oferece suporte por email

### Opção 3: Consultoria
- Você instala e configura para o cliente
- Cobra $1000-5000 por projeto
- Oferece suporte mensal

---

## 🎯 Checklist Final

- [ ] Python instalado e funcionando
- [ ] Credenciais do Gemini
- [ ] Bot Telegram criado
- [ ] Service Account Google criado
- [ ] Arquivo `.env` preenchido
- [ ] `service-account.json` na pasta
- [ ] Sistema rodando localmente
- [ ] PDF sendo lido corretamente

---

## 📞 Próximas etapas?

Quando tudo funcionar, aviса! Aí a gente:
1. Coloca em um servidor (Railway/Heroku - fácil!)
2. Cria um painel para você usar
3. Prepara documentação para vender

**Qual dúvida?** Manda aí! 🚀
