"""
PDF Report Generator for Green Chemistry Simulations
Uses Playwright to render HTML and generate high-quality PDF reports
"""
from playwright.async_api import async_playwright
from pathlib import Path
from datetime import datetime
import json
from typing import Dict, Any


async def generate_simulation_pdf(
    simulation_data: Dict[str, Any],
    output_path: str = None
) -> str:
    """
    Generate a PDF report from simulation data.
    
    Args:
        simulation_data: Dictionary containing all simulation metrics and data
        output_path: Optional path for the PDF file. If None, auto-generates filename.
    
    Returns:
        str: Path to the generated PDF file
    """
    try:
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            reaction_name = simulation_data.get('reaction_name', 'simulation') if isinstance(simulation_data, dict) else 'simulation'
            safe_name = "".join(c for c in reaction_name if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_name = safe_name.replace(' ', '_') or 'simulation'
            output_path = f"green_chem_report_{safe_name}_{timestamp}.pdf"
        
        print(f"[PDF] Generating: {output_path}")
        
        # Generate HTML content for the PDF
        html_content = generate_report_html(simulation_data)
        
        # Use Playwright async API to generate PDF
        async with async_playwright() as p:
            print("[PDF] Launching browser...")
            
            # Try to get browser executable path for debugging
            try:
                exec_path = p.chromium.executable_path
                print(f"[PDF] Chromium executable: {exec_path}")
            except Exception as e:
                print(f"[PDF] Could not get executable path: {e}")
            
            # Launch with error handling
            try:
                browser = await p.chromium.launch(
                    headless=True,
                    args=[
                        '--disable-gpu',
                        '--no-sandbox',
                        '--disable-dev-shm-usage',  # Important for Docker/Render
                        '--disable-setuid-sandbox',
                        '--single-process',  # Helps with memory constraints
                        '--disable-software-rasterizer'
                    ]
                )
            except Exception as launch_error:
                print(f"[PDF] Browser launch failed: {launch_error}")
                print("[PDF] Attempting fallback launch without headless...")
                # Fallback: try without some flags
                browser = await p.chromium.launch(
                    headless=True,
                    args=['--no-sandbox', '--disable-setuid-sandbox']
                )
            
            page = await browser.new_page()
            await page.set_content(html_content, wait_until='networkidle')
            
            # Generate PDF with proper formatting
            await page.pdf(
                path=output_path,
                format='A4',
                print_background=True,
                margin={
                    'top': '20mm',
                    'right': '15mm',
                    'bottom': '20mm',
                    'left': '15mm'
                }
            )
            
            await browser.close()
        
        print(f"[PDF] ✅ Success: {output_path}")
        return output_path
    except Exception as e:
        import traceback
        error_msg = f"PDF generation error: {str(e)}\n{traceback.format_exc()}"
        print(f"[PDF] ❌ Error: {error_msg}")
        raise Exception(f"Failed to generate PDF: {str(e)}")


def generate_report_html(data: Dict[str, Any]) -> str:
    """Generate formatted HTML for the PDF report."""
    
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
    energy = data.get('energy_kWh_per_g', 'N/A')
    
    # Calculate additional metrics - handle None/missing breakdown
    breakdown = data.get('breakdown') or {}
    product_mass = breakdown.get('product_mass_g', 0) if isinstance(breakdown, dict) else 0
    total_solvent = breakdown.get('solvent_mass_total_g', 0) if isinstance(breakdown, dict) else 0
    si = round(total_solvent / product_mass, 2) if product_mass > 0 else 'N/A'
    
    # Safe calculation for carbon footprint
    try:
        cf = round(float(energy) * 500, 2) if energy not in ('N/A', None) and energy else 'N/A'
    except (ValueError, TypeError):
        cf = 'N/A'
    
    # Get product, reactants, solvents with safe defaults
    product = data.get('product') or {}
    reactants = data.get('reactants') or []
    solvents = data.get('solvents') or []
    catalysts = data.get('catalysts') or []
    
    # Build reactants table - handle both dict and missing keys
    reactants_rows = ""
    if isinstance(reactants, list):
        for i, r in enumerate(reactants, 1):
            if isinstance(r, dict):
                reactants_rows += f"""
        <tr>
            <td>{i}</td>
            <td>{r.get('name', 'N/A')}</td>
            <td>{r.get('mw', 'N/A')}</td>
            <td>{r.get('mass_g', 'N/A')}</td>
            <td>{r.get('carbon_atoms', 'N/A')}</td>
            <td>{r.get('eq_used', 'N/A')}</td>
        </tr>
        """
    
    # Build solvents table
    solvents_rows = ""
    if isinstance(solvents, list):
        for i, s in enumerate(solvents, 1):
            if isinstance(s, dict):
                solvents_rows += f"""
        <tr>
            <td>{i}</td>
            <td>{s.get('name', 'N/A')}</td>
            <td>{s.get('mass_g', 'N/A')}</td>
            <td>{s.get('recovery_pct', 0)}%</td>
        </tr>
        """
    
    # Build catalysts table
    catalysts_rows = ""
    if isinstance(catalysts, list):
        for i, c in enumerate(catalysts, 1):
            if isinstance(c, dict):
                catalysts_rows += f"""
        <tr>
            <td>{i}</td>
            <td>{c.get('name', 'N/A')}</td>
            <td>{c.get('mw', 'N/A')}</td>
            <td>{c.get('mass_g', 'N/A')}</td>
        </tr>
        """
    
    # AI Suggestions - handle None/missing
    suggestions = data.get('ai_suggestions') or []
    suggestions_html = ""
    if isinstance(suggestions, list) and suggestions:
        for sugg in suggestions:
            if sugg:  # Skip empty suggestions
                suggestions_html += f"<li>{sugg}</li>"
    if not suggestions_html:
        suggestions_html = "<li>No suggestions available. Run simulation to generate insights.</li>"
    
    # Metric color coding helper
    def metric_color(value, thresholds):
        """Return color class based on value and thresholds (good, ok, poor)"""
        if value == 'N/A' or value is None:
            return 'gray'
        try:
            val = float(value)
            if val >= thresholds['good']:
                return 'green'
            elif val >= thresholds['ok']:
                return 'yellow'
            else:
                return 'red'
        except:
            return 'gray'
    
    # Color code key metrics
    ae_color = metric_color(ae, {'good': 80, 'ok': 60})
    rme_color = metric_color(rme, {'good': 80, 'ok': 60})
    ce_color = metric_color(ce, {'good': 80, 'ok': 60})
    
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Green Chemistry Report - {reaction_name}</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                background: white;
                padding: 20px;
            }}
            .header {{
                text-align: center;
                margin-bottom: 30px;
                padding-bottom: 20px;
                border-bottom: 3px solid #059669;
            }}
            .header h1 {{
                color: #059669;
                font-size: 28px;
                margin-bottom: 10px;
            }}
            .header .subtitle {{
                color: #666;
                font-size: 14px;
            }}
            .section {{
                margin-bottom: 25px;
                page-break-inside: avoid;
            }}
            .section-title {{
                background: #059669;
                color: white;
                padding: 10px 15px;
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 15px;
                border-radius: 5px;
            }}
            .metrics-grid {{
                display: grid;
                grid-template-columns: repeat(5, 1fr);
                gap: 10px;
                margin-bottom: 20px;
            }}
            .metric-card {{
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 15px;
                text-align: center;
                background: #f9f9f9;
            }}
            .metric-card .label {{
                font-size: 11px;
                color: #666;
                margin-bottom: 5px;
                font-weight: 600;
                text-transform: uppercase;
            }}
            .metric-card .value {{
                font-size: 24px;
                font-weight: bold;
                color: #333;
            }}
            .metric-card.green .value {{ color: #059669; }}
            .metric-card.yellow .value {{ color: #F59E0B; }}
            .metric-card.red .value {{ color: #DC2626; }}
            .metric-card.gray .value {{ color: #6B7280; }}
            
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
                font-size: 12px;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #f0f0f0;
                font-weight: bold;
                color: #333;
            }}
            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
            .product-info {{
                background: #F0FDF4;
                border-left: 4px solid #059669;
                padding: 15px;
                margin-bottom: 15px;
                border-radius: 5px;
            }}
            .product-info h3 {{
                color: #059669;
                margin-bottom: 10px;
                font-size: 16px;
            }}
            .product-info p {{
                margin: 5px 0;
                font-size: 13px;
            }}
            .suggestions {{
                background: #EFF6FF;
                border-left: 4px solid #3B82F6;
                padding: 15px;
                border-radius: 5px;
            }}
            .suggestions ul {{
                margin-left: 20px;
                margin-top: 10px;
            }}
            .suggestions li {{
                margin: 8px 0;
                font-size: 13px;
            }}
            .footer {{
                margin-top: 40px;
                padding-top: 20px;
                border-top: 2px solid #ddd;
                text-align: center;
                font-size: 11px;
                color: #666;
            }}
            .interpretation {{
                background: #FFF7ED;
                border-left: 4px solid #F59E0B;
                padding: 15px;
                margin-top: 15px;
                border-radius: 5px;
                font-size: 13px;
            }}
            .interpretation h4 {{
                color: #F59E0B;
                margin-bottom: 8px;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🌱 Green Chemistry Simulation Report</h1>
            <div class="subtitle">
                <strong>{reaction_name}</strong><br>
                Generated: {timestamp}
            </div>
        </div>

        <!-- Product Information -->
        <div class="section">
            <div class="section-title">Product Information</div>
            <div class="product-info">
                <h3>{product.get('name', 'Product')}</h3>
                <p><strong>Molecular Weight:</strong> {product.get('mw', 'N/A')} g/mol</p>
                <p><strong>Actual Mass:</strong> {product.get('actual_mass_g', 'N/A')} g</p>
                <p><strong>Carbon Atoms:</strong> {product.get('carbon_atoms', 'N/A')}</p>
            </div>
        </div>

        <!-- Key Metrics -->
        <div class="section">
            <div class="section-title">Key Green Chemistry Metrics</div>
            <div class="metrics-grid">
                <div class="metric-card {ae_color}">
                    <div class="label">Atom Economy</div>
                    <div class="value">{ae}%</div>
                </div>
                <div class="metric-card">
                    <div class="label">PMI</div>
                    <div class="value">{pmi}</div>
                </div>
                <div class="metric-card">
                    <div class="label">E-Factor</div>
                    <div class="value">{e_factor}</div>
                </div>
                <div class="metric-card {rme_color}">
                    <div class="label">RME</div>
                    <div class="value">{rme}%</div>
                </div>
                <div class="metric-card {ce_color}">
                    <div class="label">Carbon Eff.</div>
                    <div class="value">{ce}%</div>
                </div>
                <div class="metric-card">
                    <div class="label">Stoich. Factor</div>
                    <div class="value">{sf}</div>
                </div>
                <div class="metric-card">
                    <div class="label">Water Intensity</div>
                    <div class="value">{water}</div>
                </div>
                <div class="metric-card">
                    <div class="label">Energy</div>
                    <div class="value">{energy}</div>
                </div>
                <div class="metric-card">
                    <div class="label">Solvent Int.</div>
                    <div class="value">{si}</div>
                </div>
                <div class="metric-card">
                    <div class="label">Carbon Footprint</div>
                    <div class="value">{cf}</div>
                </div>
            </div>
            
            <div class="interpretation">
                <h4>Metrics Interpretation Guide:</h4>
                <ul>
                    <li><strong>Atom Economy (AE):</strong> ≥80% excellent, 60-80% good, &lt;60% needs improvement</li>
                    <li><strong>PMI:</strong> &lt;10 pharmaceutical, &lt;5 fine chemicals, &lt;1 ideal</li>
                    <li><strong>E-Factor:</strong> Lower is better; &lt;1 pharmaceutical, &lt;5 fine chemicals</li>
                    <li><strong>RME:</strong> ≥80% excellent, 60-80% good, &lt;60% needs improvement</li>
                    <li><strong>Carbon Efficiency (CE):</strong> ≥80% excellent, 60-80% good, &lt;60% needs improvement</li>
                </ul>
            </div>
        </div>

        <!-- Reactants -->
        <div class="section">
            <div class="section-title">Reactants</div>
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Name</th>
                        <th>MW (g/mol)</th>
                        <th>Mass (g)</th>
                        <th>C Atoms</th>
                        <th>Eq. Used</th>
                    </tr>
                </thead>
                <tbody>
                    {reactants_rows if reactants_rows else '<tr><td colspan="6">No reactants</td></tr>'}
                </tbody>
            </table>
        </div>

        <!-- Solvents -->
        <div class="section">
            <div class="section-title">Solvents</div>
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Name</th>
                        <th>Mass (g)</th>
                        <th>Recovery</th>
                    </tr>
                </thead>
                <tbody>
                    {solvents_rows if solvents_rows else '<tr><td colspan="4">No solvents</td></tr>'}
                </tbody>
            </table>
        </div>

        <!-- Catalysts -->
        {f'''
        <div class="section">
            <div class="section-title">Catalysts</div>
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Name</th>
                        <th>MW (g/mol)</th>
                        <th>Mass (g)</th>
                    </tr>
                </thead>
                <tbody>
                    {catalysts_rows if catalysts_rows else '<tr><td colspan="4">No catalysts</td></tr>'}
                </tbody>
            </table>
        </div>
        ''' if catalysts else ''}

        <!-- Mass Balance -->
        <div class="section">
            <div class="section-title">Mass Balance Breakdown</div>
            <table>
                <tbody>
                    <tr>
                        <th>Reactant Mass</th>
                        <td>{breakdown.get('reactant_mass_g', 0)} g</td>
                    </tr>
                    <tr>
                        <th>Catalyst Mass</th>
                        <td>{breakdown.get('catalyst_mass_g', 0)} g</td>
                    </tr>
                    <tr>
                        <th>Total Solvent Mass</th>
                        <td>{breakdown.get('solvent_mass_total_g', 0)} g</td>
                    </tr>
                    <tr>
                        <th>Aqueous Washes</th>
                        <td>{breakdown.get('aqueous_washes_g', 0)} g</td>
                    </tr>
                    <tr>
                        <th>Auxiliaries (Drying)</th>
                        <td>{breakdown.get('auxiliaries_g', 0)} g</td>
                    </tr>
                    <tr style="background: #F0FDF4; font-weight: bold;">
                        <th>Total Input Mass</th>
                        <td>{breakdown.get('total_input_mass_g', 0)} g</td>
                    </tr>
                    <tr style="background: #F0FDF4; font-weight: bold;">
                        <th>Product Mass</th>
                        <td>{breakdown.get('product_mass_g', 0)} g</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- AI Suggestions -->
        <div class="section">
            <div class="section-title">AI-Powered Recommendations</div>
            <div class="suggestions">
                <ul>
                    {suggestions_html}
                </ul>
            </div>
        </div>

        <div class="footer">
            <p><strong>Green Toolkit</strong> - Sustainable Chemistry Analysis Platform</p>
            <p>This report was automatically generated. All metrics calculated according to standard green chemistry principles.</p>
            <p>© {datetime.now().year} Green Toolkit. For educational and research purposes.</p>
        </div>
    </body>
    </html>
    """
    
    return html


if __name__ == "__main__":
    # Test with sample data
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
    
    pdf_path = generate_simulation_pdf(sample_data)
    print(f"PDF generated: {pdf_path}")
