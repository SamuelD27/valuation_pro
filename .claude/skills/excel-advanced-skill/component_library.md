# Component Library Reference

## Overview

Financial models are built from modular components. Each component has:
- **Requirements:** Input data needed
- **Outputs:** What it generates
- **Formulas:** Key calculations
- **Cell Usage:** Approximate size

## Core Components

### 1. Assumptions Panel

**Requirements:** None (always included)  
**Outputs:** Input cells for all key assumptions  
**Cell Usage:** ~20 cells  

**Typical Structure:**
```
Row 1:  [HEADER: Key Assumptions]
Row 2:  Revenue Growth | [INPUT: 10.0%]
Row 3:  EBITDA Margin  | [INPUT: 30.0%]
Row 4:  Tax Rate       | [INPUT: 25.0%]
Row 5:  WACC           | [INPUT: 10.0%]
Row 6:  Terminal Growth| [INPUT: 3.0%]
```

**Formatting:**
- Header: Dark blue background, white text
- Inputs: Light yellow background, bold
- All percentages: `0.0%` format

---

### 2. FCF Projection

**Requirements:** revenue, ebitda_margin, tax_rate, capex, nwc  
**Outputs:** 5-year FCF projection with formulas  
**Cell Usage:** ~50 cells  

**Formula Structure:**
```
Year 1 Revenue: [HISTORICAL]
Year 2-5 Revenue: =PrevYear*(1+$GrowthAssumption$)
EBITDA: =Revenue*$EBITDAMargin$
D&A: =Revenue*$DAPercent$
NOPAT: =(EBITDA-D&A)*(1-$TaxRate$)
CapEx: =Revenue*$CapExPercent$
ΔNW: =Revenue*$NWCPercent$
FCF: =NOPAT-CapEx-ΔNW
```

**Key Point:** All assumption references are absolute (`$B$5`)

---

### 3. WACC Calculation

**Requirements:** beta, risk_free_rate, market_risk_premium, debt, equity, tax_rate  
**Outputs:** cost_of_equity, cost_of_debt, wacc  
**Cell Usage:** ~30 cells  

**Formulas:**
```
Cost of Equity (CAPM):
  Re = Rf + β(Rm - Rf)
  =$RiskFree$+$Beta$*$MRP$

Total Value:
  V = E + D

WACC:
  =(E/V)*Re + (D/V)*Rd*(1-T)
  =($Equity$/($Equity$+$Debt$))*$Re$ + ($Debt$/($Equity$+$Debt$))*$Rd$*(1-$Tax$)
```

---

### 4. DCF Valuation

**Requirements:** fcf_projection, wacc, terminal_growth  
**Outputs:** pv_fcf, terminal_value, enterprise_value, equity_value  
**Cell Usage:** ~40 cells  

**Calculation Flow:**
```
1. PV of Projected FCFs:
   =NPV($WACC$, FCF_Range)

2. Terminal Value:
   Gordon Growth: =LastFCF*(1+$TermGrowth$)/($WACC$-$TermGrowth$)
   Exit Multiple: =LastEBITDA*$ExitMultiple$

3. PV of Terminal Value:
   =TerminalValue/(1+$WACC$)^5

4. Enterprise Value:
   =PV_FCFs + PV_TV

5. Equity Value:
   =EV - Debt + Cash - Preferred

6. Price Per Share:
   =EquityValue/SharesOutstanding
```

---

### 5. Sensitivity Table

**Requirements:** dcf_valuation  
**Outputs:** 2-way sensitivity table with conditional formatting  
**Cell Usage:** ~100 cells  

**Structure:**
```
        |  WACC: 8%  |  9%  |  10% |  11% | 12%
--------|-----------|------|------|------|------
TG: 2.0%| $1,250M  |$1,150|$1,050| $960 | $875
    2.5%| $1,320M  |$1,210|$1,100|$1,000| $910
    3.0%| $1,400M  |$1,275|$1,155|$1,045| $945
    3.5%| $1,490M  |$1,345|$1,215|$1,095| $985
    4.0%| $1,595M  |$1,425|$1,280|$1,150|$1,030
```

**Formula (for each cell):**
```python
# Uses DATA TABLE function or manual calculation
# Each cell recalculates DCF with different WACC/growth combination
```

**Conditional Formatting:** Color scale (red → yellow → green)

---

### 6. Debt Schedule

**Requirements:** debt_tranches, ebitda_projection, cash_sweep  
**Outputs:** Quarterly debt balance, interest expense, paydown waterfall  
**Cell Usage:** ~200 cells  

