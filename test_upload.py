"""
Test rapide de l'upload avec curl
"""

# Pour tester l'upload avec un nouveau fichier PDF et vérifier qu'il est public:

# curl.exe -X POST http://localhost:8000/upload `
#   -F "file=@votre_fichier.pdf" `
#   -F "user_id=5a4d980e-6909-4c46-b807-48502db44555" `
#   -F "name=MonDocumentTest" `
#   -F "status=public"

# Le lien retourné devrait être accessible publiquement dans le navigateur

# Exemple de commande PowerShell pour créer un fichier test et l'uploader:
"""
$content = @"
PDF TEST CONTENT
Ceci est un test de fichier PDF
"@

$content | Out-File -FilePath "test_pdf.txt" -Encoding utf8

curl.exe -X POST http://localhost:8000/upload `
  -F "file=@test_pdf.txt" `
  -F "user_id=5a4d980e-6909-4c46-b807-48502db44555" `
  -F "name=DocumentTestPublic" `
  -F "status=public"
"""
