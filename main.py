from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict, Any
from pathlib import Path
import os

# ------------------------------------------------------------------------------
# App & paths
# ------------------------------------------------------------------------------
BASE_DIR = Path(__file__).parent.resolve()

app = FastAPI(title="Green Toolkit")

# Serve /static (if present)
static_dir = BASE_DIR / "static"
if static_dir.is_dir():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Templates
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# ------------------------------------------------------------------------------
# Health
# ------------------------------------------------------------------------------
@app.get("/api/health")
def health():
    return {"ok": True}

# ------------------------------------------------------------------------------
# Atom Economy API
# ------------------------------------------------------------------------------
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

# ------------------------------------------------------------------------------
# E-factor APIs
# ------------------------------------------------------------------------------
# (1) Total-in based: E = (total_in - product) / product   [kept for compatibility]
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

# (2) Direct definition: E = waste / product
class EFactorDirectIn(BaseModel):
    waste_mass: float = Field(ge=0, description="Mass of waste (g)")
    product_mass: float = Field(gt=0, description="Mass of desired product (g)")

class EFactorDirectOut(BaseModel):
    e_factor: float

@app.post("/api/e-factor-direct", response_model=EFactorDirectOut)
def calc_e_factor_direct(payload: EFactorDirectIn):
    e = payload.waste_mass / payload.product_mass
    return {"e_factor": round(e, 4)}

# ------------------------------------------------------------------------------
# PMI (Process Mass Intensity) API
# ------------------------------------------------------------------------------
class PMIIn(BaseModel):
    total_mass_in: float = Field(gt=0, description="Total mass of all inputs (g)")
    product_mass: float = Field(gt=0, description="Mass of desired product (g)")

class PMIOut(BaseModel):
    pmi: float

@app.post("/api/pmi", response_model=PMIOut)
def calc_pmi(payload: PMIIn):
    # PMI = total mass in / product mass
    pmi = payload.total_mass_in / payload.product_mass
    return {"pmi": round(pmi, 4)}

# ------------------------------------------------------------------------------
# Water Impact API
# ------------------------------------------------------------------------------
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

# ------------------------------------------------------------------------------
# Energy Impact API
# ------------------------------------------------------------------------------
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

# ------------------------------------------------------------------------------
# Reaction Impact Report (single JSON -> all metrics)
# ------------------------------------------------------------------------------
class Product(BaseModel):
    name: Optional[str] = None
    smiles: Optional[str] = None
    mw: float = Field(gt=0, description="Molecular weight of desired product (g/mol)")
    actual_mass_g: float = Field(gt=0, description="Isolated product mass (g)")

class Reactant(BaseModel):
    name: Optional[str] = None
    smiles: Optional[str] = None
    mw: float = Field(gt=0, description="Molecular weight (g/mol)")
    mass_g: float = Field(ge=0, description="Mass charged (g)")

class Solvent(BaseModel):
    name: str
    volume_mL: float = Field(ge=0)
    density_g_per_mL: Optional[float] = Field(default=None, ge=0)
    recovery_pct: float = Field(default=0, ge=0, le=100)

class Workup(BaseModel):
    aqueous_washes_mL: float = Field(default=0, ge=0)
    organic_rinses_mL: float = Field(default=0, ge=0)
    drying_agents_g: float = Field(default=0, ge=0)

class Conditions(BaseModel):
    temp_C: Optional[float] = None
    time_h: float = Field(default=0, ge=0)
    mode: Literal["hotplate", "microwave", "reflux", "other"] = "hotplate"

class Options(BaseModel):
    count_recovered_solvent_in_pmi: bool = False  # if True, include full solvent mass in PMI numerator
    water_names: List[str] = Field(default_factory=lambda: ["water", "h2o", "deionized water"])
    energy_presets_kw: Dict[str, Dict[str, float]] = Field(default_factory=lambda: {
        "hotplate":  {"kw": 1.0, "duty": 0.35},
        "microwave": {"kw": 1.2, "duty": 0.50},
        "reflux":    {"kw": 0.8, "duty": 0.60},
        "other":     {"kw": 0.6, "duty": 0.30},
    })
    default_density_g_per_mL: float = 1.0  # used if solvent density not provided

class ReactionImpactIn(BaseModel):
    product: Product
    reactants: List[Reactant]
    solvents: List[Solvent] = Field(default_factory=list)
    workup: Workup = Workup()
    conditions: Conditions = Conditions()
    options: Options = Options()

