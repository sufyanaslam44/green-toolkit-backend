from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict, Any
from pathlib import Path
from math import isfinite
import os
import sys
import asyncio
from pdf_generator import generate_simulation_pdf

# ------------------------------------------------------------------------------
# Fix for Windows + Python 3.13 + Playwright subprocess issue
# ------------------------------------------------------------------------------
if sys.platform == 'win32':
    # Set the event loop policy to use ProactorEventLoop on Windows
    # This is required for subprocess support which Playwright needs
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    # Check if the policy was set correctly
    policy = asyncio.get_event_loop_policy()
    if not isinstance(policy, asyncio.WindowsProactorEventLoopPolicy):
        print("=" * 80)
        print("⚠️  WARNING: Event loop policy not set correctly!")
        print("⚠️  PDF generation will FAIL with NotImplementedError")
        print("=" * 80)
        print("SOLUTION: Start server using one of these methods:")
        print("  1. python run_server.py")
        print("  2. start_server.bat")
        print("  3. .\\start_server.ps1")
        print("")
        print("❌ DO NOT USE: uvicorn main:app --reload")
        print("=" * 80)
    else:
        print(f"✅ Windows ProactorEventLoop policy set correctly")

# ------------------------------------------------------------------------------
# App & paths
# ------------------------------------------------------------------------------
BASE_DIR = Path(__file__).parent.resolve()

app = FastAPI(title="Green Toolkit")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve /static (if present)
static_dir = BASE_DIR / "static"
if static_dir.is_dir():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Templates
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# ------------------------------------------------------------------------------
# Startup event - Check Playwright/Chromium availability
# ------------------------------------------------------------------------------
@app.on_event("startup")
async def startup_event():
    """Check if Playwright and Chromium are properly installed"""
    print("=" * 60)
    print("🚀 Green Toolkit Backend Starting...")
    print(f"📁 Base directory: {BASE_DIR}")
    print(f"🐍 Python: {sys.version}")
    print(f"💻 Platform: {sys.platform}")
    
    # Check if Chromium is available (use async API)
    try:
        from playwright.async_api import async_playwright
        async with async_playwright() as p:
            browser_type = p.chromium
            # Get executable path without launching
            exec_path = browser_type.executable_path
            print(f"✅ Chromium found at: {exec_path}")
            
            # Verify the file actually exists
            import os
            if os.path.exists(exec_path):
                print(f"✅ Chromium executable verified")
            else:
                print(f"❌ Chromium executable does not exist at path!")
    except Exception as e:
        print(f"⚠️  Chromium check failed: {e}")
        print("⚠️  PDF generation may not work!")
        print("⚠️  Run: python -m playwright install chromium")
    
    print("=" * 60)

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
    kwhpg = payload.kwh / payload.product_mass_g
    kwhpk = kwhpg * 1000.0
    return {"kwh_per_g": round(kwhpg, 6), "kwh_per_kg": round(kwhpk, 4)}

# ------------------------------- RME API --------------------------------------
class RMEIn(BaseModel):
    reactant_masses_g: List[float] = Field(min_items=1, description="List of reactant masses (g)")
    product_mass_g: float = Field(gt=0, description="Isolated product mass (g)")

class RMEOut(BaseModel):
    rme_pct: float

@app.post("/api/rme", response_model=RMEOut)
def calc_rme(payload: RMEIn):
    total_reactants = sum(m for m in payload.reactant_masses_g if m is not None)
    if total_reactants <= 0:
        raise HTTPException(status_code=400, detail="Total reactant mass must be > 0.")
    rme = (payload.product_mass_g / total_reactants) * 100.0
    return {"rme_pct": round(rme, 2)}

# ------------------------ Carbon Efficiency API -------------------------------
class CarbonInSpecies(BaseModel):
    mass_g: float = Field(ge=0)
    mw: float = Field(gt=0)
    carbon_atoms: int = Field(ge=0)

