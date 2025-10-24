# DCF Model Gap Analysis: Current vs Reference

## Reference Model Structure (14 Sheets)

The professional DCF model has **14 comprehensive sheets**:

### 1. **Assumptions**
- ✅ Scenario selection (Base/Downside/Upside with dropdown)
- ✅ Revenue growth drivers by segment
- ✅ Volume growth assumptions
- ✅ Price per unit assumptions
- ✅ Operating margin assumptions
- ✅ CAPEX as % of revenue
- ✅ Working capital assumptions (DSO, DPO, inventory days)
- ✅ All inputs use CHOOSE() formulas to switch scenarios

### 2. **Income Statement**
- ✅ Detailed line-by-line P&L (110 rows!)
- ✅ Multiple revenue segments with separate drivers
- ✅ Volume × Price calculations for each segment
- ✅ Cost of Goods Sold breakdown
- ✅ Operating expenses detail
- ✅ D&A, Interest, Taxes
- ✅ All projections linked to Assumptions sheet
- ✅ Growth % calculations
- ✅ Margin analysis

### 3. **Balance Sheet**
- ✅ Complete balance sheet (Assets, Liabilities, Equity)
- ✅ Fixed assets linked to PPE Schedule
- ✅ Working capital items (A/R, Inventory, A/P)
- ✅ Cash from Cash Flow Statement
- ✅ Debt from Debt Schedule
- ✅ Transaction goodwill calculation
- ✅ Shareholders' equity roll-forward
- ✅ Balance check formula

### 4. **Cash Flow Statement**
- ✅ Indirect method (Net Income → CF)
- ✅ Operating cash flow with add-backs
- ✅ Working capital changes calculated
- ✅ Investing cash flow (CAPEX)
- ✅ Financing cash flow (debt, dividends)
- ✅ Cash beginning/ending balance
- ✅ All items linked to I/S and B/S

### 5. **PPE Schedule**
- ✅ Opening balance
- ✅ Additions (CAPEX)
- ✅ Disposals
- ✅ Depreciation
- ✅ Closing balance
- ✅ Roll-forward by year

### 6. **Debt Schedule**
- ✅ Opening debt balance
- ✅ Additions
- ✅ Repayments
- ✅ Closing balance
- ✅ Interest rate assumptions
- ✅ Interest expense calculation

### 7. **WSO Cover Page**
- ✅ Company name, logo placeholder
- ✅ Model type, date
- ✅ Analyst information
- ✅ Professional branding

### 8. **DCF**
- ✅ EBITDA from Income Statement
- ✅ Less: D&A, Taxes, CAPEX, NWC Change
- ✅ = Free Cash Flow
- ✅ Discount factors (WACC-based)
- ✅ PV of FCF calculations
- ✅ Terminal value (Gordon Growth or Exit Multiple)
- ✅ Enterprise Value = Sum(PV FCF) + PV(Terminal)
- ✅ Bridge to Equity Value
- ✅ Shares outstanding
- ✅ **Implied Price Per Share**
- ✅ Sensitivity tables (WACC vs Growth, WACC vs Exit Multiple)

### 9. **LBO Modelling**
- ✅ Entry valuation (EBITDA multiple)
- ✅ Debt/Equity split
- ✅ Senior/Sub debt tranches
- ✅ Debt paydown waterfall
- ✅ Interest expense by tranche
- ✅ Exit valuation
- ✅ IRR and MOIC calculation
- ✅ Sensitivity table (Entry vs Exit multiple)

### 10. **FCFE Valuation**
- ✅ Free Cash Flow to Equity
- ✅ Cost of Equity discount rate
- ✅ PV calculations
- ✅ Equity value directly

### 11. **PE Returns Analysis**
- ✅ Multiple entry/exit scenarios
- ✅ Holding period analysis
- ✅ IRR calculations
- ✅ Distribution waterfall

### 12. **WACC Calculation**
- ✅ Cost of Equity (CAPM)
  - Risk-free rate
  - Beta
  - Market risk premium
- ✅ Cost of Debt
  - Interest rate
  - Tax shield
- ✅ Capital structure (D/E weights)
- ✅ **WACC formula with all components**

