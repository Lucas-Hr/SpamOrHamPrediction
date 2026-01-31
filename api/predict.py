import json
import joblib
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# Charger modèles une seule fois au démarrage
BASE_DIR = Path(__file__).resolve().parent

try:
    model = joblib.load(BASE_DIR / "model_fr.pkl")
    vectorizer = joblib.load(BASE_DIR / "vectorizer_fr.pkl")
except FileNotFoundError as e:
    raise RuntimeError(f"Modèles introuvables: {e}")


def handler(request):
    """Fonction handler Vercel-compatible"""
    
    # Récupérer la méthode et le chemin
    method = request.method
    path = request.path if hasattr(request, 'path') else request.get('path', '')
    
    # CORS headers
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    
    # OPTIONS request
    if method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }
    
    # Health check
    if method == 'GET' and path == '/api/health':
        response = {
            'status': 'ok',
            'service': 'Spam Detector API'
        }
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(response)
        }
    
    # Prediction endpoint
    if method == 'POST' and path == '/api/predict':
        try:
            # Parse body
            body = request.get('body', '{}')
            if isinstance(body, bytes):
                body = body.decode('utf-8')
            
            data = json.loads(body)
            text = data.get('text', '')
            
            if not text:
                return {
                    'statusCode': 400,
                    'headers': headers,
                    'body': json.dumps({'error': 'Text required'})
                }
            
            # Vectorize
            vectorized = vectorizer.transform([text])
            
            # Predict
            prediction = model.predict(vectorized)[0]
            probs = model.predict_proba(vectorized)[0]
            classes = model.classes_.tolist()
            
            # Response
            response = {
                'prediction': str(prediction),
                'confidence': round(float(max(probs)) * 100, 2),
                'probabilities': {
                    classes[0]: round(float(probs[0]), 4),
                    classes[1]: round(float(probs[1]), 4)
                }
            }
            
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps(response)
            }
            
        except Exception as e:
            return {
                'statusCode': 500,
                'headers': headers,
                'body': json.dumps({'error': str(e)})
            }
    
    # 404
    return {
        'statusCode': 404,
        'headers': headers,
        'body': json.dumps({'error': 'Not found'})
    }
