"""Telegram notification service."""

import logging
import aiohttp
from typing import List
from insurance_manager.config import settings

logger = logging.getLogger(__name__)


class TelegramService:
    """Sends notifications via Telegram bot."""

    def __init__(self):
        self.token = settings.telegram_token
        self.chat_ids = settings.telegram_chat_ids
        self.base_url = f"https://api.telegram.org/bot{self.token}"

    async def send_message(
        self,
        text: str,
        parse_mode: str = "Markdown"
    ) -> bool:
        """
        Send message to all configured chat IDs.

        Args:
            text: Message text
            parse_mode: Telegram parse mode (Markdown, HTML, etc.)

        Returns:
            True if all messages sent successfully
        """
        results = []
        async with aiohttp.ClientSession() as session:
            for chat_id in self.chat_ids:
                try:
                    payload = {
                        "chat_id": chat_id,
                        "text": text,
                        "parse_mode": parse_mode
                    }
                    async with session.post(
                        f"{self.base_url}/sendMessage",
                        json=payload
                    ) as resp:
                        if resp.status == 200:
                            logger.info(f"✅ Message sent to Telegram chat {chat_id}")
                            results.append(True)
                        else:
                            logger.error(f"❌ Failed: {resp.status}")
                            results.append(False)
                except Exception as e:
                    logger.error(f"❌ Telegram error: {str(e)}")
                    results.append(False)

        return all(results) if results else False

    async def send_expiration_alert(
        self,
        client_name: str,
        insurance_company: str,
        expiration_date: str,
        days_remaining: int
    ) -> bool:
        """Send expiration alert."""
        if days_remaining < 0:
            status = "🚨 *VENCIDO*"
        elif days_remaining == 0:
            status = "⚠️ *VENCE HOJE*"
        else:
            status = f"⚠️ *AVISO {days_remaining} DIAS*"

        message = (
            f"{status}\n\n"
            f"*Cliente:* {client_name}\n"
            f"*Seguradora:* {insurance_company}\n"
            f"*Vencimento:* {expiration_date}"
        )

        return await self.send_message(message)

    async def send_pdf_processing_notification(
        self,
        filename: str,
        status: str = "started"
    ) -> bool:
        """Send PDF processing status notification."""
        if status == "started":
            message = f"🔍 Lendo PDF: \"{filename}\"..."
        elif status == "completed":
            message = f"✅ PDF processado: {filename}"
        elif status == "failed":
            message = f"❌ Erro ao ler: {filename}"
        else:
            return False

        return await self.send_message(message)
