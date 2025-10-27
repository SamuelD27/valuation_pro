# Precedent Transactions Methodology

## Table of Contents

1. [Overview](#overview)
2. [Key Differences from Trading Comps](#key-differences-from-trading-comps)
3. [Finding Precedent Transactions](#finding-precedent-transactions)
4. [Transaction Multiples](#transaction-multiples)
5. [Control Premium Analysis](#control-premium-analysis)
6. [Synergy Valuation](#synergy-valuation)
7. [Deal Structure Considerations](#deal-structure-considerations)
8. [Applying to Target Valuation](#applying-to-target-valuation)
9. [Edge Cases](#edge-cases)

## Overview

Precedent transactions (precedent M&A) values a company by analyzing actual acquisition prices paid for comparable companies. Unlike trading comps (public market prices), precedent transactions include control premiums and synergies.

**Use cases:**
- M&A advisory (sell-side or buy-side)
- Fairness opinions
- Control valuation scenarios
- Strategic buyer analysis

## Key Differences from Trading Comps

| Metric | Trading Comps | Precedent Transactions |
|--------|--------------|----------------------|
| **Price Type** | Minority stake (public market) | Control stake (100% acquisition) |
| **Premium** | No control premium | Includes 20-40% control premium |
| **Synergies** | No synergies priced in | May include buyer-specific synergies |
| **Liquidity** | Highly liquid | Illiquid (one-time transaction) |
| **Valuation** | Lower (minority) | Higher (control + synergies) |

**Relationship:**
```
Transaction Value = Trading Comp Value × (1 + Control Premium) + Synergies
```

## Finding Precedent Transactions

### Data Sources

**Public filings:**
- S-4 (merger proxy)
- 8-K (material events)
- 10-K (subsequent event disclosures)
- Press releases

**Commercial databases:**
- CapIQ, FactSet, Bloomberg
- Mergermarket, PitchBook (PE deals)
- Industry-specific M&A databases

### Selection Criteria

**Must-haves:**
- Same or adjacent industry
- Similar size (0.5x to 2.0x target EV)
- Recent (last 3-5 years preferred)
- Publicly disclosed financials

**Nice-to-haves:**
- Similar growth/margin profile
- Same geography
- Similar buyer type (strategic vs. financial)

**Sample size:** 8-12 transactions (vs. 6-10 for trading comps)

### Transaction Relevance by Vintage

```
<1 year old:   Highly relevant (market conditions similar)
1-2 years:     Relevant
2-3 years:     Moderately relevant
3-5 years:     Less relevant (adjust for market multiple changes)
>5 years:      Exclude (too dated)
```

## Transaction Multiples

### Enterprise Value Calculation

```
Transaction EV = Equity Purchase Price + Debt Assumed - Cash Acquired

Where:
  Equity Purchase Price = Offer Price per Share × Fully Diluted Shares
  Debt Assumed = Book value of debt at close
  Cash Acquired = Cash on balance sheet at close
```

**Note:** Some buyers pay off debt at close (cash-free, debt-free basis)

### Common Transaction Multiples

**EV / LTM EBITDA:**
```
Most common M&A multiple

EV / LTM EBITDA = Transaction EV / Last Twelve Months EBITDA

EBITDA should be from latest 10-K or proxy statement
```

**EV / NTM EBITDA:**
```
EV / NTM EBITDA = Transaction EV / Next Twelve Months EBITDA

Use management projections from proxy or fairness opinion
```

**EV / Revenue:**
```
Used when target has negative EBITDA or is high-growth

EV / Revenue = Transaction EV / LTM Revenue
```

**Premium to Unaffected Price:**
```
Premium = (Offer Price - Unaffected Price) / Unaffected Price × 100%

Where:
  Unaffected Price = Stock price 1 day before announcement
                     (or 1 week if leaks suspected)
```

### Typical Transaction Multiples by Industry

| Industry | EV/EBITDA | EV/Revenue | Premium |
|----------|-----------|------------|---------|
| **Software/SaaS** | 15-25x | 5-10x | 30-50% |
| **Healthcare** | 12-18x | 2-4x | 25-40% |
| **Industrials** | 8-12x | 0.8-1.5x | 20-35% |
| **Consumer** | 10-15x | 1-2x | 25-40% |
| **Financial Services** | 12-15x P/E | 1.5-2.5x P/B | 15-30% |

## Control Premium Analysis

### Control Premium Components

```
Total Transaction Premium = Control Premium + Synergy Premium + Market Timing

Breakdown:
  Control Premium: 15-30% (ability to control strategy, cash flows)
  Synergy Premium: 5-20% (buyer-specific value creation)
  Market Timing: -5% to +10% (market conditions)
```

### Calculating Control Premium

**Method 1: Market Price Comparison**
```
Control Premium = (Transaction Price - Trading Price) / Trading Price

Example:
  Trading price (pre-announcement): $50
  Transaction price: $65
  Control Premium = ($65 - $50) / $50 = 30%
```

**Method 2: Median Premium Analysis**
```
Use median premium from precedent transactions

Steps:
1. Calculate premium for each precedent transaction
2. Find median premium (e.g., 28%)
3. Apply to target's current trading price

Target Valuation = Current Price × (1 + Median Premium)
                 = $45 × (1 + 0.28) = $57.60
```

### When to Apply Control Premium

**Apply control premium:**
- Target is public company (trading at minority price)
- Buyer is acquiring 100% or majority control
- Valuation for M&A purposes

**Do NOT apply control premium:**
- Target is already private
- Valuation is for minority stake
- Already using transaction multiples (premium baked in)

**Common error:** Double-counting control premium

## Synergy Valuation

### Types of Synergies

**Cost Synergies (60-70% of total synergies):**
```
Revenue Synergies:
- Headcount reduction (eliminate duplicate roles)
- Facility consolidation
- Vendor renegotiation (scale benefits)
- IT system consolidation

Typical: 5-15% of combined cost base
Timeline: Realize over 18-24 months
```

**Revenue Synergies (30-40% of total synergies):**
```
- Cross-selling products to combined customer base
- Geographic expansion
- Channel optimization
- Product bundling

Typical: 2-5% revenue uplift
Timeline: Realize over 24-36 months
Risk: Higher execution risk than cost synergies
```

### Quantifying Synergies

**Cost Synergies Example:**
```
Target Overhead: $50M
Estimated Redundancy: 30%
Cost Synergies = $50M × 30% = $15M annually

PV of Synergies = $15M / WACC
                = $15M / 0.10 = $150M

(Using perpetuity formula assuming sustained savings)
```

**Revenue Synergies Example:**
```
Combined Revenue: $500M
Revenue Uplift: 3%
Revenue Synergies = $500M × 3% = $15M

EBITDA Impact = $15M × 60% (margin) = $9M

PV of Synergies = $9M / WACC = $90M
```

### Synergy Discount

**Not all synergies are realized:**
```
Expected Synergies: $100M
Probability Adjustment: 70%
Risk-Adjusted Synergies = $100M × 70% = $70M

Risk factors:
- Integration complexity
- Customer attrition
- Key employee retention
- Regulatory approvals
```

## Deal Structure Considerations

### Cash vs. Stock Consideration

**All-Cash Deals:**
```
Advantages:
+ Certainty for sellers
+ No dilution for buyer shareholders
+ Clean transaction

Disadvantages:
- Requires significant debt/cash
- No tax deferral for sellers
```

**Stock Deals:**
```
Advantages:
+ No cash required
+ Tax-deferred for sellers (if structured properly)
+ Sellers participate in upside

Disadvantages:
- Dilution for buyer shareholders
- Collar risk (price fluctuation)
- More complex accounting
```

**Mixed Consideration:**
```
Most common: 50-70% cash, 30-50% stock

Example:
  Transaction value: $1B
  Cash: $700M
  Stock: $300M (at fixed exchange ratio)
```

### Earnouts and Contingent Consideration

**Earnout Structure:**
```
Upfront Payment: 70-80% of total consideration
Earnout: 20-30% over 2-3 years

Earnout Triggers:
- Revenue targets
- EBITDA targets
- Product milestones
- Customer retention

Example:
  Base price: $800M
  Earnout: Up to $200M if Year 1 revenue > $150M
  Total potential: $1,000M
```

**Earnout Valuation:**
```
Probability-Weight Earnout:

Scenario 1 (50% probability): Earn $200M
Scenario 2 (30% probability): Earn $100M
Scenario 3 (20% probability): Earn $0

Expected Value = 0.50×$200M + 0.30×$100M + 0.20×$0
               = $100M + $30M + $0 = $130M

PV of Earnout = $130M / (1 + discount rate)^time
```

## Applying to Target Valuation

### Step-by-Step Approach

**1. Calculate transaction multiples for precedents:**
```
For each precedent:
  EV / LTM EBITDA
  EV / NTM EBITDA
  EV / Revenue
  Premium to unaffected price
```

**2. Calculate statistics:**
```
Median EV/EBITDA: 12.5x
25th percentile: 11.0x
75th percentile: 14.0x
Mean: 12.8x

Use median (less sensitive to outliers)
```

**3. Apply to target company:**
```
Target LTM EBITDA: $100M

Low Case (25th %ile): $100M × 11.0x = $1,100M
Base Case (Median): $100M × 12.5x = $1,250M
High Case (75th %ile): $100M × 14.0x = $1,400M
```

**4. Adjust for synergies (if applicable):**
```
Base EV: $1,250M
+ Synergies: $150M
Adjusted EV: $1,400M
```

**5. Convert to equity value:**
```
EV: $1,400M
- Net Debt: -$200M
Equity Value: $1,200M

Price per Share = $1,200M / 50M shares = $24.00
```

### Football Field Comparison

```
Trading Comps:        |=====•=====|     $18-24 ($21 mid)
Precedent Trans:      |======•======|   $22-28 ($25 mid)
DCF:                  |====•====|       $19-25 ($22 mid)
──────────────────────────────────────────────────────
                      18   20   22   24   26   28   30
```

Precedent transactions typically yield highest valuation (control premium + synergies).

## Edge Cases

### Distressed Sales

```
Problem: Transaction at fire-sale price not representative

Solution:
- Exclude if bankruptcy/distress situation
- Or flag as "distressed comp" and weight lower
- Note: May be relevant if target is also distressed
```

### Strategic Mega-Deals

```
Problem: $50B+ megadeals may have unique strategic rationale

Example: Facebook/WhatsApp at 350x revenue

Solution:
- Exclude outliers >3 standard deviations
- Note deal rationale but don't use multiple
```

### Cross-Border Transactions

```
Problem: Currency fluctuations, different accounting standards

Solution:
- Convert all to USD at transaction date FX rate
- Adjust EBITDA for accounting differences (IFRS vs. GAAP)
- Consider country risk premium differences
```

### Private Equity Transactions

```
Problem: PE deals may have less synergy premium (financial vs. strategic)

Solution:
- Separate PE deals from strategic deals
- PE multiples typically 0.5-1.0x lower
- Useful comp for valuing to other PE buyers
```

### Partial Acquisitions

```
Problem: Buyer acquired <100% (e.g., 60%)

Solution:
- Gross up to 100% basis:
  
  Implied 100% EV = Consideration Paid / Ownership %
  
  Example: $600M for 60% stake
  Implied EV = $600M / 0.60 = $1,000M
```

### Tax-Free Reorganizations

```
Problem: Stock deals structured as tax-free may trade at premium

Solution:
- Adjust for tax benefit to sellers
- Typical: 15-20% premium for tax deferral
```

## Excel Formula Structures

**Transaction EV:**
```excel
=SharePrice * FullyDilutedShares + Debt - Cash
=C10 * C11 + C12 - C13
```

**EV/EBITDA Multiple:**
```excel
=TransactionEV / LTMEBITDA
=C15 / C16
```

**Control Premium:**
```excel
=(OfferPrice - UnaffectedPrice) / UnaffectedPrice
=(C18 - C19) / C19
```

**Median Multiple:**
```excel
=MEDIAN(L12:L24)  # Range of transaction multiples
```

**Implied Valuation:**
```excel
=TargetEBITDA * MedianMultiple - NetDebt
=$C$5 * $C$25 - $C$6
```

## Reasonable Ranges

**Transaction Multiples:**
- EV/EBITDA: 6-20x (industry-dependent)
- EV/Revenue: 0.5-10x (SaaS highest)
- Control Premium: 15-40%

**Red flags:**
- Premium <15%: May not be true change of control
- Premium >60%: Check for bidding war or desperation
- Multiple >25x EBITDA: Unless hyper-growth tech
