# Quality Validation Checklist for Generated Models

Use this checklist to validate every generated Excel model before delivery.

## Pre-Generation Checks

### Input Data Validation
- [ ] All required fields present for selected analyses
- [ ] No null/missing values in critical fields
- [ ] Historical data spans at least 3 years (for projections)
- [ ] Financial metrics are internally consistent (e.g., FCF ties to components)
- [ ] No obvious data quality issues (negative revenue, etc.)

### Capability Assessment
- [ ] Capability map generated correctly
- [ ] Confidence score calculated (0.0-1.0)
- [ ] Missing data identified and logged
- [ ] Appropriate fallback strategies selected
- [ ] User notified of any limitations

---

## Formula Validation

### Reference Accuracy
- [ ] All formulas start with `=`
- [ ] Absolute references (`$B$5`) used for assumptions
- [ ] Relative references used correctly for time series
- [ ] No hardcoded calculations (all formulas)
- [ ] Cell references point to existing cells
- [ ] No `#REF!` or `#NAME?` errors

### Calculation Logic
- [ ] FCF = NOPAT - CapEx - ΔNW (correct formula)
- [ ] WACC calculation includes all components
- [ ] NPV formula uses correct discount rate
- [ ] Terminal value denominator: (WACC - g) not (g - WACC)
- [ ] Debt paydown waterfall follows priority order
- [ ] IRR calculation includes correct cash flows and dates

### Financial Reasonableness
- [ ] Revenue growth between -20% and +50%
- [ ] EBITDA margins between 0% and 50%
- [ ] WACC between 5% and 25%
- [ ] Terminal growth between 0% and 5%
- [ ] WACC > Terminal Growth (required for DCF)
- [ ] Debt/EBITDA ratios reasonable (typically 2x-6x)
- [ ] LBO IRR between 15% and 30%
- [ ] MOIC between 1.5x and 4.0x

---

## Formatting Validation

### Color Scheme
- [ ] Headers: Dark blue (#002060) background, white text
- [ ] Inputs: Light yellow (#FFF2CC) background
- [ ] Outputs: Light blue (#D9E1F2) background
- [ ] Calculations: White background
- [ ] Consistent across all sections

### Number Formats
- [ ] Currency: `$#,##0.0,,"M"` (millions)
- [ ] Percentages: `0.0%`
- [ ] Multiples: `0.0x`
- [ ] Dates: `mm/dd/yyyy`
- [ ] Years: Plain numbers (2024, 2025, ...)

### Layout
- [ ] Column widths accommodate content (no ###)
- [ ] Rows properly aligned
- [ ] Adequate spacing between sections (1-2 blank rows)
- [ ] Borders applied to section boundaries
- [ ] Headers merged correctly

---

## Component-Specific Checks

### DCF Model
- [ ] 5-year projection period
- [ ] FCF calculated correctly for each year
- [ ] Terminal value uses appropriate method (Gordon Growth or Exit Multiple)
- [ ] PV calculations use consistent WACC
- [ ] Enterprise Value → Equity Value bridge correct
- [ ] Price per share calculation includes shares outstanding

### LBO Model
- [ ] Sources & Uses balance
- [ ] Debt tranches listed with interest rates
- [ ] Debt schedule calculates quarterly balances
- [ ] Cash sweep percentage applied correctly
- [ ] Exit assumptions clearly stated
- [ ] Returns (IRR, MOIC) calculated with XIRR

### Comps Analysis
- [ ] At least 3 comparable companies
- [ ] Outliers identified and handled
- [ ] Statistics calculated (mean, median, 25th/75th percentile)
- [ ] Implied valuation range shown
- [ ] Multiple types appropriate (EV/Revenue, EV/EBITDA, P/E)

### Sensitivity Analysis
- [ ] 2-dimensional table (WACC vs Terminal Growth)
- [ ] Range covers ±2% from base case
- [ ] Color scale applied (red → yellow → green)
- [ ] Values recalculate correctly
- [ ] Base case highlighted

---

## Error Detection

### Mathematical Errors
- [ ] No division by zero
- [ ] No circular references
- [ ] No #VALUE! errors
- [ ] No #DIV/0! errors
- [ ] No #NUM! errors

### Logic Errors
- [ ] Cash flows signed correctly (negative for outflows)
- [ ] Time periods consistent (annual, quarterly)
- [ ] Units consistent ($M, $K, etc.)
- [ ] Growth compounding correctly (not additive)

### Edge Cases
- [ ] Handles negative FCF in early years
- [ ] Handles net cash position (negative net debt)
- [ ] Handles missing comparables gracefully
- [ ] Handles zero or minimal debt

---

## Output Quality Metrics

### Confidence Scoring
| Score | Interpretation | Action |
|-------|----------------|--------|
| 0.90-1.00 | Investment-grade | Deliver with confidence |
| 0.75-0.89 | High quality | Deliver with minor notes |
| 0.60-0.74 | Moderate quality | Flag key assumptions |
| < 0.60 | Low confidence | Request more data or warn user |

### Completeness
- [ ] All feasible analyses included
- [ ] Summary/highlight section present
- [ ] Key outputs clearly identified
- [ ] Limitations documented (if any)

### Usability
- [ ] Model can be easily audited
- [ ] Key assumptions clearly labeled
- [ ] Outputs easy to locate
- [ ] Formulas can be traced
- [ ] No hidden calculations

---

## Pre-Delivery Final Check

- [ ] File saves without errors
- [ ] File opens in Excel correctly
- [ ] Formulas calculate on opening
- [ ] All sheets present (if multi-sheet)
- [ ] File size reasonable (< 5MB)
- [ ] No personal/confidential data in comments
- [ ] Filename follows convention: `CompanyName_ValuationType_Date.xlsx`

---

## Post-Delivery Validation

- [ ] User can open file
- [ ] User can modify assumptions
- [ ] Calculations update correctly
- [ ] No errors reported by user
- [ ] Model produces expected results

---

## Issue Log Template

If any checks fail, log here:

| Check Failed | Severity | Impact | Resolution | Status |
|--------------|----------|--------|------------|--------|
| WACC < Terminal Growth | HIGH | DCF undefined | Adjust terminal growth to 2.5% | FIXED |
| Missing 2 comps | MEDIUM | Limited range | Proceed with 3 comps, note limitation | NOTED |
| Column width for EV | LOW | Cosmetic | Adjusted to 15 | FIXED |

---

## Severity Definitions

- **CRITICAL:** Model cannot be used (circular refs, #REF! errors)
- **HIGH:** Results materially affected (wrong formulas, unrealistic assumptions)
- **MEDIUM:** Affects confidence but not accuracy (limited data, missing analyses)
- **LOW:** Cosmetic or minor usability issues (formatting, column widths)

**Rule:** No CRITICAL or HIGH severity issues in final delivery.
