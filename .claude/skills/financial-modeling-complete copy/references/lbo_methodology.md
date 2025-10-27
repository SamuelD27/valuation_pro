# LBO (Leveraged Buyout) Methodology

## Overview

LBO model values a company from a private equity sponsor's perspective, focusing on returns (IRR/MOIC) from using leverage to amplify equity returns.

## Core Components

1. **Sources & Uses** - Transaction structure and financing
2. **Operating Model** - Revenue, EBITDA projections
3. **Debt Schedule** - Debt paydown waterfall
4. **Exit Analysis** - Sale proceeds at exit
5. **Returns Analysis** - IRR and MOIC calculations

## 1. Sources & Uses of Funds

### Uses (What is being bought)

```
Enterprise Value = Purchase Multiple × LTM EBITDA
Purchase Price (Equity Value) = EV - Existing Debt + Transaction Expenses
Transaction Fees = 2-3% of EV (legal, banking, advisory fees)

Total Uses = Purchase Price + Transaction Fees + Financing Fees
```

**Example:**
```
LTM EBITDA: $100M
Purchase Multiple: 10.0x
Enterprise Value: $1,000M
Less: Existing Debt: -$200M
Purchase Equity Price: $800M
Transaction Fees (2%): $20M
Financing Fees: $15M
─────────────────────────
Total Uses: $835M
```

### Sources (How it's financed)

**Typical LBO Capital Structure:**
```
Senior Debt:        45-50% of Total Capital (4-5x EBITDA)
Subordinated Debt:  10-20% of Total Capital (1-2x EBITDA)
Equity:             30-40% of Total Capital
─────────────────────────────────────────────
Total Sources:      100%
```

**Leverage Ratios:**
- **Total Debt / EBITDA:** 4.0-6.0x (typical LBO leverage)
- **Senior Debt / EBITDA:** 3.0-4.5x
- **Sub Debt / EBITDA:** 1.0-2.0x

**Example:**
```
Senior Debt (4.5x EBITDA):     $450M @ 5.5% (7-year term)
Subordinated Debt (1.5x):      $150M @ 7.5% (8-year term)
Sponsor Equity:                $235M
─────────────────────────────────────────────
Total Sources:                 $835M
```

**Validation:** Total Sources must equal Total Uses

## 2. Operating Model Projections

**Key Drivers:**
- Revenue Growth: 3-8% annually (realistic, not aggressive)
- EBITDA Margin: Improve 50-200 bps through operational improvements
- CapEx: 2-4% of revenue (maintenance) or as % of D&A (100-120%)
- Change in NWC: Proportional to revenue growth

**Projection Period:** 5-7 years (typical hold period)

**Free Cash Flow (before financing):**
```
FCF = EBITDA - Taxes - CapEx - ΔNWC
```

