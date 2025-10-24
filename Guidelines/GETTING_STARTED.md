# Getting Started with ValuationPro

## Quick Start Guide

### 1. Installation

```bash
# Clone or navigate to the project directory
cd valuation_pro

# Install dependencies
pip install -r requirements.txt

# For development (includes testing tools)
pip install -e ".[dev]"
```

### 2. Run Your First DCF Valuation

The easiest way to get started is to run the example script:

```bash
python example_dcf.py
```

This will:
- Fetch Apple (AAPL) financial data
- Calculate WACC automatically
- Run a complete DCF valuation
- Generate an Excel file: `AAPL_DCF_Valuation.xlsx`

### 3. Understanding the Output

The example script will show you:

```
==================================================================================
ValuationPro - DCF Valuation Example
Company: Apple Inc. (AAPL)
==================================================================================

Step 1: Fetching financial data from yfinance...
  ✓ Financial data fetched successfully
  Current Price: $175.0
  Market Cap: $2700.0B

Step 2: Calculating WACC...
  WACC: 8.50%
  Cost of Equity: 11.20%
  Cost of Debt: 3.95%
  Risk-free Rate: 4.00%
  Beta: 1.20

... [continues with valuation]

VALUATION SUMMARY
==================================================================================
Target Price: $185.50
Rating: BUY (Upside: 6.0%)
==================================================================================
```

## Core Components

### 1. WACC Calculator

Calculate weighted average cost of capital with live market data:

```python
from src.models.wacc import WACCCalculator

wacc = WACCCalculator(
    ticker="AAPL",
    debt=100000,      # $100B in millions
    equity=2500000,   # $2.5T in millions
    tax_rate=0.21     # 21% corporate tax
)

results = wacc.calculate_wacc()
print(f"WACC: {results['wacc']:.2%}")
```

### 2. DCF Model

Run a complete discounted cash flow valuation:

```python
from src.models.dcf import DCFModel

# Historical data
company_data = {
    'revenue': [394328, 383285, 365817],  # Last 3 years in millions
    'ebit': [119437, 114301, 108949],
    'tax_rate': 0.21,
    'nwc': [10000, 9500, 9000],
    'capex': [10959, 10708, 11085],
    'da': [11519, 11104, 11284],
}

# Assumptions
assumptions = {
    'revenue_growth': [0.08, 0.07, 0.06, 0.05, 0.04],  # 5 years
    'ebit_margin': 0.30,
    'tax_rate': 0.21,
    'nwc_pct_revenue': 0.025,
    'capex_pct_revenue': 0.03,
    'terminal_growth': 0.025,
    'wacc': 0.085,
    'net_debt': 50000,
    'shares_outstanding': 15400000000,
}

# Run valuation
dcf = DCFModel(company_data, assumptions)
dcf.project_financials()
result = dcf.calculate_equity_value()

print(f"Implied Price: ${result['price_per_share']:.2f}")
```

### 3. Excel Generation

Create investment banking-quality Excel models:

```python
from src.excel.generator import ExcelGenerator

generator = ExcelGenerator(model_type='dcf')
generator.create_dcf_excel(
    dcf_model=dcf,
    assumptions=assumptions,
    company_data=company_data,
    filepath="My_DCF_Model.xlsx"
)
```

## Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_wacc.py

# Run with coverage
pytest --cov=src tests/
```

## Project Structure

```
valuation_pro/
├── src/
│   ├── models/          # Financial models (DCF, LBO, WACC, Comps)
│   ├── data/            # Data fetching and parsing
│   ├── excel/           # Excel generation and formatting
│   └── utils/           # Validation and helper functions
├── tests/               # Unit tests
├── example_dcf.py       # Complete DCF example
├── requirements.txt     # Dependencies
└── README.md           # Project overview
```

## Next Steps

### For Learning:
1. Review [FINANCE_CONCEPTS.md](docs/FINANCE_CONCEPTS.md) for valuation methodology
2. Modify `example_dcf.py` with different assumptions
3. Try valuing a different company

### For Development:
1. Implement LBO model ([src/models/lbo.py](src/models/lbo.py))
2. Add Comparable Companies analysis ([src/models/comps.py](src/models/comps.py))
3. Enhance Excel output with charts

### For Production Use:
1. Add your FRED API key for risk-free rates (optional)
2. Implement data validation for custom inputs
3. Add error handling for edge cases

## Common Issues

### Issue: yfinance data not available
**Solution**: The script automatically falls back to example data. For custom companies, you may need to input data manually.

### Issue: WACC calculation warnings
**Solution**: This is normal if WACC is outside 5-25% range. Verify your debt/equity inputs.

### Issue: Terminal growth >= WACC error
**Solution**: Terminal growth MUST be less than WACC. Reduce terminal growth or increase WACC.

### Issue: Excel file formatting issues
**Solution**: Ensure you're using Excel 2016+ or LibreOffice Calc. Older versions may not support all formatting.

## Support

- Check [README.md](README.md) for overview
- Review [FINANCE_CONCEPTS.md](docs/FINANCE_CONCEPTS.md) for methodology
- Run tests to verify installation: `pytest tests/`

## Design Philosophy

ValuationPro follows these principles:

1. **Transparency**: Every calculation is visible and traceable
2. **Flexibility**: Easy to modify assumptions and methods
3. **Excel-Native**: Users can edit generated files directly
4. **IB Standards**: Output quality matches Goldman Sachs/Morgan Stanley
5. **Robustness**: Graceful handling of missing data

---

Ready to value your first company? Run:

```bash
python example_dcf.py
```
