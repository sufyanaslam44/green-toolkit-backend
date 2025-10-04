"""PDF Report Generator for Green Chemistry Simulations.

Enhanced for reliability on Render.com (free tier) & Windows.
Adds diagnostic logging, temp-directory output, safer Chromium flags, and
environment variable toggles:

  PDF_DEBUG=1      -> verbose debug logs
  DISABLE_PDF=1    -> force-disable generation (useful for health checks)
  PDF_TMP_DIR=/tmp -> override temp output directory
"""
from playwright.async_api import async_playwright
from pathlib import Path
from datetime import datetime
import json
import os
import tempfile
from typing import Dict, Any

PDF_DEBUG = os.getenv("PDF_DEBUG", "0") == "1"
PDF_DISABLE = os.getenv("DISABLE_PDF", "0") == "1"
PDF_TMP_DIR = os.getenv("PDF_TMP_DIR")

CHROMIUM_FLAGS = [
    "--no-sandbox",
    "--disable-setuid-sandbox",
    "--disable-dev-shm-usage",
    "--disable-gpu",
    # Avoid timers being throttled in background which can occasionally hang set_content
    "--disable-background-timer-throttling",
    "--disable-renderer-backgrounding",
]

async def _attempt_install_chromium():
    """Attempt a one-time on-demand Chromium install if not present.
    This is a best-effort fallback for environments where the build step
    failed or was skipped. On restricted platforms (like Render free tier),
    this may still fail, but we provide clearer logging.
    """
    import subprocess, sys
    try:
        print('[PDF] Attempting on-demand Chromium install...')
        subprocess.run([sys.executable, '-m', 'playwright', 'install', 'chromium', '--with-deps'],
                       check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
        print('[PDF] On-demand Chromium install completed.')
    except Exception as e:
        print(f'[PDF] On-demand install failed: {e}')


def _dbg(msg: str):
    if PDF_DEBUG:
        print(f"[PDF][DEBUG] {msg}")


def _safe_name(text: str) -> str:
    s = "".join(c for c in text if c.isalnum() or c in (" ", "-", "_")).strip()
    return (s or "simulation").replace(" ", "_")


def _resolve_output(simulation_data: Dict[str, Any], output_path: str | None) -> Path:
    if output_path:
        return Path(output_path).resolve()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    rxn = simulation_data.get("reaction_name", "simulation") if isinstance(simulation_data, dict) else "simulation"
    base_dir = Path(PDF_TMP_DIR or tempfile.gettempdir())
    base_dir.mkdir(parents=True, exist_ok=True)
    return base_dir / f"green_chem_report_{_safe_name(str(rxn))}_{ts}.pdf"


async def generate_simulation_pdf(
    simulation_data: Dict[str, Any],
    output_path: str | None = None
) -> str:
    if PDF_DISABLE:
        raise RuntimeError("PDF generation disabled (DISABLE_PDF=1)")

    out_path = _resolve_output(simulation_data, output_path)
    _dbg(f"Output path: {out_path}")

    # Generate HTML first (fail fast if data invalid)
    html = generate_report_html(simulation_data)

    try:
        async with async_playwright() as p:
            _dbg("Launching Chromium with flags: " + " ".join(CHROMIUM_FLAGS))
            try:
                browser = await p.chromium.launch(headless=True, args=CHROMIUM_FLAGS)
            except Exception as launch_err:
                msg = str(launch_err).lower()
                retry = False
                if "executable" in msg and ("doesn't exist" in msg or "not found" in msg):
                    retry = True
                if retry:
                    await _attempt_install_chromium()
                    try:
                        browser = await p.chromium.launch(headless=True, args=CHROMIUM_FLAGS)
                    except Exception as second_err:
                        raise RuntimeError(
                            "Chromium executable missing after fallback install. Ensure build step includes 'python -m playwright install chromium'."
                        ) from second_err
                elif "lib" in msg and "not found" in msg:
                    raise RuntimeError(
                        "Missing system libraries for Chromium (fonts/libnss3). Requires system packages not available on free plan."
                    ) from launch_err
                elif "sandbox" in msg:
                    raise RuntimeError(
                        "Chromium sandbox error even with --no-sandbox. Container restrictions may apply."
                    ) from launch_err
                else:
                    raise

            page = await browser.new_page()
            await page.set_content(html, wait_until="domcontentloaded")
            _dbg("HTML content set; creating PDF...")
            await page.pdf(
                path=str(out_path),
                format="A4",
                print_background=True,
                margin={"top": "20mm", "right": "15mm", "bottom": "20mm", "left": "15mm"},
            )
            await browser.close()
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        print(f"[PDF] ❌ Error: {e}\n{tb}")
        # Cleanup partial file if present
        try:
            if out_path.exists():
                out_path.unlink()
        except Exception:
            pass
        raise

    print(f"[PDF] ✅ Success: {out_path}")
    return str(out_path)


def generate_report_html(data: Dict[str, Any]) -> str:
    """Generate simple, clean HTML for the PDF report - optimized for Render.com free tier."""

    reaction_name = data.get('reaction_name', 'Green Chemistry Simulation')
    timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")

    # Extract metrics with safe defaults
    ae = data.get('atom_economy_pct', 'N/A')
    pmi = data.get('pmi', 'N/A')
    e_factor = data.get('e_factor', 'N/A')
    rme = data.get('rme_pct', 'N/A')
    ce = data.get('carbon_efficiency_pct', 'N/A')
    sf = data.get('sf_overall', 'N/A')
    water = data.get('water_mL_per_g', 'N/A')
    energy = data.get('energy_Wh_per_g', 'N/A')
    
    # Calculate additional metrics
    breakdown = data.get('breakdown') or {}
    product_mass = breakdown.get('product_mass_g', 0) if isinstance(breakdown, dict) else 0
    total_solvent = breakdown.get('solvent_mass_total_g', 0) if isinstance(breakdown, dict) else 0
    si = round(total_solvent / product_mass, 2) if product_mass > 0 else 'N/A'
    
    # Carbon footprint estimate (energy is now in Wh, so divide by 2 instead of multiply by 500)
    try:
        cf = round(float(energy) * 0.5, 2) if energy not in ('N/A', None) and energy else 'N/A'
    except (ValueError, TypeError):
        cf = 'N/A'
    
    # Simple color coding helper
    def metric_color(value, thresholds):
        """Return color based on value and thresholds"""
        if value == 'N/A' or value is None:
            return '#6B7280'
        try:
            val = float(value)
            if val >= thresholds['good']:
                return '#059669'
            elif val >= thresholds['ok']:
                return '#F59E0B'
            else:
                return '#DC2626'
        except:
            return '#6B7280'
    
    # Color code key metrics
    ae_color = metric_color(ae, {'good': 80, 'ok': 60})
    rme_color = metric_color(rme, {'good': 80, 'ok': 60})
    ce_color = metric_color(ce, {'good': 80, 'ok': 60})

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Green Chemistry Metrics Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; padding: 20px; color: #333; }}
        .header {{ text-align: center; margin-bottom: 30px; border-bottom: 3px solid #059669; padding-bottom: 15px; }}
        .header h1 {{ color: #059669; font-size: 24px; margin: 0 0 10px 0; }}
        .subtitle {{ color: #666; font-size: 14px; }}
        .metrics {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin: 30px 0; }}
        .metric {{ border: 2px solid #ddd; padding: 20px; text-align: center; background: #f9f9f9; border-radius: 8px; }}
        .metric .label {{ font-size: 14px; color: #666; font-weight: bold; text-transform: uppercase; margin-bottom: 8px; }}
        .metric .value {{ font-size: 32px; font-weight: bold; }}
        .metric .unit {{ font-size: 16px; color: #666; font-weight: normal; }}
        .footer {{ margin-top: 40px; padding-top: 15px; border-top: 2px solid #ddd; text-align: center; font-size: 12px; color: #666; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Green Chemistry Metrics</h1>
        <div class="subtitle"><strong>{reaction_name}</strong><br>Generated: {timestamp}</div>
    </div>

    <div class="metrics">
        <div class="metric">
            <div class="label">Atom Economy</div>
            <div class="value" style="color:{ae_color}">{ae}<span class="unit">%</span></div>
        </div>
        <div class="metric">
            <div class="label">Process Mass Intensity</div>
            <div class="value">{pmi}</div>
        </div>
        <div class="metric">
            <div class="label">E-Factor</div>
            <div class="value">{e_factor}</div>
        </div>
        <div class="metric">
            <div class="label">Reaction Mass Efficiency</div>
            <div class="value" style="color:{rme_color}">{rme}<span class="unit">%</span></div>
        </div>
        <div class="metric">
            <div class="label">Carbon Efficiency</div>
            <div class="value" style="color:{ce_color}">{ce}<span class="unit">%</span></div>
        </div>
        <div class="metric">
            <div class="label">Stoichiometric Factor</div>
            <div class="value">{sf}</div>
        </div>
        <div class="metric">
            <div class="label">Water Intensity</div>
            <div class="value">{water}<span class="unit">mL/g</span></div>
        </div>
        <div class="metric">
            <div class="label">Energy Intensity</div>
            <div class="value">{energy}<span class="unit">Wh/g</span></div>
        </div>
        <div class="metric">
            <div class="label">Solvent Intensity</div>
            <div class="value">{si}</div>
        </div>
        <div class="metric">
            <div class="label">Carbon Footprint</div>
            <div class="value">{cf}<span class="unit">g CO2/g</span></div>
        </div>
    </div>

    <div class="footer">
        <p><strong>Green Toolkit</strong> - Sustainable Chemistry Analysis Platform</p>
        <p>© {datetime.now().year} Green Toolkit. Generated on {timestamp}</p>
    </div>
</body>
</html>"""

    return html



if __name__ == "__main__":
    # Manual quick test (synchronous wrapper)
    import asyncio
    sample_data = {
        "reaction_name": "Test Synthesis",
        "atom_economy_pct": 85.5,
        "pmi": 12.3,
        "e_factor": 11.3,
        "rme_pct": 75.2,
        "carbon_efficiency_pct": 82.1,
        "sf_overall": 1.15,
        "water_mL_per_g": 10.5,
        "energy_kWh_per_g": 0.05,
        "product": {"name": "Product A", "mw": 180.16, "actual_mass_g": 10, "carbon_atoms": 9},
        "reactants": [
            {"name": "Reactant 1", "mw": 138.12, "mass_g": 8.3, "carbon_atoms": 7, "eq_used": 1.0}
        ],
        "solvents": [
            {"name": "Ethanol", "mass_g": 50, "recovery_pct": 60}
        ],
        "breakdown": {
            "reactant_mass_g": 8.3,
            "catalyst_mass_g": 0.5,
            "solvent_mass_total_g": 50,
            "aqueous_washes_g": 100,
            "auxiliaries_g": 0,
            "total_input_mass_g": 158.8,
            "product_mass_g": 10
        },
        "ai_suggestions": ["Consider using greener solvents", "Optimize reaction time"]
    }
    path = asyncio.run(generate_simulation_pdf(sample_data))
    print("Generated:", path)
