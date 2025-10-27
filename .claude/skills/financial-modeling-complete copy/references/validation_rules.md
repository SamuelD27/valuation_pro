# Financial Model Validation Rules

## Overview

Validation rules ensure financial models produce realistic outputs and catch calculation errors. All ValuationPro models should pass these checks.

## DCF Validation Rules

### Input Validations

**WACC Range:**
```python
if not 0.05 <= wacc <= 0.25:
    raise ValueError(f"WACC {wacc:.1%} is outside reasonable range (5-25%)")
```

**Terminal Growth Rate:**
```python
if not 0.015 <= terminal_growth <= 0.05:
    raise ValueError(f"Terminal growth {terminal_growth:.1%} outside range (1.5-5%)")

if wacc <= terminal_growth:
    raise ValueError(f"WACC ({wacc:.1%}) must exceed terminal growth ({terminal_growth:.1%})")
```

**Projection Period:**
```python
if not 5 <= projection_years <= 15:
    warnings.warn(f"Projection period {projection_years} years is unusual (typical: 5-10)")
```

### Output Validations

**Terminal Value Dominance:**
```python
tv_percentage = (pv_terminal_value / enterprise_value) * 100

if tv_percentage > 90:
    warnings.warn(f"Terminal value is {tv_percentage:.1f}% of EV (should be 50-75%)")
elif tv_percentage < 40:
    warnings.warn(f"Terminal value is only {tv_percentage:.1f}% of EV")
```

**Implied EV/EBITDA Multiple:**
```python
implied_multiple = enterprise_value / ltm_ebitda

if not 4.0 <= implied_multiple <= 25.0:
    warnings.warn(f"Implied EV/EBITDA of {implied_multiple:.1f}x is unusual")
```

**Price vs. Current Market (for public companies):**
```python
price_variance = abs(implied_price - current_price) / current_price

if price_variance > 0.30:
    warnings.warn(f"Implied price {implied_price:.2f} is {price_variance:.1%} from market price {current_price:.2f}")
```

**Enterprise Value Sanity Check:**
```python
if enterprise_value <= 0:
    raise ValueError("Enterprise Value is negative or zero")

if equity_value <= 0:
    warnings.warn("Equity Value is negative (company is insolvent)")
```

### Free Cash Flow Validations

**FCF Sign Consistency:**
```python
negative_fcf_years = sum(1 for fcf in fcf_projections if fcf < 0)

if negative_fcf_years > len(fcf_projections) / 2:
    warnings.warn(f"{negative_fcf_years} out of {len(fcf_projections)} years have negative FCF")
```

**Terminal Year FCF:**
```python
if fcf_projections[-1] <= 0:
    raise ValueError("Terminal year FCF is negative - cannot calculate perpetuity value")
```

**CapEx Reasonableness:**
```python
capex_to_revenue = abs(capex) / revenue

if capex_to_revenue > 0.15:
    warnings.warn(f"CapEx is {capex_to_revenue:.1%} of revenue (typically 2-10%)")
```

## WACC Validation Rules

### Component Validations

**Risk-Free Rate:**
```python
if not 0.01 <= risk_free_rate <= 0.08:
    warnings.warn(f"Risk-free rate {risk_free_rate:.1%} is outside typical range (1-8%)")
```

**Beta:**
```python
if beta < 0:
    warnings.warn(f"Beta {beta:.2f} is negative (unusual, implies inverse market correlation)")
elif beta > 3.0:
    warnings.warn(f"Beta {beta:.2f} is very high (>3.0)")
```

**Market Risk Premium:**
```python
if not 0.04 <= market_risk_premium <= 0.10:
    warnings.warn(f"Market risk premium {market_risk_premium:.1%} outside range (4-10%)")
```

**Cost of Equity:**
```python
if not 0.08 <= cost_of_equity <= 0.25:
    warnings.warn(f"Cost of equity {cost_of_equity:.1%} is outside typical range (8-25%)")

if cost_of_equity <= risk_free_rate:
    raise ValueError(f"Cost of equity ({cost_of_equity:.1%}) cannot be less than risk-free rate ({risk_free_rate:.1%})")
```

**Cost of Debt:**
```python
if not 0.03 <= cost_of_debt <= 0.15:
    warnings.warn(f"Cost of debt {cost_of_debt:.1%} outside typical range (3-15%)")

if cost_of_debt >= cost_of_equity:
    warnings.warn(f"Cost of debt ({cost_of_debt:.1%}) exceeds cost of equity ({cost_of_equity:.1%}) - unusual")
```

