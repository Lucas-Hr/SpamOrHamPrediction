from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Spam Detector API")

# Configuration CORS pour autoriser Next.js (local et Vercel)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://*.vercel.app",  # Tous les domaines Vercel
        "https://spam-or-ham-prediction.vercel.app",  # Remplacez par votre vrai domaine
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Chargement du modèle et du vectoriseur
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model_fr.pkl")
VEC_PATH = os.path.join(BASE_DIR, "vectorizer_fr.pkl")

if not os.path.exists(MODEL_PATH) or not os.path.exists(VEC_PATH):
    raise RuntimeError(f"Les fichiers .pkl sont introuvables! Cherchés: {MODEL_PATH}, {VEC_PATH}")

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VEC_PATH)

class SMS(BaseModel):
    text: str

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