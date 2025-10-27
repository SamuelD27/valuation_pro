# Excel Formatting Standards for Investment Banking

## Overview

Professional financial models follow strict formatting conventions for clarity, auditability, and consistency. These standards are critical for ValuationPro to produce IB-quality outputs.

## Color Coding Convention

### Cell Colors by Function

**Blue/Light Blue** - Hard-coded inputs (user assumptions)
- RGB: (217, 225, 242) or hex #D9E1F2
- Font: Blue (RGB: 0, 0, 255)
- Use for: Revenue growth rates, multiples, tax rates

**Black** - Formulas (calculations)
- Font: Black (RGB: 0, 0, 0)
- Background: White or no fill
- Use for: All formula-driven cells (EBITDA, NPV, multiples)

**Green** - Links to other sheets/files
- Font: Green (RGB: 0, 176, 80)
- Use for: =OtherSheet!A1 references

**Yellow** - Outputs/Key results
- RGB: (255, 255, 0) or hex #FFFF00
- Font: Bold, Black
- Use for: Enterprise Value, Equity Value, Price Per Share

**Red** - Warnings or negative values
- Font: Red (RGB: 255, 0, 0)
- Use for: Covenant breaches, negative EBITDA, errors

### Example Color-Coding

```
[BLUE]     Revenue Growth Rate:    5.0%     ← User input
[BLACK]    Year 1 Revenue:         =B10*(1+$B$5)    ← Formula
[GREEN]    LTM EBITDA:            ='Income Statement'!H89    ← Link
[YELLOW]   Enterprise Value:       $1,234.5M    ← Key output
[RED]      Leverage Ratio:         7.2x    ← Warning (>6.0x)
```

## Number Formatting

### Standard Formats by Data Type

**Dollars (Millions):**
```
Format: #,##0.0 "M"
Example: 1234.5M
```

**Dollars (Thousands):**
```
Format: #,##0
Example: 1,235
```

**Percentages:**
```
Format: 0.0%
Example: 5.2%
```

**Multiples:**
```
Format: 0.0x
Example: 12.5x
```

**Years:**
```
Format: 0
Example: 2024
```

**Decimals (for rates):**
```
Format: 0.00% or 0.000
Example: 8.75% or 0.0875
```

### Negative Number Display

**Parentheses (preferred):**
```
Format: #,##0.0;(#,##0.0)
Example: (123.4) instead of -123.4
```

**Red font for negatives:**
```
Format: #,##0.0;[Red](#,##0.0)
```

## Cell Alignment and Sizing

### Column Widths

**Standard widths:**
- Label columns (A): 30-40 characters
- Data columns (B-Z): 12-15 characters
- Year columns: 10 characters

### Alignment Rules

**Labels:** Left-aligned
```
Revenue
EBITDA
Free Cash Flow
```

**Numbers:** Right-aligned
```
      1,234.5M
        567.8M
        890.1M
```

**Headers:** Center-aligned, Bold
```
     2023E    2024E    2025E
```

### Row Heights

**Data rows:** 15-18 pixels (default)
**Headers:** 20-25 pixels (bold, centered)
**Separator rows:** 5 pixels (visual spacing)

## Borders and Gridlines

### Top Border (Single Line)

**Use for:** Section headers
```
─────────────────────────
Free Cash Flow Calculation
```

### Double Border (Bottom)

**Use for:** Totals, final calculations
```
Enterprise Value:        1,234.5M
═════════════════════════════════
```

### No Borders

**Standard for:** All data cells
- Excel gridlines provide enough visual structure
- Only use borders for key sections/totals

## Font Standards

### Font Type

**Primary font:** Calibri or Arial (11pt)
**Alternate:** Tahoma (11pt)

**Never use:**
- Times New Roman (too formal)
- Comic Sans (unprofessional)
- Decorative fonts

### Font Styles

**Bold:**
- Headers
- Section titles
- Key outputs (Enterprise Value, IRR)

**Italic:**
- Notes and comments (below tables)
- Assumptions explanations

**Regular:**
- All data and formulas

## Sheet Organization

### Optimal Layout

