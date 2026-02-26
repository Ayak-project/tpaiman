# Cloud Storage API

API de gestion de fichiers avec authentification utilisateur et stockage sur Cloudinary.

## 🚀 Déploiement

### Backend (Render)
- URL: `https://testcloud-XXXX.onrender.com` (à mettre à jour après déploiement)
- Port: 8000

### Variables d'environnement requises
```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

## 📋 Endpoints API

### Base URL
```
Production: https://testcloud-XXXX.onrender.com
Local: http://localhost:8000
```

### 1. Inscription
**POST** `/signup`

**Body (JSON):**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "password123"
}
```

**Réponse (200):**
```json
{
  "success": true,
  "message": "Utilisateur créé avec succès",
  "user": {
    "id": "uuid",
    "name": "John Doe",
    "email": "john@example.com",
    "created_at": "2026-02-26T10:00:00"
  }
}
```

---

### 2. Connexion
**POST** `/login`

**Body (JSON):**
```json
{
  "email": "john@example.com",
  "password": "password123"
}
```

**Réponse (200):**
```json
{
  "success": true,
  "message": "Connexion réussie",
  "user": {
    "id": "uuid",
    "name": "John Doe",
    "email": "john@example.com"
  }
}
```

**Erreur (401):**
```json
{
  "detail": "Email ou mot de passe incorrect"
}
```

---

### 3. Liste de tous les utilisateurs
**GET** `/users`

**Réponse (200):**
```json
{
  "success": true,
  "users": [
    {
      "id": "uuid",
      "name": "John Doe",
      "email": "john@example.com",
      "created_at": "2026-02-26T10:00:00"
    }
  ]
}
```

---

### 4. Upload de fichier
**POST** `/upload`

**Body (FormData):**
- `file`: File (PDF, DOCX, etc.)
- `name`: string (nom du fichier sans extension)
- `user_id`: string (UUID de l'utilisateur)
- `status`: string ("private" ou "public", optionnel, défaut: "private")

**Exemple avec JavaScript:**
```javascript
const formData = new FormData();
formData.append('file', pdfFile);
formData.append('name', 'mon-fichier');
formData.append('user_id', 'user-uuid');
formData.append('status', 'private');

const response = await fetch('https://API_URL/upload', {
  method: 'POST',
  body: formData
});
```

**Réponse (200):**
```json
{
  "success": true,
  "file": {
    "id": "uuid",
    "name": "mon-fichier.pdf",
    "link": "https://res.cloudinary.com/.../fichier/mon-fichier.pdf",
    "status": "private",
    "user_id": "user-uuid",
    "created_at": "2026-02-26T10:00:00"
  },
  "message": "Fichier uploadé avec succès"
}
```

---

### 5. Liste des fichiers d'un utilisateur
**GET** `/files/{user_id}`

**Paramètres:**
- `user_id`: UUID de l'utilisateur (dans l'URL)

**Réponse (200):**
```json
{
  "success": true,
  "files": [
    {
      "id": "uuid",
      "name": "mon-fichier.pdf",
      "link": "https://res.cloudinary.com/.../fichier/mon-fichier.pdf",
      "status": "private",
      "user_id": "user-uuid",
      "created_at": "2026-02-26T10:00:00"
    }
  ]
}
```

---

### 6. Liste de tous les fichiers
**GET** `/files`

**Réponse (200):**
```json
{
  "success": true,
  "files": [...]
}
```

---

### 7. Changer le statut d'un fichier
**PATCH** `/files/{file_id}/status`

**Paramètres:**
- `file_id`: UUID du fichier (dans l'URL)

**Query Parameters:**
- `status`: string ("private" ou "public")

**Exemple:**
```
PATCH /files/abc-123/status?status=public
```

**Réponse (200):**
```json
{
  "success": true,
  "file": {
    "id": "abc-123",
    "name": "mon-fichier.pdf",
    "status": "public",
    ...
  },
  "message": "Statut mis à jour"
}
```

---

### 8. Supprimer un fichier
**DELETE** `/files/{file_id}`

**Paramètres:**
- `file_id`: UUID du fichier (dans l'URL)

**Réponse (200):**
```json
{
  "success": true,
  "message": "Fichier supprimé avec succès"
}
```

---

## 🔐 Sécurité

- Les mots de passe sont hashés avec SHA256
- CORS activé pour localhost:5173 et localhost:3000
- Upload via preset unsigned Cloudinary (`pdf_public`)

## 🗄️ Base de données (Supabase)

### Table `users`
- `id` (uuid, PK)
- `name` (text)
- `email` (text, unique)
- `password` (text, hashed)
- `created_at` (timestamp)

### Table `files`
- `id` (uuid, PK)
- `name` (text)
- `link` (text)
- `status` (text: 'private' ou 'public')
- `user_id` (uuid, FK → users.id)
- `created_at` (timestamp)

## 📦 Installation locale

```bash
# Backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python backend/server.py

# Frontend
cd frontend
npm install
npm run dev
```

## 🌐 Déploiement sur Render

1. Créer un nouveau Web Service
2. Connecter le repo GitHub
3. Configuration:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn backend.server:app --host 0.0.0.0 --port $PORT`
4. Ajouter les variables d'environnement
5. Déployer

## 👨‍💻 Contact Dev Frontend

Une fois déployé sur Render, remplacez `https://API_URL` par l'URL réelle dans vos appels API frontend.
