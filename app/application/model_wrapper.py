import logging
import tempfile
import os
import time
from app.core.config import settings

logger = logging.getLogger(__name__)

try:
    from faster_whisper import WhisperModel
    _FW_AVAILABLE = True
except Exception as e:
    logger.warning("faster_whisper not available: %s", e)
    _FW_AVAILABLE = False

class ModelWrapper:
    def __init__(self):
        self.model_name = settings.MODEL_NAME
        self.device = settings.DEVICE
        self.model = None
        if _FW_AVAILABLE:
            try:
                logger.info("Cargando faster-whisper model='%s' device=%s", self.model_name, self.device)
                self.model = WhisperModel(self.model_name, device=self.device)
                logger.info("Modelo cargado correctamente.")
            except Exception as e:
                logger.exception("Error cargando modelo: %s", e)
                self.model = None
        else:
            logger.info("faster-whisper no disponible, modo simulación activado.")

    def transcribe_wav_path(self, wav_path: str, language: str | None = "es") -> dict:
        start = time.time()
        transcription = ""
        used_model = None
        device = self.device

        if self.model is not None:
            try:
                segments, info = self.model.transcribe(wav_path, language=language)
                transcription = " ".join([s.text for s in segments]).strip()
                used_model = self.model_name
            except Exception as e:
                logger.exception("Error during model.transcribe: %s", e)
                transcription = ""
        else:
            transcription = "[simulated transcription]"

        duration = time.time() - start
        return {
            "transcription": transcription,
            "model": used_model,
            "device": device,
            "duration_seconds": round(duration, 3)
        }
