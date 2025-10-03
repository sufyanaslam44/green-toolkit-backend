# 🚀 Quick Start: PDF Report Generation

## Installation (One-Time Setup)

```bash
# 1. Install Playwright browsers (if not already done)
python -m playwright install chromium

# 2. Verify installation
python test_pdf.py
```

Expected output:
```
✓ PDF generated successfully: test_aspirin_report.pdf
```

## Usage

### Option 1: Web Interface (Easiest)

1. **Start the server**:
   ```bash
   uvicorn main:app --reload
   ```

2. **Open browser**: http://localhost:8000/simulate

3. **Run simulation**:
   - Click "Load Example" OR enter your own data
   - Click "Run Simulation"
   - Wait for metrics to appear

4. **Generate PDF**:
   - Click "Generate PDF Report" button
   - PDF downloads automatically
   - Open and review!

### Option 2: API Call

```bash
curl -X POST http://localhost:8000/api/generate-pdf \
  -H "Content-Type: application/json" \
  -d @payload.json \
  --output report.pdf
```

### Option 3: Python Script

```python
from pdf_generator import generate_simulation_pdf

data = {
    "reaction_name": "My Reaction",
    "product": {"name": "Product", "mw": 180, "actual_mass_g": 10, "carbon_atoms": 9},
    "reactants": [{"name": "Reactant", "mw": 100, "mass_g": 8, "carbon_atoms": 5, "eq_used": 1, "eq_stoich": 1}],
    "solvents": [],
    "catalysts": [],
    "atom_economy_pct": 85.5,
    "pmi": 12.3,
    "e_factor": 11.3,
    "breakdown": {}
}

pdf_path = generate_simulation_pdf(data)
print(f"PDF saved: {pdf_path}")
```

## What You'll Get

A professional PDF report with:
- ✅ All your simulation data
- ✅ Color-coded metrics (green/yellow/red)
- ✅ Complete data tables
- ✅ Mass balance
- ✅ AI suggestions
- ✅ Interpretation guide

## Troubleshooting

### Problem: "Playwright not installed"
```bash
pip install playwright
python -m playwright install chromium
```

### Problem: "Permission denied"
- Check you have write permissions in the directory
- Try specifying a different output path

### Problem: "Module not found"
```bash
# Make sure you're in the right directory
cd "d:\Webtool\VS project\green-toolkit-backend\green-toolkit-backend"
python test_pdf.py
```

## Tips

1. **Always run simulation first** before generating PDF to ensure fresh data
2. **Check the console** for any error messages
3. **File naming**: PDFs auto-name based on reaction name + timestamp
4. **Location**: PDFs save to current working directory (or browser downloads)

## Sample Output

See `test_aspirin_report.pdf` for an example of what your reports will look like!

## Need Help?

- Check `PDF_README.md` for detailed documentation
- Review `test_pdf.py` for working code examples
- See `IMPLEMENTATION_SUMMARY.md` for technical details

---

**Ready to go!** Your PDF generation feature is working. Start the server and try it out! 🎉
