# ValuationPro - Complete Analysis Guide

**Comprehensive guide for performing investment banking valuation analysis**

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [LBO Analysis](#lbo-analysis)
3. [DCF Analysis](#dcf-analysis)
4. [Data Preparation](#data-preparation)
5. [Model Comparison](#model-comparison)
6. [Advanced Analysis](#advanced-analysis)
7. [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

### Prerequisites

```bash
# Install dependencies
pip install openpyxl pandas xlsxwriter

# Verify installation
python3 -c "import openpyxl; import pandas; print('✅ Ready to go!')"
```

### 30-Second Analysis

Generate all models for a company in 30 seconds:

```bash
# Set Python path
export PYTHONPATH=/Users/samueldukmedjian/Desktop/valuation_pro

# Generate DCF model
python3 scripts/examples/example_dcf.py

# Generate LBO model
python3 scripts/examples/example_lbo.py
```

**Output:** 2 Excel files in `Examples/` folder ready for analysis
- `DCF_Model_AcmeTech.xlsx` - Complete DCF valuation model
- `LBO_Model_AcmeTech.xlsx` - Complete LBO analysis model

**Note:** All models are now single-sheet format for easier navigation and presentation.

---

## 📊 LBO Analysis

### What is an LBO?

A **Leveraged Buyout (LBO)** is a financial transaction where a company is acquired using a significant amount of borrowed money (leverage) to meet the cost of acquisition. The assets of the company being acquired are often used as collateral for the loans.

### Generate LBO Model

#### Multi-Sheet Model (Traditional Format)

```bash
PYTHONPATH=/Users/samueldukmedjian/Desktop/valuation_pro \
python3 scripts/examples/example_lbo_tool.py
```

**Output:** `Examples/LBO_Model_AcmeTech.xlsx`

**Sheets Generated:**
1. **Cover** - Title page with company info
2. **Transaction Summary** - Entry/exit valuation overview
3. **Sources & Uses** - Funding structure breakdown
4. **Assumptions** - All model inputs (debt structure, growth rates, etc.)
5. **Operating Model** - 5-year financial projections
6. **Debt Schedule** - Debt paydown and interest calculations
7. **Cash Flow Waterfall** - Cash flow distribution
8. **Returns Analysis** - IRR, MOIC, and returns metrics

#### Single-Sheet Model (Easier Navigation)

```bash
PYTHONPATH=/Users/samueldukmedjian/Desktop/valuation_pro \
python3 scripts/examples/example_lbo_single_sheet.py
```

**Output:** `Examples/LBO_Model_AcmeTech_SingleSheet.xlsx`

**All sections on ONE sheet** for easier scrolling and presentation.

### Key LBO Metrics

Open the generated Excel file and check:

**Entry Metrics:**
- Purchase Enterprise Value = LTM EBITDA × Entry Multiple
- Sources & Uses must balance (CHECK = $0)
- Sponsor Equity typically 40-60% of purchase price
- Total Debt typically 40-60% of purchase price

**Exit Metrics:**
- Exit Enterprise Value = Exit Year EBITDA × Exit Multiple
- IRR (Internal Rate of Return): Target 20-30% for PE deals
- MOIC (Multiple on Invested Capital): Target 2.0x-3.0x over 5 years

**Example Results (AcmeTech):**
```
Entry:
  Purchase EV: $5,636M (663 EBITDA × 8.5x)
  Sponsor Equity: $2,818M (50%)
  Total Debt: $2,818M (50%)

Exit (Year 5):
  Exit EBITDA: ~$1,100M
  Exit EV: ~$8,800M (8.0x multiple)
  IRR: ~22%
  MOIC: ~2.3x
```

### Customize LBO Assumptions

Edit the assumptions in the Python script or directly in Excel:

**Key Assumptions to Adjust:**

1. **Transaction Structure:**
   - `entry_multiple`: How many times EBITDA to pay (typically 7-12x)
   - `exit_multiple`: Expected exit multiple (typically 7-10x)
   - `holding_period`: Years to hold (typically 3-7 years)

2. **Debt Structure:**
   - `equity_contribution_pct`: Sponsor equity % (typically 40-60%)
   - `senior_debt_pct`: Senior debt % (typically 30-50%)
   - `subordinated_debt_pct`: Sub debt % (typically 5-15%)

3. **Operating Assumptions:**
   - `revenue_growth`: List of 5 growth rates [Y1, Y2, Y3, Y4, Y5]
   - `ebitda_margin`: Target EBITDA margin %
   - `capex_pct`: CapEx as % of revenue

**Example: Conservative Case**

```python
assumptions = {
    'entry_multiple': 9.0,      # Higher entry multiple
    'exit_multiple': 7.5,       # Lower exit multiple
    'revenue_growth': [0.05, 0.05, 0.04, 0.04, 0.03],  # Slower growth
    'ebitda_margin': 0.30,      # Lower margin
    # ... other assumptions
}
```

### LBO Analysis Checklist

- [ ] Sources & Uses balances (CHECK = $0)
- [ ] Debt/EBITDA ratio is reasonable (typically <6x)
- [ ] Interest coverage is healthy (EBITDA / Interest > 2x)
- [ ] IRR exceeds PE fund hurdle rate (typically 20%+)
- [ ] MOIC meets target (typically 2.0x+ over 5 years)
- [ ] Exit assumptions are realistic
- [ ] Debt paydown schedule is achievable

---

## 💰 DCF Analysis

### What is DCF?

**Discounted Cash Flow (DCF)** analysis values a company based on the present value of its projected future cash flows. It's an intrinsic valuation method that doesn't rely on market comparables.

### Generate DCF Model

#### Multi-Sheet Model (Traditional Format)

```bash
PYTHONPATH=/Users/samueldukmedjian/Desktop/valuation_pro \
python3 scripts/examples/example_dcf_tool.py
```

**Output:** `Examples/DCF_Model_AcmeTech.xlsx`

**Sheets Generated:**
1. **Cover** - Title page with valuation summary
2. **Assumptions** - WACC, growth rates, margins
3. **Historical Data** - 5 years of historical financials
4. **Projections** - 5-year financial projections
5. **DCF Valuation** - Present value calculations
6. **Sensitivity** - Sensitivity tables for WACC and growth

#### Single-Sheet Model (Easier Navigation)

```bash
PYTHONPATH=/Users/samueldukmedjian/Desktop/valuation_pro \
python3 scripts/examples/example_dcf_single_sheet.py
```

**Output:** `Examples/DCF_Model_AcmeTech_SingleSheet.xlsx`

### Key DCF Metrics

Open the generated Excel file and check:

**Valuation Output:**
- Enterprise Value = PV of projected FCF + PV of Terminal Value
- Equity Value = Enterprise Value - Net Debt
- Implied Price per Share = Equity Value / Shares Outstanding

**Example Results (AcmeTech):**
```
DCF Valuation:
  PV of FCF (Years 1-5): $XXX M
  PV of Terminal Value: $XXX M
  Enterprise Value: $XXX M
  Less: Net Debt: $0 M
  Equity Value: $XXX M
  Shares Outstanding: 100 M
  Implied Price per Share: $XX.XX
```

### Customize DCF Assumptions

**Critical Assumptions:**

1. **Discount Rate (WACC):**
   - `wacc`: Weighted Average Cost of Capital (typically 8-12%)
   - Higher WACC = Lower valuation
   - Lower WACC = Higher valuation

2. **Terminal Growth Rate:**
   - `terminal_growth_rate`: Long-term growth (typically 2-3%)
   - Should not exceed GDP growth
   - Very sensitive input!

3. **Projection Assumptions:**
   - `revenue_growth_rates`: 5-year growth rates
   - `ebitda_margin`: Operating margin
   - `capex_pct_revenue`: CapEx intensity
   - `nwc_pct_revenue`: Working capital needs

**Example: Base, Bull, Bear Cases**

```python
# BASE CASE
assumptions_base = {
    'wacc': 0.09,
    'terminal_growth_rate': 0.025,
    'revenue_growth_rates': [0.10, 0.10, 0.08, 0.08, 0.06],
}

# BULL CASE (optimistic)
assumptions_bull = {
    'wacc': 0.08,               # Lower discount rate
    'terminal_growth_rate': 0.03,  # Higher terminal growth
    'revenue_growth_rates': [0.15, 0.15, 0.12, 0.10, 0.08],  # Faster growth
}

# BEAR CASE (conservative)
assumptions_bear = {
    'wacc': 0.11,               # Higher discount rate
    'terminal_growth_rate': 0.02,  # Lower terminal growth
    'revenue_growth_rates': [0.05, 0.05, 0.04, 0.04, 0.03],  # Slower growth
}
```

### DCF Sensitivity Analysis

The DCF model includes sensitivity tables showing how valuation changes with:

1. **WACC vs Terminal Growth Rate**
   - Shows range of values across different discount rates
   - Helps understand valuation range

2. **Revenue Growth vs EBITDA Margin**
   - Shows operational sensitivity
   - Identifies key value drivers

**To Use Sensitivity Tables:**
1. Open Excel file
2. Navigate to Sensitivity sheet (multi-sheet) or scroll to sensitivity section (single-sheet)
3. Review valuation range across different scenarios
4. Identify which assumptions drive most value

### DCF Analysis Checklist

- [ ] WACC is reasonable for industry and company risk
- [ ] Terminal growth rate ≤ GDP growth
- [ ] Revenue growth rates are defensible
- [ ] EBITDA margins are achievable
- [ ] CapEx and NWC assumptions are realistic
- [ ] Valuation is in reasonable range vs peers
- [ ] Sensitivity analysis shows acceptable range

---

## 📁 Data Preparation

### Using Comprehensive Data Source

The tool uses `Base_datasource/Financial_Model_Data_Source.xlsx` as the data source.

**Data Structure Required:**

```
Sheet: Income Statement
- Years (row 1): 2021, 2022, 2023, 2024, 2025
- Revenue (row 2): Historical revenue values
- EBITDA (row 3): Historical EBITDA values
- ... other income statement items

Sheet: Balance Sheet
- Total Assets
- Total Liabilities
- Shareholders' Equity

Sheet: Cash Flow
- Operating Cash Flow
- CapEx
- Free Cash Flow

Sheet: Market Data
- Shares Outstanding
- Share Price
- Market Cap
```

### Verify Data Extraction

Test that data is being read correctly:

```bash
PYTHONPATH=/Users/samueldukmedjian/Desktop/valuation_pro \
python3 -c "
from src.data.comprehensive_extractor import ComprehensiveDataExtractor

with ComprehensiveDataExtractor() as extractor:
    ltm = extractor.get_ltm_metrics()
    print(f'LTM Revenue: \${ltm[\"revenue\"]:,.0f}M')
    print(f'LTM EBITDA: \${ltm[\"ebitda\"]:,.0f}M')
    print(f'Net Debt: \${ltm[\"net_debt\"]:,.0f}M')
"
```

Expected output:
```
LTM Revenue: $1,950M
LTM EBITDA: $663M
Net Debt: $0M
```

### Custom Data Source

To use your own data:

1. **Update the Excel file:** `Base_datasource/Financial_Model_Data_Source.xlsx`
2. **Match the structure:** Keep same sheet names and row/column layout
3. **Run validation:** Check data extracts correctly (see above)
4. **Regenerate models:** Run the example scripts

---

## ⚖️ Model Comparison

### Multi-Sheet vs Single-Sheet

**Multi-Sheet Models:**
✅ Traditional IB format
✅ Separated sections for clarity
✅ Professional presentation
❌ Requires clicking between sheets

**Single-Sheet Models:**
✅ All data in one place
✅ Easy to scroll through
✅ Better for quick review
✅ Easier to print
❌ Can be long

**Recommendation:** Generate both and use based on audience:
- **Multi-sheet**: Client presentations, detailed reviews
- **Single-sheet**: Internal analysis, quick reference

### LBO vs DCF - When to Use

**Use LBO When:**
- Analyzing PE-backed transaction
- Evaluating leveraged transaction
- Need to understand returns to equity investors
- Debt structure is key to value creation

**Use DCF When:**
- Performing intrinsic valuation
- Equity value for public company
- Need standalone business value
- Cash flow generation is key value driver

**Best Practice:** Use both methods and triangulate to a valuation range!

---

## 🔬 Advanced Analysis

### 1. Scenario Analysis

Generate multiple models with different assumptions:

```bash
# Base Case
python3 scripts/examples/example_lbo_tool.py

# Edit assumptions in script for Bull/Bear
# Then run again with modified assumptions
```

### 2. Sensitivity Analysis

Already built into DCF models! Check the Sensitivity sheet for:
- WACC sensitivity
- Terminal growth sensitivity
- Operating leverage sensitivity

### 3. Comparison Analysis

Compare valuations across methods:

```python
# After generating LBO and DCF models:
lbo_implied_value = 8800  # Exit EV from LBO model
dcf_enterprise_value = 900  # From DCF model

# Compare methodologies
print(f"LBO Implied Exit Value: ${lbo_implied_value}M")
print(f"DCF Enterprise Value: ${dcf_enterprise_value}M")
```

### 4. Custom Python Analysis

Use the extracted data directly in Python:

```python
from src.data.comprehensive_extractor import ComprehensiveDataExtractor
import pandas as pd

with ComprehensiveDataExtractor() as extractor:
    historical = extractor.get_historical_data(years=5)

    # Create custom analysis
    df = pd.DataFrame({
        'Year': historical['years'],
        'Revenue': historical['income_statement']['revenue'],
        'EBITDA': historical['income_statement']['ebitda']
    })

    # Calculate EBITDA margin trend
    df['EBITDA_Margin'] = df['EBITDA'] / df['Revenue']

    print(df)
    print(f"\nAverage EBITDA Margin: {df['EBITDA_Margin'].mean():.1%}")
```

---

## 🔧 Troubleshooting

### Issue: Import Errors

```bash
# Error: ModuleNotFoundError: No module named 'src'

# Solution: Set PYTHONPATH
export PYTHONPATH=/Users/samueldukmedjian/Desktop/valuation_pro
# Then run your script
```

### Issue: Data Not Loading

```bash
# Error: FileNotFoundError: Financial_Model_Data_Source.xlsx

# Solution: Verify file exists
ls -la Base_datasource/Financial_Model_Data_Source.xlsx

# Check current directory
pwd  # Should be /Users/samueldukmedjian/Desktop/valuation_pro
```

### Issue: Formulas Show #REF! in Excel

**Problem:** Cell references are broken

**Solution:**
1. Check that all bug fixes have been applied
2. Regenerate models with latest code
3. Verify using verification scripts:

```bash
python3 scripts/validation/final_verification.py
python3 scripts/validation/verify_new_bugs.py
```

### Issue: Values Don't Calculate

**Problem:** Formulas exist but values show as None or 0

**Solution:**
- Open the Excel file in Microsoft Excel or Excel for Mac
- Excel will automatically calculate formulas
- openpyxl creates formulas but doesn't calculate them

### Issue: Unexpected Results

**Debugging Checklist:**
- [ ] Data source file has correct values
- [ ] Assumptions are realistic
- [ ] All formulas reference correct cells
- [ ] Sources & Uses balances (LBO)
- [ ] Discount factors calculate correctly (DCF)

---

## 📚 Command Reference

### Essential Commands

```bash
# Set environment
export PYTHONPATH=/Users/samueldukmedjian/Desktop/valuation_pro

# Generate all models
python3 scripts/examples/example_lbo_tool.py
python3 scripts/examples/example_dcf_tool.py
python3 scripts/examples/example_lbo_single_sheet.py
python3 scripts/examples/example_dcf_single_sheet.py

# Verify models
python3 scripts/validation/final_verification.py
python3 scripts/validation/verify_new_bugs.py

# Test data extraction
python3 -c "from src.data.comprehensive_extractor import ComprehensiveDataExtractor; \
  e = ComprehensiveDataExtractor(); \
  ltm = e.get_ltm_metrics(); \
  print(ltm)"
```

### Verification Commands

```bash
# Verify Round 1 bug fixes
python3 scripts/validation/final_verification.py

# Verify Round 2 bug fixes
python3 scripts/validation/verify_new_bugs.py

# Check LBO formulas
python3 scripts/validation/verify_calculations.py
```

### Git Commands

```bash
# View commit history
git log --oneline -10

# Check current status
git status

# View all bug fix documentation
ls -la Guidelines/BUG_FIX*.md
```

---

## 🎯 Workflow Examples

### Example 1: Full Company Valuation

```bash
# 1. Update data source
# Edit Base_datasource/Financial_Model_Data_Source.xlsx with company data

# 2. Set environment
export PYTHONPATH=/Users/samueldukmedjian/Desktop/valuation_pro

# 3. Generate all models
python3 scripts/examples/example_lbo_tool.py
python3 scripts/examples/example_lbo_single_sheet.py
python3 scripts/examples/example_dcf_tool.py
python3 scripts/examples/example_dcf_single_sheet.py

# 4. Open models in Excel
open Examples/LBO_Model_AcmeTech.xlsx
open Examples/DCF_Model_AcmeTech.xlsx

# 5. Review and analyze
# - Check LBO IRR and MOIC
# - Check DCF implied price
# - Compare methodologies
# - Adjust assumptions as needed
```

### Example 2: Scenario Analysis

```python
# Edit scripts/examples/example_lbo_tool.py

# Add multiple scenarios
scenarios = {
    'base': {'revenue_growth': [0.10, 0.10, 0.08, 0.08, 0.06], 'exit_multiple': 8.0},
    'bull': {'revenue_growth': [0.15, 0.15, 0.12, 0.10, 0.08], 'exit_multiple': 9.0},
    'bear': {'revenue_growth': [0.05, 0.05, 0.04, 0.04, 0.03], 'exit_multiple': 7.0},
}

for name, scenario_assumptions in scenarios.items():
    # Update assumptions with scenario
    assumptions.update(scenario_assumptions)

    # Generate model
    lbo.generate_lbo_model(
        transaction_data=transaction_data,
        assumptions=assumptions,
        output_file=f'Examples/LBO_Model_AcmeTech_{name.upper()}.xlsx'
    )
```

Then run:
```bash
python3 scripts/examples/example_lbo_tool.py
# Generates 3 models: BASE, BULL, BEAR
```

---

## 📖 Additional Resources

### Documentation

- [BUG_FIX_SUMMARY.md](Guidelines/BUG_FIX_SUMMARY.md) - Round 1 bug fixes
- [BUG_FIX_ROUND_2.md](Guidelines/BUG_FIX_ROUND_2.md) - Round 2 bug fixes
- [VALUATION_PRO_BUG_ANALYSIS.md](Guidelines/VALUATION_PRO_BUG_ANALYSIS.md) - Original bug analysis

### Example Files

All generated examples are in the `Examples/` folder:
- `LBO_Model_AcmeTech.xlsx` - Multi-sheet LBO
- `LBO_Model_AcmeTech_SingleSheet.xlsx` - Single-sheet LBO
- `DCF_Model_AcmeTech.xlsx` - Multi-sheet DCF
- `DCF_Model_AcmeTech_SingleSheet.xlsx` - Single-sheet DCF

### Reference Models

Professional IB model examples in `Ref_models/` folder (if available).

---

## 💡 Tips & Best Practices

### Valuation Tips

1. **Always use multiple methods** - LBO, DCF, and Comparables
2. **Triangulate to a range** - No single "right" answer
3. **Test sensitivities** - Understand what drives value
4. **Be conservative** - Better to underestimate than overestimate
5. **Sanity check** - Does the valuation make business sense?

### Model Tips

1. **Use single-sheet for quick analysis** - Easier to navigate
2. **Use multi-sheet for presentations** - More professional
3. **Always verify formulas** - Run verification scripts
4. **Document assumptions** - Keep notes on why you chose values
5. **Save scenarios** - Generate Base/Bull/Bear cases

### Excel Tips

1. **Format cells** - Use currency, percentage, and number formats
2. **Add comments** - Document complex formulas
3. **Use named ranges** - Makes formulas easier to read
4. **Freeze panes** - Lock headers when scrolling
5. **Print preview** - Ensure model prints well

---

## 🆘 Getting Help

### Check Verification

```bash
# Run all verification scripts
python3 scripts/validation/final_verification.py
python3 scripts/validation/verify_new_bugs.py
```

### Debug Mode

Add print statements to see what's happening:

```python
# In any Python script
print(f"Transaction Data: {transaction_data}")
print(f"Assumptions: {assumptions}")
```

### Common Issues

1. **PYTHONPATH not set** → Models don't import
2. **Wrong directory** → Files not found
3. **Excel doesn't calculate** → Open in Excel, not preview
4. **Formulas show #REF!** → Regenerate model with fixes

---

## ✅ Quick Checklist

Before presenting models:

**Technical Checks:**
- [ ] All formulas calculate (no #REF!, #DIV/0!, #VALUE! errors)
- [ ] Sources & Uses balance (LBO)
- [ ] Present values sum correctly (DCF)
- [ ] Verification scripts pass

**Business Checks:**
- [ ] Assumptions are defensible
- [ ] Growth rates are reasonable
- [ ] Margins are achievable
- [ ] Exit multiples are realistic
- [ ] Valuation is in sensible range

**Presentation Checks:**
- [ ] Numbers are formatted (currency, %, etc.)
- [ ] Headers are clear
- [ ] Model prints cleanly
- [ ] Key outputs are highlighted

---

## 🎓 Conclusion

You now have everything needed to perform professional investment banking valuations:

✅ LBO models (multi-sheet & single-sheet)
✅ DCF models (multi-sheet & single-sheet)
✅ Data extraction tools
✅ Verification scripts
✅ This comprehensive guide

**Next Steps:**
1. Generate example models with AcmeTech data
2. Review the Excel files
3. Customize assumptions for your analysis
4. Generate multiple scenarios
5. Compare results and triangulate valuation

**Happy analyzing! 📊**

---

*Last Updated: October 24, 2025*
*Version: 2.0 (includes single-sheet models)*
