from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
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
# ---------- E-factor API ----------
class EFactorIn(BaseModel):
    total_mass_in: float = Field(gt=0, description="Total mass of inputs (g)")
    product_mass: float = Field(gt=0, description="Mass of desired product (g)")

class EFactorOut(BaseModel):
    e_factor: float

@app.post("/api/e-factor", response_model=EFactorOut)
def calc_e_factor(payload: EFactorIn):
    if payload.total_mass_in < payload.product_mass:
        raise HTTPException(status_code=400, detail="Total mass in must be ≥ product mass.")
    e = (payload.total_mass_in - payload.product_mass) / payload.product_mass
    return {"e_factor": round(e, 4)}
# ---------- PMI (Process Mass Intensity) API ----------
class PMIIn(BaseModel):
    total_mass_in: float = Field(gt=0, description="Total mass of all inputs (g)")
    product_mass: float = Field(gt=0, description="Mass of desired product (g)")

class PMIOut(BaseModel):
    pmi: float

@app.post("/api/pmi", response_model=PMIOut)
def calc_pmi(payload: PMIIn):
    # PMI = total mass in / product mass
    if payload.total_mass_in <= 0 or payload.product_mass <= 0:
        raise HTTPException(status_code=400, detail="Both values must be > 0.")
    pmi = payload.total_mass_in / payload.product_mass
    return {"pmi": round(pmi, 4)}
# ---------- Water Impact API ----------
class WaterImpactIn(BaseModel):
    water_liters: float = Field(ge=0, description="Total water used (L)")
    product_mass_g: float = Field(gt=0, description="Mass of desired product (g)")

class WaterImpactOut(BaseModel):
    liters_per_g: float
    liters_per_kg: float

@app.post("/api/water-impact", response_model=WaterImpactOut)
def calc_water_impact(payload: WaterImpactIn):
    # L per g and L per kg product
    lpg = payload.water_liters / payload.product_mass_g
    lpk = lpg * 1000.0
    return {"liters_per_g": round(lpg, 4), "liters_per_kg": round(lpk, 2)}

# ---------- Energy Impact API ----------
class EnergyImpactIn(BaseModel):
    kwh: float = Field(ge=0, description="Total energy used (kWh)")
    product_mass_g: float = Field(gt=0, description="Mass of desired product (g)")

class EnergyImpactOut(BaseModel):
    kwh_per_g: float
    kwh_per_kg: float

@app.post("/api/energy-impact", response_model=EnergyImpactOut)
def calc_energy_impact(payload: EnergyImpactIn):
    # kWh per g and per kg product
    kwhpg = payload.kwh / payload.product_mass_g
    kwhpk = kwhpg * 1000.0
    return {"kwh_per_g": round(kwhpg, 6), "kwh_per_kg": round(kwhpk, 4)}



# ---------- Pages ----------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    context = {"request": request, "title": "Green Toolkit", "subtitle": "We are ready to build green tool"}
    return templates.TemplateResponse("index.html", context)

@app.get("/tools", response_class=HTMLResponse)
def tools_page(request: Request):
    context = {"request": request, "title": "Tools & Calculators"}
    return templates.TemplateResponse("tools.html", context)
