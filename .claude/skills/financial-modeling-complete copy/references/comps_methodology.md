# Comparable Company Analysis (Comps) Methodology

## Overview

Comps values a company by comparing trading multiples of similar public companies. This is a relative valuation method (vs. DCF which is intrinsic valuation).

## Core Process

1. **Select comparable companies** (5-15 comps)
2. **Gather financial data** (revenue, EBITDA, market cap, debt)
3. **Calculate trading multiples** (EV/Revenue, EV/EBITDA, P/E)
4. **Normalize and analyze** (quartiles, median, mean)
5. **Apply multiples to target** (derive implied valuation)

## 1. Selecting Comparable Companies

### Selection Criteria

**Primary factors:**
- **Industry/Sector** - Must be in same or adjacent industry
- **Size** - Revenue/market cap within 0.5x to 2.0x of target
- **Geography** - Similar markets (US vs. international)
- **Business Model** - Similar operations and margin profile

**Secondary factors:**
- Growth rate similarity
- Profitability (margin ranges)
- Customer base (B2B vs. B2C)
- End markets served

### Number of Comps

**Ideal:** 6-12 companies
- **Minimum:** 4-5 (statistical validity)
- **Too many (>15):** Dilutes comparability
- **Too few (<4):** Not statistically meaningful

### Industry-Specific Considerations

**Tech/Software:**
- SaaS vs. licensed software
- Recurring revenue % (ARR/MRR)
- Rule of 40 (Growth % + Margin %)

**Healthcare:**
- Regulatory environment
- Patent cliffs
- Reimbursement models

**Manufacturing:**
- Capacity utilization
- Commodity input exposure
- Unionization

## 2. Gathering Financial Data

### Required Data Points

**Market Data (as of valuation date):**
- Current stock price
- Shares outstanding (diluted)
- Market capitalization

**Balance Sheet:**
- Cash and cash equivalents
- Total debt (short-term + long-term)
- Preferred stock (if any)
- Minority interest

**Income Statement:**
- Revenue (LTM and projected)
- EBITDA (LTM and projected)
- EBIT
- Net income
- EPS (diluted)

### Data Sources

- **Public filings:** 10-K, 10-Q (SEC EDGAR)
- **Financial data APIs:** yfinance, Alpha Vantage, Bloomberg
- **Equity research:** Wall Street analyst reports
- **Company presentations:** Investor relations websites

## 3. Calculating Trading Multiples

### Key Formulas

**Enterprise Value (EV):**
```
EV = Market Cap + Total Debt - Cash + Preferred Stock + Minority Interest
```

**Common Multiples:**

#### EV-Based Multiples (Capital Structure Neutral)

**EV / Revenue:**
```
EV/Revenue = Enterprise Value / LTM Revenue
```

**Typical ranges:**
- Software/SaaS: 5-15x
- Healthcare/Pharma: 3-7x
- Manufacturing: 0.5-2.0x
- Retail: 0.3-1.0x

**EV / EBITDA:**
```
EV/EBITDA = Enterprise Value / LTM EBITDA
```

**Typical ranges:**
- Tech: 10-20x
- Healthcare: 8-15x
- Industrials: 6-10x
- Mature/Cyclical: 5-8x

**EV / EBIT:**
```
EV/EBIT = Enterprise Value / LTM EBIT
```

**Use when:** D&A is significant and varies across comps

#### Equity-Based Multiples (Affected by Leverage)

**Price / Earnings (P/E):**
```
P/E = Market Cap / Net Income
P/E = Stock Price / EPS
```

**Typical ranges:**
- Growth stocks: 20-40x
- Market average: 15-20x
- Value stocks: 8-15x

**Price / Book (P/B):**
```
P/B = Market Cap / Book Value of Equity
```

**Use when:** Asset-heavy businesses (banks, real estate)

### LTM vs. Forward Multiples

**LTM (Last Twelve Months):**
- Uses trailing 12 months of actual data
- More reliable (actual results)
- Doesn't account for growth

**NTM (Next Twelve Months) / Forward:**
- Uses analyst projections
- Accounts for expected growth
- Subject to forecast error

**Best practice:** Show both LTM and NTM multiples

### Calculating NTM EBITDA Example

**Quarters:**
- Q1 2024 (actual): $25M
- Q2 2024 (actual): $27M
- Q3 2024 (actual): $28M
- Q4 2024 (projected): $30M

```
NTM EBITDA = $25M + $27M + $28M + $30M = $110M
```

## 4. Normalization and Statistical Analysis

### Handling Outliers

**Identify outliers using:**
- Interquartile range (IQR) method
- Z-score (>2 or <-2 standard deviations)
- Visual inspection

**Example - IQR Method:**
```
Q1 = 25th percentile
Q3 = 75th percentile
IQR = Q3 - Q1

Lower bound = Q1 - 1.5 × IQR
Upper bound = Q3 + 1.5 × IQR

Exclude values outside bounds
```

**When to exclude:**
- Financial distress (negative EBITDA)
- M&A activity (being acquired)
- Extreme leverage (>10x Debt/EBITDA)
- One-time events (asset sales, restructuring)

### Statistical Measures

**Median (preferred):**
- Less sensitive to outliers
- Better for small sample sizes
- Standard for IB comps

**Mean:**
- Use if sample is large and normally distributed
- Sensitive to outliers

