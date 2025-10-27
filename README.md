# ValuationPro

**Professional-grade company valuation platform** combining traditional investment banking methods with cutting-edge AI and machine learning capabilities.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![Tests](https://img.shields.io/badge/tests-42%20passed-brightgreen)
![Status](https://img.shields.io/badge/status-production--ready-success)

---

## Overview

ValuationPro provides comprehensive financial modeling and valuation tools used by investment bankers, private equity professionals, and corporate finance teams.

### Core Capabilities

- **DCF (Discounted Cash Flow) Models** - Full projection engine with terminal value and sensitivity analysis
- **LBO (Leveraged Buyout) Models** - Sources & Uses, debt schedules, returns analysis
- **Excel Generation** - Investment banking-quality Excel models with formulas (not hardcoded values)
- **Data Extraction** - Intelligent extraction from Excel, PDFs, and APIs
- **WACC Calculations** - Real-time cost of capital calculations using market data

### Advanced Features (In Development)

- **Monte Carlo Simulations** - Probabilistic valuation analysis
- **Machine Learning** - Revenue forecasting, churn prediction, credit risk modeling
- **AI-Powered Analysis** - Claude integration for document extraction and insights
- **Interactive Dashboards** - Web-based valuation dashboards

---

## Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd valuation_pro

# Install core dependencies
pip install -e .

# OR install with specific feature sets
pip install -e ".[dev]"    # Development tools
pip install -e ".[ml]"     # Machine learning features
pip install -e ".[llm]"    # AI/Claude integration
pip install -e ".[viz]"    # Visualization tools
pip install -e ".[all]"    # Everything
```

### Environment Setup

```bash
# Set Python path (add to .bashrc or .zshrc for persistence)
export PYTHONPATH="/path/to/valuation_pro:$PYTHONPATH"

# Optional: Set API keys for data providers
export ANTHROPIC_API_KEY="your-claude-api-key"
export ALPHA_VANTAGE_KEY="your-key"
export FMP_API_KEY="your-key"
```

---

## Available Commands

### Testing

```bash
# Run all tests
python3 -m pytest tests/

# Run with verbose output
python3 -m pytest tests/ -v

# Run specific test file
python3 -m pytest tests/test_dcf.py

# Run with coverage
python3 -m pytest tests/ --cov=src

# Run specific test by name
python3 -m pytest tests/test_dcf.py::TestDCFModel::test_calculate_fcf
```

### Example Scripts

```bash
# Generate DCF model
PYTHONPATH=/path/to/valuation_pro python3 scripts/examples/example_dcf.py

# Generate LBO model
PYTHONPATH=/path/to/valuation_pro python3 scripts/examples/example_lbo.py
```

### Code Quality

```bash
# Format code with Black
python3 -m black src/ tests/

# Run linting
python3 -m flake8 src/ tests/

# Type checking (if mypy installed)
python3 -m mypy src/
```

### Python Interactive Usage

```python
# DCF Valuation Example
from src.models.dcf import DCFModel

company_data = {
    'revenue': [100000],  # $100M
    'ebit': [25000],
    'tax_rate': 0.21,
    'nwc': [10000],
    'capex': [3000],
    'da': [5000],
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
print(f"Implied Price: ${result['price_per_share']:.2f}")
```

```python
# Data Pipeline Example
from src.data.pipeline import FinancialDataPipeline

pipeline = FinancialDataPipeline()

# Extract from Excel
result = pipeline.execute("path/to/financials.xlsx")
data = result['data']
print(data.summary())

# Extract from API (ticker symbol)
result = pipeline.execute("AAPL", years=5)
```

```python
# WACC Calculation Example
from src.models.wacc import WACCCalculator

calc = WACCCalculator(
    ticker="AAPL",
    debt=100000,      # $100B
    equity=2500000,   # $2.5T
    tax_rate=0.21
)

result = calc.calculate_wacc(interest_expense=5000)
print(f"WACC: {result['wacc']:.2%}")
```

```python
# Excel Generation Example
from src.excel.three_statement_generator import ThreeStatementGenerator

generator = ThreeStatementGenerator(ticker="ACME")
generator.generate_full_model(
    company_data=company_data,
    assumptions=assumptions,
    wacc_data=wacc_data,
    filepath="output/model.xlsx"
)
```

---

## Repository Structure

```
valuation_pro/
├── src/
│   ├── analytics/              # Monte Carlo, distributions, stress tests
│   │   ├── monte_carlo.py
│   │   ├── distributions.py
│   │   ├── stress_tests.py
│   │   └── risk_metrics.py
│   │
│   ├── data/                   # Data extraction pipeline
│   │   ├── extractors/
│   │   ├── normalizers/
│   │   ├── validators/
│   │   ├── pipeline.py
│   │   └── schema.py
│   │
│   ├── excel/                  # Excel model generation
│   │   ├── three_statement_generator.py
│   │   ├── formatter.py
│   │   └── formula_builder.py
│   │
│   ├── llm/                    # AI/Claude integration
│   │   ├── document_processor.py
│   │   ├── extractors/         # 10-K, contracts, earnings
│   │   └── reasoning/          # Valuation advisor, risk analyzer
│   │
│   ├── ml/                     # Machine learning
│   │   ├── forecasting/        # LSTM, Prophet, ensemble
│   │   ├── cohort/             # Retention, churn, LTV
│   │   └── predictive/         # Credit risk, deal scoring
│   │
│   ├── models/                 # Core valuation models
│   │   ├── dcf.py
│   │   └── wacc.py
│   │
│   ├── tools/                  # Excel output tools
│   │   ├── dcf_tool.py
│   │   └── lbo_tool.py
│   │
│   └── visualization/          # Charts and dashboards
│       ├── tornado_charts.py
│       ├── monte_carlo_viz.py
│       └── dashboards/
│
├── tests/                      # Comprehensive test suite
│   ├── test_dcf.py
│   ├── test_wacc.py
│   └── test_excel_formulas.py
│
├── scripts/                    # Utility scripts
│   ├── examples/
│   ├── inspection/
│   └── validation/
│
├── Examples/                   # Generated output files
├── Guidelines/                 # Documentation
├── Ref_models/                 # Reference models
└── Base_datasource/            # Sample data
```

---

## Feature Status

### ✅ Production Ready

- DCF Valuation Models
- LBO Models
- WACC Calculations
- Excel Generation (11-sheet models)
- Data Extraction (Excel, APIs)
- Data Normalization & Validation
- Comprehensive Test Suite (42 tests)

### 🚧 Framework Ready (Awaiting Implementation)

- Monte Carlo Simulations
- ML Revenue Forecasting
- Cohort Analysis
- Credit Risk Modeling
- Claude/LLM Integration
- Interactive Dashboards
- Tornado Charts & Visualizations

---

## Testing

All core functionality is thoroughly tested:

```bash
$ python3 -m pytest tests/
======================== 42 passed, 1 warning in 1.70s =========================
```

**Test Coverage:**
- DCF Models: 15 tests
- WACC Calculator: 15 tests
- Excel Formula Generation: 8 tests
- Data Pipeline: Integration tests
- Edge Cases: Zero debt, high leverage, negative FCF

---

## Development

### Running Tests

```bash
# All tests
python3 -m pytest tests/ -v

# Specific module
python3 -m pytest tests/test_dcf.py -v

# With coverage report
python3 -m pytest tests/ --cov=src --cov-report=html
```

### Code Formatting

```bash
# Format with Black
python3 -m black src/ tests/

# Check linting
python3 -m flake8 src/ tests/ --max-line-length=100
```

### Adding New Features

1. Create module in appropriate `src/` subdirectory
2. Add corresponding tests in `tests/`
3. Update this README
4. Ensure all tests pass

---

## Configuration

### API Keys

Create a `.env` file in the project root:

```bash
# Data Providers
ALPHA_VANTAGE_KEY=your_key_here
FMP_API_KEY=your_key_here
FRED_API_KEY=your_key_here

# AI/ML Services
ANTHROPIC_API_KEY=your_claude_key_here

# Optional
OPENAI_API_KEY=your_openai_key_here
```

### Custom Settings

```python
# In your scripts
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('ANTHROPIC_API_KEY')
```

---

## Example Outputs

The tool generates professional-grade Excel models:

- **DCF Models**: `Examples/DCF_Model_AcmeTech.xlsx`
- **LBO Models**: `Examples/LBO_Model_AcmeTech.xlsx`

All Excel files contain:
- ✅ Formulas (not hardcoded values)
- ✅ Cross-sheet references
- ✅ Scenario analysis with CHOOSE()
- ✅ Investment banking formatting
- ✅ Sensitivity tables

---

## Roadmap

### Q1 2025
- ✅ Core DCF/LBO models
- ✅ Excel generation
- ✅ Data extraction pipeline
- 🚧 Monte Carlo simulations
- 🚧 Basic ML forecasting

### Q2 2025
- 📋 Claude integration for 10-K extraction
- 📋 Interactive dashboards
- 📋 Advanced ML models (LSTM, Prophet)
- 📋 Cohort analysis for SaaS

### Q3 2025
- 📋 Credit risk modeling
- 📋 Deal scoring system
- 📋 Automated comparable analysis
- 📋 API endpoints

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Guidelines

- Write tests for new features
- Follow Black code formatting
- Update documentation
- Ensure all tests pass

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## Support

For questions, issues, or feature requests:
- 📧 Email: support@valuationpro.com
- 🐛 Issues: GitHub Issues
- 📚 Docs: `/docs` directory

---

## Acknowledgments

- Investment Banking Institute for financial modeling standards
- Wall Street Oasis for Excel template inspiration
- Anthropic for Claude AI capabilities
- Open source community for excellent tools

---

## Quick Reference

### Common Commands

| Command | Description |
|---------|-------------|
| `pytest tests/` | Run all tests |
| `python3 scripts/examples/example_dcf.py` | Generate DCF model |
| `python3 scripts/examples/example_lbo.py` | Generate LBO model |
| `python3 -m black src/` | Format code |
| `pip install -e ".[all]"` | Install all features |

### Import Shortcuts

```python
# Core models
from src.models.dcf import DCFModel
from src.models.wacc import WACCCalculator

# Data pipeline
from src.data.pipeline import FinancialDataPipeline

# Excel generation
from src.excel.three_statement_generator import ThreeStatementGenerator

# Tools
from src.tools.dcf_tool import DCFTool
from src.tools.lbo_tool import LBOTool
```

---

**Built with ❤️ for the finance community**
