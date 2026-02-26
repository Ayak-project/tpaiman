# 🔧 Configuration Cloudinary pour PDF publics

## ⚠️ Le problème :
Les fichiers de type "raw" (PDF, DOCX, etc.) dans Cloudinary nécessitent une configuration spéciale dans le dashboard pour être accessibles publiquement.

## ✅ Solution : Configurer Cloudinary Dashboard

### Étape 1 : Aller dans les paramètres Cloudinary
1. Va sur : https://console.cloudinary.com/
2. Connecte-toi avec ton compte
3. Sélectionne ton cloud : **dup3ubbol**

### Étape 2 : Activer l'accès public pour les fichiers "raw"
1. Dans le menu de gauche, clique sur **"Settings"** (⚙️)
2. Va dans l'onglet **"Security"**
3. Trouve la section **"Allowed fetch domains"** ou **"Resource access control"**
4. Cherche l'option **"Restricted media types"**
5. Assure-toi que **"raw"** n'est PAS dans la liste des types restreints
6. Ou active l'option **"Allow accessing raw files via URL"**

### Étape 3 : Alternative - Utiliser "auto" au lieu de "raw"
Si la configuration ci-dessus ne fonctionne pas, on peut changer le type de ressource dans le code.

## 🔄 Solution alternative dans le code

Au lieu d'utiliser `resource_type="raw"`, on peut utiliser `resource_type="auto"` qui détecte automatiquement le type et gère mieux l'accès public.

### Modification à faire :

Dans `backend/server.py`, ligne ~210, remplace :
```python
resource_type="raw",
```

Par :
```python
resource_type="auto",
```

Et aussi dans la génération d'URL signée, ligne ~218 :
```python
resource_type="raw",
```

Par :
```python
resource_type="auto",
```

## 💡 Solution la plus simple : Upload en tant qu'image

Les PDFs peuvent être uploadés comme des images dans Cloudinary, ce qui les rend automatiquement publics.

Modifie le code pour utiliser `resource_type="image"` et `format="pdf"`.

---

# 🚀 Quelle solution essayer ?

**Option 1 (Recommandée) :** Change le code pour utiliser `resource_type="auto"`
- Plus simple
- Fonctionne immédiatement
- Pas besoin de config Cloudinary

**Option 2 :** Configure Cloudinary dashboard
- Nécessite accès admin
- Plus complexe
- Garde le type "raw"

Veux-tu que je modifie le code pour utiliser `resource_type="auto"` ?
