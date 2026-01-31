# Traitement Automatique de Langage Naturel
Institut : **ISPM – Institut Supérieur Polytechnique de Madagascar**

Site web : [www.ispm-edu.com]

## Membres du groupe
**ESIIA5** | RABEANTOANDRO Mirantsoa Adrianna - création du dataset malagasy et de l'architecture du modèle adapté

**ESIIA5** | RAKOTOHARIMALALA Ny Hasina Sedera - recherche du dataset français et de l'architecture du modèle adapté

**ESIIA5** | RAKOTOMALALA Nirinifitiavana Sarobidy - recherche du dataset Malagasy et du côté backend Python

**ESIIA5** | RANDRIAMIARISOA Henintsoa Lucas - création de l'application web et déploiement du projet

**IMTICIA5** | RASOLONJATOVO Soatiana Andrianina - recherche du dataset français et de l'architecture du modèle adapté

**ESIIA5** | RAZAIARIMIHAJASOA Tsantaniony Fankasitrahana - création du dataset malagasy et du dataset français

## Stack technologique
Pour répondre aux exigences de performance et de déploiement moderne, nous avons opté pour une architecture découplée (Decoupled Architecture) :

### 1. Machine Learning
La partie intelligence artificielle est entièrement implémentée en Python, en utilisant les bibliothèques suivantes :

**Scikit-Learn** : Utilisation pour la création des pipelines de classification, les modèles SVM et Naive Bayes, ainsi que pour les outils d'évaluation (Accuracy, F1-score).

**Pandas & NumPy** : Pour la manipulation, le nettoyage et la structuration des données d'entraînement.

**Joblib / Pickle** : Pour la sérialisation et la sauvegarde des modèles entraînés afin de les rendre réutilisables en production.

### 2. Développement Backend
**Python Serverless Functions** : Déploiement sur Vercel utilisant des fonctions Python serverless (BaseHTTPRequestHandler) pour créer l'API de prédiction. Les endpoints `/api/predict` et `/api/health` traitent les requêtes HTTP en temps réel sans gestion de serveur.

**Dépendances Backend** : 
- `joblib` : Pour le chargement des modèles pré-entraînés (.pkl)
- `scikit-learn` : Bibliothèque d'apprentissage automatique utilisée lors de l'entraînement
- `pandas` & `numpy` : Utilisées lors du prétraitement des données d'entraînement

### 3. Interface Utilisateur (Frontend)
**Next.js** : Framework React utilisé pour construire une interface web fluide, réactive et optimisée pour l'utilisateur final.

### 4. Déploiement et Hébergement
**Vercel** : Plateforme choisie pour l'hébergement de l'application web et de l'API. Elle garantit une URL publique fonctionnelle accessible au moment de l'évaluation.

**GitHub** : Utilisé pour le versionnage du code source et la gestion des commits.

## Modèle prédictif et processus de traitement des données
Le projet suit deux pipelines distincts pour s'adapter aux particularités linguistiques de chaque dataset.

### 1. Pipeline Français (FR)
Le traitement pour la langue française se concentre sur la gestion des structures grammaticales complexes et du vocabulaire étendu.

**Prétraitement** : Normalisation du texte (minuscules), suppression de la ponctuation et filtrage des mots vides (Stop Words) français.

**Vectorisation** : Utilisation de TF-IDF pour transformer les messages en vecteurs numériques en valorisant les mots discriminants pour le SPAM.

**Modélisation** : Application d'un classifieur pour obtenir la prédiction et son score de confiance.

### 2. Pipeline Malgache (MG)
Le traitement pour la langue malgache a été optimisé pour gérer les spécificités du "texting" local et la structure de la langue.

**Prétraitement** : Nettoyage spécifique incluant la gestion des caractères malgaches et des abréviations courantes utilisées par les utilisateurs locaux.

**Vectorisation** : Utilisation du Bag of Words (Sac de mots) pour capturer l'occurrence des mots-clés typiques des arnaques par SMS à Madagascar.

**Modélisation** : Un modèle probabiliste léger a été privilégié pour sa robustesse face à un dataset plus restreint.

## Méthodes ML
L'évaluation a porté sur plusieurs modèles en utilisant l'Accuracy et le F1-score comme métriques de référence.

### 1. Pour la langue Française : SVM (Support Vector Machine)
**Pourquoi** : Le SVM s'est avéré le plus performant pour le français car il excelle dans la séparation des classes (SPAM vs HAM) lorsque les données sont représentées dans des espaces de haute dimension (comme avec TF-IDF).

**Résultat** : Meilleure robustesse face aux messages ambigus.

### 2. Pour la langue Malgache : Naive Bayes
**Pourquoi** : L'algorithme Multinomial Naive Bayes a été sélectionné pour le malgache. Il est particulièrement efficace pour la classification de texte basée sur les fréquences de mots, même avec un volume de données d'entraînement réduit.

**Résultat** : Grande rapidité d'exécution et prédictions fiables sur les mots-clés locaux identifiés.

## Datasets utilisés
Le projet utilise une approche multilingue basée sur deux jeux de données distincts pour assurer une détection robuste en français et en malgache.

### 1. Dataset Français (FR) 
Le jeu de données francophone a été constitué pour couvrir les spécificités des SMS modernes.

**Source** : Mélange de données issues de sources « open » (internet, Kaggle, Hugging Face) et de messages générés pour équilibrer les classes.

**Contenu** : Messages courts variés incluant des promotions, des notifications de service (SPAM) et des échanges personnels (HAM).

**Prétraitement** : Nettoyage des caractères spéciaux, suppression des "Stop Words" et normalisation du texte pour l'entraînement du modèle Python.

### 2. Dataset Malgache (MG) - Bonus 
Conformément aux objectifs bonus du hackathon, un dataset spécifique à la langue malgache a été intégré.

**Méthode de collecte** : Création et annotation par l'équipe pour capturer les expressions locales et le "texting" en malgache.

**Spécificités** : Prise en compte des variations dialectales courantes dans les SMS à Madagascar et des mots-clés typiques des arnaques locales.

**Annotation** : Chaque message a été labellisé avec rigueur par l'équipe pour garantir un score de confiance élevé lors de la prédiction.

## Hébergement de l'application web
Lien URL : [https://spam-or-ham-prediction.vercel.app/]