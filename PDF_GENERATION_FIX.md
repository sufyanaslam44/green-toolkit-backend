# PDF Generation Fix - Summary

## Issue Identified
The "Generate PDF Report" button was not working because the frontend JavaScript was not properly storing the complete simulation data needed for PDF generation.

## Root Cause
When the simulation ran successfully, only the API response (computed metrics) was being stored in `window.lastSimulationData`, but the PDF generation requires **both** the input data (product, reactants, solvents, etc.) **and** the computed metrics.

## Fix Applied
Modified `templates/sim.html` to store complete data:

### Before:
```javascript
function renderAll(data) {
  window.lastSimulationData = data;  // Only stored API response
  // ...
}
```

### After:
```javascript
function renderAll(data) {
  window.lastSimulationData = {
    ...data,  // API response with computed metrics
    // Also store current input data
    product: buildPayload().product,
    reactants: buildPayload().reactants,
    solvents: buildPayload().solvents || [],
    catalysts: buildPayload().catalysts || [],
    workup: buildPayload().workup,
    conditions: buildPayload().conditions
  };
  // ...
}
```

Also simplified the PDF generation button handler since all data is now properly stored.

## Testing Instructions

### Local Testing:
1. **Start the server:**
   ```powershell
   cd "d:\Webtool\VS project\green-toolkit-backend\green-toolkit-backend"
   python run_server.py
   ```

2. **Open browser:**
   Navigate to: `http://localhost:8000/simulate`

3. **Run a simulation:**
   - Fill in product information (name, MW, mass, carbon atoms)
   - Add at least one reactant (name, MW, mass)
   - Add solvents if desired
   - Click "Run Simulation"

4. **Generate PDF:**
   - After simulation completes successfully, the "Generate PDF Report" button will appear
   - Click the button
   - PDF should download automatically with filename like: `green_chem_report_<ReactionName>_<timestamp>.pdf`

### Expected Behavior:
- ✅ PDF generation completes in ~5-10 seconds
- ✅ PDF downloads automatically
- ✅ PDF contains all simulation data:
  - Product information
  - Reactants, solvents, catalysts tables
  - All computed metrics (AE, PMI, E-factor, RME, CE, SF, water, energy, SI, CO2)
  - Mass balance breakdown
  - AI suggestions (if any)

### On Render.com Deployment:
The same fix applies. After pushing to Git and deploying:

1. Build logs should show:
   ```
   Chromium 130.0.6723.31 downloaded to /opt/render/.cache/ms-playwright/chromium-1140
   FFMPEG downloaded to /opt/render/.cache/ms-playwright/ffmpeg-1010
   ```

2. Test on deployed URL:
   - Navigate to `https://your-app.onrender.com/simulate`
   - Run simulation
   - Click "Generate PDF Report"
   - PDF should download

## Files Modified:
- `templates/sim.html` - Fixed data storage and PDF generation handler

## Key Points:
1. **Data Storage**: Now properly stores both input data and computed metrics
2. **PDF Generator**: Backend `pdf_generator.py` requires complete simulation data including:
   - Product details
   - Reactants list
   - Solvents list
   - Catalysts list
   - All computed metrics
   - Mass balance breakdown

3. **Browser Compatibility**: PDF generation uses Playwright which requires:
   - Chromium browser installed (locally or on server)
   - Proper async event loop (handled by `run_server.py` or `start_server.bat`)

## Troubleshooting:

### If PDF still doesn't download:
1. **Check browser console** (F12) for JavaScript errors
2. **Check network tab** (F12 → Network) to see if `/api/generate-pdf` request succeeds
3. **Check server logs** for PDF generation errors
4. **Verify Chromium is installed:**
   ```powershell
   python -m playwright install chromium
   ```

### Common Errors:
- **"Please run a simulation first"**: Click "Run Simulation" button before generating PDF
- **"Chromium browser not installed"**: Run `python -m playwright install chromium`
- **Timeout errors**: PDF generation taking too long (check server resources)

## Testing on Render:
After deployment, monitor logs:
```
[PDF] Generating: green_chem_report_<name>_<timestamp>.pdf
[PDF] Launching browser...
[PDF] ✅ Success: green_chem_report_<name>_<timestamp>.pdf
```

If you see these logs, PDF generation is working correctly on the server.
