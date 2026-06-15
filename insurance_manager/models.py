"""Data models for insurance policies."""

from pydantic import BaseModel, Field
from typing import Optional


class PolicyData(BaseModel):
    """Extracted data from insurance PDF."""

    n_apolice: str = Field(..., description="Policy number (digits only)")
    apolice_anterior: Optional[str] = Field(None, description="Previous policy number")
    nome: str = Field(..., description="Client name")
    cpf: str = Field(..., description="CPF (11 digits)")
    telefone: str = Field(..., description="Phone with area code")
    seguradora: str = Field(..., description="Insurance company")
    tipo: str = Field(..., description="Insurance type")
    valor: str = Field(..., description="Total value")
    emissao: str = Field(..., description="Issue date DD/MM/YYYY")
    expira_em: str = Field(..., description="Expiration date DD/MM/YYYY")
    nascimento: str = Field(..., description="Birth date DD/MM/YYYY")
    endereco: str = Field(..., description="Full address")
    email: Optional[str] = Field(None, description="Email address")


class NotificationPayload(BaseModel):
    """Telegram notification payload."""

    message: str
    parse_mode: str = "Markdown"


class RenewalReminder(BaseModel):
    """Email renewal reminder."""

    client_name: str
    email: str
    insurance_company: str
    expiration_date: str
    days_remaining: int