class ReactionImpactOut(BaseModel):
    atom_economy_pct: Optional[float]
    pmi: Optional[float]
    e_factor: Optional[float]
    water_L_per_g: Optional[float]
    energy_kWh_per_g: Optional[float]
    breakdown: Dict[str, Any]
    ai_suggestions: List[str] = []  # placeholder for future AI

def compute_impact(payload: ReactionImpactIn) -> ReactionImpactOut:
    if not payload.reactants:
        raise HTTPException(status_code=400, detail="Provide at least one reactant.")
    p = payload.product
    opts = payload.options

    # Masses (g)
    reactant_mass_g = sum(r.mass_g for r in payload.reactants)

    # Solvent mass (g) with recovery
    solvent_mass_total_g = 0.0
    solvent_mass_nonrecovered_g = 0.0
    water_mL_total = float(payload.workup.aqueous_washes_mL)

    water_name_set = {n.lower() for n in opts.water_names}

    for s in payload.solvents:
        dens = s.density_g_per_mL if s.density_g_per_mL is not None else opts.default_density_g_per_mL
        mass_g = s.volume_mL * dens
        solvent_mass_total_g += mass_g
        nonrec_g = mass_g * (1.0 - s.recovery_pct/100.0)
        solvent_mass_nonrecovered_g += nonrec_g
        # Count reaction solvent water into water usage if its name matches
        if s.name.strip().lower() in water_name_set:
            water_mL_total += s.volume_mL

    auxiliaries_g = payload.workup.drying_agents_g

    product_mass_g = p.actual_mass_g
    if product_mass_g <= 0:
        raise HTTPException(status_code=400, detail="Product mass must be > 0.")

    # PMI numerator choice
    if opts.count_recovered_solvent_in_pmi:
        pmi_numerator_g = reactant_mass_g + solvent_mass_total_g + auxiliaries_g
    else:
        pmi_numerator_g = reactant_mass_g + solvent_mass_nonrecovered_g + auxiliaries_g

    # Core metrics
    pmi = pmi_numerator_g / product_mass_g
    e_factor = (pmi_numerator_g - product_mass_g) / product_mass_g

    sum_reactant_mw = sum(r.mw for r in payload.reactants)
    atom_economy = (100.0 * p.mw / sum_reactant_mw) if sum_reactant_mw > 0 else None

    # Water intensity (L/g)
    water_L_per_g = (water_mL_total / 1000.0) / product_mass_g

    # Energy intensity (kWh/g), simple estimator
    mode = payload.conditions.mode
    time_h = payload.conditions.time_h or 0.0
    preset = opts.energy_presets_kw.get(mode, opts.energy_presets_kw["other"])
    kwh = preset["kw"] * preset["duty"] * time_h
    energy_kWh_per_g = kwh / product_mass_g if product_mass_g > 0 else None

    breakdown = {
        "reactant_mass_g": round(reactant_mass_g, 4),
        "solvent_mass_total_g": round(solvent_mass_total_g, 4),
        "solvent_mass_nonrecovered_g": round(solvent_mass_nonrecovered_g, 4),
        "auxiliaries_g": round(auxiliaries_g, 4),
        "pmi_numerator_g": round(pmi_numerator_g, 4),
        "product_mass_g": round(product_mass_g, 4),
        "water_total_mL": round(water_mL_total, 2),
        "energy_kWh_total_est": round(kwh, 4),
        "energy_mode": mode,
        "options": {
            "count_recovered_solvent_in_pmi": opts.count_recovered_solvent_in_pmi
        }
    }

    return ReactionImpactOut(
        atom_economy_pct = round(atom_economy, 2) if atom_economy is not None else None,
        pmi = round(pmi, 3),
        e_factor = round(e_factor, 3),
        water_L_per_g = round(water_L_per_g, 4),
        energy_kWh_per_g = round(energy_kWh_per_g, 6) if energy_kWh_per_g is not None else None,
        breakdown = breakdown,
        ai_suggestions = []  # to be filled later by AI module
    )

@app.post("/api/impact/compute", response_model=ReactionImpactOut)
def reaction_impact(payload: ReactionImpactIn):
    try:
        return compute_impact(payload)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {e}")

# ------------------------------------------------------------------------------
# Pages
# ------------------------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    context = {"request": request, "title": "Green Toolkit", "subtitle": "We are ready to build green tool"}
    return templates.TemplateResponse("index.html", context)

@app.get("/tools", response_class=HTMLResponse)
def tools_page(request: Request):
    context = {"request": request, "title": "Tools & Calculators"}
    return templates.TemplateResponse("tools.html", context)
