import pandas as pd
import numpy as np
import re
import string
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns

# ========================================
# ÉTAPE 1: CHARGEMENT DES DONNÉES
# ========================================
print("=" * 60)
print("CHARGEMENT DES DONNÉES")
print("=" * 60)

df = pd.read_csv('/mnt/user-data/outputs/spam_detection_dataset.csv')
print(f"Nombre total de messages: {len(df)}")
print(f"Spam (1): {(df['label'] == 1).sum()} ({(df['label'] == 1).sum() / len(df) * 100:.1f}%)")
print(f"Normal (0): {(df['label'] == 0).sum()} ({(df['label'] == 0).sum() / len(df) * 100:.1f}%)")
print(f"\nExemples de données:")
print(df.head())

# ========================================
# ÉTAPE 2: NETTOYAGE
# ========================================
print("\n" + "=" * 60)
print("ÉTAPE 2: NETTOYAGE DU TEXTE")
print("=" * 60)

def nettoyer_texte(texte):
    """
    Nettoie le texte en:
    - Supprimant les URLs
    - Supprimant les emails
    - Supprimant les chiffres (optionnel, on garde pour le contexte)
    - Supprimant les caractères spéciaux excessifs
    - Normalisant les espaces
    """
    # Supprimer les URLs
    texte = re.sub(r'http\S+|www\.\S+', '', texte)
    texte = re.sub(r'\S+\.(com|fr|net|org)\S*', '', texte)
    
    # Supprimer les emails
    texte = re.sub(r'\S+@\S+', '', texte)
    
    # Normaliser les espaces multiples
    texte = re.sub(r'\s+', ' ', texte)
    
    # Supprimer les espaces en début et fin
    texte = texte.strip()
    
    return texte

df['texte_nettoye'] = df['message'].apply(nettoyer_texte)
print("Exemple avant nettoyage:")
print(df['message'].iloc[0])
print("\nAprès nettoyage:")
print(df['texte_nettoye'].iloc[0])

# ========================================
# ÉTAPE 3: TOKENISATION
# ========================================
print("\n" + "=" * 60)
print("ÉTAPE 3: TOKENISATION")
print("=" * 60)

def tokeniser(texte):
    """
    Tokenise le texte en mots individuels
    """
    # Convertir en minuscules pour la normalisation
    texte = texte.lower()
    
    # Séparer par espaces et ponctuation
    tokens = re.findall(r'\b\w+\b', texte)
    
    return tokens

df['tokens'] = df['texte_nettoye'].apply(tokeniser)
print("Exemple de tokenisation:")
print(f"Texte: {df['texte_nettoye'].iloc[0]}")
print(f"Tokens: {df['tokens'].iloc[0]}")

# ========================================
# ÉTAPE 4: SUPPRESSION DES STOPWORDS (LÉGER)
# ========================================
print("\n" + "=" * 60)
print("ÉTAPE 4: SUPPRESSION DES STOPWORDS (LÉGER)")
print("=" * 60)

# Liste légère de stopwords français (les plus communs)
stopwords_fr = {
    'le', 'la', 'les', 'un', 'une', 'des', 'du', 'de', 'et', 'ou', 
    'mais', 'donc', 'or', 'ni', 'car', 'ce', 'ces', 'cet', 'cette',
    'est', 'sont', 'a', 'ont', 'être', 'avoir', 'fait', 'faire',
    'je', 'tu', 'il', 'elle', 'nous', 'vous', 'ils', 'elles',
    'mon', 'ton', 'son', 'ma', 'ta', 'sa', 'mes', 'tes', 'ses',
    'dans', 'sur', 'sous', 'avec', 'sans', 'pour', 'par', 'en'
}

def supprimer_stopwords(tokens):
    """
    Supprime les stopwords de la liste de tokens
    """
    return [token for token in tokens if token not in stopwords_fr and len(token) > 1]

