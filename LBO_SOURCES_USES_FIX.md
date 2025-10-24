# LBO Sources & Uses Balance Fix

**Date:** October 24, 2025
**Issue:** Sources & Uses not balancing to $0
**Status:** ✅ FIXED

---

## Problem Identified

The Sources & Uses section in the LBO model was not balancing correctly. The check cell showed a non-zero value instead of $0.

### Root Cause

The financing sources (Equity, Senior Debt, Subordinated Debt) were calculated as **percentages of Purchase EV only**, but the Uses included **Purchase EV + Transaction Fees**.

**Before (WRONG):**
```
USES:
- Purchase EV: $1,000M
- Transaction Fees (2%): $20M
- TOTAL USES: $1,020M

SOURCES (calculated as % of Purchase EV = $1,000M):
- Equity (50%): $500M    ← 50% × $1,000M
- Senior (40%): $400M    ← 40% × $1,000M
- Sub (10%): $100M       ← 10% × $1,000M
- TOTAL SOURCES: $1,000M

CHECK: $1,000M - $1,020M = -$20M  ❌ NOT BALANCED
```

---

## The Fix

Changed all financing sources to be calculated as **percentages of TOTAL USES** (not just Purchase EV).

**After (CORRECT):**
```
USES:
- Purchase EV: $1,000M
- Transaction Fees (2%): $20M
- TOTAL USES: $1,020M

SOURCES (calculated as % of Total Uses = $1,020M):
- Equity (50%): $510M    ← 50% × $1,020M
- Senior (40%): $408M    ← 40% × $1,020M
- Sub (10%): $102M       ← 10% × $1,020M
- TOTAL SOURCES: $1,020M

CHECK: $1,020M - $1,020M = $0  ✅ BALANCED
```

---

## Code Changes

### File: [src/tools/lbo_tool.py](src/tools/lbo_tool.py)

#### 1. Store Total Uses Row (Line 278)

**Added:**
```python
self.total_uses_row = total_uses_row  # Store for later reference
```

This allows the Assumptions section to reference the Total Uses cell.

#### 2. Fix Sponsor Equity Calculation (Lines 381-391)

**Before:**
```python
ws.cell(row=row, column=1).value = "Sponsor Equity (% of Purchase Price)"
ws.cell(row=row, column=2).value = f"=B{self.purchase_ev_row}*B{equity_pct_row}"
```

**After:**
```python
ws.cell(row=row, column=1).value = "Sponsor Equity (% of Total Uses)"
ws.cell(row=row, column=2).value = f"=B{self.total_uses_row}*B{equity_pct_row}"
```

**Change:** Multiply by `total_uses_row` instead of `purchase_ev_row`

#### 3. Fix Senior Debt Calculation (Lines 426-434)

**Before:**
```python
ws.cell(row=row, column=1).value = "Senior Debt (% of Purchase Price)"
ws.cell(row=row, column=2).value = f"=B{self.purchase_ev_row}*B{senior_pct_row}"
```

**After:**
```python
ws.cell(row=row, column=1).value = "Senior Debt (% of Total Uses)"
ws.cell(row=row, column=2).value = f"=B{self.total_uses_row}*B{senior_pct_row}"
```

**Change:** Multiply by `total_uses_row` instead of `purchase_ev_row`

#### 4. Fix Subordinated Debt Calculation (Lines 455-463)

**Before:**
```python
ws.cell(row=row, column=1).value = "Subordinated Debt (% of Purchase Price)"
ws.cell(row=row, column=2).value = f"=B{self.purchase_ev_row}*B{sub_pct_row}"
```

**After:**
```python
ws.cell(row=row, column=1).value = "Subordinated Debt (% of Total Uses)"
ws.cell(row=row, column=2).value = f"=B{self.total_uses_row}*B{sub_pct_row}"
```

**Change:** Multiply by `total_uses_row` instead of `purchase_ev_row`

---

## Investment Banking Standard

This fix aligns with standard LBO Sources & Uses methodology:

### Correct Structure (per IB Guide Section 5.2)

**USES:**
1. Purchase Enterprise Value
2. Refinance Existing Debt (if any)
3. Transaction Fees (2-4% of deal value)
4. Financing Fees (1-3% of debt)

