"""
Test PDF generation with minimal data to verify error handling
"""
import asyncio
import sys
from pdf_generator import generate_simulation_pdf

# Fix for Windows + Python 3.13 + Playwright
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

async def run_tests():
    # Test 1: Minimal data (simulating what frontend might send)
    print("Test 1: Minimal data with None/missing fields...")
    minimal_data = {
        "reaction_name": "Test Reaction",
        "product": {
            "name": "Test Product",
            "mw": 100,
            "actual_mass_g": 10
        },
        "reactants": [
            {
                "name": "Reactant 1",
                "mw": 80,
                "mass_g": 8
            }
        ],
        "solvents": [],
        "catalysts": [],
        "breakdown": None,  # This was causing the error!
        "atom_economy_pct": 80.0,
        "pmi": 12.0
    }

    try:
        pdf_path = await generate_simulation_pdf(minimal_data, "test_minimal.pdf")
        print(f"✓ Test 1 PASSED: {pdf_path}")
    except Exception as e:
        print(f"✗ Test 1 FAILED: {e}")
        import traceback
        traceback.print_exc()

    # Test 2: Missing breakdown entirely
    print("\nTest 2: Missing breakdown field...")
    no_breakdown_data = {
        "reaction_name": "No Breakdown Test",
        "product": {"name": "Product", "mw": 100, "actual_mass_g": 10},
        "reactants": [{"name": "R1", "mw": 80, "mass_g": 8}],
    }

    try:
        pdf_path = await generate_simulation_pdf(no_breakdown_data, "test_no_breakdown.pdf")
        print(f"✓ Test 2 PASSED: {pdf_path}")
    except Exception as e:
        print(f"✗ Test 2 FAILED: {e}")

    # Test 3: Empty arrays
    print("\nTest 3: Empty arrays...")
    empty_arrays_data = {
        "reaction_name": "Empty Arrays Test",
        "product": {"name": "Product", "mw": 100, "actual_mass_g": 10},
        "reactants": [],
        "solvents": [],
        "catalysts": [],
        "ai_suggestions": None
    }

    try:
        pdf_path = await generate_simulation_pdf(empty_arrays_data, "test_empty_arrays.pdf")
        print(f"✓ Test 3 PASSED: {pdf_path}")
    except Exception as e:
        print(f"✗ Test 3 FAILED: {e}")

    print("\n" + "="*50)
    print("All tests completed!")
    print("If all tests passed, the PDF generation is now robust.")

if __name__ == "__main__":
    asyncio.run(run_tests())
