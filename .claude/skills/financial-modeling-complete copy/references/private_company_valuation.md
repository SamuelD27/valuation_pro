# Private Company Valuation Methodology

## Table of Contents

1. [Overview](#overview)
2. [Key Valuation Differences](#key-valuation-differences)
3. [Discount for Lack of Marketability (DLOM)](#discount-for-lack-of-marketability-dlom)
4. [Size Premium](#size-premium)
5. [Control Premium](#control-premium)
6. [Minority Discount](#minority-discount)
7. [Illiquidity Adjustments](#illiquidity-adjustments)
8. [Restricted Stock Studies](#restricted-stock-studies)
9. [IPO Studies](#ipo-studies)
10. [Application Framework](#application-framework)

## Overview

Private company valuation requires adjustments to public company valuation methodologies to account for lack of liquidity, size, and control considerations.

**Key principle:**
```
Private Company Value = Public Equivalent Value × (1 - DLOM) × Other Adjustments
```

## Key Valuation Differences

### Public vs. Private Companies

| Factor | Public Company | Private Company |
|--------|---------------|-----------------|
| **Liquidity** | High (daily trading) | Low/None |
| **Information** | Extensive disclosure | Limited |
| **Governance** | Strong (SOX, etc.) | Variable |
| **Access to Capital** | Easy (equity markets) | Difficult/Expensive |
| **Valuation** | Market-determined | Appraisal-required |

### Typical Valuation Impact

```
Public Company Value: $100M (trading comps)

Adjustments:
- DLOM (25%): -$25M
- Size Premium (3%): -$3M
───────────────────────
Private Company Value: $72M

Net Discount: 28%
```

## Discount for Lack of Marketability (DLOM)

### Definition

DLOM compensates for the inability to quickly sell shares at fair market value.

**Applies to:**
- Minority stakes in private companies
- Restricted stock in public companies
- Illiquid partnership interests

### DLOM Ranges

**Empirical studies show:**
```
Restricted Stock Studies: 20-30% discount
Pre-IPO Studies: 40-50% discount
Private Company Sales: 20-35% discount

Typical DLOM: 25-30% for private companies
```

### Factors Affecting DLOM

**Higher DLOM (30-40%):**
- No near-term liquidity event
- Closely held (family business)
- Restrictive transfer provisions
- Weak financial performance
- Small company (<$10M revenue)

**Lower DLOM (15-25%):**
- Near-term IPO or sale expected
- Professional management
- Strong financial performance
- Put rights or redemption features
- Larger company (>$100M revenue)

### DLOM Calculation Methods

**Method 1: Comparable Sales**
```
Find private company sales in same industry

Example:
  5 recent private SaaS company sales:
    Company A: 30% discount to public comps
    Company B: 25% discount
    Company C: 28% discount
    Company D: 32% discount
    Company E: 27% discount
  
  Median DLOM: 28%
```

**Method 2: Restricted Stock Studies**
```
Analyze discounts on restricted public company stock

SEC Rule 144:
  Pre-2008: 1-year holding period
  Post-2008: 6-month holding period
  
Observed discounts: 20-35%
```

**Method 3: Option Pricing Model**
```
Treat DLOM as cost of a put option

DLOM = Put Option Value / Stock Price

Inputs:
- Stock volatility
- Risk-free rate
- Holding period

Black-Scholes based calculation
```

## Size Premium

### Overview

Small companies have higher cost of capital due to higher risk.

**Size premium formula:**
```
Adjusted Cost of Equity = CAPM Cost of Equity + Size Premium

Re_adjusted = Rf + β × MRP + Size Premium
```

### Size Premium by Company Size

**Duff & Phelps Size Study:**

| Market Cap | Size Premium |
|------------|-------------|
| **Micro-Cap (<$100M)** | 4.0-6.0% |
| **Small-Cap ($100M-$500M)** | 3.0-4.0% |
| **Mid-Cap ($500M-$2B)** | 2.0-3.0% |
| **Large-Cap ($2B-$10B)** | 1.0-2.0% |
| **Mega-Cap (>$10B)** | 0.0-0.5% |

**Alternative: Revenue-based**

| Revenue | Size Premium |
|---------|-------------|
| **<$10M** | 5.0-6.0% |
| **$10M-$50M** | 4.0-5.0% |
| **$50M-$100M** | 3.0-4.0% |
| **$100M-$500M** | 2.0-3.0% |
| **>$500M** | 0.5-2.0% |

### Application Example

```
Base WACC Calculation:
  Risk-free rate: 4.0%
  Beta: 1.2
  MRP: 6.0%
  Cost of Equity = 4.0% + 1.2×6.0% = 11.2%

Size Adjustment:
  Company revenue: $25M
  Size premium: 4.5%
  Adjusted Cost of Equity = 11.2% + 4.5% = 15.7%
```

## Control Premium

### Definition

Control premium represents additional value from ability to control company decisions.

**Control rights include:**
- Elect board of directors
- Set strategy and operations
- Declare dividends
- Approve M&A transactions
- Change capital structure

### Control Premium Ranges

**Empirical data:**
```
Median Control Premium: 30%
25th percentile: 20%
75th percentile: 40%

Industry-specific:
  Tech/Software: 35-45%
  Healthcare: 30-40%
  Manufacturing: 25-35%
  Utilities: 15-25%
```

### When to Apply

**Apply control premium:**
```
Valuing controlling interest (>50%)
Buyer acquiring control
Strategic M&A analysis

Control Value = Minority Value × (1 + Control Premium)

Example:
  Minority value (per share): $20
  Control premium: 30%
  Control value = $20 × 1.30 = $26
```

**Do NOT apply control premium:**
```
Minority stakes (<50%)
Already using precedent transaction comps (premium included)
Passive investment analysis
```

### Control Premium vs. Synergies

**Important distinction:**
```
Control Premium: Generic value from control (any buyer)
Synergies: Buyer-specific value creation

Total M&A Premium = Control Premium + Synergy Premium

Example:
  Trading price: $50
  + Control premium (25%): +$12.50
  = Control value: $62.50
  + Synergies (15%): +$9.38
  = Strategic buyer price: $71.88
```

## Minority Discount

### Definition

Minority discount is the inverse of control premium - reduction in value for lack of control.

**Formula:**
```
Minority Discount = 1 - [1 / (1 + Control Premium)]

Example:
  Control premium: 30%
  Minority discount = 1 - (1/1.30) = 23.1%
```

### Application

```
Control Value per Share: $100

Apply Minority Discount:
  Minority discount: 23%
  Minority Value = $100 × (1 - 0.23) = $77

OR (algebraically equivalent):
  Minority Value = $100 / 1.30 = $77
```

### Levels of Control

| Ownership % | Control Level | Discount |
|-------------|--------------|----------|
| **>50%** | Full control | 0% |
| **25-50%** | Significant influence | 10-15% |
| **10-25%** | Board seat possible | 20-25% |
| **<10%** | Passive minority | 25-35% |

## Illiquidity Adjustments

### Types of Illiquidity

**1. Holding Period Restrictions:**
```
Cannot sell for specified period

Discount based on:
- Length of restriction
- Volatility of value
- Cost of capital

Typical: 5% per year of restriction
```

**2. Transfer Restrictions:**
```
Right of first refusal (ROFR)
Consent requirements
Buy-sell agreements

Typical: 5-15% discount
```

**3. Thin Market:**
```
Few potential buyers
Industry-specific
Geographic limitations

Typical: 10-20% discount
```

### Cumulative Discounts

**Layering approach:**
```
Public Equivalent Value: $100M

Step 1: Apply size premium
  Adjust WACC by +3%
  PV impact: -$15M
  Value: $85M

Step 2: Apply DLOM
  DLOM: 25%
  Discount: $85M × 0.25 = $21M
  Value: $64M

Step 3: Apply minority discount (if applicable)
  Minority discount: 23%
  Discount: $64M × 0.23 = $15M
  Final value: $49M

Total Discount: 51% from public equivalent
```

**Note:** Order matters! Apply sequentially, not additively.

## Restricted Stock Studies

### Methodology

Studies compare restricted stock prices to freely trading stock of same company.

**Key studies:**
- SEC institutional investor study (1971): 26% average discount
- Moroney study (1973): 35% average discount
- Maher study (1976): 35% average discount
- Gelman study (1983): 33% average discount
- Johnson study (2001): 20% average discount

**Modern era (post-2008):**
- 6-month holding period (vs. 1-year pre-2008)
- Discounts: 15-25%

### Factors Affecting Discount

**Higher restricted stock discount:**
- Longer holding period
- Higher volatility
- Smaller company
- Weaker financials

**Lower restricted stock discount:**
- Registration rights
- Shorter holding period
- Larger company
- Strong financials

## IPO Studies

### Pre-IPO Transaction Studies

Compare prices of private placements shortly before IPO to eventual IPO price.

**Emory Studies (1997-2020):**
```
Median discount by time before IPO:
  0-3 months: 25%
  3-6 months: 30%
  6-12 months: 35%
  12-18 months: 40%
  18-24 months: 45%
```

**Interpretation:**
- Reflects DLOM + uncertainty about IPO success
- Higher discounts for longer pre-IPO periods
- Validates DLOM of 25-35% for illiquid private stock

## Application Framework

### Decision Tree

**Step 1: Determine base valuation**
```
Use DCF, Comps, or other method
Result: Public-equivalent value
```

**Step 2: Is it a private company?**
```
Yes → Apply DLOM (typically 25-30%)
No → Skip to Step 4
```

**Step 3: Apply size premium**
```
Adjust cost of capital for company size
Impact on WACC: +2-5%
```

**Step 4: Determine ownership level**
```
>50% control → No additional discount
<50% minority → Apply minority discount (20-30%)
```

**Step 5: Other illiquidity factors?**
```
Holding restrictions → Apply additional 5-15%
Transfer restrictions → Apply additional 5-10%
```

### Example: Full Valuation

**Target:** Private SaaS company, 20% stake

```
Step 1: DCF Valuation (public-equivalent)
  Equity Value: $100M

Step 2: Apply DLOM
  DLOM: 25%
  Value: $100M × (1 - 0.25) = $75M

Step 3: Apply size premium
  Revenue: $20M → size premium 4%
  Adjust WACC: 10% → 14%
  Re-run DCF: $82M → $82M × (1 - 0.25) = $61M

Step 4: Apply minority discount
  Ownership: 20% (minority)
  Minority discount: 23%
  Value: $61M × (1 - 0.23) = $47M

Step 5: 20% stake value
  Total value: $47M
  20% stake: $47M × 0.20 = $9.4M

Implied value per share (10M shares): $0.94
```

### When NOT to Apply Adjustments

**DLOM:**
- Already using private company transactions (discount baked in)
- Valuing for immediate sale (liquidity event)
- Controlling interest being sold

**Size premium:**
- Already using public comps of similar size
- Company has access to public markets

**Control/Minority:**
- Already using appropriate comp set
- Valuing entire company (not specific stake)

## Excel Implementation

**DLOM Calculation:**
```excel
=PublicValue * (1 - DLOM)
=C10 * (1 - C11)
```

**Size-Adjusted WACC:**
```excel
=BaseWACC + SizePremium
=C15 + C16
```

**Minority Discount:**
```excel
=1 - (1 / (1 + ControlPremium))
=1 - (1 / (1 + C20))
```

**Cumulative Adjustment:**
```excel
=PublicValue * (1 - DLOM) * (1 - MinorityDiscount)
=C10 * (1 - C11) * (1 - C22)
```

## Validation Ranges

**DLOM:** 15-40% (typically 25-30%)
**Size Premium:** 0-6% added to cost of equity
**Control Premium:** 15-45% (typically 25-35%)
**Minority Discount:** 15-35% (typically 20-30%)

**Red flags:**
- Total discount >60% (check for double-counting)
- DLOM <15% for truly illiquid company
- Control premium <20% for genuine control transfer
