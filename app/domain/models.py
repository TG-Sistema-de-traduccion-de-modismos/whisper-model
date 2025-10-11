from pydantic import BaseModel
from typing import Optional

class InferenceResponse(BaseModel):
    transcription: str
    model: Optional[str] = None
    device: Optional[str] = None
    duration_seconds: Optional[float] = None
