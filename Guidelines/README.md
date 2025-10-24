# ValuationPro

**Investment Banking-Quality Company Valuation Models in Python**

## Overview

ValuationPro is a professional-grade Python platform for generating comprehensive company valuation models. It produces Excel outputs that meet investment banking standards (Goldman Sachs, Morgan Stanley quality).

## Supported Valuation Methods

- **DCF (Discounted Cash Flow)**: Enterprise value using projected free cash flows
- **LBO (Leveraged Buyout)**: Private equity returns analysis with debt modeling
- **Comparable Companies**: Relative valuation using trading multiples
- **Precedent Transactions**: M&A transaction multiples analysis
- **Merger Model**: Accretion/dilution analysis

## Features

- Automated data fetching from yfinance and FRED
- IB-standard Excel formatting (blue inputs, formula-driven)
- Sensitivity analysis tables
- WACC calculation with market data
- Comprehensive error handling and validation
- PEP 8 compliant code

## Installation

```bash
pip install -r requirements.txt
```

For development:
```bash
pip install -e ".[dev]"
```

## Quick Start

```python
from src.models.wacc import WACCCalculator
from src.models.dcf import DCFModel

# Calculate WACC
wacc_calc = WACCCalculator(
    ticker="AAPL",
    debt=100000,  # $100B
    equity=2500000,  # $2.5T
    tax_rate=0.21
)
results = wacc_calc.calculate_wacc()
print(f"WACC: {results['wacc']:.2%}")

# Run DCF Model
# (See documentation for full examples)
```

## Project Structure

```
valuationpro/
├── src/
│   ├── models/        # Valuation models (DCF, LBO, etc.)
│   ├── data/          # Data fetching and parsing
│   ├── excel/         # Excel generation and formatting
│   └── utils/         # Validation and helpers
├── tests/             # Unit and integration tests
└── docs/              # Documentation
```

## Testing

```bash
pytest tests/
```

## Design Principles

1. **Transparency**: Every calculation is traceable from input to output
2. **Flexibility**: Easy to modify assumptions and methodologies
3. **Excel-Native**: Users can edit generated files directly
4. **Robustness**: Graceful handling of missing data and API failures
5. **IB Standards**: Output quality matching top-tier investment banks

## Documentation

See [FINANCE_CONCEPTS.md](docs/FINANCE_CONCEPTS.md) for detailed methodology explanations.

## License

MIT License

## Contributing

Contributions welcome! Please ensure code passes `black` formatting and all tests.
