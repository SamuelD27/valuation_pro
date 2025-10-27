# Financial Concepts - Quick Reference

**Purpose:** Central formula reference and navigation guide for all valuation methodologies.

## Table of Contents

1. [Core Valuation Formulas](#core-valuation-formulas)
2. [DCF (Discounted Cash Flow)](#dcf-discounted-cash-flow)
3. [LBO (Leveraged Buyout)](#lbo-leveraged-buyout)
4. [Comps (Trading Multiples)](#comps-trading-multiples)
5. [Precedent Transactions](#precedent-transactions)
6. [WACC (Cost of Capital)](#wacc-cost-of-capital)
7. [Private Company Adjustments](#private-company-adjustments)
8. [Returns Analysis](#returns-analysis)
9. [When to Read Detailed Files](#when-to-read-detailed-files)

---

## Core Valuation Formulas

### Enterprise Value to Equity Value Bridge

```
Enterprise Value (EV)
- Net Debt (Total Debt - Cash)
- Preferred Stock
- Minority Interest
+ Equity Investments (at market value)
─────────────────────────────
= Equity Value

Price Per Share = Equity Value / Diluted Shares Outstanding
```

### Net Debt Calculation

```
Net Debt = Short-term Debt + Long-term Debt - Cash & Cash Equivalents

Note: If Cash > Debt, Net Debt is negative (net cash position)
```

---

## DCF (Discounted Cash Flow)

**Full methodology:** `dcf_methodology.md`

### Free Cash Flow (FCFF)

```
FCFF = NOPAT - CapEx - ΔNWC + D&A

Where:
  NOPAT = EBIT × (1 - Tax Rate)
  ΔNW = Change in Net Working Capital
  NWC = (Current Assets - Cash) - (Current Liabilities - Short-term Debt)
```

### Terminal Value (Gordon Growth)

```
TV = FCF_final × (1 + g) / (WACC - g)

CRITICAL: WACC must be > g
```

### Terminal Value (Exit Multiple)

```
TV = EBITDA_final × Exit_Multiple

Typical multiples: 6-15x depending on industry
```

### Present Value

```
PV_FCF = FCF_year_n / (1 + WACC)^n

PV_TV = TV / (1 + WACC)^n  [where n = final projection year]
```

### Enterprise Value

```
EV = Σ(PV of projected FCFs) + PV of Terminal Value
```

---

## LBO (Leveraged Buyout)

**Full methodology:** `lbo_methodology.md`

### Sources & Uses

```
USES:
  Purchase Price = Entry Multiple × LTM EBITDA
  Transaction Fees (2-3% of EV)
  Financing Fees
  ─────────────
  Total Uses

SOURCES:
  Senior Debt (4-5x EBITDA) @ 5-7%
  Subordinated Debt (1-2x EBITDA) @ 7-9%
  Sponsor Equity (30-40% of total)
  ─────────────
  Total Sources

CRITICAL: Sources must equal Uses
```

### Free Cash Flow (before financing)

```
FCF = EBITDA - Cash Taxes - CapEx - ΔNWC

Note: Interest is NOT deducted (it's in the financing layer)
```

### Debt Paydown Waterfall

```
Opening Debt Balance
- Mandatory Amortization
- Cash Sweep (50-75% of excess FCF)
= Closing Debt Balance

Interest Expense = Average Balance × Interest Rate
Average Balance = (Opening + Closing) / 2
```

### Exit Analysis

```
Exit EV = Exit Multiple × Final Year EBITDA
Gross Proceeds = Exit EV - Remaining Debt
Net Proceeds = Gross Proceeds - Transaction Costs (1-2%)
```

---

## Comps (Trading Multiples)

**Full methodology:** `comps_methodology.md`

### Enterprise Value

```
EV = Market Cap + Total Debt - Cash + Preferred Stock + Minority Interest
```

### Key Multiples

```
EV/EBITDA = Enterprise Value / LTM EBITDA
EV/Revenue = Enterprise Value / LTM Revenue
P/E = Market Cap / Net Income = Price Per Share / EPS
P/B = Market Cap / Book Value of Equity
```

### Applying to Target

```
Implied EV = Target Metric × Median Multiple from Comps

Example:
  Target EBITDA: $100M
  Median EV/EBITDA from comps: 12.0x
  Implied EV = $100M × 12.0x = $1,200M
```

---

## Precedent Transactions

**Full methodology:** `precedent_transactions.md`

### Key Difference from Trading Comps

```
Precedent Transactions = Actual M&A deal multiples (includes control premium)
Trading Comps = Public market trading multiples (minority stake)

Control Premium typically: 20-40%
```

### Transaction Multiples

```
Transaction EV / LTM EBITDA
Transaction EV / LTM Revenue
Transaction Price / Book Value

Premium to Unaffected Price = (Offer Price - Pre-announcement Price) / Pre-announcement Price
```

---

## WACC (Cost of Capital)

**Full methodology:** `wacc_methodology.md`

### Core Formula

```
WACC = (E/V) × Re + (D/V) × Rd × (1 - Tc)

Where:
  E = Market Value of Equity
  D = Market Value of Debt
  V = E + D (Total Capital)
  Re = Cost of Equity
  Rd = Cost of Debt (pre-tax)
  Tc = Corporate Tax Rate
```

### Cost of Equity (CAPM)

```
Re = Rf + β × (Rm - Rf)

Where:
  Rf = Risk-Free Rate (10Y Treasury)
  β = Beta (systematic risk)
  Rm - Rf = Market Risk Premium (typically 6%)
```

### Levered Beta

```
βlevered = βunlevered × [1 + (1 - Tc) × (D/E)]

Use when adjusting for different capital structures
```

---

## Private Company Adjustments

**Full methodology:** `private_company_valuation.md`

### Discount for Lack of Marketability (DLOM)

```
DLOM = 20-35% for private companies

Adjusted Equity Value = Public Market Equity Value × (1 - DLOM)
```

### Size Premium

```
Small Company Premium = 2-5%

Adjusted Re = CAPM Cost of Equity + Size Premium
```

### Control Premium

```
Control Premium = 20-40%

Control Value = Minority Value × (1 + Control Premium)
```

### Illiquidity Discount

```
Illiquidity Discount = 20-30%

Applies to: Restricted stock, private placements, illiquid assets
```

---

## Returns Analysis

### IRR (Internal Rate of Return)

```
NPV = -Initial_Investment + Σ(CF_t / (1 + IRR)^t) = 0

Solve for IRR iteratively

Python: numpy.irr(cash_flows)
Excel: =IRR(cash_flow_range)
```

### MOIC (Multiple on Invested Capital)

```
MOIC = Total Proceeds / Initial Equity Investment

Example:
  Initial Equity: $200M
  Exit Proceeds: $600M
  MOIC = 600 / 200 = 3.0x
```

### Relationship Between IRR and MOIC

```
5-year hold:
  2.0x MOIC ≈ 15% IRR
  3.0x MOIC ≈ 25% IRR
  4.0x MOIC ≈ 32% IRR
  5.0x MOIC ≈ 38% IRR
```

### Cash-on-Cash Return

```
Cash-on-Cash = Annual Cash Distribution / Initial Equity Investment

Used for: Real estate, dividend-paying investments
```

---

## When to Read Detailed Files

### For DCF Implementation
→ Read `dcf_methodology.md` (full formulas, edge cases, sensitivity)
→ Read `wacc_methodology.md` (discount rate calculation)

### For LBO Implementation
→ Read `lbo_methodology.md` (sources & uses, debt waterfall, covenants)
→ Read `industries/private_equity.md` (PE-specific structures)

### For Comps Analysis
→ Read `comps_methodology.md` (selection criteria, normalization, outliers)
→ Read industry-specific file (e.g., `industries/saas_tech.md`)

### For M&A Valuation
→ Read `precedent_transactions.md` (control premiums, synergies)
→ Read `private_company_valuation.md` (DLOM, adjustments)

### For Venture/Startup Valuation
→ Read `venture_capital_valuation.md` (VC method, option pool, liquidation preferences)

### For Excel Output
→ Read `excel_standards.md` (IB formatting, colors, formulas)

### For Validation
→ Read `validation_rules.md` (acceptable ranges, error detection)
→ Run validation scripts: `validate_dcf.py`, `validate_lbo.py`

---

## Quick Validation Ranges

| Metric | Minimum | Maximum | Typical |
|--------|---------|---------|---------|
| **DCF** |
| WACC | 5% | 25% | 8-12% |
| Terminal Growth | 1.5% | 5% | 2-3% |
| Terminal Value % of EV | 40% | 90% | 50-75% |
| **LBO** |
| Initial Leverage | 3.0x | 7.0x | 4-6x EBITDA |
| IRR | 10% | 40% | 20-25% |
| MOIC | 1.5x | 6.0x | 2.5-4.0x |
| **Comps** |
| EV/EBITDA | 4x | 25x | 8-15x |
| EV/Revenue | 0.5x | 20x | 1-5x |
| P/E | 8x | 40x | 15-25x |

---

## Navigation Guide

**Methodology Files:**
- `dcf_methodology.md` - Discounted Cash Flow
- `lbo_methodology.md` - Leveraged Buyout
- `comps_methodology.md` - Trading Comparables
- `precedent_transactions.md` - M&A Comparables
- `ddm_methodology.md` - Dividend Discount Model
- `sotp_methodology.md` - Sum-of-the-Parts
- `venture_capital_valuation.md` - VC/Startup Valuation
- `wacc_methodology.md` - Cost of Capital

**Supporting Files:**
- `private_company_valuation.md` - DLOM, control premiums
- `excel_standards.md` - IB formatting
- `validation_rules.md` - Quality checks

**Industry-Specific:**
- `industries/saas_tech.md` - Software/SaaS
- `industries/healthcare.md` - Healthcare/Pharma
- `industries/manufacturing.md` - Industrials/Manufacturing
- `industries/financial_services.md` - Banks/Insurance
- `industries/private_equity.md` - PE/M&A specific (DEEP content)

**Scripts:**
- `validate_dcf.py` - DCF validation CLI tool
- `validate_lbo.py` - LBO validation CLI tool
- `validate_comps.py` - Comps validation CLI tool
- `chart_examples.py` - Excel chart generation code