class CarbonEfficiencyIn(BaseModel):
    product: CarbonInSpecies
    reactants: List[CarbonInSpecies] = Field(min_items=1)

class CarbonEfficiencyOut(BaseModel):
    carbon_efficiency_pct: float

@app.post("/api/carbon-efficiency", response_model=CarbonEfficiencyOut)
def calc_carbon_efficiency(payload: CarbonEfficiencyIn):
    nP = payload.product.mass_g / payload.product.mw
    totalC_in = sum((r.mass_g / r.mw) * r.carbon_atoms for r in payload.reactants)
    totalC_out = nP * payload.product.carbon_atoms
    if totalC_in <= 0:
        raise HTTPException(status_code=400, detail="Total carbon-in must be > 0.")
    ce = (totalC_out / totalC_in) * 100.0
    return {"carbon_efficiency_pct": round(ce, 2)}

# ------------------------ Stoichiometric Factor API ---------------------------
class SFDetail(BaseModel):
    name: Optional[str] = None
    excess_ratio: float

class SFEntry(BaseModel):
    name: Optional[str] = None
    eq_used: float = Field(ge=0)
    eq_stoich: float = Field(gt=0)

class StoichiometricFactorIn(BaseModel):
    species: List[SFEntry] = Field(min_items=1)

class StoichiometricFactorOut(BaseModel):
    sf_overall: float
    details: List[SFDetail]

@app.post("/api/stoichiometric-factor", response_model=StoichiometricFactorOut)
def calc_stoichiometric_factor(payload: StoichiometricFactorIn):
    used = sum(s.eq_used for s in payload.species)
    req  = sum(s.eq_stoich for s in payload.species)
    if req <= 0:
        raise HTTPException(status_code=400, detail="Sum of stoichiometric equivalents must be > 0.")
    overall = used / req
    details = [{"name": s.name or f"species_{i+1}", "excess_ratio": round(s.eq_used / s.eq_stoich, 4)} 
               for i, s in enumerate(payload.species)]
    return {"sf_overall": round(overall, 4), "details": details}

# ------------------------------------------------------------------------------
# Reaction Impact Report (single JSON -> all metrics)
# ------------------------------------------------------------------------------
class Product(BaseModel):
    name: Optional[str] = None
    smiles: Optional[str] = None
    mw: float = Field(gt=0, description="Molecular weight of desired product (g/mol)")
    actual_mass_g: float = Field(gt=0, description="Isolated product mass (g)")
    carbon_atoms: Optional[int] = Field(default=None, ge=0, description="Number of carbon atoms in product molecule")

class Reactant(BaseModel):
    name: Optional[str] = None
    smiles: Optional[str] = None
    mw: float = Field(gt=0, description="Molecular weight (g/mol)")
    mass_g: float = Field(ge=0, description="Mass charged (g)")
    carbon_atoms: Optional[int] = Field(default=None, ge=0, description="Number of carbon atoms per molecule")
    eq_used: Optional[float]   = Field(default=None, ge=0, description="Equivalents actually used vs limiting reagent = 1")
    eq_stoich: Optional[float] = Field(default=None, gt=0, description="Stoichiometric equivalents required by balanced equation")

class Solvent(BaseModel):
    name: str
    mass_g: float = Field(ge=0, description="Mass of solvent (g)")
    recovery_pct: float = Field(default=0, ge=0, le=100)

class Catalyst(BaseModel):
    name: Optional[str] = None
    mw: float = Field(gt=0, description="Molecular weight (g/mol)")
    mass_g: float = Field(ge=0, description="Mass of catalyst (g)")

class Workup(BaseModel):
    aqueous_washes_g: float = Field(default=0, ge=0)
    organic_rinses_g: float = Field(default=0, ge=0)
    drying_agents_g: float = Field(default=0, ge=0)

