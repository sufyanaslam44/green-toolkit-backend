"""
Test the FastAPI PDF endpoint directly
"""
import asyncio
import sys
import json
from main import app, generate_pdf_report, PDFGenerationIn

# Fix for Windows
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

async def test_fastapi_endpoint():
    """Test the PDF generation endpoint"""
    print("="*60)
    print("TESTING FASTAPI PDF ENDPOINT")
    print("="*60)
    
    # Sample data
    test_data = {
        "reaction_name": "Test from FastAPI",
        "product": {
            "name": "Test Product",
            "mw": 180.16,
            "actual_mass_g": 10.0,
            "carbon_atoms": 9
        },
        "reactants": [
            {
                "name": "Test Reactant",
                "mw": 138.12,
                "mass_g": 8.3,
                "carbon_atoms": 7,
                "eq_used": 1.0,
                "eq_stoich": 1.0
            }
        ],
        "solvents": [],
        "catalysts": [],
        "workup": {
            "aqueous_washes_g": 0,
            "organic_rinses_g": 0,
            "drying_agents_g": 0
        },
        "conditions": {
            "temp_C": 25,
            "time_h": 1.0,
            "mode": "hotplate"
        },
        "options": {},
        "atom_economy_pct": 85.5,
        "pmi": 15.88,
        "e_factor": 14.88,
        "rme_pct": 48.78,
        "carbon_efficiency_pct": 82.14,
        "sf_overall": 1.1,
        "breakdown": {
            "reactant_mass_g": 8.3,
            "product_mass_g": 10.0
        }
    }
    
    print("\n[TEST] Creating PDFGenerationIn model...")
    try:
        payload = PDFGenerationIn(**test_data)
        print("[TEST] ✓ Model created successfully")
        
        print("\n[TEST] Calling generate_pdf_report endpoint...")
        result = await generate_pdf_report(payload)
        
        print(f"\n[TEST] ✓ PDF generated!")
        print(f"[TEST] Result type: {type(result)}")
        print(f"[TEST] Result: {result}")
        
        print("\n" + "="*60)
        print("✅ FASTAPI ENDPOINT TEST PASSED!")
        print("="*60)
        return True
        
    except Exception as e:
        print(f"\n[TEST] ❌ ERROR:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        import traceback
        print("\nFull traceback:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing FastAPI PDF endpoint...\n")
    success = asyncio.run(test_fastapi_endpoint())
    
    if success:
        print("\n✅ Endpoint test PASSED")
        exit(0)
    else:
        print("\n❌ Endpoint test FAILED")
        exit(1)
