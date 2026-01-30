# Traitement Automatique de Langage Naturel
Institut d'enseignement : **ISPM – Institut Supérieur Polytechnique de Madagascar**

Site web : [www.ispm-edu.com]

## Membres du groupe
**ESIIA5** RABEANTOANDRO Mirantsoa Adrianna

**ESIIA5** RAKOTOHARIMALALA Ny Hasina Sedera - recherche du dataset français et de l'architecture du modèle adapté

**ESIIA5** RAKOTOMALALA Nirinifitiavana Sarobidy - recherche du dataset Malagasy

**ESIIA5** RANDRIAMIARISOA Henintsoa Lucas - création de l'application web

**IMTICIA5** RASOLONJATOVO Soatiana Andrianina - recherche du dataset français et de l'architecture du modèle adapté

**ESIIA5** RAZAIARIMIHAJASOA Tsantaniony Fankasitrahana

## Stack technologique
L'application web est créé en [Next.js] et le backend en [FastAPI].

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



This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
