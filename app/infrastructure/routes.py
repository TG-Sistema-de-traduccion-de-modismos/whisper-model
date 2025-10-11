from fastapi import APIRouter, UploadFile, File, HTTPException
import tempfile, os, logging
from app.application.model_wrapper import ModelWrapper
from app.domain.models import InferenceResponse
from app.core.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)

model_wrapper = ModelWrapper()

@router.post("/infer", response_model=InferenceResponse)
async def infer(file: UploadFile = File(...)):
    if not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="El archivo debe ser audio")

    tmp_path = None
    try:
        suffix = os.path.splitext(file.filename)[1] or ".wav"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        result = model_wrapper.transcribe_wav_path(tmp_path, language="es")
        return result

    except Exception as e:
        logger.exception("Error en /infer: %s", e)
        raise HTTPException(status_code=500, detail=f"Error en inferencia: {str(e)}")
    finally:
        try:
            if tmp_path and os.path.exists(tmp_path):
                os.unlink(tmp_path)
        except Exception:
            pass

@router.get("/health")
def health():
    available = model_wrapper.model is not None
    return {
        "status": "ok" if available else "degraded",
        "model_loaded": available,
        "model_name": model_wrapper.model_name,
        "device": model_wrapper.device
    }