df['tokens_filtres'] = df['tokens'].apply(supprimer_stopwords)
print("Exemple avant suppression stopwords:")
print(df['tokens'].iloc[0])
print("\nAprès suppression stopwords:")
print(df['tokens_filtres'].iloc[0])

# ========================================
# ÉTAPE 5: NORMALISATION
# ========================================
print("\n" + "=" * 60)
print("ÉTAPE 5: NORMALISATION")
print("=" * 60)

def normaliser(tokens):
    """
    Normalise les tokens:
    - Déjà en minuscules (fait lors de la tokenisation)
    - Supprime la ponctuation résiduelle
    - Garde les accents (important pour le français)
    """
    tokens_normalises = []
    for token in tokens:
        # Supprimer la ponctuation résiduelle
        token = token.strip(string.punctuation)
        if token:  # Si le token n'est pas vide après nettoyage
            tokens_normalises.append(token)
    return tokens_normalises

df['tokens_normalises'] = df['tokens_filtres'].apply(normaliser)

# Reconstruire le texte pour TF-IDF
df['texte_final'] = df['tokens_normalises'].apply(lambda x: ' '.join(x))

print("Exemple de texte final normalisé:")
print(df['texte_final'].iloc[0])

# ========================================
# ÉTAPE 6: TF-IDF (1-2 GRAMS)
# ========================================
print("\n" + "=" * 60)
print("ÉTAPE 6: VECTORISATION TF-IDF (1-2 GRAMS)")
print("=" * 60)

# Séparation des données
X = df['texte_final']
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Taille du jeu d'entraînement: {len(X_train)}")
print(f"Taille du jeu de test: {len(X_test)}")

# Vectorisation TF-IDF avec 1-grams et 2-grams
tfidf_vectorizer = TfidfVectorizer(
    ngram_range=(1, 2),  # 1-grams et 2-grams
    max_features=5000,    # Limiter le nombre de features
    min_df=2,             # Ignorer les termes qui apparaissent dans moins de 2 documents
    max_df=0.95           # Ignorer les termes qui apparaissent dans plus de 95% des documents
)

X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
X_test_tfidf = tfidf_vectorizer.transform(X_test)

print(f"Shape des features TF-IDF: {X_train_tfidf.shape}")
print(f"Nombre de features (n-grams): {len(tfidf_vectorizer.get_feature_names_out())}")

# Afficher quelques features importantes
features = tfidf_vectorizer.get_feature_names_out()
print(f"\nExemples de features (n-grams):")
print(f"Premiers 20: {features[:20]}")
print(f"Derniers 20: {features[-20:]}")

# ========================================
# ÉTAPE 7: ENTRAÎNEMENT DES MODÈLES ML
# ========================================
print("\n" + "=" * 60)
print("ÉTAPE 7: ENTRAÎNEMENT DES MODÈLES ML")
print("=" * 60)

# Dictionnaire pour stocker les modèles et leurs performances
modeles = {
    'Naive Bayes': MultinomialNB(),
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
    'SVM': SVC(kernel='linear', probability=True, random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42)
}

resultats = {}

