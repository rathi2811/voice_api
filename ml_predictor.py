# =====================================
# ML Predictor for AI vs Human Voice
# Used by API (Group 1)
# =====================================

import librosa
import numpy as np
import joblib
import os

# -------------------------------------
# Load trained model & scaler (once)
# -------------------------------------
MODEL_PATH = "voice_model.pkl"
SCALER_PATH = "scaler.pkl"

if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
    raise FileNotFoundError("Model or scaler file not found. Train the model first.")

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)


# -------------------------------------
# Feature extraction (SAME as training)
# -------------------------------------
def extract_features(audio_path):
    audio, sr = librosa.load(audio_path)

    # 1. MFCC
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
    mfcc_mean = np.mean(mfcc)
    mfcc_std = np.std(mfcc)

    # 2. Energy
    energy = np.mean(audio ** 2)

    # 3. Smoothness / variation
    variation = np.std(audio)

    # 4. Pitch disabled (stability + speed)
    pitch_var = 0

    # 5. Silence ratio
    silence_ratio = np.sum(np.abs(audio) < 0.01) / len(audio)

    return [
        mfcc_mean,
        mfcc_std,
        energy,
        variation,
        pitch_var,
        silence_ratio
    ]


# -------------------------------------
# MAIN FUNCTION (API will call this)
# -------------------------------------
def predict_voice(audio_path):
    """
    Input:
        audio_path (str): path to MP3 audio file

    Output:
        result (str): "AI_GENERATED" or "HUMAN"
        confidence (float): value between 0.0 and 1.0
    """

    features = extract_features(audio_path)

    X = np.array(features).reshape(1, -1)
    X = scaler.transform(X)

    probabilities = model.predict_proba(X)[0]
    prediction = model.predict(X)[0]

    if prediction == 1:
        return "AI_GENERATED", round(float(probabilities[1]), 2)
    else:
        return "HUMAN", round(float(probabilities[0]), 2)
