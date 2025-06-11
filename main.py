from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import xgboost as xgb
import joblib
import numpy as np
import scipy.sparse as sp

app = FastAPI()

# Servir archivos estáticos (CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Cargar el modelo XGBoost desde .json
model = xgb.Booster()
model.load_model("xgboost_model.json")
vectorizer = joblib.load("vectorizer.pkl")


def process_codes(code1: str, code2: str):
    """
    Aplica el mismo procesamiento que usaste al entrenar:
    1. Vectoriza ambos códigos
    2. Obtiene la diferencia absoluta
    3. Lo convierte a DMatrix para XGBoost
    """
    X1 = vectorizer.transform([code1])
    X2 = vectorizer.transform([code2])
    X = sp.csr_matrix(np.abs(X1 - X2))
    dmatrix = xgb.DMatrix(X)
    return dmatrix


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "result": None}
    )


@app.post("/", response_class=HTMLResponse)
async def check_plagiarism(
    request: Request, file1: UploadFile = File(...), file2: UploadFile = File(...)
):
    code1 = (await file1.read()).decode("utf-8", errors="ignore")
    code2 = (await file2.read()).decode("utf-8", errors="ignore")
    dmatrix = process_codes(code1, code2)
    pred = model.predict(dmatrix)[0]

    # XGBoost espera DMatrix para predecir
    pred = model.predict(dmatrix)[0]
    print(pred)
    result = "Plagio" if pred > 0.5 else "No Plagio"

    return templates.TemplateResponse(
        "index.html", {"request": request, "result": result}
    )
