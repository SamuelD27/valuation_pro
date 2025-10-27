# WACC (Weighted Average Cost of Capital) Methodology

## Overview

WACC is the blended cost of debt and equity financing, used as the discount rate in DCF valuations.

## Core Formula

```
WACC = (E/V) × Re + (D/V) × Rd × (1 - Tc)
```

**Where:**
- **E** = Market Value of Equity
- **D** = Market Value of Debt
- **V** = E + D (Total Capital)
- **Re** = Cost of Equity
- **Rd** = Cost of Debt
- **Tc** = Corporate Tax Rate

## Cost of Equity (Re) - CAPM

```
Re = Rf + β × (Rm - Rf) + α
```

**Where:**
- **Rf** = Risk-Free Rate (10-year US Treasury yield)
- **β** = Beta (systematic risk vs. market)
- **Rm** = Expected Market Return (typically 10-11% long-term)
- **Rm - Rf** = Market Risk Premium (typically 5-7%)
- **α** = Company-Specific Risk Premium (optional, for small/private companies)

### Risk-Free Rate (Rf)

**Source:** 10-year US Treasury yield

**Typical values:**
- Normal environment: 3-5%
- Low-rate environment: 1-3%
- High-rate environment: 5-7%

**Fetch from:** FRED API, Yahoo Finance, or Treasury.gov

### Beta (β)

**Definition:** Measures stock's volatility relative to market (S&P 500)

**Interpretation:**
- β = 1.0: Moves with market
- β > 1.0: More volatile than market (tech, growth stocks)
- β < 1.0: Less volatile than market (utilities, consumer staples)
- β < 0: Moves opposite to market (rare, e.g., gold miners)

**Sources:**
- Yahoo Finance (historical beta)
- Bloomberg (adjusted beta)
- Manual calculation from historical returns

**Levered vs. Unlevered Beta:**

```
βlevered = βunlevered × [1 + (1 - Tc) × (D/E)]
```

**When to unlever/relever:**
- Use industry average unlevered beta
- Relever using target capital structure

### Market Risk Premium (Rm - Rf)

**Historical US average:** 5-7%

**Standard assumption:** 6% (for most DCF models)

**Adjustments:**
- Emerging markets: +2-5% country risk premium
- Small-cap stocks: +3-5% size premium

### Company-Specific Risk Premium (α)

**Additional risk premium for:**
- **Private companies:** +2-5%
- **Small companies (<$100M revenue):** +2-3%
- **Single-product companies:** +1-2%
- **Emerging market operations:** +2-4%

**Formula with adjustments:**
```
Re = Rf + β × MRP + Size Premium + Private Company Premium
```

## Cost of Debt (Rd)

### Method 1: Weighted Average of Debt Instruments

```
Rd = Σ (Debt_i / Total_Debt) × Interest_Rate_i
```

**Example:**
- Senior Debt: $40M @ 5.5%
- Subordinated Debt: $15M @ 7.5%

```
Rd = (40/55) × 5.5% + (15/55) × 7.5% = 6.05%
```

### Method 2: Interest Expense / Total Debt

```
Rd = Interest Expense / Average Total Debt
```

**Use when:** Actual debt costs are known from financial statements

### Method 3: Credit Spread Approach

```
Rd = Risk-Free Rate + Credit Spread
```

**Credit spreads by rating:**
- AAA/AA: 0.5-1.0%
- A: 1.0-1.5%
- BBB: 1.5-2.5%
- BB (junk): 3.0-4.5%
- B: 4.5-6.0%
- CCC or below: 6.0%+

## Tax Rate (Tc)

**US Federal Corporate Tax Rate:** 21% (as of 2024)

**Add state taxes:** Varies by state (0-12%)
- California: ~8.84%
- Texas: 0%
- New York: ~6.5%

**Effective Tax Rate:**
```
Effective Tc = Federal Rate × (1 - State Rate) + State Rate
```

**Example (California):**
```
Effective Tc = 21% × (1 - 0.0884) + 8.84% = 27.98%
```

**For most models:** Use 25% as reasonable approximation for US companies

## Capital Structure Weights (E/V and D/V)