**Tax Rate:**
```python
if not 0.15 <= tax_rate <= 0.40:
    warnings.warn(f"Tax rate {tax_rate:.1%} outside typical range (15-40%)")
```

### Capital Structure Validations

**Weights Sum to 1:**
```python
total_weight = equity_weight + debt_weight

if not 0.99 <= total_weight <= 1.01:
    raise ValueError(f"Capital structure weights sum to {total_weight:.2%} (must be 100%)")
```

**Leverage Check:**
```python
if debt_weight > 0.70:
    warnings.warn(f"Debt weight {debt_weight:.1%} is very high (>70%)")
```

**Negative Debt:**
```python
if market_value_debt < 0:
    warnings.warn("Company has net cash position (negative debt)")
    # WACC = Cost of Equity (unlevered)
```

## LBO Validation Rules

### Initial Setup Validations

**Leverage Ratio:**
```python
leverage_ratio = total_debt / ltm_ebitda

if leverage_ratio > 7.0:
    raise ValueError(f"Leverage ratio {leverage_ratio:.1f}x exceeds typical maximum (6-7x)")
elif leverage_ratio < 3.0:
    warnings.warn(f"Leverage ratio {leverage_ratio:.1f}x is low for LBO (typically 4-6x)")
```

**Equity Contribution:**
```python
equity_percentage = equity_investment / total_sources

if not 0.25 <= equity_percentage <= 0.50:
    warnings.warn(f"Equity is {equity_percentage:.1%} of capital (typical range: 30-40%)")
```

**Purchase Multiple:**
```python
if not 6.0 <= purchase_multiple <= 15.0:
    warnings.warn(f"Purchase multiple {purchase_multiple:.1f}x outside typical range (8-12x)")
```

**Sources = Uses Check:**
```python
if not 0.999 <= (total_sources / total_uses) <= 1.001:
    raise ValueError(f"Sources ({total_sources:.1f}M) ≠ Uses ({total_uses:.1f}M)")
```

### Operating Model Validations

**Revenue Growth:**
```python
if revenue_growth > 0.15:
    warnings.warn(f"Revenue growth {revenue_growth:.1%} is aggressive (>15%)")
```

**EBITDA Margin Improvement:**
```python
margin_expansion = final_margin - initial_margin

if margin_expansion > 0.05:
    warnings.warn(f"EBITDA margin expanding by {margin_expansion:.1%} (>500bps is aggressive)")
```

**Free Cash Flow Conversion:**
```python
fcf_conversion = fcf / ebitda

if not 0.40 <= fcf_conversion <= 0.80:
    warnings.warn(f"FCF conversion {fcf_conversion:.1%} outside typical range (50-70%)")
```

### Debt Schedule Validations

**Debt Balance Monotonically Decreasing:**
```python
for i in range(len(debt_balances) - 1):
    if debt_balances[i+1] > debt_balances[i]:
        warnings.warn(f"Debt balance increased in Year {i+1} (should be paying down)")
```

**Debt Fully Paid or Nearly Paid:**
```python
remaining_debt_ratio = final_debt_balance / initial_debt_balance

if remaining_debt_ratio > 0.50:
    warnings.warn(f"Still {remaining_debt_ratio:.1%} of debt remaining at exit")
```

**Negative Debt Balance:**
```python
if any(balance < 0 for balance in debt_balances):
    raise ValueError("Debt balance cannot be negative")
```

**Interest Coverage:**
```python
interest_coverage = ebitda / interest_expense

if interest_coverage < 2.0:
    raise ValueError(f"Interest coverage {interest_coverage:.1f}x below covenant threshold (2.0x)")
```

### Returns Validations

**IRR Range:**
```python
if irr < 0.10:
    warnings.warn(f"IRR {irr:.1%} is very low (<10%)")
elif irr < 0.15:
    warnings.warn(f"IRR {irr:.1%} below typical PE hurdle rate (15-20%)")
elif irr > 0.40:
    warnings.warn(f"IRR {irr:.1%} is exceptionally high (>40%) - verify assumptions")
```

