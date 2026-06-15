"""FastAPI application main module."""

import logging
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from insurance_manager.config import settings
from insurance_manager.services.pdf_processor import PDFProcessor
from insurance_manager.services.telegram_service import TelegramService
from insurance_manager.services.email_service import EmailService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="Insurance Manager API",
    description="Professional insurance policy management system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
pdf_processor = PDFProcessor()
telegram_service = TelegramService()
email_service = EmailService()


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "message": "Insurance Manager API is running"}


@app.post("/upload-policy")
async def upload_policy(file: UploadFile = File(...)):
    """
    Upload and process an insurance PDF.

    Args:
        file: PDF file to upload

    Returns:
        Extracted policy data
    """
    try:
        contents = await file.read()
        filename = file.filename or "policy.pdf"

        # Send processing notification
        await telegram_service.send_pdf_processing_notification(filename, "started")

        # Extract policy data
        policy_data = pdf_processor.extract_policy_data(contents, filename)

        # Send success notification
        msg = f"✅ SUCESSO: {policy_data.nome}"
        await telegram_service.send_message(msg)

        return {
            "status": "success",
            "message": "Policy processed successfully",
            "data": policy_data.dict()
        }

    except ValueError as e:
        error_msg = f"❌ Erro ao ler PDF: {str(e)}"
        await telegram_service.send_message(error_msg)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        error_msg = f"❌ Erro ao processar: {str(e)}"
        await telegram_service.send_message(error_msg)
        logger.error(f"Error processing file: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/webhook/telegram")
async def telegram_webhook(request_body: dict):
    """Telegram webhook endpoint for handling bot messages."""
    try:
        if "message" in request_body:
            message = request_body["message"]
            text = message.get("text", "").lower()

            if text == "/ajuda":
                await telegram_service.send_message(
                    "🤖 *Comandos:*\n"
                    "/upload - Enviar PDF\n"
                    "/ajuda - Este menu"
                )

        return {"ok": True}

    except Exception as e:
        logger.error(f"Error handling webhook: {str(e)}")
        return {"ok": False}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )
