"""
Test script for PDF generation
"""
import asyncio
import sys
from pdf_generator import generate_simulation_pdf

# Fix for Windows + Python 3.13 + Playwright
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# Sample data matching the Aspirin example
sample_data = {
    "reaction_name": "Synthesis of Aspirin",
    "atom_economy_pct": 85.5,
    "pmi": 15.88,
    "e_factor": 14.88,
    "rme_pct": 48.78,
    "carbon_efficiency_pct": 82.14,
    "sf_overall": 1.1,
    "water_mL_per_g": 10.0,
    "energy_kWh_per_g": 0.0525,
    "product": {
        "name": "Aspirin",
        "mw": 180.16,
        "actual_mass_g": 10.0,
        "carbon_atoms": 9
    },
    "reactants": [
        {
            "name": "Salicylic Acid",
            "mw": 138.12,
            "mass_g": 8.3,
            "carbon_atoms": 7,
            "eq_used": 1.0,
            "eq_stoich": 1.0
        },
        {
            "name": "Acetic Anhydride",
            "mw": 102.09,
            "mass_g": 12.2,
            "carbon_atoms": 4,
            "eq_used": 1.2,
            "eq_stoich": 1.0
        }
    ],
    "solvents": [
        {
            "name": "Ethyl Acetate",
            "mass_g": 45.1,
            "recovery_pct": 60
        },
        {
            "name": "Water",
            "mass_g": 150.0,
            "recovery_pct": 0
        }
    ],
    "catalysts": [
        {
            "name": "Sulfuric Acid",
            "mw": 98.08,
            "mass_g": 0.5
        }
    ],
    "breakdown": {
        "reactant_mass_g": 20.5,
        "catalyst_mass_g": 0.5,
        "solvent_mass_total_g": 195.1,
        "aqueous_washes_g": 100.0,
        "auxiliaries_g": 0.0,
        "total_input_mass_g": 316.1,
        "product_mass_g": 10.0,
        "water_total_g": 250.0,
        "energy_kWh_total_est": 0.525
    },
    "ai_suggestions": [
        "Consider replacing acetic anhydride with a greener acylating agent",
        "Explore water-based solvent systems to reduce organic solvent use",
        "Optimize catalyst loading - sulfuric acid can be reduced",
        "Implement solvent recovery to improve sustainability metrics"
    ]
}

async def main():
    print("Generating PDF report for Aspirin synthesis...")
    try:
        pdf_path = await generate_simulation_pdf(sample_data, "test_aspirin_report.pdf")
        print(f"✓ PDF generated successfully: {pdf_path}")
        print("\nYou can now open the PDF to verify the formatting.")
    except Exception as e:
        print(f"✗ Error generating PDF: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