**Single-Sheet Approach (Preferred for ValuationPro):**
```
Rows 1-10:    Header (Company name, valuation date)
Rows 12-30:   Assumptions section (blue inputs)
Rows 32-60:   Operating model (revenue, EBITDA, FCF)
Rows 62-80:   Valuation calculation (DCF or LBO)
Rows 82-100:  Sensitivity analysis
Rows 102-120: Charts and outputs
```

**Multi-Sheet Approach (Enterprise models):**
```
Sheet 1: Cover Page (Executive Summary)
Sheet 2: Assumptions (All inputs)
Sheet 3: Income Statement
Sheet 4: Balance Sheet
Sheet 5: Cash Flow Statement
Sheet 6: DCF Valuation
Sheet 7: LBO Analysis
Sheet 8: Comps
Sheet 9: Football Field
```

### Sheet Naming

**Good names:**
- Assumptions
- DCF
- LBO
- Comps
- Sensitivity

**Avoid:**
- Sheet1, Sheet2 (generic)
- Very long names (>20 characters)
- Special characters

## Formula Best Practices

### Absolute vs. Relative References

**Use absolute ($) for:**
- Assumptions that don't change
- WACC, tax rate, growth rates

```excel
=D20 * (1 + $C$5)  # D20 varies by year, $C$5 is fixed growth rate
```

**Use relative for:**
- Year-over-year calculations
- Formulas that copy across columns

```excel
=D20 + D21 + D22  # Copies to E20+E21+E22, F20+F21+F22, etc.
```

### Named Ranges

**Define names for key assumptions:**
```
WACC = Assumptions!$C$5
Tax_Rate = Assumptions!$C$6
Terminal_Growth = Assumptions!$C$7
```

**Usage:**
```excel
=NPV(WACC, D20:H20)  # More readable than cell references
```

### Avoid Hardcoding

**Bad:**
```excel
=Revenue * 0.25  # What is 0.25? Tax rate? Margin?
```

**Good:**
```excel
=Revenue * Tax_Rate  # Clear reference to named range
=Revenue * $C$6      # Clear reference to cell with "Tax Rate" label
```

## Headers and Labels

### Section Headers

**Format:**
- Bold, 12-14pt
- Top border (single line)
- Extra spacing (1-2 blank rows before)

**Example:**
```
─────────────────────────────────
FREE CASH FLOW CALCULATION (2023-2027)
─────────────────────────────────
```

### Row Labels

**Indentation for hierarchy:**
```
Revenue
  Product A
  Product B
  
EBITDA
  EBIT
  (+) D&A
```

**Use consistent terminology:**
- "EBITDA" not "Ebitda" or "ebitda"
- "CapEx" not "Capex" or "CAPEX"
- "Free Cash Flow" not "FCF" (spell out first time)

## Conditional Formatting

### Highlight Thresholds

**Leverage covenant breach (>5.0x):**
```
Rule: =D10 > 5.0
Format: Red fill, bold
```

**Interest coverage warning (<2.0x):**
```
Rule: =E15 < 2.0
Format: Yellow fill, orange text
```

**Positive vs. Negative FCF:**
```
Rule: =F20 < 0
Format: Red text
```

### Data Bars (for sensitivity tables)

**Color scale:**
- Green: High values (good)
- Yellow: Mid values
- Red: Low values (bad)

**Example:** IRR sensitivity table
- >25%: Dark green
- 20-25%: Light green
- 15-20%: Yellow
- <15%: Red

## Charts and Visualizations

### Chart Types by Use Case

**Waterfall Chart:**
- Uses: FCF build-up, EV bridge
- Format: Blue positive bars, red negative bars

**Bar Chart:**
- Uses: Comps multiples comparison
- Format: Horizontal bars, sorted by value

**Line Chart:**
- Uses: Revenue/EBITDA projections over time
- Format: Solid line, data point markers

**Football Field:**
- Uses: Valuation range summary
- Format: Horizontal bars with midpoint dots

### Chart Formatting

**Titles:** Bold, 12-14pt, above chart
**Axis Labels:** 10pt, clear units (e.g., "$M" or "%")
**Legend:** Bottom or right, only if multiple series
**Colors:** Consistent with cell color scheme (blue inputs, black outputs)

