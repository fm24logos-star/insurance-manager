"""Email service for sending notifications."""

import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from insurance_manager.config import settings

logger = logging.getLogger(__name__)


class EmailService:
    """Sends email notifications for renewals and reminders."""

    def __init__(self):
        self.smtp_server = settings.smtp_server
        self.smtp_port = settings.smtp_port
        self.username = settings.smtp_username
        self.password = settings.smtp_password

    def send_renewal_reminder(
        self,
        recipient_email: str,
        client_name: str,
        insurance_company: str,
        expiration_date: str,
        days_remaining: int
    ) -> bool:
        """Send renewal reminder email."""
        try:
            subject = f"⚠️ Lembrete de Renovação: Seu seguro {insurance_company}"
            body = f"""Olá, {client_name}, tudo bem?

Gostaríamos de lembrar que o seu seguro da {insurance_company} vence em {days_remaining} dias, previsto para o dia {expiration_date}.

Para garantirmos a continuidade da sua proteção e buscarmos as melhores condições para a renovação, por favor, entre em contato conosco o quanto antes.

Att.
Arvani Corretora de Seguros
(11) 91536-1616
            """

            return self._send_email(recipient_email, subject, body)

        except Exception as e:
            logger.error(f"❌ Error sending renewal reminder: {str(e)}")
            return False

    def send_mid_term_reminder(
        self,
        recipient_email: str,
        client_name: str,
        insurance_company: str,
        expiration_date: str
    ) -> bool:
        """Send mid-term reminder email."""
        try:
            subject = f"Seguro {insurance_company} na metade da vigência"
            body = f"""Olá, {client_name}, tudo bem?

Passando apenas para desejar um ótimo dia e lembrar que estamos na metade da vigência do seu seguro da {insurance_company}.

Sua proteção segue ativa até o dia {expiration_date}. Não precisa fazer nada agora, mas lembre-se que estamos à disposição para qualquer dúvida ou assistência que precisar!

Att.,
Arvani Corretora de Seguros
(11) 91536-1616
            """

            return self._send_email(recipient_email, subject, body)

        except Exception as e:
            logger.error(f"❌ Error sending reminder: {str(e)}")
            return False

    def _send_email(self, recipient: str, subject: str, body: str) -> bool:
        """Internal method to send email."""
        try:
            if not self.username or not self.password:
                logger.warning("⚠️ Email service not configured")
                return False

            msg = MIMEMultipart()
            msg["From"] = self.username
            msg["To"] = recipient
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)

            logger.info(f"✅ Email sent to {recipient}")
            return True

        except Exception as e:
            logger.error(f"❌ Error sending email: {str(e)}")
            return False
