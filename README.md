# HUS-Examensprojekt
Examens Projekt Malmö Universitet för Hållbar Utveckling Skåne


## Create and start local virutual enviroment
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

## Install backend packets
```powershell
pip install fastapi uvicorn pydantic ruff pytest
```


## Install fronend packets
```powershell
npm --prefix frontend install
```

## Start command
```powershell
.\start.ps1
```


**Frontend:** [http://localhost:5173/](http://localhost:5173/)
**Backend:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
**API-dokumentation:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)




### Backend Dependencies

**`fastapi`** – API framework
**`uvicorn`** – Server emulation to run FastAPI locally
**`pydantic`** – Data validation and parsing
**`ruff`** – Python Linter
**`pytest`** – Testing framework