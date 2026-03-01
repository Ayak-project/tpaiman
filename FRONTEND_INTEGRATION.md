# 📘 Guide d'Intégration Frontend - Cloud API

## 🌐 URL de Production

**Base URL**: `https://cloud-backend-80wx.onrender.com`

L'API est déployée sur Render et disponible 24/7. CORS est activé pour toutes les origines.

---

## 🚀 Démarrage Rapide

```javascript
const API_URL = 'https://cloud-backend-80wx.onrender.com';

// Exemple de requête simple
const response = await fetch(`${API_URL}/`);
const data = await response.json();
console.log(data); // { status: "ok", message: "Cloud Backend API is running" }
```

---

## 📚 Endpoints Disponibles

### 1. **Health Check**

**GET** `/`

Vérifier que l'API est en ligne.

**Réponse :**
```json
{
  "status": "ok",
  "message": "Cloud Backend API is running"
}
```

---

### 2. **Test Base de Données**

**GET** `/test-db`

Tester la connexion à Supabase.

**Réponse :**
```json
{
  "status": "success",
  "message": "Database connection successful",
  "users_count": 5
}
```

---

## 👤 Authentification

### 3. **Inscription Utilisateur**

**POST** `/signup`

Créer un nouveau compte utilisateur.

**Body (JSON) :**
```json
{
  "email": "user@example.com",
  "password": "motdepasse123",
  "name": "Jean Dupont"  // optionnel
}
```

**Réponse (succès) :**
```json
{
  "success": true,
  "user": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "email": "user@example.com",
    "name": "Jean Dupont"
  },
  "message": "Utilisateur créé avec succès"
}
```

**Réponse (erreur) :**
```json
{
  "detail": "Email déjà utilisé"
}
```

**Exemple JS :**
```javascript
const signup = async (email, password, name) => {
  const response = await fetch(`${API_URL}/signup`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password, name })
  });
  return await response.json();
};
```

---

### 4. **Connexion Utilisateur**

**POST** `/login`

Connecter un utilisateur existant.

**Body (JSON) :**
```json
{
  "email": "user@example.com",
  "password": "motdepasse123"
}
```

**Réponse (succès) :**
```json
{
  "success": true,
  "user": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "email": "user@example.com",
    "name": "Jean Dupont"
  },
  "message": "Connexion réussie"
}
```

**Réponse (erreur) :**
```json
{
  "detail": "Email ou mot de passe incorrect"
}
```

**Exemple JS :**
```javascript
const login = async (email, password) => {
  const response = await fetch(`${API_URL}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  return await response.json();
};
```

---

### 5. **Liste des Utilisateurs**

**GET** `/users`

Récupérer tous les utilisateurs (sans mots de passe).

**Réponse :**
```json
{
  "success": true,
  "users": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "email": "user1@example.com",
      "name": "Jean Dupont",
      "created_at": "2026-03-01T10:30:00.000Z"
    },
    {
      "id": "987e6543-e21b-12d3-a456-426614174111",
      "email": "user2@example.com",
      "name": "Marie Martin",
      "created_at": "2026-03-01T11:15:00.000Z"
    }
  ],
  "count": 2
}
```

---

## 📁 Gestion des Fichiers

### 6. **Upload de Fichier**

**POST** `/upload`

Uploader un fichier sur Cloudinary et le sauvegarder dans la base de données.

**Content-Type**: `multipart/form-data`

**Form Data :**
- `file` (File) : Le fichier à uploader
- `user_id` (string) : ID de l'utilisateur
- `name` (string) : Nom du fichier (sans extension)
- `status` (string) : `"private"` ou `"public"` (défaut: `"private"`)

**Réponse (succès) :**
```json
{
  "success": true,
  "file": {
    "id": "456e7890-e12b-34d5-a678-426614174222",
    "name": "mon-document.pdf",
    "link": "https://res.cloudinary.com/dup3ubbol/raw/upload/v1234567890/fichier/mon-document.pdf",
    "status": "private",
    "user_id": "123e4567-e89b-12d3-a456-426614174000",
    "created_at": "2026-03-01T12:00:00.000Z"
  },
  "message": "Fichier uploadé avec succès"
}
```

**Exemple JS :**
```javascript
const uploadFile = async (file, userId, fileName, status = 'private') => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('user_id', userId);
  formData.append('name', fileName);
  formData.append('status', status);

  const response = await fetch(`${API_URL}/upload`, {
    method: 'POST',
    body: formData  // Ne pas définir Content-Type, le navigateur le fait automatiquement
  });
  return await response.json();
};

