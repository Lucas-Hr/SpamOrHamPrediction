# Guide de test local et déploiement SpamOrHamPrediction

## 1. Test local complet

### Backend Python (Flask)

1. Placez-vous dans le dossier `api/` :
   ```bash
   cd api
   ```
2. Installez les dépendances Python (dans un venv de préférence) :
   ```bash
   uv venv .venv --python 3.11.9
   python -m ensurepip --upgrade
   python -m pip install -r requirements.txt
   ```
3. Vérifiez la présence de `model_fr.pkl` et `vectorizer_fr.pkl` dans `api/`
4. Lancez le serveur Flask :
   ```bash
   python app.py
   ```
   Le backend sera accessible sur http://localhost:8000
5. Testez l'API Python directement :
   ```bash
   curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"text": "Ceci est un message"}'
   ```

### Frontend Next.js (proxy)

1. À la racine du projet, créez un fichier `.env.local` :
   ```env
   BACKEND_URL=http://localhost:8000
   ```
2. Installez les dépendances Node.js :
   ```bash
   npm install
   ```
3. Lancez le serveur Next.js :
   ```bash
   npm run dev
   ```
4. Accédez à http://localhost:3000 et testez l'interface.

---

## 2. Déploiement Railway (backend Python)

1. Créez un projet sur https://railway.app/
2. Importez le dossier `api/` comme service Python
3. Vérifiez que le fichier `Procfile` est bien présent dans `api/` avec le contenu :
   ```
   web: python app.py
   ```
4. Railway détecte le `Procfile` et installe les dépendances de `requirements.txt`
5. Placez les fichiers `model_fr.pkl` et `vectorizer_fr.pkl` dans `api/`
6. Une fois déployé, notez l’URL publique Railway (ex: `https://votre-backend.up.railway.app`)

---

## 3. Déploiement Vercel (frontend Next.js)

1. Déployez le projet sur Vercel (repo GitHub)
2. Dans le dashboard Vercel, ajoutez la variable d’environnement :
   - `BACKEND_URL = https://votre-backend.up.railway.app`
3. Assurez-vous que le fichier `src/pages/api/predict.ts` utilise bien `process.env.BACKEND_URL` en adaptant le URL dans la ligne de code 3.
4. Le frontend Next.js utilisera `/api/predict` qui proxy vers Railway.
5. Après modification de `.env.local` ou de la variable sur Vercel, redémarrez le serveur Next.js ou redeployez.

## 5. Remarques complémentaires

- Après modification de `.env.local`, redémarrez le serveur Next.js (`npm run dev`).
- Node.js 18+ recommandé pour le support natif de `fetch` côté serveur.
- Pour la sécurité, pensez à ajouter CORS sur le backend Flask si usage public.

---

## 4. Conseils

- Ne gardez qu’un seul fichier de modèles par langue dans `api/`
- Ne mettez pas de code Python dans les API routes Next.js
- Pour d’autres langues, dupliquez le backend Flask
- En cas de problème, vérifiez les logs Railway et Vercel