## Page Layout (for Printing)

### Print Settings

**Orientation:** Landscape (for wide tables)
**Margins:** Narrow (0.5" all sides)
**Scaling:** Fit to 1 page wide (adjust height as needed)

### Headers/Footers

**Header (Left):** Company Name
**Header (Right):** Valuation Date
**Footer (Center):** Page X of Y
**Footer (Right):** File name, Version, Date

**Example:**
```
Header: Apple Inc. DCF Analysis          As of: 12/31/2024
Footer:                  Page 1 of 3     DCF_Model_v3_2024.xlsx
```

### Page Breaks

**Insert manual page breaks:**
- After each major section
- Before sensitivity tables
- Before charts

## Error Checking

### Common Excel Errors to Avoid

**#DIV/0!** - Division by zero
```
Fix: =IFERROR(A1/B1, 0)  # Returns 0 if B1 is zero
```

**#REF!** - Invalid cell reference
```
Fix: Check for deleted rows/columns
```

**#VALUE!** - Wrong data type
```
Fix: Ensure numbers aren't stored as text
```

**#N/A** - Lookup value not found
```
Fix: =IFERROR(VLOOKUP(...), "Not Found")
```

### Circular Reference Warnings

**Intentional circulars (rare in ValuationPro):**
- Enable iterative calculations: File → Options → Formulas → Enable iterative calculation
- Max iterations: 100
- Maximum change: 0.001

**Unintentional circulars:**
- Trace and break the loop
- Use helper columns or separate sheets

## Data Validation

### Dropdown Lists

**For user inputs:**
```
Valuation Method: [DCF | LBO | Comps]
Terminal Value Method: [Gordon Growth | Exit Multiple]
```

**Setup:**
1. Data → Data Validation
2. Allow: List
3. Source: DCF,LBO,Comps

### Input Constraints

**Revenue Growth Rate:** 0% to 30%
**WACC:** 5% to 20%
**Terminal Growth:** 1% to 5%

**Setup:**
1. Data → Data Validation
2. Allow: Decimal
3. Data: between 0.05 and 0.20

## Comments and Documentation

### Cell Comments

**When to add:**
- Complex formulas (explain logic)
- Assumptions (cite source)
- Unusual adjustments (explain why)

**Format:**
```
Comment: "Beta sourced from Bloomberg as of 12/31/2024. 
          Represents 3-year regression vs. S&P 500."
```

### Assumptions Documentation

**Create assumption log:**
```
Row | Assumption         | Value | Source           | Date
─────────────────────────────────────────────────────────
5   | Revenue Growth     | 5.0%  | Management Guide | 12/1/24
6   | WACC              | 9.5%  | CAPM Calculation | 12/1/24
7   | Terminal Growth   | 2.5%  | GDP Forecast     | 12/1/24
```

## Version Control

### File Naming Convention

**Format:**
```
[Company]_[Model]_v[X]_[Date].xlsx
```

**Examples:**
```
AAPL_DCF_v1_2024-12-01.xlsx
TSLA_LBO_v3_2024-12-15.xlsx
```

### Version History Sheet

**Track changes:**
```
Version | Date      | Author | Changes Made
─────────────────────────────────────────────────
v1      | 12/1/24   | JS     | Initial build
v2      | 12/5/24   | JS     | Updated WACC calc
v3      | 12/10/24  | SM     | Added sensitivity
```

## Final Checklist

Before finalizing any Excel output:

- [ ] All inputs are blue, formulas are black
- [ ] Key outputs are highlighted (yellow)
- [ ] Numbers formatted correctly (M, %, x)
- [ ] Negative numbers in parentheses
- [ ] Headers are bold and centered
- [ ] Sheet names are descriptive
- [ ] No hardcoded values in formulas (use cell references)
- [ ] All assumptions documented with sources
- [ ] Circular references resolved
- [ ] Error checks (#DIV/0!, #REF!, etc.) resolved
- [ ] Sensitivity tables included
- [ ] Charts are formatted and titled
- [ ] Page setup configured for printing
- [ ] File saved with proper version name