// Utilisation
const fileInput = document.querySelector('input[type="file"]');
const file = fileInput.files[0];
const result = await uploadFile(file, 'user-id-123', 'rapport-mensuel', 'public');
```

---

### 7. **Récupérer les Fichiers d'un Utilisateur**

**GET** `/files/{user_id}`

Obtenir tous les fichiers d'un utilisateur spécifique.

**Réponse :**
```json
{
  "success": true,
  "files": [
    {
      "id": "456e7890-e12b-34d5-a678-426614174222",
      "name": "mon-document.pdf",
      "link": "https://res.cloudinary.com/...",
      "status": "private",
      "user_id": "123e4567-e89b-12d3-a456-426614174000",
      "created_at": "2026-03-01T12:00:00.000Z"
    }
  ],
  "count": 1
}
```

**Exemple JS :**
```javascript
const getUserFiles = async (userId) => {
  const response = await fetch(`${API_URL}/files/${userId}`);
  return await response.json();
};
```

---

### 8. **Récupérer Tous les Fichiers**

**GET** `/files`

Obtenir tous les fichiers de tous les utilisateurs.

**Réponse :** (même format que l'endpoint précédent)

---

### 9. **Modifier le Status d'un Fichier**

**PATCH** `/files/{file_id}/status`

Changer un fichier de `private` à `public` ou vice-versa.

**Body (JSON) :**
```json
{
  "status": "public"
}
```

**Réponse (succès) :**
```json
{
  "success": true,
  "file": {
    "id": "456e7890-e12b-34d5-a678-426614174222",
    "name": "mon-document.pdf",
    "status": "public",
    "link": "https://res.cloudinary.com/...",
    "user_id": "123e4567-e89b-12d3-a456-426614174000",
    "created_at": "2026-03-01T12:00:00.000Z"
  },
  "message": "Status changé en public"
}
```

**Exemple JS :**
```javascript
const updateFileStatus = async (fileId, status) => {
  const response = await fetch(`${API_URL}/files/${fileId}/status`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ status })
  });
  return await response.json();
};

// Utilisation
await updateFileStatus('file-id-456', 'public');
```

---

### 10. **Supprimer un Fichier**

**DELETE** `/files/{file_id}`

Supprimer un fichier de la base de données (le fichier reste sur Cloudinary).

**Réponse (succès) :**
```json
{
  "success": true,
  "message": "Fichier supprimé avec succès"
}
```

**Exemple JS :**
```javascript
const deleteFile = async (fileId) => {
  const response = await fetch(`${API_URL}/files/${fileId}`, {
    method: 'DELETE'
  });
  return await response.json();
};
```

---

## 🔐 Gestion des Erreurs

Toutes les erreurs HTTP retournent un objet avec un champ `detail` :

```json
{
  "detail": "Message d'erreur explicite"
}
```

**Codes HTTP courants :**
- `200` : Succès
- `400` : Requête invalide (ex: données manquantes)
- `401` : Non autorisé (mauvais identifiants)
- `404` : Ressource non trouvée
- `500` : Erreur serveur

**Exemple de gestion d'erreur :**
```javascript
try {
  const response = await fetch(`${API_URL}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  
  const data = await response.json();
  
  if (!response.ok) {
    // Erreur HTTP
    console.error('Erreur:', data.detail);
    return;
  }
  
  // Succès
  console.log('Connecté:', data.user);
  
} catch (error) {
  // Erreur réseau
  console.error('Erreur réseau:', error.message);
}
```

---

## 🎯 Workflow Recommandé

### Flux Utilisateur Typique

1. **Inscription** → `POST /signup`
2. **Connexion** → `POST /login` → Récupérer `user.id`
3. **Uploader un fichier** → `POST /upload` avec `user_id`
4. **Voir ses fichiers** → `GET /files/{user_id}`
5. **Modifier status** → `PATCH /files/{file_id}/status`
6. **Supprimer** → `DELETE /files/{file_id}`

### Exemple Complet d'Application

```javascript
// Configuration
const API_URL = 'https://cloud-backend-80wx.onrender.com';

// State management (exemple avec React)
const [user, setUser] = useState(null);
const [files, setFiles] = useState([]);

// 1. Connexion
const handleLogin = async (email, password) => {
  const res = await fetch(`${API_URL}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  const data = await res.json();
  
  if (data.success) {
    setUser(data.user);
    loadUserFiles(data.user.id);
  }
};

// 2. Charger les fichiers de l'utilisateur
const loadUserFiles = async (userId) => {
  const res = await fetch(`${API_URL}/files/${userId}`);
  const data = await res.json();
  
  if (data.success) {
    setFiles(data.files);
  }
};

// 3. Uploader un fichier
const handleUpload = async (file, fileName) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('user_id', user.id);
  formData.append('name', fileName);
  formData.append('status', 'private');

  const res = await fetch(`${API_URL}/upload`, {
    method: 'POST',
    body: formData
  });
  const data = await res.json();
  
  if (data.success) {
    loadUserFiles(user.id); // Recharger la liste
  }
};

