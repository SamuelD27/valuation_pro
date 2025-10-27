# DCF (Discounted Cash Flow) Methodology

## Overview

DCF values a company by discounting projected future cash flows to present value using WACC.

## Standard 5-Step Process

1. **Project Free Cash Flows** (typically 5-10 years)
2. **Calculate Terminal Value** (perpetuity value beyond projection period)
3. **Discount to Present Value** using WACC
4. **Calculate Enterprise Value** (sum of PV of FCFs + PV of Terminal Value)
5. **Convert to Equity Value** (EV - Net Debt + Cash)

## Core Formula: Free Cash Flow to Firm (FCFF)

```
FCFF = NOPAT - CapEx - ΔNWC + D&A
```

**Where:**
- **NOPAT** = EBIT × (1 - Tax Rate)
- **CapEx** = Capital Expenditures (negative number)
- **ΔNWC** = Change in Net Working Capital
  - NWC = (Current Assets - Cash) - (Current Liabilities - Short-term Debt)
- **D&A** = Depreciation & Amortization (add back non-cash expense)

**Alternative Calculation:**
```
FCFF = EBITDA × (1 - Tax Rate) + Tax Shield on D&A - CapEx - ΔNWC
```

**Tax Shield on D&A:**
```
Tax Shield = D&A × Tax Rate
```

## Terminal Value Calculation

### Method 1: Gordon Growth (Perpetuity Growth)

```
TV = FCF_final × (1 + g) / (WACC - g)
```

**Where:**
- **g** = Perpetual growth rate (typically 2-3% for GDP growth)
- **FCF_final** = Last year's projected FCF
- **WACC** = Weighted Average Cost of Capital

**CRITICAL VALIDATION:** WACC must be > g (otherwise TV is negative/infinite)

### Method 2: Exit Multiple

```
TV = EBITDA_final × Exit_Multiple
```

**Where:**
- **Exit_Multiple** = EV/EBITDA multiple (from comps or industry average)
- **EBITDA_final** = Last year's projected EBITDA

**Typical multiples by industry:**
- Software/Tech: 10-15x
- Healthcare: 8-12x
- Manufacturing: 6-8x
- Retail: 5-7x

## Present Value Calculation

**Discount each year's FCF:**
```
PV_FCF = FCF_year_n / (1 + WACC)^n
```

**Discount Terminal Value:**
```
PV_TV = TV / (1 + WACC)^n
```

Where n = final projection year

## Enterprise Value to Equity Value Bridge

```
Enterprise Value (EV) = PV of all FCFs + PV of Terminal Value

Equity Value = EV - Net Debt - Preferred Stock - Minority Interest + Cash & Equivalents
```

**Net Debt Calculation:**
```
Net Debt = Total Debt - Cash & Cash Equivalents
```

**Price Per Share:**
```
Price Per Share = Equity Value / Diluted Shares Outstanding
```

## Edge Cases & Validations

### Negative Free Cash Flows

**High-growth companies** may have negative FCFs in early years due to heavy CapEx/R&D.

**Handling:**
- Still discount negative FCFs (reduces PV)
- Ensure terminal year FCF is positive
- Consider using FCFE (Free Cash Flow to Equity) instead if equity is funding losses

### WACC > Terminal Growth Rate

**CRITICAL:** If WACC ≤ g, terminal value formula breaks (negative/infinite).

**Validation:**
```python
if wacc <= terminal_growth_rate:
    raise ValueError(f"WACC ({wacc:.2%}) must be greater than terminal growth rate ({terminal_growth_rate:.2%})")
```

### Missing Financial Data

**Handle gracefully:**
- Use industry averages for missing tax rates (21% for US federal)
- Estimate CapEx as % of revenue (historical average or industry norm)
- Approximate D&A from PP&E if not disclosed

### Unrealistic Terminal Value Dominance

**Terminal Value should be 50-75% of EV** in most mature companies.

**If TV > 90% of EV:**
- Check if growth assumptions are too optimistic
- Consider using exit multiple method instead
- Review projection period length (may need to extend)

## Sensitivity Analysis

**Two-way table:** WACC vs. Terminal Growth Rate

**Typical ranges:**
- WACC: ±200 bps from base case (e.g., 8%, 9%, 10%, 11%, 12%)
- Terminal Growth: 1.5%, 2.0%, 2.5%, 3.0%, 3.5%

**Implementation:**
```python
for wacc in wacc_range:
    for growth in growth_range:
        ev = calculate_dcf(wacc=wacc, terminal_growth=growth)
        sensitivity_matrix[wacc][growth] = ev
```

## Common Errors to Avoid

1. **Circular references** - WACC depends on debt/equity mix, which changes with valuation
   - Solution: Use target capital structure, not current
   
2. **Tax inconsistency** - Using after-tax WACC but forgetting tax shield on interest
   - Solution: Ensure NOPAT calculation properly excludes interest
   
3. **Wrong discount factor** - Discounting to beginning vs. end of year
   - Solution: Mid-year convention: divide by (1 + WACC)^(n - 0.5)
   
4. **Perpetuity formula error** - Using final year FCF instead of next year's FCF
   - Solution: TV = FCF_final × (1 + g) / (WACC - g)

## Reasonable Output Ranges

**Validation checks:**
- WACC: 7-15% (mature companies typically 8-12%)
- Terminal growth: 1.5-3.5% (long-term GDP growth)
- EV/EBITDA (implied): 5-20x (depends on industry)
- Price within ±30% of market price (for public companies)

## Excel Formula Structure

**Cell references should use absolute references for assumptions:**
```excel
=D20*(1+$C$27)/($C$26-$C$27)  # Terminal Value
```

**Year references should be relative:**
```excel
=D12+D14+D16+D18+D10  # FCF calculation (relative column)
```

**Discount factor:**
```excel
=1/((1+$C$26)^D5)  # Where D5 is year number, $C$26 is WACC
```
