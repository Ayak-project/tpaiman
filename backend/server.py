from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from supabase import create_client, Client
import hashlib
import cloudinary
import cloudinary.uploader
from typing import Optional

# load environment variables from bd/.env or root .env
env_path = os.path.join(os.path.dirname(__file__), "..", "bd", ".env")
if not os.path.exists(env_path):
    env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=env_path)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_URL et SUPABASE_KEY requis dans .env")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Cloudinary configuration
CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

if not CLOUDINARY_CLOUD_NAME or not CLOUDINARY_API_KEY or not CLOUDINARY_API_SECRET:
    raise RuntimeError("Cloudinary credentials requis dans .env")

cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET
)

def hash_password(password: str) -> str:
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

app = FastAPI(title="Cloud Backend API")

# Configuration CORS pour permettre les requêtes depuis le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autoriser toutes les origines pour le déploiement
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "message": "Cloud Backend API is running"}


@app.get("/test-db")
async def test_db():
    """Test database connection"""
    try:
        result = supabase.table('users').select('id', count='exact').execute()
        return {
            "status": "success",
            "message": "Database connection successful",
            "users_count": result.count if hasattr(result, 'count') else len(result.data)
        }
    except Exception as exc:
        print(f"Database connection error: {exc}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(exc)}")


class UserCreate(BaseModel):
    email: str
    password: str
    name: str | None = None


class UserLogin(BaseModel):
    email: str
    password: str


@app.post("/signup")
async def signup(user: UserCreate):
    """Créer un nouvel utilisateur dans la table users"""
    print("signup:", user.email)
    
    try:
        # Vérifier si l'email existe déjà
        existing = supabase.table('users').select('email').eq('email', user.email).execute()
        if existing.data:
            raise HTTPException(status_code=400, detail="Email déjà utilisé")
        
        # Insérer dans la table users
        user_data = {
            "email": user.email,
            "name": user.name if user.name else user.email.split('@')[0],
            "password": hash_password(user.password)
        }
        
        result = supabase.table('users').insert(user_data).execute()
        
        if not result.data:
            raise HTTPException(status_code=500, detail="Erreur lors de la création")
        
        created_user = result.data[0]
        return {
            "success": True,
            "user": {
                "id": created_user["id"],
                "email": created_user["email"],
                "name": created_user["name"]
            },
            "message": "Utilisateur créé avec succès"
        }
        
    except HTTPException:
        raise
    except Exception as exc:
        print(f"Error during signup: {exc}")
        raise HTTPException(status_code=400, detail=str(exc))


@app.post("/login")
async def login(credentials: UserLogin):
    """Connexion utilisateur"""
    try:
        # Chercher l'utilisateur par email
        result = supabase.table('users').select('*').eq('email', credentials.email).execute()
        
        if not result.data:
            raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
        
        user = result.data[0]
        
        # Vérifier le mot de passe
        if user["password"] != hash_password(credentials.password):
            raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
        
        return {
            "success": True,
            "user": {
                "id": user["id"],
                "email": user["email"],
                "name": user["name"]
            },
            "message": "Connexion réussie"
        }
        
    except HTTPException:
        raise
    except Exception as exc:
        print(f"Error during login: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/users")
