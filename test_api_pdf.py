"""Test PDF generation API endpoint"""
import requests
import json

# Complete payload with all required data
payload = {
    "reaction_name": "Aspirin Synthesis Test",
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
            "mass_g": 6.1,
            "carbon_atoms": 4,
            "eq_used": 1.2,
            "eq_stoich": 1.0
        }
    ],
    "solvents": [
        {
            "name": "Ethanol",
            "mass_g": 50.0,
            "recovery_pct": 60.0
        }
    ],
    "catalysts": [
        {
            "name": "Sulfuric Acid",
            "mw": 98.08,
            "mass_g": 0.5
        }
    ],
    "workup": {
        "aqueous_washes_g": 100.0,
        "organic_rinses_g": 0.0,
        "drying_agents_g": 2.0
    },
    "conditions": {
        "temp_C": 85.0,
        "time_h": 2.0,
        "mode": "reflux"
    },
    # Include computed metrics (as they would come from /api/impact/compute)
    "atom_economy_pct": 75.2,
    "pmi": 16.79,
    "e_factor": 15.79,
    "water_mL_per_g": 10.0,
    "energy_kWh_per_g": 0.096,
    "rme_pct": 69.44,
    "carbon_efficiency_pct": 82.1,
    "sf_overall": 1.1,
    "breakdown": {
        "reactant_mass_g": 14.4,
        "catalyst_mass_g": 0.5,
        "solvent_mass_total_g": 50.0,
        "aqueous_washes_g": 100.0,
        "auxiliaries_g": 2.0,
        "total_input_mass_g": 166.9,
        "product_mass_g": 10.0
    },
    "ai_suggestions": [
        "Consider using greener solvents like ethanol or water",
        "Optimize reaction time to reduce energy consumption",
        "Increase solvent recovery percentage to improve sustainability"
    ]
}

print("Testing PDF Generation API...")
print("=" * 60)

try:
    # Send request to generate PDF
    response = requests.post(
        'http://localhost:8000/api/generate-pdf',
        json=payload,
        timeout=30
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Content-Type: {response.headers.get('Content-Type')}")
    
    if response.status_code == 200:
        # Save the PDF
        filename = "test_output.pdf"
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"\n✅ SUCCESS! PDF saved as: {filename}")
        print(f"PDF size: {len(response.content)} bytes")
    else:
        print(f"\n❌ ERROR {response.status_code}")
        try:
            error = response.json()
            print(f"Error detail: {error}")
        except:
            print(f"Response text: {response.text[:500]}")
            
except requests.exceptions.RequestException as e:
    print(f"\n❌ REQUEST ERROR: {e}")
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

print("=" * 60)