### 13. **Football Field**
- ✅ Valuation summary chart
- ✅ DCF range
- ✅ Comps range
- ✅ Precedent transactions
- ✅ Current trading price
- ✅ Visual comparison

### 14. **Charts**
- ✅ Revenue growth chart
- ✅ EBITDA margin trend
- ✅ FCF waterfall
- ✅ Valuation bridge

---

## Our Current Model (5 Sheets)

### What We Have:
1. ❌ **Assumptions** - Incomplete (no scenarios, no detailed drivers)
2. ❌ **Summary** - Basic metrics only
3. ❌ **Historical** - Empty!
4. ❌ **Projections** - Just DataFrame dump, no detail
5. ❌ **Valuation** - Basic sensitivity only

### Critical Missing Features:

#### 1. **No Three-Statement Integration**
- ❌ No Income Statement sheet
- ❌ No Balance Sheet sheet
- ❌ No Cash Flow Statement sheet
- ❌ No linking between statements

#### 2. **No Supporting Schedules**
- ❌ No PPE Schedule
- ❌ No Debt Schedule
- ❌ No Working Capital Schedule
- ❌ No Tax Schedule

#### 3. **Hardcoded Values Instead of Formulas**
- ❌ Python calculations stored as values
- ❌ No Excel formulas for year-over-year
- ❌ Can't change assumptions and see impact
- ❌ Not truly "Excel-native"

#### 4. **No Scenario Analysis**
- ❌ No Base/Upside/Downside cases
- ❌ No dropdown to switch scenarios
- ❌ Single path only

#### 5. **Missing Valuation Methods**
- ❌ No LBO model
- ❌ No FCFE valuation
- ❌ No PE returns analysis
- ❌ No Football Field chart

#### 6. **Poor Layout**
- ❌ Not following IB standards
- ❌ No proper headers
- ❌ No color coding
- ❌ No merged cells for sections

#### 7. **Missing Revenue Detail**
- ❌ No segment breakdown
- ❌ No volume × price drivers
- ❌ No growth rate detail by product

#### 8. **Incomplete DCF Calculation**
- ❌ No visible EBITDA → EBIT → NOPAT flow
- ❌ No terminal value calculation shown
- ❌ No discount factor table
- ❌ No waterfall showing FCF sources

---

## Key Differences

| Feature | Reference Model | Our Model | Status |
|---------|----------------|-----------|--------|
| **Sheets** | 14 | 5 | ❌ 64% missing |
| **Income Statement** | Full P&L (110 rows) | None | ❌ Missing |
| **Balance Sheet** | Complete B/S | None | ❌ Missing |
| **Cash Flow** | Full CF statement | None | ❌ Missing |
| **Formulas** | 100% Excel formulas | Python values | ❌ Wrong approach |
| **3-Statement Link** | Fully integrated | None | ❌ Missing |
| **Scenarios** | 3 cases with dropdown | Single case | ❌ Missing |
| **Revenue Drivers** | Volume × Price by segment | Single growth rate | ❌ Too simple |
| **Working Capital** | DSO/DIO/DPO drivers | % of revenue | ❌ Less detailed |
| **LBO Model** | Complete with debt waterfall | Not implemented | ❌ Missing |
| **WACC Sheet** | Dedicated calculation sheet | Embedded in Python | ❌ Not visible |
| **Football Field** | Visual valuation range | None | ❌ Missing |
| **Charts** | Multiple charts | None | ❌ Missing |
| **Cover Page** | Professional | None | ❌ Missing |

---

## What Needs to Be Rebuilt

### Phase 1: Core Structure (CRITICAL)
1. **Rewrite Excel Generator completely**
   - Create 3-statement model first
   - Use ONLY Excel formulas
   - Link sheets properly
   - Implement scenario switching

2. **Income Statement**
   - Revenue by segment
   - Volume × Price drivers
   - COGS detail
   - Opex breakdown
   - EBITDA, EBIT calculations
   - Link to Assumptions

3. **Balance Sheet**
   - Assets (Fixed, Current)
   - Liabilities (Debt, Payables)
   - Equity roll-forward
   - Link to PPE/Debt schedules
   - Cash from CF statement

