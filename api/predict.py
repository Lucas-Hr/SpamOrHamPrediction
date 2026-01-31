from http.server import BaseHTTPRequestHandler
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

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/predict':
            try:
                # Lire le body
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length)
                data = json.loads(body.decode('utf-8'))
                
                text = data.get('text', '')
                if not text:
                    self._send_response(400, {"error": "Text required"})
                    return
                
                # Vectoriser
                vectorized = vectorizer.transform([text])
                
                # Prédire
                prediction = model.predict(vectorized)[0]
                probs = model.predict_proba(vectorized)[0]
                classes = model.classes_.tolist()
                
                # Réponse
                response = {
                    "prediction": str(prediction),
                    "confidence": round(float(max(probs)) * 100, 2),
                    "probabilities": {
                        classes[0]: round(float(probs[0]), 4),
                        classes[1]: round(float(probs[1]), 4)
                    }
                }
                
                self._send_response(200, response)
                
            except Exception as e:
                self._send_response(500, {"error": str(e)})
        else:
            self._send_response(404, {"error": "Not found"})
    
    def do_GET(self):
        if self.path == '/api/health':
            self._send_response(200, {"status": "ok"})
        else:
            self._send_response(404, {"error": "Not found"})
    
    def _send_response(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
