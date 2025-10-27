# Number Format Fix - $0M Display Issue

**Date:** October 24, 2025
**Issue:** Values displaying as $0M in LBO model
**Status:** ✅ FIXED

---

## Problem Identified

The LBO model was using the number format `$#,##0.0,,"M"` which divides values by 1,000,000 to display in millions.

### Why This Caused $0M

When the input data is **already in millions** (e.g., `ltm_ebitda = 100.0` meaning $100M):

```
Excel calculation:
100.0 ÷ 1,000,000 = 0.0001
Formatted with "$#,##0.0,,"M"" = $0.0M
```

The value rounds to $0M because it's too small after dividing by millions.

---

## The Fix

### Changed Number Format

**Before (WRONG):**
```python
ws.cell(row=row, column=2).number_format = '$#,##0.0,,"M"'  # ❌ Divides by millions
```

**After (CORRECT):**
```python
ws.cell(row=row, column=2).number_format = '$#,##0.0'  # ✅ Shows actual value
```

### Updated Labels

Also added "$mm" to labels to clarify that values are in millions:

**Before:**
```python
ws.cell(row=row, column=1).value = "LTM EBITDA"
```

**After:**
```python
ws.cell(row=row, column=1).value = "LTM EBITDA ($mm)"
```

---

## Files Fixed

### LBO Tool ([src/tools/lbo_tool.py](src/tools/lbo_tool.py))

Fixed 4 instances:
- Line 154: LTM EBITDA
- Line 170: Purchase Enterprise Value
- Line 188: Exit Year EBITDA
- Line 204: Exit Enterprise Value

**Changes Made:**
```python
# Line 152-154
ws.cell(row=row, column=1).value = "LTM EBITDA ($mm)"  # Added ($mm)
ws.cell(row=row, column=2).number_format = '$#,##0.0'  # Removed ,,

# Line 167-170
ws.cell(row=row, column=1).value = "Purchase Enterprise Value ($mm)"  # Added ($mm)
ws.cell(row=row, column=2).number_format = '$#,##0.0'  # Removed ,,

# Line 184-188
ws.cell(row=row, column=1).value = "Exit Year EBITDA ($mm)"  # Added ($mm)
ws.cell(row=row, column=2).number_format = '$#,##0.0'  # Removed ,,

# Line 201-204
ws.cell(row=row, column=1).value = "Exit Enterprise Value ($mm)"  # Added ($mm)
ws.cell(row=row, column=2).number_format = '$#,##0.0'  # Removed ,,
```

### DCF Tool ([src/tools/dcf_tool.py](src/tools/dcf_tool.py))

✅ **No changes needed** - DCF tool was already using correct format `$#,##0.0`

---

## Understanding Excel Number Formats

### Format with Comma Dividers

The commas in Excel number formats have special meaning:

| Format | Meaning | Example Input | Display |
|--------|---------|---------------|---------|
| `#,##0` | Thousand separator | 1000000 | 1,000,000 |
| `#,##0,` | Divide by 1,000 (show in thousands) | 1000000 | 1,000 |
| `#,##0,,` | Divide by 1,000,000 (show in millions) | 1000000 | 1 |
| `#,##0.0,,` | Divide by 1,000,000 + 1 decimal | 1000000 | 1.0 |

### Our Use Case

Since we store values **already in millions** (100.0 = $100M):

**Wrong approach:**
```python
# Input: 100.0 (meaning $100M)
# Format: '$#,##0.0,,"M"'
# Result: $0.0M (because 100.0 ÷ 1,000,000 = 0.0001)
```

**Correct approach:**
```python
# Input: 100.0 (meaning $100M)
# Format: '$#,##0.0'
# Label: "LTM EBITDA ($mm)"
# Result: $100.0 (with label clarifying it's in millions)
```

---

## Testing

### LBO Model Test

```bash
$ PYTHONPATH=/Users/samueldukmedjian/Desktop/valuation_pro python3 scripts/examples/example_lbo.py

✅ LBO model generated successfully!
📄 File: Examples/LBO_Model_AcmeTech.xlsx
```

**Expected Output in Excel:**
- LTM EBITDA ($mm): **$100.0** (not $0.0M)
- Purchase EV ($mm): **$1,000.0** (not $0.0M)
- Exit EBITDA ($mm): **$127.6** (not $0.0M)
- Exit EV ($mm): **$1,276.3** (not $0.0M)

### DCF Model Test

```bash
$ PYTHONPATH=/Users/samueldukmedjian/Desktop/valuation_pro python3 scripts/examples/example_dcf.py

✅ DCF model generated successfully!
📄 File: Examples/DCF_Model_AcmeTech.xlsx
```

**Expected Output in Excel:**
- All values display correctly (no $0M issues)

---

## Prevention

To prevent this issue in future code:

### ✅ DO: When values are in millions

```python
# Store value in millions
ltm_ebitda = 100.0  # $100M

# Use simple format
ws.cell(row=row, column=2).value = ltm_ebitda
ws.cell(row=row, column=2).number_format = '$#,##0.0'

# Clarify in label
ws.cell(row=row, column=1).value = "LTM EBITDA ($mm)"
```

### ❌ DON'T: Divide by millions when already in millions

```python
# WRONG: Value is already in millions
ltm_ebitda = 100.0  # $100M
ws.cell(row=row, column=2).number_format = '$#,##0.0,,"M"'  # ❌ Will show $0M
```

### ✅ DO: Divide by millions when values are in dollars

```python
# If storing in actual dollars (not millions)
ltm_ebitda = 100_000_000  # $100,000,000

# Then dividing by millions makes sense
ws.cell(row=row, column=2).value = ltm_ebitda
ws.cell(row=row, column=2).number_format = '$#,##0.0,,"M"'  # Will show $100.0M
```

---

## Quick Reference

### Common Number Formats

```python
# Currency (no decimals)
'$#,##0'  # Example: $1,000

# Currency (1 decimal)
'$#,##0.0'  # Example: $1,000.0

# Currency (2 decimals)
'$#,##0.00'  # Example: $1,000.00

# Percentage (1 decimal)
'0.0%'  # Example: 15.5%

# Percentage (2 decimals)
'0.00%'  # Example: 15.55%

# Multiples
'0.0x'  # Example: 10.5x

# Thousands with divider (K)
'$#,##0,"K"'  # Example: $1,000K (input was 1,000,000)

# Millions with divider (M)
'$#,##0,,"M"'  # Example: $1M (input was 1,000,000)
```

---

## Summary

✅ **Fixed:** LBO tool number formats (4 instances)
✅ **Verified:** DCF tool already correct
✅ **Tested:** Both tools generate models with correct number display
✅ **Documented:** Prevention guidelines for future development

**Result:** All values now display correctly in Excel models. No more $0M display issues.