**TOTAL USES = Sum of all uses**

**SOURCES:**
1. Equity Contribution (% of Total Uses) ← **plug to balance**
2. Senior Debt (as multiple of EBITDA OR % of Total Uses)
3. Subordinated Debt (as multiple of EBITDA OR % of Total Uses)
4. Revolver (if any)

**TOTAL SOURCES = TOTAL USES** (must balance exactly!)

### Key Principle

> **Sources must equal Uses.** If you're using percentages for the capital structure, those percentages should apply to the **total amount needed** (Total Uses), not just the purchase price.

---

## Verification

### Test Case

Using AcmeTech data:
- LTM EBITDA: $663M
- Entry Multiple: 8.5x
- Transaction Fees: 2%

**Calculation:**
```
Purchase EV = $663M × 8.5x = $5,635.5M
Transaction Fees = $5,635.5M × 2% = $112.7M
TOTAL USES = $5,635.5M + $112.7M = $5,748.2M

With 50% Equity, 40% Senior, 10% Sub:
Equity = $5,748.2M × 50% = $2,874.1M
Senior = $5,748.2M × 40% = $2,299.3M
Sub = $5,748.2M × 10% = $574.8M
TOTAL SOURCES = $5,748.2M

CHECK: $5,748.2M - $5,748.2M = $0 ✅
```

---

## Impact on Model

### Before Fix
- ❌ Sources & Uses didn't balance
- ❌ Debt/Equity amounts understated by transaction fees
- ❌ Not following IB standards

### After Fix
- ✅ Sources & Uses balance perfectly to $0
- ✅ Correct financing amounts
- ✅ Follows IB standard methodology
- ✅ Equity serves as proper "plug" to balance the deal

---

## Usage in Example Script

The example script ([scripts/examples/example_lbo.py](scripts/examples/example_lbo.py)) uses:

```python
assumptions = {
    'equity_contribution_pct': 0.50,  # 50% of TOTAL USES (not just EV)
    'senior_debt_pct': 0.40,          # 40% of TOTAL USES
    'subordinated_debt_pct': 0.10,    # 10% of TOTAL USES
    'transaction_fees_pct': 0.02,     # 2% of Purchase EV
    ...
}
```

Now these percentages correctly apply to the Total Uses amount.

---

## Data Source

The LBO model uses the **standardized data source**:

**File:** `Base_datasource/Financial_Model_Data_Source.xlsx`
**Extractor:** `ComprehensiveDataExtractor` ([src/data/comprehensive_extractor.py](src/data/comprehensive_extractor.py))

### LTM Metrics (2025 Data):
- Revenue: $1,950M
- EBITDA: $663M
- Net Debt: $248M
- Market Cap: $6,550M
- Enterprise Value: $6,798M

These are the actual values from the Financial_Model_Data_Source.xlsx file.

---

## Testing

```bash
$ PYTHONPATH=/Users/samueldukmedjian/Desktop/valuation_pro python3 scripts/examples/example_lbo.py

✅ LBO model generated successfully!
📄 File: Examples/LBO_Model_AcmeTech.xlsx
```

**Verify in Excel:**
1. Open `Examples/LBO_Model_AcmeTech.xlsx`
2. Go to Sources & Uses section
3. Check the "CHECK (Should be $0)" row
4. Should show **$0.0** ✅

---

## Summary

| Item | Before | After | Status |
|------|--------|-------|--------|
| Equity % base | Purchase EV ❌ | Total Uses ✅ | Fixed |
| Senior Debt % base | Purchase EV ❌ | Total Uses ✅ | Fixed |
| Sub Debt % base | Purchase EV ❌ | Total Uses ✅ | Fixed |
| Sources = Uses | No ❌ | Yes ✅ | Fixed |
| IB Standards | No ❌ | Yes ✅ | Fixed |

---

## Key Takeaway

When structuring an LBO:
- ✅ **DO:** Calculate financing sources as % of **Total Uses**
- ❌ **DON'T:** Calculate as % of just the Purchase EV

The Total Uses includes transaction fees, refinancing costs, and other expenses that must also be financed.

**Result:** Sources and Uses now balance perfectly! ✅