// 4. Changer le status d'un fichier
const toggleFileStatus = async (fileId, currentStatus) => {
  const newStatus = currentStatus === 'private' ? 'public' : 'private';
  
  const res = await fetch(`${API_URL}/files/${fileId}/status`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ status: newStatus })
  });
  const data = await res.json();
  
  if (data.success) {
    loadUserFiles(user.id); // Recharger la liste
  }
};

// 5. Supprimer un fichier
const deleteFile = async (fileId) => {
  const res = await fetch(`${API_URL}/files/${fileId}`, {
    method: 'DELETE'
  });
  const data = await res.json();
  
  if (data.success) {
    loadUserFiles(user.id); // Recharger la liste
  }
};
```

---

## 🔧 Configuration Frontend

### Variables d'Environnement (Vite)

Créez un fichier `.env` dans votre projet frontend :

```env
VITE_API_URL=https://cloud-backend-80wx.onrender.com
```

Utilisation :
```javascript
const API_URL = import.meta.env.VITE_API_URL;
```

### Variables d'Environnement (Create React App)

```env
REACT_APP_API_URL=https://cloud-backend-80wx.onrender.com
```

Utilisation :
```javascript
const API_URL = process.env.REACT_APP_API_URL;
```

---

## 📌 Notes Importantes

1. **CORS** : L'API accepte les requêtes de toutes les origines. Pas besoin de configuration spéciale.

2. **Formats de fichiers** : L'upload supporte tous types de fichiers (PDF, images, documents, etc.)

3. **Taille limite** : Cloudinary gratuit limite à ~10MB par fichier.

4. **Status Private/Public** : 
   - `private` : fichier visible uniquement par le propriétaire
   - `public` : fichier visible par tous (selon votre logique frontend)

5. **UUID** : Tous les IDs (utilisateurs, fichiers) sont des UUID au format standard.

6. **Timestamps** : Les dates sont au format ISO 8601 (`2026-03-01T12:00:00.000Z`).

---

## 🐛 Debugging

### Tester l'API avec curl

```bash
# Health check
curl https://cloud-backend-80wx.onrender.com/

# Login
curl -X POST https://cloud-backend-80wx.onrender.com/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

# Upload (avec fichier)
curl -X POST https://cloud-backend-80wx.onrender.com/upload \
  -F "file=@document.pdf" \
  -F "user_id=123e4567-e89b-12d3-a456-426614174000" \
  -F "name=mon-doc" \
  -F "status=private"
```

### Tester avec Postman

Importez cette collection (endpoints à créer manuellement) ou utilisez directement les URLs ci-dessus.

---

## 📞 Support

Pour toute question ou problème :
- Consulter les logs Render : https://dashboard.render.com/web/srv-d6i1hlma2pns738qfd3g
- Vérifier le status de l'API : `GET /`
- Tester la DB : `GET /test-db`

---

## 🎉 Bon développement !

L'API est prête à l'emploi. N'hésitez pas à contacter l'équipe backend si vous rencontrez des problèmes ou avez besoin d'endpoints supplémentaires.