**Note:** Interest expense is NOT deducted (it's in the financing layer)

## 3. Debt Schedule (Cash Flow Waterfall)

### Priority of Cash Flows

1. **Operating Expenses** - Pay bills, run business
2. **Interest Payments** - Senior debt first, then subordinated
3. **Mandatory Amortization** - Required principal payments
4. **Optional Paydown** - Excess cash sweeps
5. **Cash to Equity** - Remaining cash to sponsor

### Debt Paydown Logic

**Senior Debt:**
```
Opening Balance
+ Additions (if any)
- Mandatory Amortization (per schedule)
- Cash Sweep (% of excess FCF)
= Closing Balance

Interest Expense = Average Balance × Interest Rate
```

**Cash Sweep:** Typically 50-75% of excess cash (after mandatory payments)

**Subordinated Debt:**
```
Same structure as senior debt
Interest-only period: 2-3 years (no amortization)
Then mandatory amortization kicks in
```

### Debt Covenants

**Leverage Covenant:** Total Debt / EBITDA < 5.0x (example)
**Interest Coverage:** EBITDA / Interest Expense > 2.0x

**Validation in model:**
```python
if (total_debt / ebitda) > leverage_covenant:
    raise CovenantViolation("Leverage covenant breached")
```

## 4. Exit Analysis

### Exit Assumptions

**Exit Year:** Typically Year 5-7

**Exit Multiple:** EV / EBITDA at exit
- Conservative: Same as entry multiple (e.g., 10.0x)
- Optimistic: +0.5-1.0x multiple expansion (if margins improved)

**Exit Enterprise Value:**
```
Exit EV = Exit Multiple × Final Year EBITDA
```

**Proceeds to Equity:**
```
Gross Proceeds = Exit EV - Remaining Debt
Net Proceeds = Gross Proceeds - Transaction Costs (1-2%)
```

**Example (Year 5 exit):**
```
EBITDA Year 5: $130M
Exit Multiple: 10.5x
Exit EV: $1,365M
Less: Remaining Debt: -$150M
Gross Equity Proceeds: $1,215M
Less: Transaction Costs (1.5%): -$18M
Net Proceeds to Sponsor: $1,197M
```

## 5. Returns Analysis

### IRR (Internal Rate of Return)

**Formula:**
```
NPV = -Initial_Investment + Σ(Cash_Flow_t / (1 + IRR)^t) + Exit_Proceeds / (1 + IRR)^n = 0
```

**Solve for IRR iteratively**

**Target IRR for PE funds:**
- Top-quartile: 25-30%+
- Median: 20-25%
- Acceptable: 15-20%
- Below 15%: Poor deal

**Python calculation:**
```python
import numpy as np

cash_flows = [-initial_equity_investment, 
              cf_year1, cf_year2, cf_year3, 
              cf_year4, cf_year5 + exit_proceeds]
              
irr = np.irr(cash_flows)
```

**Note:** Include any interim cash distributions (dividends) in annual cash flows

### MOIC (Multiple on Invested Capital)

```
MOIC = Total Proceeds / Initial Equity Investment
```

**Example:**
```
Initial Equity: $235M
Exit Proceeds: $1,197M
MOIC = 1,197 / 235 = 5.1x
```

**Interpretation:**
- MOIC < 2.0x: Poor return
- MOIC 2.0-3.0x: Acceptable
- MOIC 3.0-5.0x: Good
- MOIC > 5.0x: Excellent

**Relationship between IRR and MOIC:**
- 5-year hold, 3.0x MOIC → ~25% IRR
- 5-year hold, 5.0x MOIC → ~38% IRR
- 7-year hold, 3.0x MOIC → ~17% IRR

### Sensitivity Analysis

**Three-way sensitivity table:**

**Axes:**
1. Exit Multiple (9.0x, 9.5x, 10.0x, 10.5x, 11.0x)
2. Revenue Growth (Base -2%, Base -1%, Base, Base +1%, Base +2%)
3. Output: IRR or MOIC

**Example table (IRR %):**

| Exit Multiple | -2% Rev | -1% Rev | Base | +1% Rev | +2% Rev |
|---------------|---------|---------|------|---------|---------|
| 9.0x          | 15%     | 17%     | 19%  | 21%     | 23%     |
| 9.5x          | 18%     | 20%     | 22%  | 24%     | 26%     |
| 10.0x         | 21%     | 23%     | 25%  | 27%     | 29%     |
| 10.5x         | 24%     | 26%     | 28%  | 30%     | 32%     |
| 11.0x         | 27%     | 29%     | 31%  | 33%     | 35%     |

## Edge Cases & Validations

### Zero Debt at Exit

**Problem:** If FCF is very strong, debt may be fully paid off before exit.

**Handling:**
- This is actually GOOD (more equity value)
- Track when debt reaches $0
- After payoff, cash accumulates on balance sheet
- Include excess cash in exit equity value

**Validation:**
```python
if closing_debt_balance < 0:
    raise ValueError("Debt cannot be negative. Adjust cash sweep percentage.")
```

### Negative Cash Flow / Covenant Breach

**If operating performance deteriorates:**
- May breach leverage or coverage covenants
- May not generate enough FCF to cover interest

**Model should flag this:**
```python
if ebitda / interest_expense < 2.0:
    warnings.warn("Interest coverage covenant at risk")
```

**Solution:** Equity injection from sponsor (dilutive)

### Unrealistic Leverage

**Check initial leverage:**
```python
if (total_debt / ltm_ebitda) > 7.0:
    raise ValueError("Leverage ratio too high for typical LBO")
```

**Lenders won't finance >6.0-7.0x EBITDA** in most industries

### Missing Amortization Schedule

**If debt schedule shows no paydown:**
- Check that FCF is being correctly calculated
- Verify cash sweep logic is working
- Ensure debt payments are pulling from correct FCF

## Common Errors

1. **Circular reference in debt balance**
   - Interest depends on average balance
   - Balance depends on paydown
   - Paydown depends on FCF minus interest
   - **Solution:** Use prior year's balance or iterate

2. **Not including transaction fees in Uses**
   - Fees typically add 2-5% to purchase price

3. **Forgetting cash sweep / optional paydown**
   - Model should use excess cash to pay down debt
   - Increases returns by reducing interest burden

4. **Wrong interest calculation**
   - Use average balance (opening + closing) / 2
   - Not just opening or closing balance

5. **Inconsistent EBITDA definitions**
   - Sources & Uses should use LTM EBITDA
   - Exit should use projected Year N EBITDA

## Excel Formula Structures

**Opening Debt Balance (Year 1):**
```excel
=Sources!$C$9  # Senior debt from Sources & Uses
```

**Interest Expense:**
```excel
=AVERAGE(D29:D32) * D34  # Average balance × interest rate
```

**Closing Debt Balance:**
```excel
=D29 - D31  # Opening balance - repayment
```

**Cash Available for Debt Paydown:**
```excel
=D16 - D19 - D20  # FCF - mandatory amortization - required reserves
```

**IRR Calculation:**
```excel
=IRR(B100:H100)  # Range of cash flows from Year 0 to Exit
```

**MOIC Calculation:**
```excel
=H102 / B102  # Exit proceeds / Initial equity investment
```

## Typical Excel Layout (Single Sheet)

```
Rows 1-20:   Sources & Uses table
Rows 22-40:  Operating model (Revenue, EBITDA, FCF)
Rows 42-60:  Senior Debt schedule
Rows 62-80:  Subordinated Debt schedule
Rows 82-90:  Exit analysis
Rows 92-100: Returns (IRR, MOIC)
Rows 102-120: Sensitivity tables
```

## Reasonable Output Ranges

**Validation checks:**
- Initial leverage: 4.0-6.5x EBITDA
- IRR: 15-35% (target 20-25%)
- MOIC: 2.0-6.0x (target 3.0x+)
- Debt fully paid or nearly paid by exit
- Exit EV > Entry EV (value creation)
- Equity as % of sources: 25-40%

**Red flags:**
- IRR < 15%: Deal doesn't meet hurdle rate
- MOIC < 2.0x: Poor return
- Debt balance increasing over time: Negative FCF (problem)
- Exit EV < Entry EV: Value destruction