4. **Cash Flow Statement**
   - Start with Net Income
   - Add back D&A
   - Working capital changes
   - CAPEX (link to PPE)
   - Debt changes
   - Calculate ending cash

### Phase 2: Supporting Schedules
5. **PPE Schedule**
   - Opening + CAPEX - Depr = Closing
   - Feed Balance Sheet

6. **Debt Schedule**
   - Opening + Draws - Repayments = Closing
   - Calculate interest expense
   - Feed Income Statement

7. **Working Capital Schedule**
   - A/R (DSO driver)
   - Inventory (DIO driver)
   - A/P (DPO driver)
   - Calculate changes

### Phase 3: Valuation Sheets
8. **DCF Sheet**
   - EBITDA - D&A = EBIT
   - EBIT × (1-T) = NOPAT
   - NOPAT - CAPEX - ΔNWC = FCF
   - Discount factors
   - PV(FCF) by year
   - Terminal value
   - Sum to Enterprise Value
   - Bridge to Equity Value
   - Shares → Price per share

9. **WACC Calculation**
   - Cost of Equity inputs
   - Cost of Debt inputs
   - Capital structure
   - Formula display

10. **Sensitivity Tables**
    - WACC vs Terminal Growth
    - Entry vs Exit Multiple
    - Revenue Growth vs Margin

### Phase 4: Advanced Features
11. **LBO Model**
    - Entry valuation
    - Debt structure
    - Debt paydown
    - Exit calculation
    - IRR/MOIC

12. **Football Field**
    - DCF range
    - Trading comps
    - Precedent M&A
    - Visual chart

13. **Charts**
    - Revenue/EBITDA trends
    - FCF waterfall
    - Valuation bridge

14. **Cover Page**
    - Company info
    - Date/analyst
    - Professional layout

---

## Formula Examples from Reference

### Scenario Switching:
```excel
=CHOOSE($B$2, I14, I15, I16)
```
Where B2 = 1 (Base), 2 (Downside), 3 (Upside)

### Revenue Calculation:
```excel
=Volume × Price
=H17 * H20
```

### Year Headers:
```excel
=+D12+1  (increments previous year)
```

### Cross-Sheet References:
```excel
='Income Statement'!H89  (EBITDA)
=-'Income Statement'!H82 (D&A)
=+'Cash Flow Statement'!H19 (CAPEX)
```

### FCF Formula:
```excel
=+D12+D14+D16+D18+D10
(EBIT + Taxes + CAPEX + NWC Change + D&A)
```

### Discount Factor:
```excel
=1/(1+$D$28)^D5
```

### PV Calculation:
```excel
=D20*D22  (FCF × Discount Factor)
```

---

## Action Plan

### Immediate (This Week):
1. ✅ **Create new Excel generator from scratch**
   - Follow reference model structure exactly
   - Build 3-statement model first
   - Use formula-driven approach

2. ✅ **Implement scenario selection**
   - Add dropdown in Assumptions
   - Use CHOOSE() for all driver inputs

3. ✅ **Build Income Statement**
   - Revenue segments
   - Full cost structure
   - Link to Assumptions

### Short-term (Next Week):
4. Balance Sheet with linkages
5. Cash Flow Statement
6. PPE and Debt schedules
7. DCF calculation sheet
8. WACC sheet

### Medium-term (Following Week):
9. LBO model
10. Football Field chart
11. Sensitivity tables
12. Professional formatting

---

## Success Criteria

### Model must:
- ✅ Have 14 sheets minimum
- ✅ Use 100% Excel formulas (no hardcoded Python values)
- ✅ Support 3 scenarios (Base/Upside/Downside)
- ✅ Have fully integrated 3-statement model
- ✅ Show clear audit trail (every calculation traceable)
- ✅ Match IB formatting standards
- ✅ Include sensitivity analysis
- ✅ Generate LBO analysis
- ✅ Produce Football Field chart
- ✅ Be completely editable in Excel

---

**Bottom Line**: Our current model is **about 20% complete** compared to the reference. We need a complete rebuild following the reference structure.

**Estimated Effort**: 20-30 hours to rebuild properly

**Priority**: HIGH - This is critical for production use