for nom, modele in modeles.items():
    print(f"\n{'='*60}")
    print(f"Entraînement: {nom}")
    print(f"{'='*60}")
    
    # Entraînement
    modele.fit(X_train_tfidf, y_train)
    
    # Prédictions
    y_pred = modele.predict(X_test_tfidf)
    
    # Calcul des métriques
    accuracy = accuracy_score(y_test, y_pred)
    
    # Cross-validation (sur le jeu d'entraînement)
    cv_scores = cross_val_score(modele, X_train_tfidf, y_train, cv=5)
    
    print(f"\nAccuracy sur le test: {accuracy:.4f}")
    print(f"Cross-validation scores: {cv_scores}")
    print(f"CV Mean: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
    
    print(f"\nRapport de classification:")
    print(classification_report(y_test, y_pred, 
                                target_names=['Normal (0)', 'Spam (1)'],
                                digits=4))
    
    # Matrice de confusion
    cm = confusion_matrix(y_test, y_pred)
    print(f"\nMatrice de confusion:")
    print(f"                Prédit Normal  Prédit Spam")
    print(f"Réel Normal     {cm[0][0]:^14d} {cm[0][1]:^12d}")
    print(f"Réel Spam       {cm[1][0]:^14d} {cm[1][1]:^12d}")
    
    # Stocker les résultats
    resultats[nom] = {
        'modele': modele,
        'accuracy': accuracy,
        'cv_scores': cv_scores,
        'y_pred': y_pred,
        'confusion_matrix': cm
    }

# ========================================
# COMPARAISON DES MODÈLES
# ========================================
print("\n" + "=" * 60)
print("COMPARAISON DES MODÈLES")
print("=" * 60)

comparaison = pd.DataFrame({
    'Modèle': list(resultats.keys()),
    'Accuracy': [resultats[m]['accuracy'] for m in resultats.keys()],
    'CV Mean': [resultats[m]['cv_scores'].mean() for m in resultats.keys()],
    'CV Std': [resultats[m]['cv_scores'].std() for m in resultats.keys()]
})

comparaison = comparaison.sort_values('Accuracy', ascending=False)
print("\n", comparaison.to_string(index=False))

# Meilleur modèle
meilleur_modele_nom = comparaison.iloc[0]['Modèle']
meilleur_modele = resultats[meilleur_modele_nom]['modele']
print(f"\n🏆 Meilleur modèle: {meilleur_modele_nom} (Accuracy: {comparaison.iloc[0]['Accuracy']:.4f})")

# ========================================
# VISUALISATIONS
# ========================================
print("\n" + "=" * 60)
print("CRÉATION DES VISUALISATIONS")
print("=" * 60)

# Figure 1: Comparaison des accuracies
fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# Graphique 1: Accuracies
ax1 = axes[0, 0]
modeles_noms = list(resultats.keys())
accuracies = [resultats[m]['accuracy'] for m in modeles_noms]
colors = ['#2ecc71' if acc == max(accuracies) else '#3498db' for acc in accuracies]
bars = ax1.bar(modeles_noms, accuracies, color=colors, alpha=0.8, edgecolor='black')
ax1.set_ylabel('Accuracy', fontsize=12, fontweight='bold')
ax1.set_title('Comparaison des Accuracies des Modèles', fontsize=14, fontweight='bold')
ax1.set_ylim([0.85, 1.0])
ax1.grid(axis='y', alpha=0.3)
for bar in bars:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:.4f}', ha='center', va='bottom', fontweight='bold')

# Graphique 2: Matrice de confusion du meilleur modèle
ax2 = axes[0, 1]
cm = resultats[meilleur_modele_nom]['confusion_matrix']
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax2, 
            xticklabels=['Normal', 'Spam'],
            yticklabels=['Normal', 'Spam'],
            cbar_kws={'label': 'Nombre de prédictions'})
ax2.set_title(f'Matrice de Confusion - {meilleur_modele_nom}', fontsize=14, fontweight='bold')
ax2.set_ylabel('Vraie Classe', fontsize=12, fontweight='bold')
ax2.set_xlabel('Classe Prédite', fontsize=12, fontweight='bold')

# Graphique 3: Scores de cross-validation
ax3 = axes[1, 0]
for nom, data in resultats.items():
    cv_scores = data['cv_scores']
    ax3.plot(range(1, 6), cv_scores, marker='o', label=nom, linewidth=2)
ax3.set_xlabel('Fold', fontsize=12, fontweight='bold')
ax3.set_ylabel('Score', fontsize=12, fontweight='bold')
ax3.set_title('Scores de Cross-Validation (5-Fold)', fontsize=14, fontweight='bold')
ax3.legend()
ax3.grid(True, alpha=0.3)
ax3.set_ylim([0.85, 1.0])

