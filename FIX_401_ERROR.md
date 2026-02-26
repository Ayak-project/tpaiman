# ⚠️ Solution pour l'erreur 401 sur les PDFs Cloudinary

## Problème identifié :
Les fichiers "raw" (PDF, DOCX, etc.) dans Cloudinary nécessitent une authentification par défaut, ce qui cause l'erreur HTTP 401.

## Solution mise en place :
✅ **URLs signées avec longue expiration (10 ans)**

### Modifications apportées :

#### Backend :
- Changement de `type="upload"` → `type="authenticated"`
- Génération d'URLs signées avec `cloudinary.utils.cloudinary_url()`
- Expiration de 10 ans pour éviter que les liens expirent
- Les URLs contiennent une signature qui autorise l'accès

## 🧪 Comment tester :

### 1. Uploader un NOUVEAU fichier :
- Va sur http://localhost:5173
- Connecte-toi
- Onglet "Upload"
- Entre un nom (ex: "TestPDF")
- Sélectionne un PDF
- Upload

### 2. Le nouveau lien généré :
- Sera automatiquement signé
- S'ouvrira directement dans le navigateur
- Sera accessible pendant 10 ans

## 📝 Note importante :

**Les anciens fichiers** (comme `ras2.pdf`) uploadés avant cette modification auront toujours l'erreur 401 car ils n'ont pas d'URL signée.

**Solution pour les anciens fichiers :**
- Il faut re-uploader les fichiers avec le nouveau système
- Ou ajouter un endpoint pour régénérer les URLs signées (à faire si besoin)

## 🔗 Exemple d'URL signée :

```
https://res.cloudinary.com/dup3ubbol/raw/authenticated/s--signature--/v1234/fichier/document.pdf
```

La partie `s--signature--` permet l'accès authentifié au fichier.
