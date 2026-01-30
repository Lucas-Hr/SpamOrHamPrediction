import joblib
import re
import pandas as pd

# ========================================
# 1. ARCHITECTURE DE NETTOYAGE (Identique à l'entraînement)
# ========================================
STOP_WORDS_MG = ['ny', 'dia', 'fa', 'amin', 'any', 'izay', 'ho', 'nefa', 've', 'sa', 'indray', 'hoe', 'sy', 'efa']

def nettoyer_mg(text):
    if not isinstance(text, str): return ""
    # Normalisation de base
    text = text.lower().replace("’", "'")
    text = re.sub(r'[^a-z0-9% ]', ' ', text)
    
    # Gestion des abréviations SMS malgaches
    replacements = {
        r'\bzah\b': 'izaho', 
        r'\bb\b': 'be', 
        r'\bd\b': 'dia', 
        r'\bt@\b': 'tamin',
        r'\bav\b': 'avy',
        r'\bew\b': 'eo'
    }
    for pattern, repl in replacements.items():
        text = re.sub(pattern, repl, text)
        
    return " ".join([w for w in text.split() if w not in STOP_WORDS_MG])

# ========================================
# 2. CHARGEMENT DES FICHIERS PICKLE
# ========================================
try:
    print("🔄 Chargement du modèle et du vectorizer...")
    model = joblib.load('best_model_mg.pkl')
    vectorizer = joblib.load('vectorizer_mg.pkl')
    print("✅ Architecture Naive Bayes prête.")
except FileNotFoundError:
    print("❌ Erreur : Les fichiers .pkl sont introuvables. Vérifiez les noms.")
    exit()

# ========================================
# 3. FONCTION DE PRÉDICTION ET MÉTRIQUES
# ========================================
def analyser_message():
    print("\n" + "="*50)
    print("Saisissez un message (ou tapez 'quitter' pour sortir)")
    print("="*50)
    
    while True:
        user_input = input("\n📝 Message à tester : ")
        
        if user_input.lower() == 'quitter':
            break
            
        # Prétraitement
        cleaned_text = nettoyer_mg(user_input)
        
        # Transformation vectorielle
        vectorized_text = vectorizer.transform([cleaned_text])
        
        # Prédiction
        prediction = model.predict(vectorized_text)[0]
        probabilities = model.predict_proba(vectorized_text)[0]
        
        # Affichage des résultats
        label = "SPAM 🚨" if prediction == 1 else "HAM ✅"
        confiance = probabilities[prediction] * 100
        
        print(f"\n--- RÉSULTATS DE L'ÉVALUATION ---")
        print(f"🔹 Texte nettoyé : {cleaned_text}")
        print(f"🔹 Classification : {label}")
        print(f"🔹 Score de confiance : {confiance:.2f}%")
        
        # Explication des métriques locales (pourquoi ce choix ?)
        # On montre la probabilité pour chaque classe
        print(f"📊 Métriques de probabilité : [Ham: {probabilities[0]:.4f} | Spam: {probabilities[1]:.4f}]")

# Lancement de l'interface de commande
if __name__ == "__main__":
    analyser_message()