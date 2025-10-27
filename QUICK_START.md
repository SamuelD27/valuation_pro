# ValuationPro Quick Start Guide

## Installation

```bash
cd /path/to/valuation_pro

# Core features only
pip install -e .

# With all features
pip install -e ".[all]"
```

## Essential Commands

### Setup Environment

```bash
# Set PYTHONPATH (required for scripts)
export PYTHONPATH="/Users/samueldukmedjian/Desktop/valuation_pro:$PYTHONPATH"

# Add to ~/.bashrc or ~/.zshrc for persistence
echo 'export PYTHONPATH="/Users/samueldukmedjian/Desktop/valuation_pro:$PYTHONPATH"' >> ~/.bashrc
```

### Run Tests

```bash
# All tests
python3 -m pytest tests/

# Verbose output
python3 -m pytest tests/ -v

# Specific test
python3 -m pytest tests/test_dcf.py::TestDCFModel::test_calculate_fcf
```

### Generate Models

```bash
# DCF Model
PYTHONPATH=/Users/samueldukmedjian/Desktop/valuation_pro python3 scripts/examples/example_dcf.py

# LBO Model
PYTHONPATH=/Users/samueldukmedjian/Desktop/valuation_pro python3 scripts/examples/example_lbo.py
```

### Python Interactive

```python
# DCF Example
from src.models.dcf import DCFModel

company_data = {
    'revenue': [100000],
    'ebit': [25000],
    'tax_rate': 0.21,
    'nwc': [10000],
}

assumptions = {
    'revenue_growth': [0.10, 0.08, 0.06, 0.05, 0.04],
    'ebit_margin': 0.25,
    'tax_rate': 0.21,
    'nwc_pct_revenue': 0.10,
    'capex_pct_revenue': 0.03,
    'terminal_growth': 0.025,
    'wacc': 0.09,
    'net_debt': 50000,
    'shares_outstanding': 100_000_000,
}

model = DCFModel(company_data, assumptions)
result = model.calculate_equity_value()
print(f"Price: ${result['price_per_share']:.2f}")
```

```python
# Data Pipeline
from src.data.pipeline import FinancialDataPipeline

pipeline = FinancialDataPipeline()
result = pipeline.execute("AAPL", years=5)
print(result['data'].summary())
```

```python
# WACC Calculator
from src.models.wacc import WACCCalculator

calc = WACCCalculator(
    ticker="AAPL",
    debt=100000,
    equity=2500000,
    tax_rate=0.21
)
result = calc.calculate_wacc(interest_expense=5000)
print(f"WACC: {result['wacc']:.2%}")
```

## Common Tasks

### Check Installation

```bash
python3 -c "from src.models.dcf import DCFModel; print('✅ Installation successful')"
```

### Run All Tests

```bash
python3 -m pytest tests/ -v
```

### Format Code

```bash
python3 -m black src/ tests/
```

### View Test Coverage

```bash
python3 -m pytest tests/ --cov=src --cov-report=html
open htmlcov/index.html
```

## Project Structure

```
valuation_pro/
├── src/                    # Source code
│   ├── analytics/          # Monte Carlo, risk metrics
│   ├── data/               # Data extraction
│   ├── excel/              # Excel generation
│   ├── llm/                # Claude integration
│   ├── ml/                 # Machine learning
│   ├── models/             # DCF, WACC
│   ├── tools/              # High-level tools
│   └── visualization/      # Charts, dashboards
│
├── tests/                  # Test suite (42 tests)
├── scripts/examples/       # Example scripts
├── Examples/               # Generated outputs
└── docs/                   # Documentation
```

## Feature Installation

```bash
# Machine Learning
pip install -e ".[ml]"

# LLM/Claude
pip install -e ".[llm]"

# Visualization
pip install -e ".[viz]"

# Development Tools
pip install -e ".[dev]"

# Everything
pip install -e ".[all]"
```

## Getting Help

- **README.md** - Comprehensive guide
- **ARCHITECTURE.md** - Technical details
- **Tests** - See `tests/` for usage examples
- **Docstrings** - All functions documented

## Status Check

```bash
# Verify everything works
python3 -m pytest tests/ -v
python3 scripts/examples/example_dcf.py
python3 scripts/examples/example_lbo.py
```

Expected output:
```
======================== 42 passed, 1 warning in 1.75s =========================
✅ DCF model generated successfully!
✅ LBO model generated successfully!
```

---

**Quick Links**
- [README.md](README.md) - Full documentation
- [ARCHITECTURE.md](ARCHITECTURE.md) - Technical architecture
- [REORGANIZATION_SUMMARY.md](REORGANIZATION_SUMMARY.md) - Recent changes
