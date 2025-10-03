# PDF Report Generation for Green Toolkit

## Overview

This feature allows users to generate professional PDF reports from their green chemistry simulation results using Playwright for high-quality HTML-to-PDF rendering.

## Features

✅ **Professional Formatting**: Clean, well-organized layout with color-coded metrics
✅ **Comprehensive Data**: Includes all simulation inputs, metrics, and AI suggestions
✅ **Visual Indicators**: Color-coded performance indicators (green/yellow/red)
✅ **Interpretation Guide**: Built-in metrics interpretation for easy understanding
✅ **Mass Balance**: Detailed breakdown of all inputs and outputs
✅ **Auto-naming**: Intelligent filename generation based on reaction name and timestamp

## Installation

### 1. Install Playwright
```bash
pip install playwright
```

### 2. Install Chromium Browser
```bash
python -m playwright install chromium
```

### 3. Verify Installation
```bash
python test_pdf.py
```

This will generate a test PDF (`test_aspirin_report.pdf`) with sample data.

## Usage

### From the Web Interface

1. **Run a Simulation**: Enter your reaction data and click "Run Simulation"
2. **Generate PDF**: Click the "Generate PDF Report" button (visible after simulation)
3. **Download**: The PDF will automatically download to your browser's default location

### From the API

**Endpoint**: `POST /api/generate-pdf`

**Request Body**:
```json
{
  "reaction_name": "Synthesis of Aspirin",
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
    }
  ],
  "solvents": [...],
  "catalysts": [...],
  "atom_economy_pct": 85.5,
  "pmi": 15.88,
  "e_factor": 14.88,
  ...
}
```

**Response**: PDF file (application/pdf)

### Programmatically

```python
from pdf_generator import generate_simulation_pdf

data = {
    "reaction_name": "My Reaction",
    "product": {...},
    "reactants": [...],
    "atom_economy_pct": 85.0,
    ...
}

pdf_path = generate_simulation_pdf(data, "my_report.pdf")
print(f"PDF saved to: {pdf_path}")
```

## Report Structure

The generated PDF includes:

### 1. Header
- Reaction name
- Generation timestamp
- Green Toolkit branding

### 2. Product Information
- Name, molecular weight, mass, carbon atoms
- Highlighted in green box

### 3. Key Metrics Grid
- **Atom Economy** (AE)
- **Process Mass Intensity** (PMI)
- **E-Factor**
- **Reaction Mass Efficiency** (RME)
- **Carbon Efficiency** (CE)
- **Stoichiometric Factor** (SF)
- **Water Intensity**
- **Energy per gram**
- **Solvent Intensity**
- **Carbon Footprint**

### 4. Interpretation Guide
- Thresholds for each metric (excellent/good/needs improvement)
- Industry benchmarks

### 5. Data Tables
- **Reactants**: Name, MW, mass, carbon atoms, equivalents
- **Solvents**: Name, mass, recovery percentage
- **Catalysts**: Name, MW, mass

### 6. Mass Balance
- Complete breakdown of inputs and outputs
- Total masses highlighted

### 7. AI Recommendations
- Context-aware suggestions for improvement
- Best practices for green chemistry

## Customization

### Custom Output Path
```python
pdf_path = generate_simulation_pdf(data, output_path="/path/to/custom_report.pdf")
```

### Auto-generated Filename Format
```
green_chem_report_{reaction_name}_{timestamp}.pdf
```
Example: `green_chem_report_Synthesis_of_Aspirin_20250103_143025.pdf`

## Metric Color Coding

### Green (Excellent)
- **AE/RME/CE**: ≥80%
- **PMI**: <5
- **E-Factor**: <1

### Yellow (Good)
- **AE/RME/CE**: 60-79%
- **PMI**: 5-10
- **E-Factor**: 1-5

### Red (Needs Improvement)
- **AE/RME/CE**: <60%
- **PMI**: >10
- **E-Factor**: >5

## Technical Details

### PDF Settings
- **Format**: A4
- **Margins**: Top/Bottom 20mm, Left/Right 15mm
- **Background**: Printed (preserves colors)
- **Orientation**: Portrait

### Browser Engine
- **Chromium** (via Playwright)
- Headless rendering for fast generation
- Full CSS3 and HTML5 support

## Troubleshooting

### "Playwright not found"
```bash
pip install playwright
python -m playwright install chromium
```

### "Browser executable not found"
```bash
# Reinstall browsers
python -m playwright install --force chromium
```

### PDF generation fails
1. Check that `playwright` package is installed
2. Ensure Chromium browser is installed
3. Verify write permissions in output directory
4. Check logs for detailed error messages

### Large file size
- PDFs are typically 50-200 KB depending on content
- If larger, consider reducing embedded images (future feature)

## Performance

- **Generation Time**: ~2-5 seconds per report
- **File Size**: Typically 50-150 KB
- **Concurrent Requests**: Supports multiple simultaneous generations

## Future Enhancements

🔮 **Planned Features**:
- [ ] Chart/graph embedding in PDF
- [ ] Custom branding/logo support
- [ ] Multiple report templates
- [ ] Batch PDF generation
- [ ] Email delivery option
- [ ] Comparison reports (multiple reactions)

## Dependencies

- `playwright>=1.55.0` - Browser automation and PDF rendering
- `fastapi>=0.117.0` - Web framework
- `pydantic>=2.11.0` - Data validation

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review test_pdf.py for working examples
3. Check Playwright documentation: https://playwright.dev/python/

## License

Part of the Green Toolkit project. See main project LICENSE.

---

**Built with ❤️ for sustainable chemistry**
