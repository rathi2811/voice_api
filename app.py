from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import requests
import tempfile
import os

from ml_predictor import predict_voice

app = FastAPI()
class VoiceRequest(BaseModel):
    audio_url: str
API_KEY = "my_secret_key_123"
@app.get("/")
def home():
    return {"message": "API chal rahi hai"}

@app.post("/check-voice")
def check_voice(data: VoiceRequest, authorization: str = Header(None)):

    # API KEY CHECK
if not authorization:
    raise HTTPException(status_code=401, detail="Authorization header missing")

if not authorization.startswith("Bearer "):
    raise HTTPException(status_code=401, detail="Invalid token format")

token = authorization.split(" ")[1]

if token != API_KEY:
    raise HTTPException(status_code=401, detail="Invalid API key")

    # AUDIO DOWNLOAD
    try:
        response = requests.get(data.audio_url, timeout=10)
        response.raise_for_status()
    except:
        raise HTTPException(status_code=400, detail="Invalid audio URL")

    # TEMP FILE SAVE
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp:
        temp.write(response.content)
        audio_path = temp.name

    # ML PREDICTION
    try:
        result, confidence = predict_voice(audio_path)
    except:
        os.remove(audio_path)
        raise HTTPException(status_code=500, detail="Prediction failed")

    # CLEANUP
    os.remove(audio_path)

    return {
        "result": result,
        "confidence": round(float(confidence), 3)
    }


