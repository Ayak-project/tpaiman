# 📤 Guide Complet : Upload de Fichiers

## 🎯 Endpoint d'Upload

**POST** `https://cloud-backend-80wx.onrender.com/upload`

---

## 📋 Prérequis

1. L'utilisateur doit être connecté et vous devez avoir son `user_id`
2. Le fichier doit être sélectionné via un `<input type="file">`
3. La requête doit utiliser `FormData` (pas JSON !)

---

## ✅ Implémentation Correcte

### 1. HTML - Input File

```html
<form onSubmit={handleUpload}>
  <input 
    type="file" 
    onChange={(e) => setSelectedFile(e.target.files[0])}
    required 
  />
  
  <input 
    type="text" 
    placeholder="Nom du fichier (sans extension)"
    value={fileName}
    onChange={(e) => setFileName(e.target.value)}
    required 
  />
  
  <select value={status} onChange={(e) => setStatus(e.target.value)}>
    <option value="private">Privé</option>
    <option value="public">Public</option>
  </select>
  
  <button type="submit">Uploader</button>
</form>
```

---

### 2. JavaScript/React - Fonction d'Upload

```javascript
const API_URL = 'https://cloud-backend-80wx.onrender.com';

const handleUpload = async (e) => {
  e.preventDefault();
  
  // 1. Vérifications
  if (!selectedFile) {
    alert('Veuillez sélectionner un fichier');
    return;
  }
  
  if (!fileName) {
    alert('Veuillez donner un nom au fichier');
    return;
  }
  
  if (!user || !user.id) {
    alert('Vous devez être connecté');
    return;
  }
  
  // 2. Créer FormData
  const formData = new FormData();
  formData.append('file', selectedFile);           // Le fichier lui-même
  formData.append('user_id', user.id);             // ID de l'utilisateur connecté
  formData.append('name', fileName);               // Nom sans extension
  formData.append('status', status);               // "private" ou "public"
  
  try {
    // 3. Envoyer la requête
    const response = await fetch(`${API_URL}/upload`, {
      method: 'POST',
      body: formData
      // ⚠️ NE PAS mettre de headers Content-Type !
      // Le navigateur le fait automatiquement avec FormData
    });
    
    // 4. Traiter la réponse
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.detail || 'Erreur lors de l\'upload');
    }
    
    console.log('✅ Fichier uploadé:', data.file);
    alert(`Fichier "${data.file.name}" uploadé avec succès !`);
    
    // 5. Réinitialiser le formulaire
    setSelectedFile(null);
    setFileName('');
    e.target.reset(); // Reset le input file
    
    // 6. Recharger la liste des fichiers
    loadUserFiles();
    
  } catch (error) {
    console.error('❌ Erreur upload:', error);
    alert('Erreur: ' + error.message);
  }
};
```

---

### 3. Exemple Complet avec State Management

```javascript
import { useState } from 'react';

function UploadSection({ user }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileName, setFileName] = useState('');
  const [status, setStatus] = useState('private');
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');

  const API_URL = 'https://cloud-backend-80wx.onrender.com';

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
      // Suggérer un nom basé sur le fichier (sans extension)
      const nameWithoutExt = file.name.split('.').slice(0, -1).join('.');
      setFileName(nameWithoutExt);
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    
    if (!selectedFile || !fileName) {
      setMessage('❌ Veuillez remplir tous les champs');
      return;
    }

    setUploading(true);
    setMessage('📤 Upload en cours...');

    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('user_id', user.id);
    formData.append('name', fileName);
    formData.append('status', status);

    try {
      const response = await fetch(`${API_URL}/upload`, {
        method: 'POST',
        body: formData
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Erreur');
      }

      setMessage(`✅ ${data.message}`);
      setSelectedFile(null);
      setFileName('');
      e.target.reset();

    } catch (error) {
      setMessage(`❌ ${error.message}`);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div>
      <h2>Uploader un fichier</h2>
      
      <form onSubmit={handleUpload}>
        <div>
          <label>Fichier :</label>
          <input 
            type="file" 
            onChange={handleFileChange}
            disabled={uploading}
            required 
          />
          {selectedFile && (
            <p>Fichier sélectionné : {selectedFile.name} ({(selectedFile.size / 1024).toFixed(2)} KB)</p>
          )}
        </div>

        <div>
          <label>Nom du fichier (sans extension) :</label>
          <input 
            type="text"
            value={fileName}
            onChange={(e) => setFileName(e.target.value)}
            placeholder="mon-document"
            disabled={uploading}
            required 
          />
        </div>

        <div>
          <label>Visibilité :</label>
          <select value={status} onChange={(e) => setStatus(e.target.value)} disabled={uploading}>
            <option value="private">Privé</option>
            <option value="public">Public</option>
          </select>
        </div>

        <button type="submit" disabled={uploading || !selectedFile || !fileName}>
          {uploading ? 'Upload en cours...' : 'Uploader'}
        </button>
      </form>

      {message && <p>{message}</p>}
    </div>
  );
}

export default UploadSection;
```

