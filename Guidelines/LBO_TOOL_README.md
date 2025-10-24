# LBO Tool - Pixel-Perfect LBO Model Generator

## Overview

The **LBO Tool** is a focused, single-purpose tool that generates investment banking-quality Leveraged Buyout (LBO) models in Excel. Every calculation uses **Excel formulas** (no hardcoded values), ensuring the model is fully editable and audit-friendly.

## Features

✅ **8 Professional Sheets**:
- Cover Sheet with transaction overview
- Transaction Summary with entry/exit valuations
- Sources & Uses of Funds
- Assumptions (transaction, debt, operating)
- Operating Model (5-year projections)
- Debt Schedule with amortization
- Cash Flow Waterfall
- Returns Analysis (IRR & MOIC)

✅ **Investment Banking Standards**:
- Proper table borders throughout
- Dark blue section headers (4472C4) with white text
- Light yellow input cells (FFF2CC) for easy identification
- All values formatted with proper number formats ($M, %, etc.)

✅ **100% Formula-Driven**:
- No hardcoded Python values
- All calculations use Excel formulas
- Cross-sheet references for linked data
- Fully editable in Excel

## Installation

```bash
# Install required dependencies
pip install openpyxl pandas
```

## Quick Start

```python
from src.tools.lbo_tool import LBOTool

# Initialize the LBO tool
lbo_tool = LBOTool(
    company_name="Target Company Inc.",
    sponsor="Private Equity Firm"
)

# Define transaction data
transaction_data = {
    'ltm_revenue': 180000,      # LTM Revenue ($M)
    'ltm_ebitda': 52000,        # LTM EBITDA ($M)
    'entry_multiple': 10.0,     # Entry multiple (x)
    'exit_multiple': 11.0,      # Exit multiple (x)
    'transaction_date': '2024-01-01',
    'holding_period': 5,        # Years
}

# Define LBO assumptions
assumptions = {
    # Transaction fees
    'transaction_fees_pct': 0.02,        # 2%
    'financing_fees_pct': 0.03,          # 3%

    # Sources of funds
    'senior_debt_pct': 0.40,             # 40%
    'subordinated_debt_pct': 0.10,       # 10%
    'equity_contribution_pct': 0.50,     # 50%

    # Debt terms
    'senior_debt_rate': 0.055,           # 5.5%
    'sub_debt_rate': 0.095,              # 9.5%
    'senior_amortization_pct': 0.05,     # 5% annual

    # Operating assumptions (5-year projections)
    'revenue_growth': [0.06, 0.06, 0.05, 0.05, 0.04],
    'ebitda_margin': 0.29,               # 29%
    'depreciation_pct_revenue': 0.02,    # 2%
    'capex_pct_revenue': 0.025,          # 2.5%
    'nwc_pct_revenue': 0.10,             # 10%
    'tax_rate': 0.21,                    # 21%
}

# Generate the LBO model
lbo_tool.generate_lbo_model(
    transaction_data=transaction_data,
    assumptions=assumptions,
    output_file="LBO_Model.xlsx"
)
```

## Using with Excel Data Extractor

You can extract historical financial data from Excel files using the `FinancialStatementExtractor`:

```python
from src.data.excel_extractor import FinancialStatementExtractor

# Extract data from Excel files
extractor = FinancialStatementExtractor()
is_data = extractor.extract_income_statement('income-statement.xlsx')
bs_data = extractor.extract_balance_sheet('balance-sheet.xlsx')

# Use extracted data for LTM metrics
ltm_revenue = is_data['revenue']['Total Revenues'][-1]
ltm_ebitda = 52000  # Calculate from extracted data

transaction_data = {
    'ltm_revenue': ltm_revenue,
    'ltm_ebitda': ltm_ebitda,
    # ... rest of transaction data
}
```

## Model Structure

### 1. Cover Sheet
Professional cover page with:
- Company name and sponsor
- Transaction date
- Model reference links to all other sheets

### 2. Transaction Summary
Entry and exit valuations:
- **Entry**: LTM EBITDA × Entry Multiple = Purchase EV
- **Exit**: Projected EBITDA × Exit Multiple = Exit EV
- Links to other sheets for detailed calculations

### 3. Sources & Uses of Funds
Classic S&U table showing:
- **Uses**: Purchase EV, Transaction Fees, Financing Fees
- **Sources**: Senior Debt, Subordinated Debt, Equity Contribution
- Automatic balancing check

### 4. Assumptions Sheet
All model inputs in one place:
- Transaction assumptions (multiples, fees)
- Debt structure and terms
- Operating assumptions (margins, growth rates)
- **Yellow cells** = editable inputs

### 5. Operating Model
5-year financial projections:
- Revenue (with custom growth rates per year)
- EBITDA (based on margin assumption)
- D&A (% of revenue)
- EBIT = EBITDA - D&A
- Taxes
- Net Income
- CapEx and NWC changes
- Unlevered Free Cash Flow

### 6. Debt Schedule
Debt tracking over holding period:
- Beginning balance
- Mandatory amortization (% of original balance)
- Optional prepayments (from excess cash flow)
- Interest expense (average balance method)
- Ending balance

### 7. Cash Flow Waterfall
Distribution waterfall showing:
- Operating cash flow
- Debt service (interest + amortization)
- CapEx and NWC requirements
- Excess cash flow available for prepayments

