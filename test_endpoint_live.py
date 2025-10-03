"""
Test the live /api/generate-pdf endpoint
"""
import asyncio
import sys
import requests
import json

# Set event loop policy for Windows
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# Sample payload matching the web interface
test_payload = {
    "reaction_name": "Test PDF Generation",
    "product": {
        "name": "Test Product",
        "mw": 180.0,
        "actual_mass_g": 10.0  # Fixed: use actual_mass_g not mass_g
    },
    "reactants": [
        {
            "name": "Reactant A",
            "mw": 100.0,
            "mass_g": 15.0
        }
    ],
    "solvents": [],
    "catalysts": [],
    "workup": {},
    "conditions": {},
    "atom_economy_pct": 85.5,
    "pmi": 2.5,
    "e_factor": 1.5,
    "water_mL_per_g": 10.0,
    "energy_kWh_per_g": 2.0,
    "rme_pct": 75.0,
    "carbon_efficiency_pct": 80.0,
    "sf_overall": 3.5,
    "sf_details": [],
    "breakdown": {},
    "ai_suggestions": []
}

print("Testing live endpoint: http://localhost:8000/api/generate-pdf")
print("=" * 60)

try:
    response = requests.post(
        "http://localhost:8000/api/generate-pdf",
        json=test_payload,
        timeout=30
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    
    if response.status_code == 200:
        print("✅ SUCCESS! PDF generated")
        print(f"Content-Type: {response.headers.get('content-type')}")
        print(f"Content-Length: {len(response.content)} bytes")
        
        # Save the PDF
        filename = "test_from_endpoint.pdf"
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"✅ Saved to: {filename}")
    else:
        print("❌ ERROR!")
        print(f"Response: {response.text}")
        
except requests.exceptions.RequestException as e:
    print(f"❌ Request failed: {e}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    import traceback
    traceback.print_exc()
