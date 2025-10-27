# Excel Advanced Skills - Quick Start Guide

## What This Skill Does

This skill teaches AI assistants (like Claude Code) how to **dynamically generate investment banking-grade Excel models** using openpyxl, where the structure and content adapt based on available input data rather than following fixed templates.

## Key Capabilities

✅ Analyze input data to determine what analyses are feasible  
✅ Select and assemble modular components (DCF, LBO, Comps, etc.)  
✅ Generate Excel formulas with correct absolute/relative references  
✅ Apply IB-standard formatting (colors, borders, number formats)  
✅ Validate outputs for errors and unrealistic values  
✅ Handle edge cases (missing data, negative values, outliers)

## Quick Reference

### When to Use This Skill

Use when you need to:
- Generate financial models that adapt to different input scenarios
- Build Excel files programmatically with openpyxl
- Ensure formulas are transparent and audit-ready
- Apply investment banking formatting standards
- Handle varying data completeness gracefully

### Files Included

```
excel-advanced-skill/
├── SKILL.md                          # Main skill documentation (comprehensive)
├── README.md                         # This file
├── examples/
│   ├── dynamic_generation_example.py # Complete working example
│   └── decision_logic_example.py     # Input analysis & capability mapping
├── reference/
│   ├── openpyxl_best_practices.md   # Technical reference for openpyxl
│   └── component_library.md          # Reusable component catalog
└── templates/
    └── quality_checklist.md          # Validation framework
```

## Core Concepts

### 1. Intelligence-Based Generation

Traditional: `template + data → Excel`  
Advanced: `analyze inputs → determine capabilities → build custom model → validate`

### 2. Component Library Pattern

Models are built from reusable components:
- `assumptions_panel`
- `fcf_projection`
- `wacc_calculation`
- `dcf_valuation`
- `sensitivity_table`
- `debt_schedule`
- `lbo_returns`
- `comps_table`
- `football_field`

Each component knows what it needs and what it generates.

### 3. Formula Builder System

Instead of hardcoding calculations, use a FormulaBuilder that ensures:
- Correct cell references
- Proper absolute/relative addressing ($B$5 vs B5)
- Valid Excel formula syntax
- No circular references

### 4. Quality Scoring

Every generation gets a confidence score (0.0-1.0) based on:
- Data completeness (40%)
- Data consistency (30%)
- Historical depth (15%)
- Market data availability (15%)

## Quick Examples

### Example 1: Analyze Inputs

```python
analyzer = InputAnalyzer()
capabilities = analyzer.analyze_and_map_capabilities(input_data)

# Returns:
# {
#     'analyses': {
#         'dcf': {'feasible': True, 'level': 'advanced', 'confidence': 0.95},
#         'lbo': {'feasible': True, 'level': 'basic', 'confidence': 0.80},
#         'comps': {'feasible': False, 'reason': 'missing_comparables'}
#     },
#     'components': ['fcf_projection', 'wacc', 'terminal_value', ...],
#     'quality_score': 0.87
# }
```

### Example 2: Build a Formula

```python
formula_builder = FormulaBuilder()

fcf_formula = formula_builder.build_formula('fcf', {
    'ebitda_cell': 'F10',
    'da_cell': 'F11',
    'tax_rate': '$B$5',  # Absolute reference
    'capex_cell': 'F15',
    'nwc_cell': 'F20'
})

# Returns: "=(F10-F11)*(1-$B$5)-F15-F20"
# NOPAT minus CapEx minus NWC change
```

### Example 3: Generate Complete Model

```python
generator = DynamicModelGenerator()

workbook = generator.generate_model(
    input_data={'revenue': 1500, 'ebitda': 450, ...},
    company_name='TechCorp'
)

workbook.save('TechCorp_Valuation.xlsx')
```

## Most Important Rules

### Formula Generation

❌ **WRONG:** `ws['C10'].value = 1500 * 1.15`  
✅ **CORRECT:** `ws['C10'].value = "=B10*$B$5"`

Always use formulas for transparency and auditability.

### Absolute vs Relative References

❌ **WRONG:** `ws['F10'].value = "=E10*(1+B5)"`  (growth assumption moves when copied)  
✅ **CORRECT:** `ws['F10'].value = "=E10*(1+$B$5)"`  (growth assumption stays fixed)

### Cell Indexing

❌ **WRONG:** `ws.cell(row=0, column=1)`  (openpyxl is 1-indexed)  
✅ **CORRECT:** `ws.cell(row=1, column=1)`

## Common Use Cases

| Scenario | What This Skill Provides |
|----------|--------------------------|
| "I have revenue, EBITDA, tax rate, but no debt schedule" | Generates DCF + basic LBO (skips debt waterfall) |
| "I have full financials + 5 comparable companies" | Generates DCF + sensitivity + comps + football field |
| "I only have transaction multiples from precedent deals" | Generates precedent transaction analysis only |
| "User uploaded Excel with unusual structure" | Extracts data, normalizes, generates standard model |

## Integration with ValuationPro

This skill is designed to work with:

1. **Data Fetcher** - Provides normalized input data
2. **ML Pipeline** - Enriches data with forecasts/adjustments
3. **Excel Generator** - Uses this skill's patterns to build outputs
4. **Validation Layer** - Uses quality checks from this skill

## Next Steps

1. **Read SKILL.md** - Comprehensive guide with all patterns
2. **Check examples/** - Working code implementations
3. **Review reference/** - Deep dives into specific topics
4. **Use templates/** - Checklists for quality assurance

## Quick Tips

💡 Always analyze inputs first before deciding what to generate  
💡 Use components as building blocks, not monolithic templates  
💡 Formulas must reference cells, never hardcode values  
💡 Test with realistic company data (e.g., Apple)  
💡 Validate every generated model for errors  
💡 Format like an investment banker (blue headers, yellow inputs, blue outputs)

---

**For detailed implementation guidance, see SKILL.md (the main skill document)**