**MOIC Range:**
```python
if moic < 2.0:
    warnings.warn(f"MOIC {moic:.1f}x is below target (2.0-3.0x minimum)")
elif moic > 6.0:
    warnings.warn(f"MOIC {moic:.1f}x is very high (>6x) - verify assumptions")
```

**Value Creation Check:**
```python
if exit_ev < entry_ev:
    warnings.warn(f"Exit EV ({exit_ev:.1f}M) < Entry EV ({entry_ev:.1f}M) - value destruction")
```

**Exit Multiple Reasonableness:**
```python
if abs(exit_multiple - entry_multiple) > 2.0:
    warnings.warn(f"Exit multiple {exit_multiple:.1f}x differs significantly from entry {entry_multiple:.1f}x")
```

## Comps Validation Rules

### Company Selection Validations

**Sample Size:**
```python
if num_comps < 4:
    raise ValueError(f"Only {num_comps} comps - need at least 4 for statistical validity")
elif num_comps > 15:
    warnings.warn(f"{num_comps} comps may include non-comparable companies")
```

**Negative EBITDA Companies:**
```python
negative_ebitda_count = sum(1 for ebitda in comp_ebitdas if ebitda < 0)

if negative_ebitda_count > num_comps * 0.25:
    warnings.warn(f"{negative_ebitda_count} comps have negative EBITDA (>25% of sample)")
```

### Multiple Validations

**EV/EBITDA Range:**
```python
if not 3.0 <= ev_ebitda_multiple <= 30.0:
    warnings.warn(f"EV/EBITDA {ev_ebitda_multiple:.1f}x outside typical range (5-20x)")
```

**EV/Revenue Range:**
```python
if not 0.3 <= ev_revenue_multiple <= 20.0:
    warnings.warn(f"EV/Revenue {ev_revenue_multiple:.1f}x outside typical range")
```

**P/E Range:**
```python
if not 5.0 <= pe_multiple <= 50.0:
    warnings.warn(f"P/E {pe_multiple:.1f}x outside typical range (10-30x)")
```

**Outlier Detection:**
```python
q1 = np.percentile(multiples, 25)
q3 = np.percentile(multiples, 75)
iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

outliers = [m for m in multiples if m < lower_bound or m > upper_bound]

if len(outliers) > num_comps * 0.20:
    warnings.warn(f"{len(outliers)} outliers detected (>20% of sample)")
```

### Statistical Validations

**Valuation Range Width:**
```python
valuation_range_ratio = high_case_value / low_case_value

if valuation_range_ratio > 2.5:
    warnings.warn(f"Valuation range is very wide (high/low ratio: {valuation_range_ratio:.1f}x)")
```

**Median vs. Mean Divergence:**
```python
divergence = abs(median_multiple - mean_multiple) / median_multiple

if divergence > 0.20:
    warnings.warn(f"Median and mean multiples diverge by {divergence:.1%} (may indicate skewed distribution)")
```

## General Financial Statement Validations

### Balance Sheet Checks

**Assets = Liabilities + Equity:**
```python
if not 0.999 <= (total_assets / (total_liabilities + equity)) <= 1.001:
    raise ValueError("Balance sheet does not balance")
```

**Positive Equity:**
```python
if equity < 0:
    warnings.warn("Company has negative equity (balance sheet insolvency)")
```

**Current Ratio:**
```python
current_ratio = current_assets / current_liabilities

if current_ratio < 1.0:
    warnings.warn(f"Current ratio {current_ratio:.2f} < 1.0 (liquidity risk)")
```

### Income Statement Checks

**Gross Margin:**
```python
gross_margin = (revenue - cogs) / revenue

if not 0.20 <= gross_margin <= 0.90:
    warnings.warn(f"Gross margin {gross_margin:.1%} outside typical range (30-70%)")
```

**EBITDA Margin:**
```python
ebitda_margin = ebitda / revenue

if ebitda_margin < 0:
    warnings.warn("Negative EBITDA margin (company is unprofitable)")
elif ebitda_margin > 0.50:
    warnings.warn(f"EBITDA margin {ebitda_margin:.1%} is very high (>50%)")
```

**Tax Rate Validation:**
```python
implied_tax_rate = tax_expense / pretax_income

if not 0.10 <= implied_tax_rate <= 0.45:
    warnings.warn(f"Implied tax rate {implied_tax_rate:.1%} outside typical range (21-35%)")
```

### Cash Flow Statement Checks