**Quartiles:**
- 25th percentile: Low valuation
- Median (50th): Base case
- 75th percentile: High valuation

**Formula:**
```
Percentile(array, k)  # Excel: =PERCENTILE.INC(range, k)
```

## 5. Applying Multiples to Target

### Valuation Range Approach

**Calculate three scenarios:**

**Low Case (25th percentile):**
```
EV_low = Target_EBITDA × Percentile_25_Multiple
Equity_Value_low = EV_low - Net_Debt
```

**Base Case (Median):**
```
EV_base = Target_EBITDA × Median_Multiple
Equity_Value_base = EV_base - Net_Debt
```

**High Case (75th percentile):**
```
EV_high = Target_EBITDA × Percentile_75_Multiple
Equity_Value_high = EV_high - Net_Debt
```

### Implied Price Per Share

```
Price_Per_Share = Equity_Value / Diluted_Shares_Outstanding
```

**Example:**
```
Target EBITDA: $150M
Median EV/EBITDA: 12.0x
EV = $150M × 12.0 = $1,800M
Less: Net Debt = -$300M
Equity Value = $1,500M
Diluted Shares: 100M
Implied Price = $1,500M / 100M = $15.00 per share
```

## Football Field Valuation Chart

**Visual representation of valuation ranges:**

```
DCF Method:         |========•========|  $12-18/share
LBO Analysis:       |=======•========|   $13-19/share  
Trading Comps:      |=======•======|     $11-17/share
Precedent Trans:    |=========•=====|    $14-20/share
52-Week Range:      •---------------•    $10-22/share
                    10  12  14  16  18  20  22
```

**Format:**
- X-axis: Price per share or Enterprise Value
- Each bar: Low to High valuation range
- Dot: Midpoint (median/base case)

## Edge Cases & Adjustments

### Negative EBITDA

**Company has negative EBITDA:**
- Cannot use EV/EBITDA multiple (undefined)
- Use EV/Revenue instead
- Apply appropriate discount for unprofitability

### High Growth Companies

**Adjust for growth differences:**

**PEG Ratio (Price/Earnings to Growth):**
```
PEG = (P/E) / Earnings_Growth_Rate_%
```

**Interpretation:**
- PEG < 1.0: Undervalued relative to growth
- PEG = 1.0: Fairly valued
- PEG > 1.0: Overvalued relative to growth

**Adjust multiples for growth:**
```
Adjusted_Multiple = Comp_Multiple × (Target_Growth / Comp_Growth)
```

### Different Fiscal Year Ends

**Align time periods:**
- Use calendar year or fiscal year consistently
- Convert all comps to same period (e.g., CY2024)
- Adjust for seasonality if necessary

### Different Accounting Standards

**US GAAP vs. IFRS:**
- IFRS may capitalize R&D (US GAAP expenses it)
- Adjust EBITDA to make comparable
- Normalize for one-time items

### Minority Stakes / Equity Investments

**If target owns equity in other companies:**
```
Adjusted_EV = Market_EV + Equity_Investments_at_Market_Value
```

## Common Errors to Avoid

1. **Using inconsistent metrics**
   - Mixing LTM and NTM multiples
   - Comparing companies with different fiscal years

2. **Not normalizing for non-recurring items**
   - One-time gains/losses
   - Restructuring charges
   - Asset impairments

3. **Including non-comparable companies**
   - Different business models
   - Different geographies/regulations
   - Different growth profiles

4. **Ignoring capital structure differences**
   - Use EV-based multiples (not P/E) for highly leveraged comps
   - Adjust for different debt levels

5. **Not checking for staleness**
   - Use current stock prices (not outdated)
   - Refresh data monthly for live models

## Excel Formula Structures

**Market Capitalization:**
```excel
=SharePrice * DilutedShares
=C8 * D8
```

**Enterprise Value:**
```excel
=MarketCap + TotalDebt - Cash + PreferredStock
=E8 + F8 - G8 + H8
```

**EV/EBITDA Multiple:**
```excel
=EnterpriseValue / EBITDA
=I8 / J8
```

**Median Multiple:**
```excel
=MEDIAN(L8:L20)  # Range of EV/EBITDA multiples
```

**25th/75th Percentile:**
```excel
=PERCENTILE.INC(L8:L20, 0.25)  # 25th percentile
=PERCENTILE.INC(L8:L20, 0.75)  # 75th percentile
```

**Implied Valuation (using median):**
```excel
=TargetEBITDA * MedianMultiple - NetDebt
=$C$5 * $C$10 - $C$6
```

## Typical Excel Layout

```
Rows 1-5:    Header and summary stats
Rows 7-10:   Column headers
Rows 12-25:  Comparable companies data (one row per company)
Rows 27-30:  Statistical analysis (Max, 75th, Median, 25th, Min)
Rows 32-40:  Target company valuation calculation
Rows 42-50:  Football field chart
```

## Reasonable Output Ranges

**Validation checks:**
- EV/EBITDA: 5-20x (varies by industry)
- EV/Revenue: 0.5-15x (SaaS highest)
- P/E: 10-30x (growth vs. value)
- Implied price within ±30% of current trading price (for public companies)

**Red flags:**
- Multiple outliers (>25% of sample)
- Huge valuation range (75th/25th ratio > 2.5x)
- Negative multiples (check EBITDA sign)
- Implied valuation >50% from market price (recheck comps selection)
