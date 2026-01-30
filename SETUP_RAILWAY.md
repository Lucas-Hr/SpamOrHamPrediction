# 🚀 SETUP RAILWAY - Guide Complet

## 📋 RÉSUMÉ RAPIDE

**Branche**: `backendSetup-2`  
**Service Backend**: Railway.app (Gratuit + Pas de cold start!)  
**Service Frontend**: Vercel (Gratuit)  
**Temps pour finir**: ~45 minutes  
**Coût**: $0/mois (1er mois)

---

## ✅ MODIFICATIONS APPORTÉES

### 1️⃣ Fichier Modifié: `api/main.py`

**CORS configuré pour Vercel + Railway:**

```python
# Configuration CORS pour autoriser Next.js (local et Vercel)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://*.vercel.app",  # Tous les domaines Vercel
        "https://yourapp.vercel.app",  # Remplacez par votre vrai domaine
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### 2️⃣ Fichier Modifié: `src/components/inputMessage.tsx`

**Route API corrigée (ligne 14):**

```typescript
// AVANT:
const res = await fetch('/backend/predict', {

// APRÈS:
const res = await fetch('/api/predict', {
```

---

### 3️⃣ Nouveaux Fichiers Créés

#### `src/app/api/predict/route.ts` (Proxy API)
```typescript
import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { text } = body;

    if (!text || typeof text !== 'string') {
      return NextResponse.json(
        { error: 'Invalid input: text is required' },
        { status: 400 }
      );
    }

    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';
    
    const response = await fetch(`${backendUrl}/predict`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text }),
    });

    if (!response.ok) {
      throw new Error(`Backend returned status ${response.status}`);
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Prediction error:', error);
    return NextResponse.json(
      { error: 'Failed to process prediction' },
      { status: 500 }
    );
  }
}
```

#### `.env.local`
```bash
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

#### `.env.example`
```bash
# DÉVELOPPEMENT
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000

# PRODUCTION (Railway)
# NEXT_PUBLIC_BACKEND_URL=https://your-backend.railway.app
```

#### `Procfile`
```
web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker api.main:app
```

---

## 🧪 TESTER LOCALEMENT (10 min)

```bash
# Terminal 1: Backend
cd api
pip install -r requirements.txt
python main.py
# → Uvicorn running on http://0.0.0.0:8000

# Terminal 2: Frontend
npm install
npm run dev
# → http://localhost:3000

# Terminal 3: Test
curl -X POST http://localhost:3000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Test message"}'
```

✅ Si ça marche, continuez!

---

## 🚀 DÉPLOIEMENT RAILWAY (6 étapes)

### Étape 1: Git Push (2 min)
```bash
git add .
git commit -m "fix: liaison frontend-backend avec Railway"
git push origin backendSetup-2
```

### Étape 2: Créer compte Railway (1 min)
- Aller sur https://railway.app
- Sign Up avec GitHub

### Étape 3: Créer Web Service (10 min)
1. Dashboard → "New Project"
2. "Deploy from GitHub repo"
3. Sélectionner `SpamOrHamPrediction` branche `backendSetup-2`
4. Railway détecte Python automatiquement
5. Attendre ~5 min pour déploiement
6. **Copier l'URL**: `https://your-backend.railway.app`

**Vérifier**: `curl https://your-backend.railway.app/docs` → Swagger UI OK ✅

### Étape 4: Configurer Vercel (5 min)
1. https://vercel.com/dashboard
2. Sélectionner projet `spam-ham-prediction`
3. Settings → Environment Variables
4. Ajouter:
   ```
   Key: NEXT_PUBLIC_BACKEND_URL
   Value: https://your-backend.railway.app
   ```
5. Save → Vercel redéploie auto

### Étape 5: Mettre à jour CORS (2 min)
1. Dans `api/main.py`, remplacer:
   ```python
   "https://yourapp.vercel.app"  # ← Par votre URL Vercel réelle
   ```
2. Git push:
   ```bash
   git add api/main.py
   git commit -m "update: CORS pour Vercel"
   git push origin backendSetup-2
   ```
3. Railway redéploie automatiquement

### Étape 6: Tester en Production (5 min)
1. Ouvrir: `https://yourapp.vercel.app`
2. Entrer un message → Cliquer "Tester"
3. ✅ Voir la prédiction!

---

## 🆘 DÉPANNAGE

### Erreur CORS
```
Access to XMLHttpRequest... has been blocked by CORS policy
```
**Solution**: 
- Vérifier domaine Vercel dans `api/main.py`
- Attendre 2 min pour redéploiement Railway

### Erreur "Failed to process prediction"
**Solution**:
- Vérifier `NEXT_PUBLIC_BACKEND_URL` dans Vercel
- Vérifier logs Railway (Dashboard → Logs)

### Erreur "Cannot reach backend"
**Solution**:
- Tester: `curl https://your-backend.railway.app/docs`
- Vérifier Railway n'affiche pas d'erreur

---

## 📊 RÉSUMÉ DES FICHIERS

| Fichier | Action | Changement |
|---------|--------|-----------|
| `api/main.py` | ✏️ Modifié | CORS configuré |
| `src/components/inputMessage.tsx` | ✏️ Modifié | Route API corrigée |
| `src/app/api/predict/route.ts` | ✨ Créé | Proxy API |
| `.env.local` | ✨ Créé | Config locale |
| `.env.example` | ✨ Créé | Documentation |
| `Procfile` | ✨ Créé | Config Railway |
| `README.md` | ✅ Conservé | Non modifié |

---

## ✅ CHECKLIST FINALE

- [ ] Tests locaux OK
- [ ] Git push réussi
- [ ] Backend déployé sur Railway
- [ ] Frontend configuré sur Vercel
- [ ] CORS mis à jour
- [ ] Tests en production OK
- [ ] ✅ C'est terminé!

---

## 💰 COÛT FINAL

```
Frontend (Vercel):  $0/mois
Backend (Railway):  $5 crédit/mois gratuit
────────────────────────────
TOTAL:              $0/mois (1er mois)
```

---

## ⚡ POURQUOI RAILWAY?

- ✅ **Pas de cold start** (contrairement à Render)
- ✅ Performances excellentes
- ✅ $5 crédit/mois gratuit
- ✅ Déploiement GitHub automatique
- ✅ Très facile à utiliser

---

*Configuration Railway - 30 Janvier 2026*  
*Branche: backendSetup-2*  
*État: ✅ PRÊT POUR PRODUCTION*