class Conditions(BaseModel):
    temp_C: Optional[float] = None
    time_h: float = Field(default=0, ge=0)
    mode: Literal["hotplate", "microwave", "reflux", "other"] = "hotplate"

class Options(BaseModel):
    count_recovered_solvent_in_pmi: bool = False
    water_names: List[str] = Field(default_factory=lambda: ["water", "h2o", "deionized water"])
    energy_presets_kw: Dict[str, Dict[str, float]] = Field(default_factory=lambda: {
        "hotplate":  {"kw": 1.0, "duty": 0.35},
        "microwave": {"kw": 1.2, "duty": 0.50},
        "reflux":    {"kw": 0.8, "duty": 0.60},
        "other":     {"kw": 0.6, "duty": 0.30},
    })
    default_density_g_per_mL: float = 1.0

class ReactionImpactIn(BaseModel):
    product: Product
    reactants: List[Reactant]
    solvents: List[Solvent] = Field(default_factory=list)
    catalysts: List[Catalyst] = Field(default_factory=list)
    workup: Workup = Workup()
    conditions: Conditions = Conditions()
    options: Options = Options()

class ReactionImpactOut(BaseModel):
    atom_economy_pct: Optional[float]
    pmi: Optional[float]
    e_factor: Optional[float]
    water_mL_per_g: Optional[float]
    energy_kWh_per_g: Optional[float]
    rme_pct: Optional[float] = None
    carbon_efficiency_pct: Optional[float] = None
    sf_overall: Optional[float] = None
    sf_details: Optional[List[SFDetail]] = None
    breakdown: Dict[str, Any]
    ai_suggestions: List[str] = []

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
    
    # Track water separately for water intensity metric (includes aqueous washes + water solvents)
    water_g_total = float(payload.workup.aqueous_washes_g)
    water_name_set = {n.lower() for n in opts.water_names}

    for s in payload.solvents:
        mass_g = s.mass_g
        solvent_mass_total_g += mass_g
        nonrec_g = mass_g * (1.0 - s.recovery_pct/100.0)
        solvent_mass_nonrecovered_g += nonrec_g
        # Count reaction solvent water into water usage for water intensity metric only
        if s.name.strip().lower() in water_name_set:
            water_g_total += s.mass_g

    auxiliaries_g = payload.workup.drying_agents_g

    # Catalyst mass
    catalyst_mass_g = sum(c.mass_g for c in payload.catalysts)

    product_mass_g = p.actual_mass_g
    if product_mass_g <= 0:
        raise HTTPException(status_code=400, detail="Product mass must be > 0.")

    # PMI (Process Mass Intensity) = Total Mass of All Input Materials / Mass of Final Product
    # Total Input = Reactants + Catalysts + ALL Solvents + Aqueous washes + auxiliaries (drying agents)
    # PMI counts ALL materials that enter the process, regardless of recovery
    total_input_mass_g = reactant_mass_g + catalyst_mass_g + solvent_mass_total_g + payload.workup.aqueous_washes_g + auxiliaries_g

    pmi = total_input_mass_g / product_mass_g if product_mass_g > 0 else 0
    
    # E-factor = (Total mass in - Product mass out) / Product mass out
    # Standard E-factor uses ALL inputs, same as PMI
    # E-factor represents waste generation: higher E-factor = more waste per unit product
    e_factor = (total_input_mass_g - product_mass_g) / product_mass_g

    sum_reactant_mw = sum(r.mw for r in payload.reactants)
    atom_economy = (100.0 * p.mw / sum_reactant_mw) if sum_reactant_mw > 0 else None

    # Water intensity (mL/g) - water_g_total in grams = mL (since water density = 1 g/mL)
    water_mL_per_g = (water_g_total / product_mass_g) if product_mass_g > 0 else 0

    mode = payload.conditions.mode
    time_h = payload.conditions.time_h or 0.0
    preset = opts.energy_presets_kw.get(mode, opts.energy_presets_kw["other"])
    kwh = preset["kw"] * preset["duty"] * time_h
    energy_kWh_per_g = kwh / product_mass_g if product_mass_g > 0 else None

    breakdown = {
        "reactant_mass_g": round(reactant_mass_g, 4),
        "catalyst_mass_g": round(catalyst_mass_g, 4),
        "solvent_mass_total_g": round(solvent_mass_total_g, 4),
        "solvent_mass_nonrecovered_g": round(solvent_mass_nonrecovered_g, 4),
        "auxiliaries_g": round(auxiliaries_g, 4),
        "aqueous_washes_g": round(payload.workup.aqueous_washes_g, 2),
        "total_input_mass_g": round(total_input_mass_g, 4),
        "product_mass_g": round(product_mass_g, 4),
        "water_total_g": round(water_g_total, 2),
        "energy_kWh_total_est": round(kwh, 4),
        "energy_mode": mode,
        "options": {
            "count_recovered_solvent_in_pmi": opts.count_recovered_solvent_in_pmi
        }
    }

    rme_pct = None
    reactant_mass_g = sum(r.mass_g for r in payload.reactants)
    if product_mass_g > 0 and reactant_mass_g > 0:
        rme_pct = round((product_mass_g / reactant_mass_g) * 100.0, 2)

    carbon_efficiency_pct = None
    try:
        if payload.product.carbon_atoms is not None and all(
            r.carbon_atoms is not None for r in payload.reactants
        ):
            nP = payload.product.actual_mass_g / payload.product.mw
            totalC_in = 0.0
            for r in payload.reactants:
                nR = r.mass_g / r.mw
                totalC_in += nR * r.carbon_atoms
            totalC_out = nP * payload.product.carbon_atoms
            if totalC_in > 0:
                carbon_efficiency_pct = round((totalC_out / totalC_in) * 100.0, 2)
    except Exception:
        pass

    sf_overall = None
    sf_details = None
    try:
        pairs = [(r.name or f"reactant_{i+1}", r.eq_used, r.eq_stoich) for i, r in enumerate(payload.reactants)]
        pairs = [(n, eu, es) for (n, eu, es) in pairs if (eu is not None and es is not None and es > 0)]
        if pairs:
            per = [{"name": n, "excess_ratio": round(eu / es, 4)} for (n, eu, es) in pairs if isfinite(eu / es)]
            sum_used = sum(eu for (_, eu, es) in pairs)
            sum_req  = sum(es for (_, eu, es) in pairs)
            if sum_req > 0:
                sf_overall = round(sum_used / sum_req, 4)
                sf_details = per
    except Exception:
        pass

    return ReactionImpactOut(
        atom_economy_pct = round(atom_economy, 2) if atom_economy is not None else None,
        pmi = round(pmi, 3),
        e_factor = round(e_factor, 3),
        water_mL_per_g = round(water_mL_per_g, 2),
        energy_kWh_per_g = round(energy_kWh_per_g, 6) if energy_kWh_per_g is not None else None,
        rme_pct = rme_pct,
        carbon_efficiency_pct = carbon_efficiency_pct,
        sf_overall = sf_overall,
        sf_details = sf_details,
        breakdown = breakdown,
        ai_suggestions = []
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
# PDF Generation API
# ------------------------------------------------------------------------------
class PDFGenerationIn(BaseModel):
    """Request body for PDF generation - includes all simulation data"""
    reaction_name: Optional[str] = "Green Chemistry Simulation"
    product: Product
    reactants: List[Reactant]
    solvents: List[Solvent] = Field(default_factory=list)
    catalysts: List[Catalyst] = Field(default_factory=list)
    workup: Workup = Workup()
    conditions: Conditions = Conditions()
    # Include computed metrics
    atom_economy_pct: Optional[float] = None
    pmi: Optional[float] = None
    e_factor: Optional[float] = None
    water_mL_per_g: Optional[float] = None
    energy_kWh_per_g: Optional[float] = None
    rme_pct: Optional[float] = None
    carbon_efficiency_pct: Optional[float] = None
    sf_overall: Optional[float] = None
    sf_details: Optional[List[SFDetail]] = None
    breakdown: Optional[Dict[str, Any]] = None
    ai_suggestions: List[str] = Field(default_factory=list)

@app.post("/api/generate-pdf")
async def generate_pdf_report(payload: PDFGenerationIn):
    """Generate a PDF report from simulation data"""
    try:
        # Convert payload to dict for PDF generator
        data_dict = payload.model_dump()
        
        print(f"[API] PDF request for: {data_dict.get('reaction_name', 'unnamed')}")
        
        # Add timeout to prevent hanging
        import asyncio
        try:
            # 60 second timeout for PDF generation
            pdf_path = await asyncio.wait_for(
                generate_simulation_pdf(data_dict),
                timeout=60.0
            )
        except asyncio.TimeoutError:
            raise HTTPException(
                status_code=504,
                detail="PDF generation timed out (>60s). Service may be under heavy load."
            )
        
        # Return the PDF file
        return FileResponse(
            path=pdf_path,
            media_type='application/pdf',
            filename=Path(pdf_path).name,
            headers={
                "Content-Disposition": f'attachment; filename="{Path(pdf_path).name}"'
            }
        )
    except HTTPException:
        raise  # Re-raise HTTP exceptions as-is
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"[API] ❌ PDF generation error:\n{error_trace}")
        
        # Return detailed error for debugging
        raise HTTPException(
            status_code=500,
            detail={
                "error": "PDF generation failed",
                "message": str(e),
                "type": type(e).__name__
            }
        )

