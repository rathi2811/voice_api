
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import os
import base64
import uuid

from ml_predictor import predict_voice

app = FastAPI()

API_KEY = os.getenv("API_KEY", "my_secret_key_123")


from pydantic import BaseModel, Field

class VoiceRequest(BaseModel):
    language: str
    audio_format: str = Field(..., alias="audioFormat")
    audio_base64: str = Field(..., alias="audioBase64")

    class Config:
        populate_by_name = True
@app.post("/check-voice")
def check_voice(req: VoiceRequest, x_api_key: str = Header(None)):
    ...


    # ---- API KEY CHECK ----
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    # ---- BASE64 -> FILE ----
    try:
        audio_bytes = base64.b64decode(req.audio_base64)
    except:
        raise HTTPException(status_code=400, detail="Invalid base64 audio")

    temp_path = f"/tmp/{uuid.uuid4()}.mp3"

    with open(temp_path, "wb") as f:
        f.write(audio_bytes)

    # ---- PREDICT ----


    # ---- FINAL RESPONSE ----
    return {
        "language": req.language,
        "audio_format": req.audio_format,
        "prediction": result
    }
