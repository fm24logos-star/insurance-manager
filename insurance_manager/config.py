"""Configuration module using environment variables."""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Google Sheets
    google_sheets_credentials_json: str
    google_spreadsheet_id: str

    # Telegram
    telegram_token: str
    telegram_chat_ids: List[str]

    # Google Gemini
    gemini_api_key: str

    # Google Drive
    google_drive_folder_id: str

    # Server
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = False

    # Email
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""

    # Webhook
    webhook_url: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