### 8. Returns Analysis
Key return metrics:
- **IRR**: (Exit Equity Value / Initial Equity)^(1/Years) - 1
- **MOIC**: Exit Equity Value / Initial Equity
- Cash-on-cash multiples

## Formula Examples

All calculations use Excel formulas for transparency and editability:

```excel
# Purchase Enterprise Value
=B5*B6  (LTM EBITDA × Entry Multiple)

# Total Uses
=SUM(B10:B12)

# Revenue Year 1
=B4*(1+Assumptions!B29)  (Prior year × growth rate)

# EBITDA
=C4*Assumptions!$B$33  (Revenue × margin)

# Interest Expense
=(B9+C9)/2*Assumptions!$B$15  (Avg balance × rate)

# IRR
=(B9/B12)^(1/B13)-1  ((Exit/Entry)^(1/Years) - 1)

# MOIC
=B9/B12  (Exit Equity / Initial Equity)
```

## Color Coding

The model uses professional investment banking color standards:

| Element | Color | Hex Code | Meaning |
|---------|-------|----------|---------|
| Section Headers | Dark Blue | #4472C4 | Section titles (white text) |
| Input Cells | Light Yellow | #FFF2CC | User-editable assumptions |
| Calculated Cells | White | #FFFFFF | Formula-driven outputs |
| Table Borders | Black | #000000 | Thin borders around all tables |

## Validation

Run the validation script to verify formulas:

```bash
python validate_lbo.py
```

This checks that:
- All 8 sheets are present
- Key calculations use formulas (not values)
- Cross-sheet references work correctly
- Returns metrics calculate properly

## Example Output

Running `example_lbo_tool.py` generates a complete LBO model with:

```
Entry Valuation:
  LTM EBITDA:        $52.0M
  Entry Multiple:    10.0x
  Purchase EV:       $520.0M

Financing:
  Senior Debt (40%): $208.0M @ 5.5%
  Sub Debt (10%):    $52.0M @ 9.5%
  Equity (50%):      $260.0M

Exit Valuation (Year 5):
  Projected EBITDA:  ~$67.0M
  Exit Multiple:     11.0x
  Exit EV:           ~$737.0M

Returns:
  IRR:               ~22%
  MOIC:              ~2.3x
```

## Technical Details

### Dependencies
- `openpyxl`: Excel file creation and manipulation
- `pandas`: Data handling (optional, for extractor)

### File Structure
```
src/
  tools/
    lbo_tool.py          # Main LBO model generator
  data/
    excel_extractor.py   # Financial data extraction

example_lbo_tool.py      # Usage example
validate_lbo.py          # Formula validation
```

### Key Methods

**LBOTool Class**:
- `__init__(company_name, sponsor)`: Initialize with company details
- `generate_lbo_model(transaction_data, assumptions, output_file)`: Main generation method
- `_create_cover_sheet()`: Cover page
- `_create_transaction_summary()`: Entry/exit valuations
- `_create_sources_uses()`: S&U table
- `_create_assumptions_sheet()`: All inputs
- `_create_operating_model()`: Financial projections
- `_create_debt_schedule()`: Debt tracking
- `_create_cash_flow_waterfall()`: CF distribution
- `_create_returns_analysis()`: IRR & MOIC

### Formula Generation Pattern

All values are written as formula strings:

```python
# WRONG: Hardcoded value
ws.cell(row=5, column=2).value = 520000

# CORRECT: Formula
ws.cell(row=5, column=2).value = "=B3*B4"  # EBITDA × Multiple
```

This ensures the Excel model remains:
- **Auditable**: Users can see all calculation logic
- **Flexible**: Change inputs and model updates automatically
- **Professional**: Matches IB standards

## Comparison to Old Generator

| Feature | Old Multi-Purpose Tool | New LBO Tool |
|---------|----------------------|--------------|
| Lines of Code | 2,056 | 850 |
| Focus | All valuations | LBO only |
| Formulas | Mixed | 100% formulas |
| Table Borders | Partial | Complete |
| Color Scheme | Gray/Blue | Dark Blue/Yellow |
| Maintainability | Complex | Simple |

## Best Practices

1. **Always use the extractor for historical data** when available
2. **Review assumptions sheet** before running scenarios
3. **Check Sources & Uses balancing** to ensure proper financing
4. **Validate debt schedule** to confirm amortization works correctly
5. **Review returns analysis** for reasonableness (20-25% IRR typical for PE)

## Troubleshooting

**Issue**: Model shows #REF! errors
- **Cause**: Sheet references broken
- **Fix**: Ensure all sheet names match exactly (case-sensitive)

**Issue**: Debt balance doesn't amortize correctly
- **Cause**: Amortization percentage too high
- **Fix**: Reduce `senior_amortization_pct` to 5% or lower

**Issue**: Returns seem unrealistic
- **Cause**: Exit multiple or EBITDA growth too aggressive
- **Fix**: Use realistic multiples (10-12x) and margins (25-30%)

## Future Enhancements

Potential additions:
- Multiple debt tranches (1st lien, 2nd lien, mezz)
- Revolver with borrowing base
- Management rollover equity
- Dividend recaps during hold period
- Sensitivity tables for IRR/MOIC
- Transaction comparables analysis

## Support

For issues or questions:
1. Check that all required files are present
2. Verify openpyxl is installed correctly
3. Run validation script to check formulas
4. Review example script for proper usage

## License

Internal use only - Investment Banking Valuation Platform
