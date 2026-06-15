# Insurance Manager 🛡️

Professional insurance policy management system with automated PDF processing, Google Sheets integration, and Telegram notifications.

## Features ✨

- **PDF Processing**: Automatic extraction of policy data using Google Gemini AI
- **Telegram Notifications**: Real-time alerts for expirations and processing status
- **Email Reminders**: Automated renewal and mid-term reminders
- **REST API**: FastAPI-powered API for easy integration
- **Environment Configuration**: Secure credential management via .env

## Quick Start 🚀

### Prerequisites
- Python 3.10+
- Poetry
- Google Gemini API Key
- Telegram Bot Token

### Installation

```bash
# Clone repository
git clone https://github.com/fm24logos-star/insurance-manager.git
cd insurance-manager

# Install dependencies
poetry install

# Create .env file
cp .env.example .env

# Edit .env with your credentials
nano .env

# Run API
poetry run python -m insurance_manager.api.main
```

## Configuration 📋

Create `.env` file with your credentials:

```env
GOOGLE_SHEETS_CREDENTIALS_JSON=path/to/service-account.json
GOOGLE_SPREADSHEET_ID=your-spreadsheet-id
TELEGRAM_TOKEN=your-bot-token
TELEGRAM_CHAT_IDS=chat_id_1,chat_id_2
GEMINI_API_KEY=your-gemini-api-key
GOOGLE_DRIVE_FOLDER_ID=your-folder-id
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=False
```

## Usage 📖

### Health Check
```bash
curl http://localhost:8000/
```

### Upload Policy PDF
```bash
curl -X POST "http://localhost:8000/upload-policy" \
  -H "accept: application/json" \
  -F "file=@policy.pdf"
```

Response:
```json
{
  "status": "success",
  "message": "Policy processed successfully",
  "data": {
    "n_apolice": "123456",
    "nome": "João Silva",
    "cpf": "12345678901",
    "seguradora": "Porto",
    "tipo": "Auto",
    "expira_em": "15/06/2025"
  }
}
```

## API Endpoints

- `GET /` - Health check
- `POST /upload-policy` - Upload and process PDF
- `POST /webhook/telegram` - Telegram webhook

## Project Structure 🏗️

```
insurance_manager/
├── api/              # FastAPI application
├── services/         # Business logic
│   ├── pdf_processor.py      # Gemini PDF extraction
│   ├── telegram_service.py   # Telegram notifications
│   └── email_service.py      # Email sending
├── models.py         # Pydantic data models
└── config.py         # Environment configuration
```

## Key Features 🎯

### PDF Extraction
Uses Google Gemini AI to extract insurance policy data:
- Policy number
- Client name and CPF
- Insurance company and type
- Expiration date
- Contact information

### Telegram Integration
Real-time notifications for:
- PDF processing status
- Policy expiration alerts
- Success/error messages

### Email Service
Sends automated emails for:
- Renewal reminders (15 days before expiration)
- Mid-term reminders (50% of policy term)

## Security 🔐

- Credentials managed via environment variables
- No sensitive data in code
- HTTPS ready
- Input validation with Pydantic

## Deployment 🌐

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
RUN pip install poetry
COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-dev
COPY insurance_manager ./insurance_manager
CMD ["poetry", "run", "python", "-m", "insurance_manager.api.main"]
```

### Environment Variables
Set all variables from `.env.example` in your hosting platform (Heroku, Railway, etc.)

## Customization 🎨

### Add Custom Fields
Edit `insurance_manager/models.py`:
```python
class PolicyData(BaseModel):
    your_field: Optional[str] = Field(None, description="Description")
```

### Change PDF Extraction Logic
Edit `insurance_manager/services/pdf_processor.py` and update the Gemini prompt.

## Troubleshooting 🐛

### "QUOTA_EXHAUSTED" Error
- Google Gemini has rate limits
- Retry logic with 8-second delays is implemented
- Upgrade API tier if needed

### Service Account Error
- Verify credentials JSON file exists
- Check file permissions
- Share Sheets and Drive with service account email

### Telegram Not Sending
- Verify TOKEN is correct
- Check CHAT_IDS format (comma-separated)
- Run `/start` with bot first

## License 📄

MIT License - See LICENSE file

## Support 💬

- Issues: [GitHub Issues](https://github.com/fm24logos-star/insurance-manager/issues)
- Email: support@arvani.com.br
- WhatsApp: (11) 91536-1616

---

**Made with ❤️ by Arvani Corretora de Seguros**
