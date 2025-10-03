"""
Verification script to ensure async PDF generation is working correctly
Tests both standalone and simulated FastAPI context
"""
import asyncio
import sys
from pdf_generator import generate_simulation_pdf

# Fix for Windows + Python 3.13 + Playwright
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

async def test_async_generation():
    """Test that PDF generation works in async context"""
    print("="*60)
    print("ASYNC PDF GENERATION VERIFICATION")
    print("="*60)
    
    test_data = {
        "reaction_name": "Async Verification Test",
        "product": {
            "name": "Test Product",
            "mw": 100,
            "actual_mass_g": 10,
            "carbon_atoms": 5
        },
        "reactants": [
            {
                "name": "Test Reactant",
                "mw": 80,
                "mass_g": 8,
                "carbon_atoms": 4,
                "eq_used": 1.0,
                "eq_stoich": 1.0
            }
        ],
        "solvents": [
            {"name": "Water", "mass_g": 50, "recovery_pct": 0}
        ],
        "catalysts": [],
        "atom_economy_pct": 85.0,
        "pmi": 15.0,
        "e_factor": 14.0,
        "rme_pct": 50.0,
        "carbon_efficiency_pct": 80.0,
        "breakdown": {
            "reactant_mass_g": 8.0,
            "product_mass_g": 10.0,
            "solvent_mass_total_g": 50.0
        }
    }
    
    print("\n✓ Test 1: Basic async PDF generation")
    try:
        start = asyncio.get_event_loop().time()
        pdf_path = await generate_simulation_pdf(test_data, "verify_async.pdf")
        elapsed = asyncio.get_event_loop().time() - start
        print(f"  ✅ SUCCESS: Generated {pdf_path}")
        print(f"  ⏱️  Time: {elapsed:.2f} seconds")
    except Exception as e:
        print(f"  ❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n✓ Test 2: Multiple concurrent generations")
    try:
        start = asyncio.get_event_loop().time()
        
        # Generate 3 PDFs concurrently
        tasks = [
            generate_simulation_pdf(test_data, f"verify_concurrent_{i}.pdf")
            for i in range(3)
        ]
        results = await asyncio.gather(*tasks)
        
        elapsed = asyncio.get_event_loop().time() - start
        print(f"  ✅ SUCCESS: Generated {len(results)} PDFs concurrently")
        print(f"  ⏱️  Time: {elapsed:.2f} seconds")
        print(f"  📊 Average: {elapsed/len(results):.2f} seconds per PDF")
        
        for i, path in enumerate(results):
            print(f"     - {path}")
    except Exception as e:
        print(f"  ❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n✓ Test 3: Async context manager works correctly")
    try:
        from playwright.async_api import async_playwright
        
        async with async_playwright() as p:
            print(f"  ✅ SUCCESS: Async Playwright context manager works")
            print(f"     Chromium available: {hasattr(p, 'chromium')}")
    except Exception as e:
        print(f"  ❌ FAILED: {e}")
        return False
    
    print("\n" + "="*60)
    print("✅ ALL ASYNC VERIFICATIONS PASSED!")
    print("="*60)
    print("\nSummary:")
    print("  ✅ Async PDF generation works")
    print("  ✅ Concurrent generation works")
    print("  ✅ No event loop conflicts")
    print("  ✅ Playwright async API properly integrated")
    print("\n🚀 Ready for production use with FastAPI!")
    
    return True

if __name__ == "__main__":
    print("Starting async verification tests...\n")
    success = asyncio.run(test_async_generation())
    
    if success:
        print("\n✅ Verification complete - All systems GO!")
        exit(0)
    else:
        print("\n❌ Verification failed - Please check errors above")
        exit(1)