**CapEx as % of Revenue:**
```python
capex_percentage = abs(capex) / revenue

if capex_percentage > 0.20:
    warnings.warn(f"CapEx {capex_percentage:.1%} of revenue is very high (>20%)")
```

**Working Capital Changes:**
```python
nwc_change = current_nwc - previous_nwc

if abs(nwc_change / revenue) > 0.10:
    warnings.warn(f"NWC change is {abs(nwc_change)/revenue:.1%} of revenue (>10% is unusual)")
```

## Data Quality Checks

### Missing Data Detection

**Critical Fields:**
```python
required_fields = ['revenue', 'ebitda', 'market_cap', 'total_debt', 'cash']

for field in required_fields:
    if field not in data or data[field] is None:
        raise ValueError(f"Missing required field: {field}")
```

**Data Freshness:**
```python
from datetime import datetime, timedelta

if (datetime.now() - data_date).days > 90:
    warnings.warn(f"Data is {(datetime.now() - data_date).days} days old (>90 days)")
```

### Data Type Validations

**Numeric Fields:**
```python
numeric_fields = ['revenue', 'ebitda', 'wacc', 'beta']

for field in numeric_fields:
    if not isinstance(data[field], (int, float)):
        raise TypeError(f"{field} must be numeric, got {type(data[field])}")
```

**Percentage Fields (must be decimals, not >1):**
```python
percentage_fields = ['wacc', 'terminal_growth', 'tax_rate']

for field in percentage_fields:
    if data[field] > 1.0:
        raise ValueError(f"{field} = {data[field]} should be decimal (e.g., 0.09 not 9)")
```

## Reasonable Range Summary Table

| Metric                  | Minimum | Maximum | Typical Range |
|-------------------------|---------|---------|---------------|
| **DCF**                 |         |         |               |
| WACC                    | 5%      | 25%     | 8-12%         |
| Terminal Growth         | 1.5%    | 5%      | 2-3%          |
| EV/EBITDA (implied)     | 4x      | 25x     | 8-15x         |
| Terminal Value % of EV  | 40%     | 90%     | 50-75%        |
| **WACC Components**     |         |         |               |
| Risk-Free Rate          | 1%      | 8%      | 3-5%          |
| Beta                    | 0.3     | 3.0     | 0.8-1.5       |
| Market Risk Premium     | 4%      | 10%     | 5-7%          |
| Cost of Equity          | 8%      | 25%     | 10-15%        |
| Cost of Debt (pre-tax)  | 3%      | 15%     | 5-8%          |
| Tax Rate                | 15%     | 40%     | 21-28%        |
| **LBO**                 |         |         |               |
| Initial Leverage        | 3.0x    | 7.0x    | 4-6x EBITDA   |
| IRR                     | 10%     | 40%     | 20-25%        |
| MOIC                    | 1.5x    | 6.0x    | 2.5-4.0x      |
| Equity % of Capital     | 25%     | 50%     | 30-40%        |
| Purchase Multiple       | 6x      | 15x     | 8-12x EBITDA  |
| Exit Multiple           | 6x      | 15x     | 8-12x EBITDA  |
| **Comps**               |         |         |               |
| EV/EBITDA               | 3x      | 30x     | 8-15x         |
| EV/Revenue              | 0.3x    | 20x     | 1-5x          |
| P/E                     | 5x      | 50x     | 15-25x        |
| Number of Comps         | 4       | 15      | 6-10          |
| **Financial Ratios**    |         |         |               |
| Gross Margin            | 20%     | 90%     | 40-60%        |
| EBITDA Margin           | -10%    | 50%     | 15-30%        |
| Current Ratio           | 0.5     | 3.0     | 1.2-2.0       |
| Debt/Equity             | 0.0     | 3.0     | 0.3-1.0       |

## Validation Severity Levels

**ERROR (raise exception):**
- Data structure errors (missing required fields)
- Mathematical impossibilities (division by zero, negative enterprise value)
- Balance sheet doesn't balance
- Sources ≠ Uses in LBO

**WARNING (log warning):**
- Values outside typical ranges but not impossible
- Unusual relationships between metrics
- Statistical outliers
- Data quality concerns (staleness, implied values)

**INFO (log info):**
- Model assumptions for transparency
- Data sources and dates
- Methodology choices (Gordon Growth vs. Exit Multiple)