---

## 🔍 Détails Importants

### FormData - Les 4 Champs Requis

| Champ | Type | Description | Exemple |
|-------|------|-------------|---------|
| `file` | File | Le fichier à uploader | `document.pdf` |
| `user_id` | string | UUID de l'utilisateur connecté | `"123e4567-e89b-12d3-a456-426614174000"` |
| `name` | string | Nom du fichier **SANS extension** | `"rapport-mensuel"` |
| `status` | string | `"private"` ou `"public"` | `"private"` |

---

## ❌ Erreurs Courantes

### 1. ❌ Envoyer du JSON au lieu de FormData

**MAUVAIS** :
```javascript
// ❌ NE MARCHE PAS
const response = await fetch(`${API_URL}/upload`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ file: selectedFile, user_id: user.id })
});
```

**BON** :
```javascript
// ✅ MARCHE
const formData = new FormData();
formData.append('file', selectedFile);
formData.append('user_id', user.id);
formData.append('name', fileName);
formData.append('status', status);

const response = await fetch(`${API_URL}/upload`, {
  method: 'POST',
  body: formData  // Pas de headers !
});
```

---

### 2. ❌ Ajouter manuellement le Content-Type

**MAUVAIS** :
```javascript
// ❌ NE MARCHE PAS
const response = await fetch(`${API_URL}/upload`, {
  method: 'POST',
  headers: {
    'Content-Type': 'multipart/form-data'  // ❌ PAS COMME ÇA
  },
  body: formData
});
```

**BON** :
```javascript
// ✅ MARCHE - Le navigateur ajoute le header automatiquement
const response = await fetch(`${API_URL}/upload`, {
  method: 'POST',
  body: formData
  // Pas de headers du tout !
});
```

> **Pourquoi ?** Le navigateur ajoute automatiquement `Content-Type: multipart/form-data; boundary=...` avec le bon `boundary`. Si vous le mettez manuellement, le boundary ne sera pas correct.

---

### 3. ❌ Oublier le `user_id`

Le backend a **besoin** de l'ID utilisateur pour savoir à qui appartient le fichier.

```javascript
// ✅ Après le login, sauvegarder l'utilisateur
const loginResponse = await fetch(`${API_URL}/login`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email, password })
});
const loginData = await loginResponse.json();

if (loginData.success) {
  setUser(loginData.user);  // ⭐ Sauvegarder l'utilisateur
  // loginData.user.id contient l'UUID
}

// Puis lors de l'upload
formData.append('user_id', user.id);  // ✅
```

---

### 4. ❌ Mettre l'extension dans le champ `name`

**MAUVAIS** :
```javascript
formData.append('name', 'rapport.pdf');  // ❌ Avec extension
```

**BON** :
```javascript
formData.append('name', 'rapport');  // ✅ Sans extension
```

> L'extension est automatiquement récupérée du fichier original et ajoutée par le backend.

---

### 5. ❌ Ne pas vérifier `response.ok`

**MAUVAIS** :
```javascript
const response = await fetch(`${API_URL}/upload`, {
  method: 'POST',
  body: formData
});
const data = await response.json();
// ❌ Pas de vérification d'erreur
console.log(data);
```

