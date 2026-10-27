# Tillåt skriptkörning i denna process
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# 1. Starta frontend (Vite dev-server) i ett eget bakgrundsfönster
Start-Process powershell -ArgumentList "-NoExit", "-Command", "npm --prefix frontend run dev"

# 2. Vänta 3 sekunder så att Vite hinner starta upp på port 5173
Start-Sleep -Seconds 3

# 3. Starta backend i det aktiva fönstret
# Aktivera virtuella miljön och kör modulen från backend-mappen
.venv\Scripts\Activate.ps1
$env:PYTHONPATH = "backend/src"
python -m susearch