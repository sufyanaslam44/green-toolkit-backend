"""
Minimal Playwright PDF test - Debug version
This creates the simplest possible PDF to test if Playwright works
"""
import asyncio
import sys
from playwright.async_api import async_playwright

# Fix for Windows + Python 3.13
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

async def test_simple_pdf():
    """Generate the simplest possible PDF"""
    print("="*60)
    print("SIMPLE PDF GENERATION TEST")
    print("="*60)
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Test PDF</title>
    </head>
    <body>
        <h1>PDF Report is generated</h1>
    </body>
    </html>
    """
    
    print("\n[DEBUG] Step 1: Initializing Playwright...")
    try:
        async with async_playwright() as p:
            print("[DEBUG] ✓ Playwright initialized")
            
            print("[DEBUG] Step 2: Launching Chromium browser...")
            browser = await p.chromium.launch(
                headless=True,
                args=['--disable-gpu', '--no-sandbox']
            )
            print("[DEBUG] ✓ Browser launched")
            
            print("[DEBUG] Step 3: Creating new page...")
            page = await browser.new_page()
            print("[DEBUG] ✓ Page created")
            
            print("[DEBUG] Step 4: Setting HTML content...")
            await page.set_content(html_content)
            print("[DEBUG] ✓ Content set")
            
            print("[DEBUG] Step 5: Generating PDF...")
            pdf_path = "simple_test.pdf"
            await page.pdf(
                path=pdf_path,
                format='A4',
                print_background=True
            )
            print(f"[DEBUG] ✓ PDF generated: {pdf_path}")
            
            print("[DEBUG] Step 6: Closing browser...")
            await browser.close()
            print("[DEBUG] ✓ Browser closed")
            
            print("\n" + "="*60)
            print(f"✅ SUCCESS! PDF created: {pdf_path}")
            print("="*60)
            return pdf_path
            
    except Exception as e:
        print(f"\n❌ ERROR at some step:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        import traceback
        print("\nFull traceback:")
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print("Starting simple PDF test with debug output...\n")
    result = asyncio.run(test_simple_pdf())
    
    if result:
        print(f"\n✅ Test PASSED - Check {result}")
        exit(0)
    else:
        print("\n❌ Test FAILED - See errors above")
        exit(1)
