# HUS-Examensprojekt
Examens Projekt Malmö Universitet för Hållbar Utveckling Skåne


## Navigate to the project folder
```powershell
cd SuSearch
```

## Create and start local virutual enviroment
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```
### Chromebook
```powershell
python3 -m venv .venv
source .venv/bin/activate
```

## Install backend packets
```powershell
pip install uvicorn pydantic ruff pytest

pip install pandas sentence-transformers torch scipy

pip install "psycopg[binary]" pgvector

pip install pywebview

pip install langchain-text-splitters yake
```


## Install fronend packets
```powershell
npm --prefix frontend install
```

## Start command
```powershell
.\start.ps1


npm --prefix frontend run dev


cd SuSearch/frontend/src
cd SuSearch/backend/src/susearch
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

**`pandas`** – Data analysis, CSV manipulation and DataFrame structures
**`sentence-transformers`** – Framework for computing dense vector representations and sentence embeddings
**`torch`** – Deep learning engine running the underlying transformer tensor computations
**`scipy`** – Scientific computing library used for statistical correlations and similarity metrics
**`transformers`** – Hugging Face core library for downloading, tokenizing, and running BERT and NER models
