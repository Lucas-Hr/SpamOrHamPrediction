import json
import joblib
from pathlib import Path

# Charger modèles une seule fois au démarrage
BASE_DIR = Path(__file__).resolve().parent

try:
    model = joblib.load(BASE_DIR / "model_fr.pkl")
    vectorizer = joblib.load(BASE_DIR / "vectorizer_fr.pkl")
except FileNotFoundError as e:
    raise RuntimeError(f"Modèles introuvables: {e}")


def handler(req, res):
    """Vercel Serverless Function - Predict endpoint"""
    
    # CORS headers
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    res.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    
    # OPTIONS request
    if req.method == 'OPTIONS':
        return res.status(200).end()
    
    # Health check
    if req.method == 'GET' and req.path == '/api/health':
        return res.status(200).json({
            'status': 'ok',
            'service': 'Spam Detector API'
        })
    
    # Prediction endpoint
    if req.method == 'POST' and req.path == '/api/predict':
        try:
            # Parse body
            body = req.body if isinstance(req.body, dict) else {}
            text = body.get('text', '')
            
            if not text:
                return res.status(400).json({'error': 'Text required'})
            
            # Vectorize
            vectorized = vectorizer.transform([text])
            
            # Predict
            prediction = model.predict(vectorized)[0]
            probs = model.predict_proba(vectorized)[0]
            classes = model.classes_.tolist()
            
            # Response
            return res.status(200).json({
                'prediction': str(prediction),
                'confidence': round(float(max(probs)) * 100, 2),
                'probabilities': {
                    classes[0]: round(float(probs[0]), 4),
                    classes[1]: round(float(probs[1]), 4)
                }
            })
            
        except Exception as e:
            return res.status(500).json({'error': str(e)})
    
    # 404
    return res.status(404).json({'error': 'Not found'})
