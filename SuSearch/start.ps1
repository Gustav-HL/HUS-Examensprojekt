# Tillåt skriptkörning
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# 1. Starta backend i ett eget fönster
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& { cd ''; .venv\Scripts\Activate.ps1; python backend/src/susearch/__main__.py }"

# 2. Starta frontend i nuvarande fönster
npm --prefix frontend run dev
