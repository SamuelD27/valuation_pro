# Private Equity & M&A - Deep Dive

## Table of Contents

1. [PE Fund Structure & Economics](#pe-fund-structure--economics)
2. [LBO Transaction Structures](#lbo-transaction-structures)
3. [Debt Financing](#debt-financing)
4. [Operational Value Creation](#operational-value-creation)
5. [Portfolio Company Management](#portfolio-company-management)
6. [Exit Strategies](#exit-strategies)
7. [Returns Analysis](#returns-analysis)
8. [Deal Sourcing & Diligence](#deal-sourcing--diligence)
9. [Management Incentive Plans](#management-incentive-plans)
10. [Advanced LBO Structures](#advanced-lbo-structures)

---

## PE Fund Structure & Economics

### Fund Structure

**Limited Partnership (LP) Structure:**
```
Limited Partners (LPs) → 99% ownership
  - Pension funds, endowments, insurance companies
  - Family offices, sovereign wealth funds
  - Commit capital, limited liability

General Partner (GP) → 1% ownership
  - PE firm managing the fund
  - Unlimited liability
  - Makes all investment decisions
```

### 2 & 20 Fee Structure

**Management Fees:**
```
Annual Management Fee = 2% × Committed Capital (first 5 years)
                      = 2% × Invested Capital (after investment period)

Example:
  $1B fund
  Year 1-5: $20M/year management fee
  Year 6+: $15M/year (if 75% invested)
```

**Carried Interest (Carry):**
```
Carry = 20% of profits above hurdle rate

Typical Hurdle Rate: 8% IRR preferred return to LPs

Distribution Waterfall:
1. Return of LP capital (100% to LPs)
2. Preferred return (8% IRR to LPs)
3. GP catch-up (until GP has 20% of profits)
4. Remaining profits split 80/20 (LPs/GP)
```

### Fund Lifecycle

```
Investment Period: Years 1-5
  - Deploy capital into portfolio companies
  - Typically invest in 10-20 companies

Harvest Period: Years 5-10
  - Exit investments
  - Return capital + profits to LPs

Extensions: +1 to +2 years common
```

---

## LBO Transaction Structures

### Standard LBO Structure

**Capital Stack:**
```
Senior Debt:           40-50%   @ 5.5-7.0%   [L+450-550 bps]
Subordinated Debt:     10-20%   @ 8-10%      [L+700-900 bps]
Mezzanine/PIK:        0-10%    @ 12-15%     [PIK toggle]
Preferred Equity:      0-5%     @ 12-14%     [dividend]
Common Equity:         30-40%   @ N/A        [residual]
─────────────────────────────────────────────
Total:                 100%
```

**Leverage Ratios by Vintage:**
```
Pre-2008: 6-7x Total Debt / EBITDA
2009-2019: 4-5x (post-crisis deleveraging)
2020-2023: 5-6x (return to higher leverage)
2024+: 4.5-5.5x (rising rates impact)
```

### Syndicated Loan Structure

**Term Loan B (TLB):**
- Most common senior debt instrument
- 7-year maturity
- SOFR + 400-500 bps spread
- 1% annual amortization (bullet repayment)
- Broadly syndicated to CLOs and loan funds

**Revolving Credit Facility:**
- $10-50M (smaller deals) to $500M+ (larger deals)
- Used for working capital fluctuations
- Undrawn commitment fee: 0.25-0.50%

**Second Lien:**
- Sits behind first lien but ahead of mezzanine
- SOFR + 700-800 bps
- 8-year maturity
- Less common post-2010

### Covenant Structures

**Covenant-Lite (Cov-Lite):**
```
Maintenance Covenants: NONE (on term loans)
Incurrence Covenants: Only triggered by specific actions
  - Restricted payments
  - Additional debt incurrence
  - Asset sales

Typical since 2015+ for sponsored deals
```

**Springing Covenants (Revolver):**
```
Only tested when revolver is >35% drawn

Maximum Total Leverage: 5.5x-6.0x
Minimum Interest Coverage: 2.0x-2.5x
Minimum Fixed Charge Coverage: 1.0x-1.2x
```

---

## Debt Financing

### Debt Sizing

**Senior Debt Capacity:**
```
Senior Debt = 4.0-4.5x LTM EBITDA
            OR
            = 3.5-4.0x Current Year EBITDA

Stress Test: Can company cover 2.0x interest at trough EBITDA?
```

**Total Debt Capacity:**
```
Total Debt / EBITDA Tests:
  Stable, mature business: 5.5-6.0x
  Cyclical business: 4.0-4.5x
  High-growth business: 4.5-5.5x
  
Interest Coverage Test:
  EBITDA / Interest Expense > 2.0x at trough
```

### Debt Paydown Strategy

**Mandatory Amortization:**
```
Term Loan B: 1% per year (de minimis)
Term Loan A: 5-10% per year (less common)

Payment = Outstanding Balance × Amortization %
```

**Cash Sweep:**
```
Typical Structure:
  50% of Excess Cash Flow sweeps to debt paydown

Excess Cash Flow = 
  EBITDA
  - Cash Interest
  - Cash Taxes
  - CapEx
  - Mandatory Amortization
  - ΔNWC
  - Restricted Payments (dividends, distributions)
```

**Debt Paydown Priority (Waterfall):**
```
1. Pay interest (senior first, then subordinated)
2. Mandatory amortization
3. Cash sweep to senior debt
4. Optional prepayment to subordinated debt
5. Remaining cash to equity (or retained)
```

### Interest Rate Management

**SOFR Transition:**
```
Post-LIBOR (2023+):
  SOFR (Secured Overnight Financing Rate)
  Floor: 0.50-1.00%
  Spread: 400-550 bps for TLB

Example:
  SOFR: 5.0%
  Floor: 0.75%
  Spread: +450 bps
  All-in Rate: 5.0% + 4.50% = 9.50%
```

**Interest Rate Hedging:**
```
Swap Strategy:
  Hedge 50-75% of debt
  3-5 year swap term
  Pay fixed (e.g., 4.5%), receive floating

Cap Strategy:
  Buy cap at 5.0% or 6.0%
  Cheaper than swap but downside protection
```

---

## Operational Value Creation

### 100-Day Plan

**Immediate Actions (Days 1-30):**
```
- Install new management (CEO, CFO if needed)
- Establish board reporting cadence (monthly)
- Implement weekly KPI dashboards
- Begin vendor/customer meetings
- Launch operational assessment
```

**Quick Wins (Days 30-100):**
```
- Renegotiate top supplier contracts (5-10% savings)
- Implement price increases (2-5%)
- Reduce headcount in non-core areas (if needed)
- Accelerate collections (improve DSO by 5-10 days)
- Defer non-critical CapEx
```

### Value Creation Levers

**Revenue Growth (30-40% of value creation):**
```
Organic Growth:
  - Pricing optimization (2-3% annual increase)
  - Sales force effectiveness (CRM, comp plans)
  - New product launches
  - Geographic expansion

Add-on Acquisitions:
  - Bolt-on competitors (consolidation play)
  - Adjacent products/services
  - Geographic fill-ins
  - Typical: 2-5 add-ons per platform
```

**Margin Expansion (25-35% of value creation):**
```
Gross Margin:
  - Vendor negotiation (5-10% cost savings)
  - Product mix optimization
  - Pricing actions

SG&A Reduction:
  - Centralize back-office (finance, HR, IT)
  - Renegotiate insurance, rent
  - Reduce travel/entertainment
  - Target: 200-300 bps EBITDA margin expansion
```

**Working Capital Improvement (10-15% of value creation):**
```
DSO (Days Sales Outstanding):
  - Accelerate collections
  - Offer early payment discounts
  - Target: Reduce DSO by 5-10 days

DPO (Days Payable Outstanding):
  - Extend payment terms with vendors
  - Target: Increase DPO by 5-10 days

Inventory Turns:
  - JIT inventory management
  - SKU rationalization
  - Target: Increase turns by 1-2x
```

**Multiple Expansion (20-30% of value creation):**
```
Drivers:
  - Improved growth profile (show momentum)
  - Margin expansion (show operational excellence)
  - Reduced customer concentration
  - Improved management team
  - Platform for add-ons (strategic buyer premium)

Typical: +0.5 to +1.5x exit multiple expansion
```

**Deleveraging (15-20% of value creation):**
```
Natural deleveraging from FCF generation
  Initial: 5.0x Debt/EBITDA
  Exit (Year 5): 2.0-3.0x Debt/EBITDA
  
Each 1.0x of debt paydown = equity value increase
```

---

## Portfolio Company Management

### Board Composition

**Standard PE Board:**
```
5-7 Total Members:
  - 2-3 PE firm representatives (including board chair)
  - CEO (management representative)
  - 2-3 Independent directors (operating partners, industry experts)
  
Meeting Frequency: Monthly or Quarterly
```

### Financial Reporting

**Monthly Board Package Contents:**
```
1. Executive Summary (1 page)
   - Key highlights, lowlights, actions

2. Financial Dashboard
   - Revenue vs. budget/LY
   - EBITDA vs. budget/LY
   - Cash flow and liquidity
   - Leverage ratio tracking

3. KPI Dashboard (10-15 metrics)
   - Customer: NPS, retention, CAC, LTV
   - Operations: Utilization, capacity, quality
   - Financial: GM%, EBITDA%, DSO, DPO
   
4. Variance Analysis
   - Budget vs. actual explanation
   
5. 13-Week Cash Flow Forecast
   - Rolling forecast update
   
6. Debt Compliance Certificate
   - Covenant calculations
```

### Management Incentive Plans (MIP)

**Equity Pool Structure:**
```
Management Equity Pool: 10-20% of equity

Allocation:
  CEO: 30-50% of pool
  CFO: 15-25% of pool
  Other C-suite: 5-10% each
  VP-level: 2-5% each
```

**Vesting Schedule:**
```
Time-Based Vesting:
  4-year vest with 1-year cliff
  25% per year thereafter

Performance-Based Vesting:
  Tranches tied to MOIC:
    - 50% vests at 2.0x MOIC
    - 75% vests at 2.5x MOIC
    - 100% vests at 3.0x MOIC
```

**Option Strike Price:**
```
Common Stock FMV at close
  Determined by 409A valuation
  Typically 5-10% of preferred equity value

Example:
  Enterprise Value: $500M
  Debt: $300M
  Preferred Equity (PE): $200M
  Common Equity FMV: $20M (10% of preferred)
  
  Management buys options at $20M strike
```

---

## Exit Strategies

### Exit Route Analysis

**Secondary Buyout (40-50% of exits):**
```
Sell to another PE firm

Advantages:
  + Quick process (3-4 months)
  + Certainty of close
  + Competitive auction dynamics

Disadvantages:
  - Buyer scrutiny (fellow PE)
  - May leave value on table vs. strategic

Typical Buyer Profile:
  - Larger fund (platform for add-ons)
  - Different strategy (operational vs. growth)
```

**Strategic Sale (30-40% of exits):**
```
Sell to strategic buyer (corporation)

Advantages:
  + Highest valuation (synergies)
  + Multiple expansion potential

Disadvantages:
  - Longer process (6-9 months)
  - Integration risk
  - Antitrust concerns

Synergy Premium: 20-40% above standalone value
```

**IPO (5-10% of exits):**
```
Take company public

Advantages:
  + Highest potential valuation
  + Partial liquidity (can hold stake)
  + Prestige

Disadvantages:
  - Longest process (9-12 months)
  - Market risk
  - High cost ($5-10M+)
  - Ongoing compliance burden

Requirements:
  - $100M+ EBITDA (typically)
  - Clean financials
  - Strong growth story
```

**Dividend Recap (not an exit):**
```
Refinance debt to pay dividend to equity

Use Cases:
  - Return capital to LPs mid-hold
  - Reset cost basis
  - Hedge if exit timing uncertain

Structure:
  - Add 1-2x EBITDA of new debt
  - Pay proceeds as dividend
  - Increases leverage
```

### Exit Timing Optimization

**Optimal Exit Windows:**
```
Years 3-5: Sweet spot
  - Demonstrated value creation
  - Still has growth story
  - Minimizes J-curve impact on fund returns

Years 5-7: Most common
  - Full operational improvements realized
  - Multiple exit routes available

Years 7+: Late
  - Fund pressure to exit
  - May need to accept lower multiple
```

**Exit Preparation (12-18 months out):**
```
Financial:
  - Clean up accounting (GAAP compliance)
  - Install robust financial systems
  - Normalize EBITDA (back out one-time items)

Operational:
  - Strengthen management team
  - Document processes
  - Reduce customer concentration

Growth:
  - Show momentum (accelerating growth)
  - Visibility into pipeline
  - New products launching
```

---

## Returns Analysis

### J-Curve Effect

```
Fund IRR by Year:
  Year 1: -5% (fees, expenses)
  Year 2: -2%
  Year 3: 5% (first exits)
  Year 4: 12%
  Year 5: 18%
  Year 6: 22%
  Year 7: 25%
  Years 8-10: 23-28% (final exits)
  
Early exits improve fund IRR significantly
```

### DPI, RVPI, TVPI Metrics

**DPI (Distributions to Paid-In Capital):**
```
DPI = Cumulative Distributions / Paid-In Capital

Measures: Cash returned to LPs
Target: >1.5x by Year 5, >2.0x by fund end
```

**RVPI (Residual Value to Paid-In Capital):**
```
RVPI = NAV of Remaining Investments / Paid-In Capital

Measures: Unrealized value still in fund
```

**TVPI (Total Value to Paid-In Capital):**
```
TVPI = (Distributions + NAV) / Paid-In Capital
     = DPI + RVPI

Measures: Total multiple on invested capital
Target: >2.5x (top quartile funds: >3.0x)
```

### Benchmarking Returns

**Top Quartile Performance:**
```
IRR: 25%+ (net to LPs)
TVPI: 3.0x+
Vintage matters: 2009-2011 vintages outperformed
```

**Median Performance:**
```
IRR: 15-18% (net to LPs)
TVPI: 2.0-2.5x
```

**Deal-Level Returns:**
```
Home Runs (15-20% of deals): 5.0x+ MOIC, 40%+ IRR
Solid Performers (40-50%): 2.5-4.0x MOIC, 20-30% IRR
Mediocre (20-30%): 1.5-2.5x MOIC, 10-20% IRR
Losses (10-15%): <1.0x MOIC, negative IRR
```

---

## Deal Sourcing & Diligence

### Deal Flow Sources

**Intermediated (70-80% of deals):**
```
Investment Banks:
  - Organized auctions
  - 5-15 bidders typical
  - Higher multiples (competitive)

Business Brokers:
  - Smaller deals (<$50M EV)
  - Less sophisticated sellers
  - Better pricing opportunity
```

**Proprietary (20-30% of deals):**
```
Direct Relationships:
  - Industry contacts
  - Prior portfolio company management
  - Family offices

Advantages:
  - Less competition
  - Better pricing (0.5-1.0x lower multiple)
  - Faster execution
```

### Due Diligence Checklist

**Commercial Diligence (4-6 weeks):**
```
Market Assessment:
  - Market size, growth, trends
  - Competitive landscape
  - Customer concentration

Revenue Quality:
  - Customer retention rates
  - Pricing trends
  - Contract terms (length, renewal rates)

Growth Drivers:
  - New products in pipeline
  - Geographic expansion potential
  - Market share gains
```

**Financial Diligence (3-4 weeks):**
```
Quality of Earnings (QofE):
  - Normalize EBITDA
  - Adjust for one-time items
  - Identify run-rate adjustments

Working Capital:
  - Required working capital
  - Seasonal fluctuations
  - Peg at closing (target balance)

CapEx:
  - Maintenance vs. growth CapEx
  - Deferred maintenance issues
```

**Operational Diligence (3-4 weeks):**
```
Management Assessment:
  - CEO capability
  - Bench strength
  - Retention risk

IT Systems:
  - ERP capability
  - Data security
  - Technical debt

Operations:
  - Facility condition
  - Supply chain resilience
  - Process maturity
```

**Legal Diligence (2-3 weeks):**
```
- Material contracts review
- Litigation history
- Regulatory compliance
- IP ownership
- Environmental issues
```

---

## Advanced LBO Structures

### Dividend Recapitalization

```
Structure:
  Year 2-3 into hold period
  Refinance debt to pay dividend

Example:
  Entry: $500M EV, $300M debt (5.0x), $200M equity
  Year 3: EBITDA grown to $75M
  Refi: Add $100M new debt (total debt 5.3x)
  Dividend: $100M to equity holders

Result:
  - Equity investors get money back early
  - Reduces risk
  - Still own 100% of company
```

### Portf olio Company Cross-Holdings

```
Structure:
  PortCo A acquires PortCo B
  Both owned by same fund

Benefits:
  - Create larger platform
  - Synergies
  - Higher exit multiple

Example:
  $50M EBITDA PortCo A (10x multiple)
  + $20M EBITDA PortCo B (8x multiple)
  = $70M EBITDA combined (12x multiple)
  Value creation from multiple arbitrage
```

### Management Rollover

```
Structure:
  Management sells some equity but rolls significant portion

Example:
  Management owns 15% at exit
  Exit proceeds: $500M
  Management gets $75M
  
  But rolls $25M into new deal (5% of NewCo)
  Cash out: $50M
  Rollover: $25M → potential for another bite at apple
```

### Buy-and-Build Strategy

```
Platform Acquisition:
  Year 0: Acquire $100M revenue platform
  Purchase Multiple: 8.0x EBITDA

Add-On Acquisitions:
  Year 1-4: Acquire 5 bolt-ons
  Each: $20-30M revenue, 6.0-7.0x multiple
  
Exit:
  Year 5: $250M combined revenue
  Exit Multiple: 10.0x (larger scale premium)
  
Value Creation:
  - Revenue growth: 2.5x
  - Multiple arbitrage: 6.5x avg acquisition vs. 10.0x exit
  - Multiple expansion: +2.0x from scale/growth
```

This deep PE/M&A knowledge should inform all LBO modeling and PE-related analyses in ValuationPro.
