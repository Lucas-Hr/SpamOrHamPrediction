import pandas as pd
import numpy as np
import re
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

# Sklearn imports
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, f1_score, confusion_matrix

# ========================================
# 1. NETTOYAGE PROFESSIONNEL DU MALGACHE
# ========================================
STOP_WORDS_MG = ['ny', 'dia', 'fa', 'amin', 'any', 'izay', 'ho', 'nefa', 've', 'sa', 'indray', 'hoe', 'sy', 'efa']

def nettoyer_mg(text):
    if not isinstance(text, str): return ""
    text = text.lower().replace("’", "'")
    # On garde les chiffres et % pour les montants financiers
    text = re.sub(r'[^a-z0-9% ]', ' ', text)
    # Normalisation SMS
    replacements = {r'\bzah\b': 'izaho', r'\bb\b': 'be', r'\bd\b': 'dia', r'\bt@\b': 'tamin'}
    for pattern, repl in replacements.items():
        text = re.sub(pattern, repl, text)
    return " ".join([w for w in text.split() if w not in STOP_WORDS_MG])

# ========================================
# 2. CHARGEMENT ET PRÉPARATION
# ========================================
print("📂 Chargement du dataset...")
df = pd.read_csv('dataset_final_mg.csv')
df = df.dropna(subset=['text_mg'])
df['label_num'] = df['label'].map({'spam': 1, 'ham': 0})

print("🧹 Nettoyage en cours...")
df['clean_text'] = df['text_mg'].apply(nettoyer_mg)

# Vectorisation par N-Grams (1,2) pour capter les expressions comme "nahazo vola"
vectorizer = TfidfVectorizer(max_features=3000, ngram_range=(1, 2))
X = vectorizer.fit_transform(df['clean_text'])
y = df['label_num']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# ========================================
# 3. COMPÉTITION DES MODÈLES
# ========================================
modeles = {
    "Naive Bayes": MultinomialNB(alpha=0.1),
    "Logistic Regression": LogisticRegression(solver='liblinear'),
    "SVM (Linear)": SVC(kernel='linear', probability=True),
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42)
}

resultats = []

print("\n" + "="*50)
print(f"{'Modèle':<20} | {'Accuracy':<10} | {'F1-Score':<10}")
print("="*50)

best_f1 = 0
best_model_name = ""

for nom, model in modeles.items():
    # Entraînement
    model.fit(X_train, y_train)
    # Prédiction
    y_pred = model.predict(X_test)
    
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    print(f"{nom:<20} | {acc:<10.4f} | {f1:<10.4f}")
    
    resultats.append({'nom': nom, 'f1': f1, 'model': model})
    
    if f1 > best_f1:
        best_f1 = f1
        best_model_name = nom
        joblib.dump(model, 'best_model_mg.pkl')

print("="*50)
print(f"🏆 Le gagnant est : {best_model_name} (F1: {best_f1:.4f})")

# Sauvegarde du vectorizer correspondant
joblib.dump(vectorizer, 'vectorizer_mg.pkl')

# ========================================
# 4. VISUALISATION DU GAGNANT
# ========================================

best_model = joblib.load('best_model_mg.pkl')
y_pred_final = best_model.predict(X_test)

plt.figure(figsize=(6,5))
sns.heatmap(confusion_matrix(y_test, y_pred_final), annot=True, fmt='d', cmap='Greens')
plt.title(f'Matrice de Confusion : {best_model_name}')
plt.ylabel('Réel')
plt.xlabel('Prédit')
plt.show()

# ========================================
# 5. TEST D'INFÉRENCE RÉEL
# ========================================
def verifier_message(msg):
    txt = nettoyer_mg(msg)
    vec = vectorizer.transform([txt])
    pred = best_model.predict(vec)[0]
    proba = best_model.predict_proba(vec)[0]
    lbl = "SPAM 🚨" if pred == 1 else "HAM ✅"
    print(f"\nMessage : {msg}\nRésultat : {lbl} ({max(proba)*100:.2f}% de confiance)")

print("\n--- TEST FINAL ---")
verifier_message("ndw am zay fa tara zah")
verifier_message("Felicitation!, ianao dia nahazo vola 7.000.000.000 tamin'ny societe SOMAVA")