### Method 1: Current Market Values (Public Companies)

```
E = Market Cap = Share Price × Diluted Shares Outstanding
D = Book Value of Debt (from balance sheet)
V = E + D
```

### Method 2: Target Capital Structure

**Preferred for valuations** - Use industry average or management's target

**Typical ranges by industry:**
- Tech/Software: 90% Equity / 10% Debt
- Utilities: 50% Equity / 50% Debt
- Manufacturing: 60-70% Equity / 30-40% Debt
- Financial Services: 10-20% Equity / 80-90% Debt (highly leveraged)

### Method 3: Comparable Companies Average

Use median capital structure from comps set.

## Complete WACC Calculation Example

**Assumptions:**
- Risk-Free Rate: 4.0%
- Beta: 1.2
- Market Risk Premium: 6.0%
- Cost of Debt (pre-tax): 6.5%
- Tax Rate: 25%
- Target Capital Structure: 70% Equity / 30% Debt

**Step 1: Calculate Cost of Equity**
```
Re = 4.0% + 1.2 × 6.0% = 11.2%
```

**Step 2: Calculate After-Tax Cost of Debt**
```
Rd × (1 - Tc) = 6.5% × (1 - 0.25) = 4.875%
```

**Step 3: Calculate WACC**
```
WACC = 0.70 × 11.2% + 0.30 × 4.875% = 9.3%
```

## Edge Cases & Adjustments

### Negative Debt (Net Cash Position)

**When Cash > Total Debt:**
- Use D = 0 in WACC formula
- WACC = Re (unlevered cost of equity)
- Or use negative debt, which increases WACC slightly

### Circular Reference Issue

**Problem:** WACC depends on capital structure → affects valuation → affects market cap → affects capital structure

**Solution:**
1. Use **target capital structure** (not current)
2. Iterate until convergence (5-10 iterations)
3. Or use industry average capital structure

### Preferred Stock

**If company has preferred stock:**

```
WACC = (E/V) × Re + (D/V) × Rd × (1 - Tc) + (P/V) × Rp
```

**Where:**
- P = Market Value of Preferred Stock
- Rp = Cost of Preferred Stock (dividend yield)
- V = E + D + P

### Private Company Adjustments

**Add company-specific risk premiums:**
```
Re = Rf + β × MRP + Illiquidity Premium + Size Premium
```

**Typical premiums:**
- Illiquidity (lack of marketability): 20-35%
- Size (small company): 3-5%

## Validation Rules

**Reasonable WACC ranges:**
- Mature, stable companies: 7-10%
- Growth companies: 10-15%
- High-risk/early-stage: 15-25%

**Red flags:**
- WACC < 5%: Likely error (too low)
- WACC > 20%: Very high risk or calculation error
- Re < Rd: Cost of equity should always exceed cost of debt

**Component checks:**
- Rf: 1-7% (depending on interest rate environment)
- β: 0.5-2.0 (most companies)
- MRP: 5-7% (historical average)
- Re: 8-18% (typical range)
- Rd (pre-tax): 3-10% (investment grade)

## Excel Cell References

**Cost of Equity calculation:**
```excel
=RiskFreeRate + Beta * MarketRiskPremium
=C7 + C8 * C9
```

**WACC calculation with absolute references:**
```excel
=(E/V)*Re + (D/V)*Rd*(1-Tc)
=($C$4)*$C$7 + ($C$5)*$C$8*(1-$C$9)
```

**After-tax cost of debt:**
```excel
=PreTaxCostOfDebt * (1 - TaxRate)
=C8 * (1 - C9)
```

## Common Errors

1. **Using book value of equity instead of market value**
   - Always use market cap for E

2. **Forgetting tax shield on debt**
   - Must multiply Rd by (1 - Tc)

3. **Inconsistent decimal/percentage format**
   - 4% should be 0.04, not 4
   - Check if inputs are >1 (percentage) or <1 (decimal)

4. **Using levered beta with industry capital structure**
   - If using industry beta, must relever using target capital structure

5. **Ignoring preferred stock**
   - Preferred stock is neither debt nor equity; needs separate term
