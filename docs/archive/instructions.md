# ValuationPro - Project Instructions

## Project Structure

### Directory Organization

**Guidelines/** - All documentation and guideline files
- Technical documentation
- Tool-specific READMEs
- Best practices and standards
- Implementation guides

**Ref_models/** - Reference Excel models
- Professional IB-standard templates
- Example models for each valuation type
- Formatting and structure references

**Base_datasource/** - Source financial data files
- Income statements
- Balance sheets
- Cash flow statements
- Other financial data used as inputs
- **ONLY .xlsx files allowed** - NO Python scripts

**Examples/** - Generated Excel model outputs
- Example LBO models, DCF models, etc.
- Output from running example scripts
- **ONLY .xlsx files allowed** - NO Python scripts

**scripts/** - All Python scripts
- `examples/` - Example/demonstration scripts (example_dcf_tool.py, example_lbo_tool.py)
- `validation/` - Model validation scripts (check formulas, values)
- `inspection/` - Data inspection and debugging scripts

**src/** - Core source code
- `tools/` - Valuation model generators (DCF, LBO, etc.)
- `data/` - Data extraction and processing
- `excel/` - Excel formatting utilities

**tests/** - Unit and integration tests
- Test files for core functionality
- Pytest-based test suite

## File Placement Rules

1. **Documentation Files (.md)**
   - All `.md` files go in `Guidelines/` folder
   - **EXCEPTION**: `instructions.md` stays in root directory
   - This file (`instructions.md`) contains project-wide instructions

2. **Reference Models**
   - All reference/template Excel files go in `Ref_models/`
   - Naming convention: `Reference_*.xlsx`
   - **ONLY Excel files** - NO Python scripts

3. **Data Source Files**
   - All financial statement Excel files go in `Base_datasource/`
   - Income statements, balance sheets, cash flow statements
   - These are formatted, unique Excel files used as data sources
   - **ONLY Excel files** - NO Python scripts

4. **Python Scripts**
   - Example scripts go in `scripts/examples/`
   - Validation scripts go in `scripts/validation/`
   - Inspection/debugging scripts go in `scripts/inspection/`
   - Naming convention: `example_*.py`, `check_*.py`, `validate_*.py`, `inspect_*.py`

5. **Generated Excel Outputs**
   - Generated models go in `Examples/` folder
   - Naming convention: `LBO_Model_*.xlsx`, `DCF_Model_*.xlsx`, etc.
   - **ONLY Excel files** - NO Python scripts

6. **Core Source Code**
   - All production code in `src/` folder
   - Tools, utilities, data extractors
   - Do not mix with scripts or examples

## Coding Standards

### Tool Development

1. **Focused, Single-Purpose Tools**
   - Each tool handles ONE valuation type (DCF, LBO, Comps, etc.)
   - No multi-purpose generators
   - Simpler, more maintainable code

2. **Excel Formula-Driven**
   - ALL calculations must use Excel formulas (e.g., `"=B5*B6"`)
   - NEVER hardcode Python-calculated values
   - Models must be fully editable in Excel

3. **Professional IB Formatting**
   - Dark blue headers (#4472C4) with white text (#FFFFFF)
   - Light yellow input cells (#FFF2CC)
   - Proper table borders on all tables
   - Consistent number formatting ($M, %, x multiples)

4. **Data Sources**
   - Use Excel files from `Base_datasource/` as inputs
   - Utilize `FinancialStatementExtractor` for data extraction
   - Avoid API dependencies where possible

### Color Scheme Standards

```python
SECTION_FILL = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")  # Dark blue
SECTION_FONT = Font(name="Calibri", size=11, bold=True, color="FFFFFF")  # White text
INPUT_FILL = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")  # Light yellow
INPUT_FONT = Font(name="Calibri", size=11, color="000000")  # Black text
```

### Formula Examples

```python
# CORRECT - Excel formula
ws.cell(row=5, column=2).value = "=B3*B4"

# WRONG - Hardcoded value
ws.cell(row=5, column=2).value = 520000
```

## Testing Requirements

1. **Formula Validation**
   - Verify all cells use formulas, not values
   - Check cross-sheet references are correct
   - Ensure no division errors (#DIV/0!)

2. **Value Verification**
   - Load with `data_only=True` to check calculated values
   - Ensure no cells showing None or 0 unexpectedly
   - Validate all summary metrics calculate correctly

3. **Example Scripts**
   - Every tool must have a corresponding example script in `scripts/examples/`
   - Example must demonstrate full usage with realistic data
   - Run with: `PYTHONPATH=/path/to/valuation_pro python3 scripts/examples/example_tool.py`

## Documentation Requirements

1. **Tool README (in Guidelines/)**
   - Overview and features
   - Installation instructions
   - Quick start guide
   - Complete usage examples
   - Technical details (methods, parameters)
   - Troubleshooting section

2. **Code Comments**
   - Clear docstrings for all classes and methods
   - Inline comments for complex logic
   - Row/column reference comments in Excel generation

## Version Control

- Commit focused, single-purpose changes
- Use descriptive commit messages
- Follow Git Safety Protocol (no force push, no skip hooks)

## Current Tools

### Implemented
1. **DCF Tool** (`src/tools/dcf_tool.py`)
   - 6 sheets: Cover, Assumptions, Historical Data, Projections, DCF Valuation, Sensitivity
   - Formula-driven discount rate, WACC, terminal value calculations
   - Example: `scripts/examples/example_dcf_tool.py`
   - Documentation: `Guidelines/DCF_TOOL_README.md`

2. **LBO Tool** (`src/tools/lbo_tool.py`)
   - 8 sheets: Cover, Transaction Summary, S&U, Assumptions, Operating Model, Debt Schedule, Cash Flow Waterfall, Returns Analysis
   - Sources & Uses balancing
   - Debt amortization and interest calculations
   - IRR and MOIC returns analysis
   - Example: `scripts/examples/example_lbo_tool.py`
   - Documentation: `Guidelines/LBO_TOOL_README.md`

### Planned
- Comparable Companies Analysis (Comps) Tool
- Precedent Transactions Tool
- Sensitivity Analysis Tool
- Waterfall Analysis Tool

## Important Notes

- **NEVER create new .md files in root directory** (except this file)
- **NEVER place Python scripts in Excel folders** (Examples/, Ref_models/, Base_datasource/)
- **ALWAYS place example scripts in scripts/examples/**
- **ALWAYS place validation scripts in scripts/validation/**
- **ALWAYS place inspection scripts in scripts/inspection/**
- **ALWAYS extract data from Base_datasource/ files**
- **NEVER use emoji in files unless explicitly requested**
- **ALWAYS test generated models for formula correctness**

## Folder Summary

```
valuation_pro/
├── Base_datasource/           # Excel data sources ONLY
├── Examples/                  # Generated Excel outputs ONLY
├── Ref_models/               # Reference Excel files ONLY
├── Guidelines/               # Documentation .md files
├── scripts/                  # All Python scripts
│   ├── examples/            # Example/demo scripts
│   ├── validation/          # Model validation scripts
│   └── inspection/          # Data inspection scripts
├── src/                     # Core source code
│   ├── tools/              # Model generators
│   ├── data/               # Data extractors
│   └── excel/              # Excel utilities
├── tests/                   # Unit tests
└── instructions.md          # This file
```

---

Last Updated: 2025-10-24