async def get_users():
    """Récupérer tous les utilisateurs"""
    try:
        result = supabase.table('users').select('id, email, name, created_at').execute()
        return {
            "success": True,
            "users": result.data,
            "count": len(result.data)
        }
    except Exception as exc:
        print(f"Error fetching users: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))


# ===== ENDPOINTS FILES =====

class FileStatusUpdate(BaseModel):
    status: str  # "private" or "public"


@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    user_id: str = Form(...),
    name: str = Form(...),
    status: str = Form("private")
):
    """Upload un fichier sur Cloudinary et sauvegarde le lien dans Supabase"""
    print(f"Upload file: {file.filename} (nom: {name}) for user {user_id}")
    
    try:
        # Vérifier que l'utilisateur existe
        user_result = supabase.table('users').select('id').eq('id', user_id).execute()
        if not user_result.data:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        
        # Vérifier le status
        if status not in ["private", "public"]:
            raise HTTPException(status_code=400, detail="Status doit être 'private' ou 'public'")
        
        # Extraire l'extension du fichier original
        import os
        original_extension = os.path.splitext(file.filename)[1].lower()  # Ex: .pdf, .docx, etc.
        
        # Upload vers Cloudinary avec un preset unsigned pour éviter les erreurs 401
        file_content = await file.read()
        
        upload_result = cloudinary.uploader.unsigned_upload(
            file_content,
            "pdf_public",  # Nom du preset unsigned créé sur Cloudinary
            folder="fichier",
            public_id=f"{name}{original_extension}",
            resource_type="raw"
        )
        
        # Récupérer l'URL publique
        file_url = upload_result.get("secure_url")
        
        # Nom complet avec extension pour l'affichage
        full_name = f"{name}{original_extension}"

        
        # Sauvegarder dans Supabase avec le nom incluant l'extension
        file_data = {
            "name": full_name,  # Nom avec extension
            "link": file_url,
            "status": status,
            "user_id": user_id
        }
        
        db_result = supabase.table('files').insert(file_data).execute()
        
        if not db_result.data:
            raise HTTPException(status_code=500, detail="Erreur lors de la sauvegarde")
        
        saved_file = db_result.data[0]
        return {
            "success": True,
            "file": {
                "id": saved_file["id"],
                "name": saved_file["name"],
                "link": saved_file["link"],
                "status": saved_file["status"],
                "user_id": saved_file["user_id"],
                "created_at": saved_file["created_at"]
            },
            "message": "Fichier uploadé avec succès"
        }
        
    except HTTPException:
        raise
    except Exception as exc:
        print(f"Error during upload: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/files/{user_id}")
async def get_user_files(user_id: str):
    """Récupérer tous les fichiers d'un utilisateur"""
    try:
        result = supabase.table('files').select('*').eq('user_id', user_id).execute()
        return {
            "success": True,
            "files": result.data,
            "count": len(result.data)
        }
    except Exception as exc:
        print(f"Error fetching files: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/files")
async def get_all_files():
    """Récupérer tous les fichiers"""
    try:
        result = supabase.table('files').select('*').execute()
        return {
            "success": True,
            "files": result.data,
            "count": len(result.data)
        }
    except Exception as exc:
        print(f"Error fetching files: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))


@app.patch("/files/{file_id}/status")
async def update_file_status(file_id: str, status_update: FileStatusUpdate):
    """Changer le status d'un fichier (private/public)"""
    try:
        if status_update.status not in ["private", "public"]:
            raise HTTPException(status_code=400, detail="Status doit être 'private' ou 'public'")
        
        result = supabase.table('files').update({
            "status": status_update.status
        }).eq('id', file_id).execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="Fichier non trouvé")
        
        updated_file = result.data[0]
        return {
            "success": True,
            "file": updated_file,
            "message": f"Status changé en {status_update.status}"
        }
        
    except HTTPException:
        raise
    except Exception as exc:
        print(f"Error updating file status: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))


@app.delete("/files/{file_id}")
async def delete_file(file_id: str):
    """Supprimer un fichier de la base de données"""
    try:
        result = supabase.table('files').delete().eq('id', file_id).execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="Fichier non trouvé")
        
        return {
            "success": True,
            "message": "Fichier supprimé avec succès"
        }
        
    except HTTPException:
        raise
    except Exception as exc:
        print(f"Error deleting file: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))


@app.patch("/files/{file_id}/regenerate-url")
async def regenerate_signed_url(file_id: str):
    """Régénérer l'URL pour un fichier existant (upload à nouveau sur Cloudinary)"""
    try:
        # Récupérer le fichier
        result = supabase.table('files').select('*').eq('id', file_id).execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="Fichier non trouvé")
        
        file_data = result.data[0]
        old_url = file_data["link"]
        file_name = file_data["name"]
        
        # Pour simplifier, on va juste retourner un message indiquant qu'il faut re-uploader
        # Car extraire et re-uploader depuis Cloudinary est complexe
        
        return {
            "success": False,
            "message": "Pour corriger l'accès au fichier, veuillez le re-uploader avec le nouveau système",
            "file_name": file_name
        }
        
    except HTTPException:
        raise
    except Exception as exc:
        print(f"Error regenerating URL: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))


if __name__ == "__main__":
    import uvicorn
    
    # Port dynamique pour Render ou port 8000 par défaut
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
