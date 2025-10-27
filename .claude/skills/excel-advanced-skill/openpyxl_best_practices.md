# openpyxl Best Practices for Financial Modeling

## The Golden Rules

### 1. Always Use Formulas, Never Hardcoded Values

❌ **WRONG:**
```python
ws['C10'].value = 1500 * 1.15  # Result: 1725 (not auditable)
```

✅ **CORRECT:**
```python
ws['B10'].value = 1500
ws['C10'].value = "=B10*1.15"  # Shows calculation path
```

**Why:** Investment bankers need to see and audit every calculation.

### 2. Master Absolute vs Relative References

| Reference Type | Example | When Used | Behavior When Copied |
|----------------|---------|-----------|---------------------|
| Relative | `B10` | Previous period values | Changes: `C10`, `D10`... |
| Absolute | `$B$10` | Assumptions, constants | Stays: `$B$10` |
| Mixed (col) | `$B10` | Same column, any row | `$B11`, `$B12`... |
| Mixed (row) | `B$10` | Same row, any column | `C$10`, `D$10`... |

**Example:** Revenue growth projection
```python
# Growth assumption in B2
ws['B2'].value = 0.15  # 15% growth

# Base year revenue in B10
ws['B10'].value = 1000

# Year 2 revenue (CORRECT)
ws['C10'].value = "=B10*(1+$B$2)"  # $B$2 stays fixed when copied right

# Year 3-5 revenue: copy formula right
# C10 becomes =C10*(1+$B$2) → CORRECT!
```

### 3. Cell Indexing is 1-Based

```python
# openpyxl uses Excel's 1-based indexing
ws.cell(row=1, column=1).value = "A1"  # ✓ Correct

# NOT Python's 0-based indexing
ws.cell(row=0, column=0).value = "Error!"  # ✗ Will fail
```

### 4. Formula String Generation

```python
def build_formula(param1, param2, constant_cell):
    """Build formula with proper reference types"""
    
    # WRONG - evaluates Python variable
    formula = f"={param1}*{param2}*{constant_cell}"  # If constant_cell="B2", wrong!
    
    # CORRECT - references cell properly
    formula = f"={param1}*{param2}*${constant_cell}"  # Adds $ for absolute
    
    # BEST - explicit absolute references
    formula = f"={param1}*{param2}*$B$2"
    
    return formula
```

### 5. Named Ranges for Complex Models

```python
# Define named range for WACC assumption
ws.workbook.defined_names['WACC'] = "'Sheet1'!$B$8"

# Now use in formulas (much cleaner!)
ws['F20'].value = "=NPV(WACC, F15:J15)"  # Instead of =NPV($B$8, F15:J15)
```

### 6. Number Formatting

```python
# Currency in millions
ws['B10'].number_format = '$#,##0.0,,"M"'  # Shows $123.4M

# Percentages
ws['B5'].number_format = '0.0%'  # Shows 12.5%

# Multiples
ws['D15'].number_format = '0.0x'  # Shows 8.5x

# Accounting format (negative in parentheses)
ws['C20'].number_format = '_($* #,##0.0_);_($* (#,##0.0);_($* "-"_);_(@_)'
```

### 7. Avoid Circular References

```python
# WRONG - circular reference
ws['A1'].value = "=B1+C1"
ws['B1'].value = "=A1*2"  # B1 depends on A1, which depends on B1!

# Excel will error on opening
```

**How to detect:** Trace dependencies before writing formulas.

### 8. Performance Optimization

```python
# SLOW - individual cell writes
for i in range(1000):
    ws.cell(row=i+1, column=1).value = i

# FASTER - batch operations
cells = [(i+1, 1, i) for i in range(1000)]
for row, col, val in cells:
    ws.cell(row, column).value = val

# FASTEST - use append for rows
for i in range(1000):
    ws.append([i, i*2, i*3])  # Appends entire row at once
```

### 9. Column Width Management

