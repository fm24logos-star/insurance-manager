"""PDF processing service using Google Gemini."""

import base64
import json
import logging
import time
from typing import Optional

try:
    import google.generativeai as genai
except ImportError:
    genai = None

from insurance_manager.config import settings
from insurance_manager.models import PolicyData

logger = logging.getLogger(__name__)


class PDFProcessor:
    """Processes insurance PDFs and extracts data using Gemini AI."""

    def __init__(self):
        if genai is None:
            raise ImportError("google-generativeai not installed")
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def extract_policy_data(self, pdf_bytes: bytes, filename: str = "") -> PolicyData:
        """
        Extract insurance policy data from PDF using Gemini.

        Args:
            pdf_bytes: PDF file content as bytes
            filename: Original filename for logging

        Returns:
            PolicyData with extracted information

        Raises:
            ValueError: If extraction fails or data is invalid
        """
        try:
            base64_data = base64.standard_b64encode(pdf_bytes).decode("utf-8")

            prompt = """Extraia os dados deste PDF de seguro e formate rigorosamente em JSON:
- n_apolice: Apenas números.
- apolice_anterior: Procure pelo número da apólice que este documento está renovando/substituindo. Se não encontrar ou não tiver certeza absoluta, retorne "Não encontrado".
- nome: Iniciais maiúsculas.
- cpf: Apenas os 11 números.
- telefone: Apenas números com DDD.
- seguradora: Mapfre, Porto, Akad, Hdi, Azul - Porto, Itau - Porto, Suhai, Fairfax, Ezze, Bradesco, Tokio, Allianz, Santuu, ou Essor.
- tipo: Bike, Auto, Moto, Residencial, Vida, Rc Medico, ou Rc profissional.
- valor: Valor total.
- emissao: Data de emissão DD/MM/AAAA.
- expira_em: Data DD/MM/AAAA.
- nascimento: Data de nascimento DD/MM/AAAA.
- endereco: Endereço completo.
- email: Endereço de e-mail ou "Não encontrado".
Responda APENAS JSON puro."""

            response = self._call_gemini_with_retry(
                prompt=prompt,
                pdf_base64=base64_data,
                filename=filename,
                max_retries=3
            )

            json_str = response.strip()
            if json_str.startswith("```"):
                json_str = json_str.split("```")[1]
                if json_str.startswith("json"):
                    json_str = json_str[4:]

            data_dict = json.loads(json_str)
            policy_data = PolicyData(**data_dict)

            logger.info(f"✅ Successfully extracted policy {policy_data.n_apolice}")
            return policy_data

        except json.JSONDecodeError as e:
            logger.error(f"❌ JSON parsing error: {str(e)}")
            raise ValueError(f"Failed to parse extracted data: {str(e)}")
        except Exception as e:
            logger.error(f"❌ Error extracting data: {str(e)}")
            raise

    def _call_gemini_with_retry(
        self,
        prompt: str,
        pdf_base64: str,
        filename: str,
        max_retries: int = 3
    ) -> str:
        """Call Gemini API with retry logic."""
        for attempt in range(max_retries):
            try:
                response = self.model.generate_content([
                    prompt,
                    {"mime_type": "application/pdf", "data": pdf_base64}
                ])

                if response.text:
                    logger.info(f"✅ Gemini API call successful")
                    return response.text

            except Exception as e:
                error_str = str(e).lower()
                attempt_num = attempt + 1

                if "resource_exhausted" in error_str:
                    reason = "QUOTA EXHAUSTED - Google limited API rate"
                elif "internal" in error_str:
                    reason = "GOOGLE INSTABILITY - Server error"
                elif "invalid_argument" in error_str:
                    reason = "INVALID FILE - PDF too large or unreadable"
                else:
                    reason = str(e)

                logger.warning(f"⏳ Retry {attempt_num}/{max_retries}. Reason: {reason}")

                if attempt_num < max_retries:
                    time.sleep(8)
                else:
                    raise RuntimeError(
                        f"❌ Failed after {max_retries} attempts. Reason: {reason}"
                    )

        raise RuntimeError("Unexpected error processing PDF")