# Graphique 4: Distribution des classes dans le dataset
ax4 = axes[1, 1]
labels = ['Normal (0)', 'Spam (1)']
sizes = [(df['label'] == 0).sum(), (df['label'] == 1).sum()]
colors_pie = ['#3498db', '#e74c3c']
explode = (0.05, 0.05)
wedges, texts, autotexts = ax4.pie(sizes, explode=explode, labels=labels, colors=colors_pie,
                                     autopct='%1.1f%%', shadow=True, startangle=90)
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(12)
ax4.set_title('Distribution des Classes dans le Dataset', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('/mnt/user-data/outputs/spam_detection_results.png', dpi=300, bbox_inches='tight')
print("Visualisations sauvegardées: spam_detection_results.png")

# ========================================
# TEST AVEC DE NOUVEAUX MESSAGES
# ========================================
print("\n" + "=" * 60)
print("TEST AVEC DE NOUVEAUX MESSAGES")
print("=" * 60)

def pipeline_prediction(texte):
    """
    Pipeline complet pour prédire si un message est un spam
    """
    # Nettoyage
    texte_nettoye = nettoyer_texte(texte)
    
    # Tokenisation
    tokens = tokeniser(texte_nettoye)
    
    # Suppression stopwords
    tokens_filtres = supprimer_stopwords(tokens)
    
    # Normalisation
    tokens_normalises = normaliser(tokens_filtres)
    
    # Reconstruction du texte
    texte_final = ' '.join(tokens_normalises)
    
    # Vectorisation TF-IDF
    texte_tfidf = tfidf_vectorizer.transform([texte_final])
    
    # Prédiction
    prediction = meilleur_modele.predict(texte_tfidf)[0]
    proba = meilleur_modele.predict_proba(texte_tfidf)[0] if hasattr(meilleur_modele, 'predict_proba') else None
    
    return prediction, proba

# Messages de test
messages_test = [
    "Gagnez 5000€ en 24h ! Cliquez maintenant sur ce lien !",
    "Salut, tu es disponible pour déjeuner demain ?",
    "URGENT: Votre compte bancaire a été suspendu ! Vérifiez immédiatement",
    "Merci pour votre email, je reviens vers vous rapidement",
    "💰💰 ARGENT FACILE 💰💰 Devenez riche sans effort !!!",
    "La réunion est confirmée pour lundi à 14h",
    "Félicitations ! Vous avez gagné un iPhone gratuit ! Réclamez-le ici",
    "Bonjour, voici le rapport que vous m'aviez demandé"
]

print("\nTest du pipeline sur de nouveaux messages:\n")
for i, message in enumerate(messages_test, 1):
    prediction, proba = pipeline_prediction(message)
    classe = "SPAM 🚨" if prediction == 1 else "NORMAL ✅"
    
    print(f"{i}. Message: {message[:60]}...")
    print(f"   Prédiction: {classe}")
    if proba is not None:
        print(f"   Probabilités: Normal={proba[0]:.3f}, Spam={proba[1]:.3f}")
    print()

# ========================================
# SAUVEGARDE DU MODÈLE
# ========================================
print("=" * 60)
print("SAUVEGARDE DU MODÈLE ET DU VECTORIZER")
print("=" * 60)

import joblib

# Sauvegarder le meilleur modèle et le vectorizer
joblib.dump(meilleur_modele, '/mnt/user-data/outputs/spam_detector_model.pkl')
joblib.dump(tfidf_vectorizer, '/mnt/user-data/outputs/tfidf_vectorizer.pkl')

print(f"✅ Modèle sauvegardé: spam_detector_model.pkl")
print(f"✅ Vectorizer sauvegardé: tfidf_vectorizer.pkl")

print("\n" + "=" * 60)
print("PIPELINE TERMINÉ AVEC SUCCÈS ! 🎉")
print("=" * 60)
