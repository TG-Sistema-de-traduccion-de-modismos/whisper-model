from fastapi import FastAPI
from app.infrastructure.routes import router
from app.core.logging_config import setup_logging
from app.core.config import settings

setup_logging()
app = FastAPI(title="Whisper Model Server", version="1.0")
app.include_router(router)