**BON** :
```javascript
const response = await fetch(`${API_URL}/upload`, {
  method: 'POST',
  body: formData
});
const data = await response.json();

if (!response.ok) {  // ✅ Vérifier les erreurs
  throw new Error(data.detail || 'Erreur upload');
}

console.log('Succès:', data);
```

---

## 🧪 Tester Votre Upload

### Test 1 : Vérifier FormData avant l'envoi

```javascript
// Afficher le contenu de FormData dans la console
const formData = new FormData();
formData.append('file', selectedFile);
formData.append('user_id', user.id);
formData.append('name', fileName);
formData.append('status', status);

// Debug
for (let [key, value] of formData.entries()) {
  console.log(key, ':', value);
}
// Devrait afficher :
// file : File { name: "document.pdf", size: 12345, ... }
// user_id : "123e4567-e89b-12d3-a456-426614174000"
// name : "rapport-mensuel"
// status : "private"
```

---

### Test 2 : Vérifier que le fichier est bien sélectionné

```javascript
const handleFileChange = (e) => {
  const file = e.target.files[0];
  console.log('Fichier sélectionné:', file);
  // Doit afficher : File { name: "...", size: ..., type: "..." }
  
  if (!file) {
    alert('Aucun fichier sélectionné');
    return;
  }
  
  setSelectedFile(file);
};
```

---

### Test 3 : Vérifier la réponse du serveur

```javascript
try {
  const response = await fetch(`${API_URL}/upload`, {
    method: 'POST',
    body: formData
  });
  
  console.log('Status HTTP:', response.status);
  // ✅ 200 = succès
  // ❌ 400 = requête invalide
  // ❌ 404 = utilisateur non trouvé
  // ❌ 500 = erreur serveur
  
  const data = await response.json();
  console.log('Réponse:', data);
  
} catch (error) {
  console.error('Erreur réseau:', error);
}
```

---

## 📊 Réponse Attendue (Succès)

```json
{
  "success": true,
  "file": {
    "id": "789e0123-e45b-67d8-a901-426614174333",
    "name": "rapport-mensuel.pdf",
    "link": "https://res.cloudinary.com/dup3ubbol/raw/upload/v1234567890/fichier/rapport-mensuel.pdf",
    "status": "private",
    "user_id": "123e4567-e89b-12d3-a456-426614174000",
    "created_at": "2026-03-01T14:30:00.000Z"
  },
  "message": "Fichier uploadé avec succès"
}
```

Vous pouvez ensuite :
- Afficher le lien : `data.file.link`
- Télécharger : `<a href={data.file.link} download>Télécharger</a>`
- Afficher dans une iframe (PDF) : `<iframe src={data.file.link} />`

---

## 🔴 Erreurs Possibles

### Erreur 400 : `Status doit être 'private' ou 'public'`

**Cause** : Le champ `status` contient autre chose que `"private"` ou `"public"`

**Solution** :
```javascript
formData.append('status', 'private');  // ou 'public'
```

---

### Erreur 404 : `Utilisateur non trouvé`

**Cause** : Le `user_id` n'existe pas dans la base de données

**Solution** : Vérifier que l'utilisateur est bien connecté et que `user.id` est un UUID valide
```javascript
console.log('User ID:', user.id);  // Doit être un UUID
```

---

### Erreur 500 : `Erreur lors de l'upload` ou erreur Cloudinary

**Causes possibles** :
1. Problème de connexion à Cloudinary
2. Fichier trop volumineux (limite ~10MB sur Cloudinary gratuit)
3. Format de fichier non supporté

**Solutions** :
- Vérifier la taille du fichier avant l'upload :
```javascript
if (selectedFile.size > 10 * 1024 * 1024) {  // 10 MB
  alert('Fichier trop volumineux (max 10 MB)');
  return;
}
```

---

### Erreur réseau : `Failed to fetch`

**Cause** : Le backend n'est pas accessible

**Solutions** :
1. Vérifier que l'URL est correcte : `https://cloud-backend-80wx.onrender.com`
2. Vérifier que le backend est en ligne : visiter `https://cloud-backend-80wx.onrender.com/` dans le navigateur
3. Vérifier la connexion internet

---

## 🎯 Checklist Finale

Avant de tester, vérifier :

