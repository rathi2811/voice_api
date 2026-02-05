import os
import joblib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "voice_model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "scaler.pkl")


# Load model & scaler safely
model = None
scaler = None

if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)


def predict_voice(audio_path: str):
    """
    Dummy prediction function.
    Tumhare actual ML features yaha aayenge.
    Abhi ke liye stable response de raha hai taaki API deploy ho jaye.
    """

    # agar model missing hai
    if model is None or scaler is None:
        return {
            "prediction": "unknown",
            "confidence": 0.0,
            "reason": "Model/Scaler file not found"
        }

    # Abhi placeholder return
    return {
        "prediction": "real",
        "confidence": 0.75
    }
