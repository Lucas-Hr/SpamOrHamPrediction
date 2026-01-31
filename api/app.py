from flask import Flask, request, jsonify
import joblib
from pathlib import Path

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
model = joblib.load(BASE_DIR / "model_fr.pkl")
vectorizer = joblib.load(BASE_DIR / "vectorizer_fr.pkl")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "Texte manquant"}), 400
    try:
        vectorized = vectorizer.transform([text])
        prediction = model.predict(vectorized)[0]
        probs = model.predict_proba(vectorized)[0]
        classes = model.classes_.tolist()
        return jsonify({
            "prediction": str(prediction),
            "confidence": round(float(max(probs)) * 100, 2),
            "probabilities": {
                classes[0]: round(float(probs[0]), 4),
                classes[1]: round(float(probs[1]), 4)
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "Spam Detector API"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