```python
# Auto-size based on content (openpyxl doesn't do this automatically!)
for column_cells in ws.columns:
    length = max(len(str(cell.value or '')) for cell in column_cells)
    ws.column_dimensions[column_cells[0].column_letter].width = length + 2

# Or set specific width
ws.column_dimensions['A'].width = 20
ws.column_dimensions['B'].width = 15
```

### 10. Error Handling for Formulas

```python
def safe_formula_write(ws, cell, formula):
    """Write formula with validation"""
    
    # Check for obvious errors
    if not formula.startswith('='):
        raise ValueError(f"Formula must start with =: {formula}")
    
    if '#REF!' in formula or '#NAME?' in formula:
        raise ValueError(f"Formula contains error: {formula}")
    
    # Check cell references are valid (basic check)
    import re
    refs = re.findall(r'[A-Z]+\d+', formula)
    for ref in refs:
        # Ensure row number is valid
        row_num = int(''.join(filter(str.isdigit, ref)))
        if row_num < 1:
            raise ValueError(f"Invalid row number in {ref}")
    
    ws[cell].value = formula
```

## Common Pitfalls

### Pitfall 1: Merged Cells Confusion

```python
# Merge cells A1:C1
ws.merge_cells('A1:C1')

# WRONG - trying to write to B1 or C1
ws['A1'].value = "Title"
ws['B1'].value = "Subtitle"  # This won't appear!

# CORRECT - only write to top-left cell
ws['A1'].value = "Title"
```

### Pitfall 2: Formula Copying Errors

```python
# Original formula in B10
ws['B10'].value = "=B5*C5"

# When copied to C10 (one column right)
# Excel interprets as: =C5*D5
# But you might have wanted: =B5*D5 (keep B5 fixed)

# Solution: Use absolute references
ws['B10'].value = "=$B$5*C5"  # Now copies as =$B$5*D5
```

### Pitfall 3: Data Type Confusion

```python
# WRONG - Excel sees as text
ws['B5'].value = "0.15"  # Text, not number!

# CORRECT - set as number
ws['B5'].value = 0.15
ws['B5'].number_format = '0.0%'  # Displays as 15%
```

## Financial Model Specific Tips

### FCF Projection Formula

```python
def fcf_projection_formula(row, assumptions_row):
    """Generate FCF formula for a given year"""
    
    # FCF = NOPAT - CapEx - ΔNW
    # NOPAT = (EBITDA - D&A) * (1 - Tax Rate)
    
    ebitda_cell = f"B{row}"
    da_cell = f"C{row}"
    tax_rate = f"$B${assumptions_row}"  # Absolute reference to assumption
    capex_cell = f"D{row}"
    nwc_cell = f"E{row}"
    
    nopat = f"(({ebitda_cell}-{da_cell})*(1-{tax_rate}))"
    fcf = f"={nopat}-{capex_cell}-{nwc_cell}"
    
    return fcf
```

### WACC Formula

```python
def wacc_formula(equity_cell, debt_cell, re_cell, rd_cell, tax_cell):
    """WACC = (E/V)*Re + (D/V)*Rd*(1-T)"""
    
    total_value = f"({equity_cell}+{debt_cell})"
    
    equity_component = f"({equity_cell}/{total_value})*{re_cell}"
    debt_component = f"({debt_cell}/{total_value})*{rd_cell}*(1-{tax_cell})"
    
    return f"={equity_component}+{debt_component}"
```

### NPV Formula

```python
def npv_formula(wacc_cell, fcf_range):
    """NPV of cash flows"""
    
    # Excel NPV function discounts from t=1, not t=0
    # If fcf_range includes t=0, handle separately
    
    return f"=NPV({wacc_cell},{fcf_range})"
```

## Testing Checklist

- [ ] All formulas start with `=`
- [ ] Absolute references use `$` where needed
- [ ] No hardcoded calculations (use formulas)
- [ ] Column widths accommodate content
- [ ] Number formats applied correctly
- [ ] No circular references
- [ ] Cell ranges are valid
- [ ] Named ranges defined for key assumptions
- [ ] Formulas produce expected results with sample data
