"""Test PDF generation"""
import asyncio
from pdf_generator import generate_simulation_pdf

# Sample test data
test_data = {
    "reaction_name": "Test Synthesis",
    "atom_economy_pct": 85.5,
    "pmi": 12.3,
    "e_factor": 11.3,
    "rme_pct": 75.2,
    "carbon_efficiency_pct": 82.1,
    "sf_overall": 1.15,
    "water_mL_per_g": 10.5,
    "energy_kWh_per_g": 0.05,
    "product": {
        "name": "Product A",
        "mw": 180.16,
        "actual_mass_g": 10,
        "carbon_atoms": 9
    },
    "reactants": [
        {
            "name": "Reactant 1",
            "mw": 138.12,
            "mass_g": 8.3,
            "carbon_atoms": 7,
            "eq_used": 1.0
        }
    ],
    "solvents": [
        {
            "name": "Ethanol",
            "mass_g": 50,
            "recovery_pct": 60
        }
    ],
    "catalysts": [],
    "breakdown": {
        "reactant_mass_g": 8.3,
        "catalyst_mass_g": 0.5,
        "solvent_mass_total_g": 50,
        "aqueous_washes_g": 100,
        "auxiliaries_g": 0,
        "total_input_mass_g": 158.8,
        "product_mass_g": 10
    },
    "ai_suggestions": [
        "Consider using greener solvents",
        "Optimize reaction time"
    ]
}

async def main():
    print("Testing PDF generation...")
    print("=" * 60)
    try:
        pdf_path = await generate_simulation_pdf(test_data)
        print(f"\n✅ SUCCESS! PDF generated at: {pdf_path}")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