# ------------------------------------------------------------------------------
# Pages (Jinja templates)
# ------------------------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    context = {"request": request, "title": "Green Toolkit", "subtitle": "We are ready to build green tool"}
    return templates.TemplateResponse("index.html", context)

@app.get("/gamification", response_class=HTMLResponse)
def gamification_page(request: Request):
    context = {"request": request, "title": "Gamification"}
    return templates.TemplateResponse("gamification.html", context)

@app.get("/tools", response_class=HTMLResponse)
def tools_page(request: Request):
    context = {"request": request, "title": "Tools & Calculators"}
    return templates.TemplateResponse("tools.html", context)

@app.get("/simulate", response_class=HTMLResponse)
def simulate_page(request: Request):
    context = {"request": request, "title": "Simulations"}
    return templates.TemplateResponse("sim.html", context)

# ------------------------------------------------------------------------------
# One-App Mode: serve the built Vite frontend (SPA) at /app
# ------------------------------------------------------------------------------
def _pick_frontend_dist() -> Optional[Path]:
    """Try to find a Vite 'dist' folder. Override with env FRONTEND_DIST."""
    env_path = os.getenv("FRONTEND_DIST")
    if env_path:
        p = Path(env_path)
        if p.is_dir():
            return p

    # Common locations (adjust if your layout differs)
    candidates = [
        BASE_DIR / "dist",
        BASE_DIR / "frontend" / "dist",
        BASE_DIR / "vite_project_1" / "dist",
        BASE_DIR.parent / "frontend" / "dist",
        BASE_DIR.parent / "vite_project_1" / "dist",
    ]
    for c in candidates:
        if c.is_dir():
            return c
    return None

_frontend_dist = _pick_frontend_dist()
if _frontend_dist:
    app.mount("/app", StaticFiles(directory=str(_frontend_dist), html=True), name="app")
else:
    # Not fatal—just print a hint. Build your Vite app to create dist/.
    print(
        "[One-App Mode] Vite 'dist' not found. Set FRONTEND_DIST env var or build your frontend "
        "(e.g. cd vite_project_1 && pnpm build)."
    )
