---
name: financial-modeling
description: Investment banking financial modeling for DCF, LBO, Comps, M&A with deep PE/private company expertise. Includes exact formulas, Excel standards, validation rules, DLOM/control premiums, and industry-specific guidance. Use when implementing valuations, financial calculations, or IB-quality Excel outputs.
---

# Financial Modeling Skill

Professional financial modeling knowledge for building ValuationPro with investment banking standards.

## Quick Start

**Read FINANCE_CONCEPTS.md first** - Central formula reference with navigation to all methodologies.

## Core Methodologies

### DCF (Discounted Cash Flow)
→ `dcf_methodology.md` - FCF, terminal value, NPV calculations
→ `wacc_methodology.md` - Cost of capital, CAPM, beta

### LBO (Leveraged Buyout)  
→ `lbo_methodology.md` - Sources & Uses, debt waterfall, IRR/MOIC
→ `industries/private_equity.md` - **DEEP PE content** (fund structures, value creation, exit strategies)

### Comps & M&A
→ `comps_methodology.md` - Trading multiples, benchmarking
→ `precedent_transactions.md` - M&A comps, control premiums
→ `private_company_valuation.md` - DLOM (20-35%), size premiums, discounts

## Key Formulas

**DCF:**
```
FCFF = NOPAT - CapEx - ΔNWC + D&A
TV = FCF_final × (1 + g) / (WACC - g)
EV = Σ(PV FCFs) + PV(TV)
```

**WACC:**
```
WACC = (E/V)×Re + (D/V)×Rd×(1-Tc)
Re = Rf + β×(Rm - Rf)
```

**LBO:**
```
Sources = Uses (CRITICAL)
IRR = solve NPV = 0
MOIC = Exit Proceeds / Initial Equity
```

## Excel & Validation

→ `excel_standards.md` - IB formatting (blue inputs, yellow outputs, formulas)
→ `validation_rules.md` - Acceptable ranges, error detection
→ `scripts/validate_dcf.py` - CLI validation tool
→ `scripts/validate_lbo.py` - CLI validation tool

## Industry-Specific

→ `industries/private_equity.md` - PE structures, value creation, exits (16 pages)
→ `industries/saas_tech.md` - ARR, Rule of 40, CAC/LTV
→ `industries/healthcare.md` - Regulatory, patent cliffs
→ `industries/manufacturing.md` - Cyclicality, capacity

## When to Use

**Triggers:** "DCF", "LBO", "Comps", "WACC", "IRR", "valuation", "Excel formatting", "IB standards", "DLOM", "control premium", "M&A"

**Always read relevant methodology file before implementing.** FINANCE_CONCEPTS.md provides navigation.

## Critical Rules

✅ Use exact formulas from references
✅ Apply IB Excel standards (colors, formats)
✅ Validate outputs (WACC 8-12%, IRR 20-25%)
✅ Handle edge cases (negative FCF, circular refs)
✅ Single-sheet layouts preferred

❌ Never hardcode values in formulas
❌ Never skip validation checks
❌ Never calculate TV with WACC ≤ growth
❌ Never ignore circular references

## Validation Ranges

| Metric | Range | Typical |
|--------|-------|---------|
| WACC | 5-25% | 8-12% |
| Terminal Growth | 1.5-5% | 2-3% |
| LBO IRR | 10-40% | 20-25% |
| DLOM | 15-40% | 25-30% |
| Control Premium | 15-45% | 25-35% |
