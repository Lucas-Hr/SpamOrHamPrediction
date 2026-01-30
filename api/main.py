from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import os
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path 
app = FastAPI(title="Spam Detector API")

# Configuration CORS pour autoriser Next.js (port 3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Chargement du modèle et du vectoriseur
# Get the absolute path to the directory containing main.py
BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "model_fr.pkl"
VEC_PATH = BASE_DIR / "vectorizer_fr.pkl"

# Check if files exist using the absolute path
if not MODEL_PATH.exists() or not VEC_PATH.exists():
    import os
    files_in_dir = os.listdir(BASE_DIR)
    raise RuntimeError(
        f"Fichiers introuvables! Chemin: {BASE_DIR}. "
        f"Fichiers vus par Vercel: {files_in_dir}"
    )
model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VEC_PATH)

class SMS(BaseModel):
    text: str

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

@app.post("/predict")
async def predict_spam(sms: SMS):
    try:
        # Transformation du texte
        data = vectorizer.transform([sms.text])
        # Prédiction
        prediction = model.predict(data)[0]
        # Calcul de probabilité (optionnel mais sympa pour l'UI)
        probs = model.predict_proba(data)[0]
        classes = model.classes_.tolist()
        prob_dict = dict(zip(classes, probs))
        confidence = max(probs)

        return {
            "prediction": prediction,
            "confidence": round(float(confidence) * 100, 2),
            "is_spam": True if prediction == "spam" else False,
            "probabilities": prob_dict

        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)