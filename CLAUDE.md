# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ValuationPro is a professional-grade investment banking valuation platform that combines traditional financial modeling (DCF, LBO) with modern data extraction pipelines and advanced analytics capabilities. The platform generates investment banking-quality Excel models with formulas (not hardcoded values) and supports multi-source data extraction.

**Key Philosophy**: Production-ready core features (DCF, LBO, data pipeline) with framework-ready advanced features (ML, LLM, analytics) awaiting implementation.

---

## Essential Commands

### Environment Setup
```bash
# CRITICAL: Set PYTHONPATH before running any scripts
export PYTHONPATH="/Users/samueldukmedjian/Desktop/valuation_pro:$PYTHONPATH"

# For permanent setup, add to ~/.bashrc or ~/.zshrc
```

### Testing
```bash
# Run all tests (42 tests, all should pass)
python3 -m pytest tests/

# Run with verbose output
python3 -m pytest tests/ -v

# Run specific test file
python3 -m pytest tests/test_dcf.py

# Run specific test by name
python3 -m pytest tests/test_dcf.py::TestDCFModel::test_calculate_fcf

# With coverage
python3 -m pytest tests/ --cov=src
```

### Generate Example Models
```bash
# Generate DCF model (outputs to Examples/)
PYTHONPATH=/Users/samueldukmedjian/Desktop/valuation_pro python3 scripts/examples/example_dcf.py

# Generate LBO model (outputs to Examples/)
PYTHONPATH=/Users/samueldukmedjian/Desktop/valuation_pro python3 scripts/examples/example_lbo.py
```

### Code Quality
```bash
# Format code
python3 -m black src/ tests/

# Lint
python3 -m flake8 src/ tests/ --max-line-length=100
```

---

## Architecture Overview

### Production-Ready Modules (✅)

**1. Core Valuation Models (`src/models/`)**
- `dcf.py` - Discounted Cash Flow valuation with terminal value and sensitivity analysis
- `wacc.py` - Weighted Average Cost of Capital with real-time market data
- Uses: pandas, numpy, numpy-financial, yfinance
- 30 comprehensive tests covering edge cases

**2. Data Extraction Pipeline (`src/data/`)**
- **Strategy Pattern**: Pluggable extractors for different sources
- `pipeline.py` - Main orchestrator with auto-routing
- `extractors/` - Excel, API extractors (base class pattern)
- `normalizers/` - Scale detection, derived field calculation
- `validators/` - Data quality checks and reconciliation
- `schema.py` - Standardized FinancialData schema

**3. Excel Generation (`src/excel/`)**
- `three_statement_generator.py` - 11-sheet models with cross-references
- `dcf_tool.py` - Single-sheet DCF models
- `lbo_tool.py` - Single-sheet LBO models
- `formatter.py` - Investment banking standard formatting
- `formula_builder.py` - Excel formula utilities
- **IMPORTANT**: All models use formulas, not hardcoded values
- **IMPORTANT**: Uses CHOOSE() for scenario analysis

**4. Tools (`src/tools/`)**
- High-level interfaces that combine models + Excel generation
- Easier to use than low-level components

### Framework-Ready Modules (🚧)

**5. Analytics (`src/analytics/`)**
- Monte Carlo simulations, stress tests, risk metrics
- Requires: `pip install -e ".[ml]"`

**6. Machine Learning (`src/ml/`)**
- `forecasting/` - LSTM, Prophet, ensemble models
- `cohort/` - Retention, churn, LTV for SaaS
- `predictive/` - Credit risk, deal scoring
- Requires: `pip install -e ".[ml]"`

**7. LLM Integration (`src/llm/`)**
- Document processing with Claude API
- 10-K extraction, contract parsing, earnings analysis
- Requires: `pip install -e ".[llm]"` and `ANTHROPIC_API_KEY`

**8. Visualization (`src/visualization/`)**
- Tornado charts, Monte Carlo viz, dashboards
- Requires: `pip install -e ".[viz]"`

---

## Data Flow Architecture

```
Input (Excel/API)
  ↓
Data Pipeline (extract → normalize → validate)
  ↓
Valuation Models (DCF/LBO/WACC)
  ↓
Excel Output (formulas + IB formatting)
```

**Key Pattern**: The pipeline returns `FinancialData` objects that can be directly fed into valuation models, which then connect to Excel generators.

---

## Critical Development Patterns

### 1. PYTHONPATH Requirement
All scripts require PYTHONPATH to be set. When running Python files:
```bash
PYTHONPATH=/Users/samueldukmedjian/Desktop/valuation_pro python3 script.py
```

### 2. Excel Formula Generation
- NEVER hardcode values in Excel cells
- ALWAYS use cell references and formulas
- Use `formula_builder.py` utilities for complex formulas
- Cross-sheet references use: `='Sheet Name'!A1`
- CHOOSE() function for scenarios: `=CHOOSE($B$1, value1, value2, value3)`