- [ ] L'utilisateur est connecté (`user.id` existe)
- [ ] Un fichier est sélectionné (`selectedFile` n'est pas null)
- [ ] Un nom est fourni (`fileName` n'est pas vide)
- [ ] Le status est `"private"` ou `"public"`
- [ ] Utilisation de `FormData` (pas JSON)
- [ ] Pas de header `Content-Type` manuel
- [ ] Les 4 champs sont ajoutés à FormData : `file`, `user_id`, `name`, `status`
- [ ] Gestion des erreurs avec `try/catch` et vérification `response.ok`

---

## 🆘 Toujours des problèmes ?

### Debug étape par étape

```javascript
const handleUpload = async (e) => {
  e.preventDefault();
  
  console.log('=== DEBUT UPLOAD ===');
  console.log('1. Fichier:', selectedFile);
  console.log('2. Nom:', fileName);
  console.log('3. User ID:', user?.id);
  console.log('4. Status:', status);
  
  if (!selectedFile) {
    console.error('❌ Pas de fichier');
    return;
  }
  
  if (!user?.id) {
    console.error('❌ Pas d\'utilisateur connecté');
    return;
  }
  
  const formData = new FormData();
  formData.append('file', selectedFile);
  formData.append('user_id', user.id);
  formData.append('name', fileName);
  formData.append('status', status);
  
  console.log('5. FormData créé');
  for (let [key, value] of formData.entries()) {
    console.log(`   ${key}:`, value);
  }
  
  try {
    console.log('6. Envoi requête...');
    const response = await fetch('https://cloud-backend-80wx.onrender.com/upload', {
      method: 'POST',
      body: formData
    });
    
    console.log('7. Réponse reçue, status:', response.status);
    
    const data = await response.json();
    console.log('8. Data:', data);
    
    if (!response.ok) {
      console.error('❌ Erreur HTTP:', data.detail);
      alert('Erreur: ' + data.detail);
      return;
    }
    
    console.log('✅ Upload réussi!');
    alert('Fichier uploadé: ' + data.file.name);
    
  } catch (error) {
    console.error('❌ Erreur:', error);
    alert('Erreur: ' + error.message);
  }
  
  console.log('=== FIN UPLOAD ===');
};
```

Avec ces logs, vous pourrez identifier exactement où ça bloque.

---

## 📞 Support

Si après avoir suivi ce guide vous rencontrez toujours des problèmes :

1. Copiez **tous** les logs de la console
2. Notez le message d'erreur exact
3. Vérifiez l'onglet Network dans les DevTools (F12) pour voir la requête HTTP
4. Contactez l'équipe backend avec ces informations

---

## ✅ Exemple Minimal Fonctionnel

```html
<!DOCTYPE html>
<html>
<head>
  <title>Test Upload</title>
</head>
<body>
  <form id="uploadForm">
    <input type="file" id="fileInput" required>
    <input type="text" id="nameInput" placeholder="Nom fichier" required>
    <button type="submit">Upload</button>
  </form>
  
  <div id="result"></div>

  <script>
    // À remplacer par un vrai user_id après login
    const USER_ID = '123e4567-e89b-12d3-a456-426614174000';
    const API_URL = 'https://cloud-backend-80wx.onrender.com';

    document.getElementById('uploadForm').addEventListener('submit', async (e) => {
      e.preventDefault();
      
      const file = document.getElementById('fileInput').files[0];
      const name = document.getElementById('nameInput').value;
      
      const formData = new FormData();
      formData.append('file', file);
      formData.append('user_id', USER_ID);
      formData.append('name', name);
      formData.append('status', 'private');
      
      try {
        const response = await fetch(`${API_URL}/upload`, {
          method: 'POST',
          body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
          document.getElementById('result').innerHTML = 
            `✅ Fichier uploadé: <a href="${data.file.link}" target="_blank">${data.file.name}</a>`;
        } else {
          document.getElementById('result').innerHTML = 
            `❌ Erreur: ${data.detail}`;
        }
      } catch (error) {
        document.getElementById('result').innerHTML = 
          `❌ Erreur réseau: ${error.message}`;
      }
    });
  </script>
</body>
</html>
```

Testez ce fichier HTML pour vérifier que l'upload fonctionne !

---

🎉 **Bon upload !**
