from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
import os

app = FastAPI(title="Green Toolkit")

# Serve /static if you later add custom JS/CSS/images
if os.path.isdir("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# ---------- Health ----------
@app.get("/api/health")
def health():
    return {"ok": True}

# ---------- Atom Economy API ----------
class AtomEconomyIn(BaseModel):
    mw_product: float = Field(gt=0, description="Molecular weight of desired product (g/mol)")
    mw_reactants_total: float = Field(gt=0, description="Sum of molecular weights of all reactants (g/mol)")

class AtomEconomyOut(BaseModel):
    atom_economy_pct: float

@app.post("/api/atom-economy", response_model=AtomEconomyOut)
def calc_atom_economy(payload: AtomEconomyIn):
    if payload.mw_product > payload.mw_reactants_total:
        raise HTTPException(status_code=400, detail="Product MW cannot exceed sum of reactants MW.")
    ae = (payload.mw_product / payload.mw_reactants_total) * 100.0
    return {"atom_economy_pct": round(ae, 2)}

# ---------- Homepage ----------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    context = {
        "request": request,
        "title": "Green Toolkit",
        "subtitle": "We are ready to build green tool",
    }
    return templates.TemplateResponse("index.html", context)