### 3. Data Extraction
- Pipeline auto-detects source type (Excel path vs ticker symbol)
- All data normalized to FinancialData schema
- Scale detection automatic (millions/billions)
- Validators check reconciliation and flag outliers

### 4. Testing Standards
- All production code has tests (currently 42 tests)
- Test edge cases: zero debt, negative FCF, high leverage
- Use pytest fixtures for common test data
- Target >80% coverage for new features

### 5. Module Organization
- Production-ready: `src/models/`, `src/data/`, `src/excel/`, `src/tools/`
- Framework-ready: `src/analytics/`, `src/ml/`, `src/llm/`, `src/visualization/`
- **DO NOT** implement framework-ready features without explicit request
- Framework modules have structure but need implementation

---

## Common Tasks

### Adding a New Valuation Model
1. Create in `src/models/new_model.py`
2. Add comprehensive docstrings with formula explanations
3. Create tests in `tests/test_new_model.py`
4. If Excel output needed, create in `src/tools/new_model_tool.py`
5. Update ARCHITECTURE.md

### Adding a New Data Source
1. Extend `BaseExtractor` in `src/data/extractors/`
2. Implement `extract()` method returning dict
3. Register in pipeline's `_determine_source_type()`
4. Add integration tests

### Implementing Framework-Ready Features
1. Check if scaffolding exists in respective module
2. Follow existing patterns from production modules
3. Add proper error handling and validation
4. Write comprehensive tests
5. Update README.md with new capabilities

### Excel Model Issues
- Check formula references (sheet names, cell addresses)
- Verify CHOOSE() scenario indices (1-based, not 0-based)
- Test with different input scales (millions vs billions)
- Use `scripts/validation/` tools to verify calculations

---

## Important Conventions

### Naming
- Classes: PascalCase (`DCFModel`, `WACCCalculator`)
- Files: snake_case (`dcf_tool.py`, `data_normalizer.py`)
- Functions: snake_case (`calculate_equity_value()`)
- Constants: UPPER_SNAKE_CASE (`SECTION_FILL`)

### Documentation
- Comprehensive docstrings for all public methods
- Include formula explanations for financial calculations
- Usage examples in docstrings
- TODO comments for future enhancements

### Type Hints
- Use type hints for function parameters and returns
- Common types: `Dict`, `List`, `Optional`, `pd.DataFrame`
- Complex data: Use `FinancialData` schema

### Error Handling
- Validate inputs at module boundaries
- Raise descriptive exceptions
- Use warnings for non-critical issues
- Log pipeline execution details

---

## Dependencies

### Core (Always Installed)
```
pandas >= 2.0.0
numpy >= 1.24.0
yfinance >= 0.2.0
openpyxl >= 3.1.0
numpy-financial >= 1.0.0
```

### Optional Feature Sets
```bash
pip install -e ".[dev]"    # pytest, black, flake8
pip install -e ".[ml]"     # scikit-learn, xgboost, tensorflow, prophet
pip install -e ".[llm]"    # anthropic, pypdf, tiktoken
pip install -e ".[viz]"    # matplotlib, seaborn, plotly, streamlit
pip install -e ".[all]"    # Everything
```

---

## Known Issues & Patterns

### Excel Generation
- Sources & Uses must balance in LBO models (use validation scripts)
- CHOOSE() requires scenario index in specific cell
- Column widths need manual adjustment via `formatter.py`
- Cross-sheet formulas need exact sheet name matches

### Data Extraction
- API rate limits for yfinance (add delays if needed)
- Excel extractors expect specific sheet names
- Scale detection may need manual verification for edge cases
- Some API data requires environment variables (keys)

### Testing
- Some tests may show warnings (expected, 1 warning is normal)
- Use `-v` flag to see detailed test output
- Coverage reports help identify untested code paths

---

## Key Files to Reference

- **ARCHITECTURE.md** - Detailed technical architecture
- **README.md** - User-facing documentation with examples
- **QUICK_START.md** - Fast setup guide
- **setup.py** - Dependency definitions
- **tests/** - Usage examples and patterns

---

## Performance Expectations

- DCF calculation: <100ms
- Excel generation: 1-2 seconds
- Data extraction: 2-5 seconds (API), <1s (Excel)
- Test suite: ~2 seconds for all 42 tests

---

## When Working on This Codebase

1. **Always check module status** (✅ production vs 🚧 framework)
2. **Set PYTHONPATH** before running any Python scripts
3. **Run tests** after changes to ensure nothing breaks
4. **Follow Excel formula patterns** - never hardcode values
5. **Use existing patterns** from production modules
6. **Update tests** when adding features
7. **Check ARCHITECTURE.md** for module-specific details
8. **Validate calculations** using example scripts
