import sys
import json
import joblib
from pathlib import Path

# Usage: python predict.py "votre texte à prédire"
if len(sys.argv) < 2:
    print(json.dumps({"error": "Texte manquant"}))
    sys.exit(1)

text = sys.argv[1]

BASE_DIR = Path(__file__).resolve().parent
try:
    model = joblib.load(BASE_DIR / "model_fr.pkl")
    vectorizer = joblib.load(BASE_DIR / "vectorizer_fr.pkl")
except FileNotFoundError as e:
    print(json.dumps({"error": f"Modèles introuvables: {e}"}))
    sys.exit(1)

try:
    vectorized = vectorizer.transform([text])
    prediction = model.predict(vectorized)[0]
    probs = model.predict_proba(vectorized)[0]
    classes = model.classes_.tolist()
    result = {
        "prediction": str(prediction),
        "confidence": round(float(max(probs)) * 100, 2),
        "probabilities": {
            classes[0]: round(float(probs[0]), 4),
            classes[1]: round(float(probs[1]), 4)
        }
    }
    print(json.dumps(result))
except Exception as e:
    print(json.dumps({"error": str(e)}))
    sys.exit(1)