**Waterfall Logic:**
```
For each quarter:
  1. Calculate interest expense per tranche
  2. Calculate cash available for debt paydown:
     Cash Available = FCF * CashSweepPercent
  3. Pay down tranches in priority order:
     a. Revolver (if drawn)
     b. Term Loan A
     c. Term Loan B
     d. Subordinated Debt
  4. Update remaining balances
```

---

### 7. LBO Returns

**Requirements:** entry_ev, exit_ev, equity_invested, distributions  
**Outputs:** moic, irr, cash_on_cash  
**Cell Usage:** ~25 cells  

**Formulas:**
```
MOIC (Multiple on Invested Capital):
  =ExitEquityValue / EntryEquityInvested

IRR:
  =XIRR(CashFlows, Dates)
  
  Where CashFlows includes:
    - Initial investment (negative)
    - Distributions (positive)
    - Exit proceeds (positive)

Cash-on-Cash:
  =(Distributions + ExitProceeds) / Equity Invested
```

---

### 8. Comps Table

**Requirements:** comparable_companies, metrics  
**Outputs:** Trading multiples, statistics, implied valuation  
**Cell Usage:** ~150 cells  

**Structure:**
```
Company    | EV   | Revenue | EBITDA | EV/Rev | EV/EBITDA
-----------|------|---------|--------|--------|----------
CompA      |$5,000| $1,200  |  $360  |  4.2x  |  13.9x
CompB      |$7,000| $1,600  |  $480  |  4.4x  |  14.6x
CompC      |$6,000| $1,400  |  $420  |  4.3x  |  14.3x
-----------|------|---------|--------|--------|----------
Mean       |      |         |        |  4.3x  |  14.3x
Median     |      |         |        |  4.3x  |  14.3x
25th %ile  |      |         |        |  4.2x  |  13.9x
75th %ile  |      |         |        |  4.4x  |  14.6x

Implied Valuation Range:
  Low  (25th): $TARGET_EBITDA * 13.9x = $X,XXXm
  Mid  (Median): $TARGET_EBITDA * 14.3x = $X,XXXm
  High (75th): $TARGET_EBITDA * 14.6x = $X,XXXm
```

**Outlier Removal:** Use IQR method before calculating statistics

---

### 9. Waterfall Chart Data

**Requirements:** starting_value, adjustments  
**Outputs:** Data formatted for waterfall chart  
**Cell Usage:** ~60 cells  

**Common Waterfalls:**
- EV → Equity Bridge
- Debt Paydown Over Time
- Revenue → EBITDA Build-up

---

### 10. Football Field Chart

**Requirements:** dcf_range, comps_range, precedent_range  
**Outputs:** Valuation range comparison chart  
**Cell Usage:** ~80 cells  

**Data Structure:**
```
Method           | Low     | High    | Midpoint
-----------------|---------|---------|----------
DCF              | $900M   | $1,100M | $1,000M
Trading Comps    | $950M   | $1,150M | $1,050M
Precedent Txns   | $1,000M | $1,200M | $1,100M
Current Price    |    [  $1,025M  ]
```

---

## Component Selection Logic

```python
def select_components(capabilities: dict) -> list:
    """Determine which components to include"""
    
    components = ['assumptions_panel']  # Always included
    
    if capabilities['dcf']['feasible']:
        components.extend(['fcf_projection', 'dcf_valuation'])
        
        if capabilities['dcf']['level'] == 'advanced':
            components.extend(['wacc_calculation', 'sensitivity_table'])
    
    if capabilities['lbo']['feasible']:
        components.append('lbo_returns')
        
        if capabilities['lbo']['level'] == 'advanced':
            components.append('debt_schedule')
    
    if capabilities['comps']['feasible']:
        components.append('comps_table')
    
    # Integrative components
    if len([c for c in components if c in ['dcf_valuation', 'comps_table']]) > 1:
        components.append('football_field')
    
    return components
```

## Layout Rules

1. **Assumptions Panel:** Always top-left (A1)
2. **Main Analysis:** Top-right or below assumptions
3. **Supporting Schedules:** Below main analysis
4. **Charts:** Bottom or right side
5. **Summary/Returns:** Highlighted box, usually top-right

## Formatting Consistency

All components follow IB standards:
- Headers: Dark blue (#002060), white text, bold
- Inputs: Light yellow (#FFF2CC), bold
- Outputs: Light blue (#D9E1F2), bold
- Calculations: White background
- Borders: Medium black for sections
