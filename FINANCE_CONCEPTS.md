# ValuationPro: Financial Concepts & Implementation Guide

## Core Valuation Methodologies

### 1. Discounted Cash Flow (DCF)
**Theory**: Value a company by projecting its future free cash flows and discounting them to present value.

**Formula**:
```
Enterprise Value = Σ(FCFt / (1 + WACC)^t) + Terminal Value / (1 + WACC)^n
Equity Value = EV + Cash - Debt - Preferred Stock
Price per Share = Equity Value / Shares Outstanding
```

**Excel Model Structure**:
- **Assumptions Tab**: Growth rates, margins, CapEx %, tax rate, WACC
- **Historical Financials**: 3-5 years of I/S, B/S, CF
- **Projections Tab**: 5-10 year forecast (revenue → EBIT → NOPAT → FCF)
- **Terminal Value**: Gordon Growth or Exit Multiple method
- **Valuation Output**: NPV calculation, sensitivity tables
- **Summary**: Price target, upside/downside, key metrics

**Python Implementation**:
- Use `pandas` for data manipulation
- `numpy.npv()` for discounting
- `openpyxl` or `xlsxwriter` for Excel generation
- Create reusable `DCFModel` class with methods for each calculation step
- Include data validation (terminal growth < WACC, realistic margins)

---

### 2. Weighted Average Cost of Capital (WACC)
**Theory**: The average rate a company pays to finance its assets, weighted by capital structure.

**Formula**:
```
WACC = (E/V × Re) + (D/V × Rd × (1 - T))

Where:
Re = Cost of Equity = Rf + β × (Rm - Rf)
Rd = Cost of Debt (pre-tax)
E = Market value of equity
D = Market value of debt
V = E + D
T = Tax rate
```

**Excel Model Structure**:
- **Inputs**: Risk-free rate (10Y Treasury), beta, market risk premium, debt balance, interest expense
- **Calculations**: Cost of equity, after-tax cost of debt, weights
- **Output**: WACC (should be 5-25% for most companies)

**Python Implementation**:
- Fetch Rf from FRED API (`fredapi` library)
- Get beta from Yahoo Finance or calculate from historical returns
- Apply validation: warn if WACC outside 5-25% range
- Store as `WACCCalculator` class

---

### 3. Comparable Company Analysis ("Comps")
**Theory**: Value a company relative to similar public companies using trading multiples.

**Key Multiples**:
- **EV/Revenue**: Useful for high-growth, low-margin companies
- **EV/EBITDA**: Most common; controls for capital structure and taxes
- **P/E Ratio**: Simple but affected by accounting, capital structure
- **EV/EBIT**: Alternative to EBITDA for CapEx-heavy industries

**Excel Model Structure**:
- **Company Selection**: 5-15 comparable public companies
- **Financial Data**: Revenue, EBITDA, EBIT, Net Income, shares, net debt
- **Multiple Calculation**: EV/EBITDA, EV/Revenue, P/E for each comp
- **Statistics**: Mean, median, 25th/75th percentile
- **Target Valuation**: Apply multiples to target company's metrics
- **Adjustments**: Normalize for outliers (±2 std dev)

**Python Implementation**:
- Use `yfinance` for market data
- Percentile calculations with `numpy.percentile()`
- Outlier detection using Z-scores or IQR method
- Generate comparison table with conditional formatting

---

### 4. Precedent Transaction Analysis
**Theory**: Value a company based on M&A transactions of similar companies.

**Differences from Comps**:
- Uses transaction multiples (includes control premium)
- Typically 20-40% higher than trading multiples
- Less liquid data—requires manual research

**Excel Model Structure**:
- **Transaction List**: Date, target, acquirer, deal value, revenue, EBITDA
- **Multiple Calculation**: EV/Revenue, EV/EBITDA at transaction
- **Statistics**: Median/mean by time period (recent weighted higher)
- **Valuation Output**: Apply to target company

**Python Implementation**:
- Similar to Comps class but with premium adjustments
- Date-based filtering (last 3-5 years most relevant)
- Flag synergies if disclosed in filings

---

### 5. Leveraged Buyout (LBO) Model
**Theory**: Determine the price a PE firm can pay while achieving target returns (typically 20-25% IRR).

**Formula**:
```
Entry EV = Purchase Price + Transaction Costs - Cash Acquired
Exit EV = EBITDA × Exit Multiple (or EV/Revenue)
Equity Value = Exit EV - Net Debt
IRR = (Exit Equity Value / Initial Equity Investment)^(1/Years) - 1
MOIC = Exit Equity Value / Initial Equity Investment
```

**Excel Model Structure**:
- **Transaction Tab**: Sources (equity, debt tranches) & Uses (purchase price, fees)
- **Projections**: 5-7 year operating model (revenue growth → EBITDA)
- **Debt Schedule**: Multiple tranches (revolver, Term Loan A/B, bonds) with PIK/cash interest
- **Cash Flow Waterfall**: EBITDA → interest → taxes → CapEx → debt paydown
- **Returns Calculation**: Exit scenarios at varying multiples, IRR/MOIC grid
- **Sensitivity Tables**: IRR sensitivity to entry/exit multiple, EBITDA growth

**Python Implementation**:
- Use `numpy_financial.irr()` for IRR calculation
- Model each debt tranche as separate class (amortizing vs. bullet)
- Implement cash sweep logic (excess cash pays down debt)
- Create waterfall visualization with priority structure

---

### 6. Merger Model (Accretion/Dilution Analysis)
**Theory**: Analyze impact of an acquisition on the acquirer's EPS.

**Formula**:
```
Pro Forma EPS = (Acquirer NI + Target NI - Synergies - Interest on Debt) / 
                (Acquirer Shares + New Shares Issued)
Accretion % = (Pro Forma EPS / Standalone EPS) - 1
```

**Excel Model Structure**:
- **Transaction Assumptions**: Purchase price, % cash vs. stock, synergies, financing
- **Standalone Financials**: Acquirer and target P&Ls
- **Pro Forma Adjustments**: Interest expense, D&A, synergies, share issuance
- **EPS Analysis**: Accretion/dilution by year
- **Sensitivity**: Accretion sensitivity to purchase price and synergy realization

**Python Implementation**:
- Model purchase price allocation (PPA) with goodwill calculation
- Track earnout provisions if applicable
- Support multiple financing scenarios (100% cash, 50/50, 100% stock)

---

## Financial Statement Analysis

### Income Statement Key Items
```
Revenue (Top Line)
- Cost of Goods Sold (COGS)
= Gross Profit
- SG&A (Selling, General & Administrative)
- R&D
- D&A (Depreciation & Amortization)
= EBIT (Operating Income)
- Interest Expense
= EBT (Pre-Tax Income)
- Taxes
= Net Income (Bottom Line)
```

### Balance Sheet Structure
```
ASSETS = LIABILITIES + EQUITY

Assets:
- Current: Cash, AR, Inventory
- Non-Current: PP&E, Intangibles, Investments

Liabilities:
- Current: AP, Short-Term Debt
- Non-Current: Long-Term Debt, Deferred Taxes

Equity:
- Common Stock, Retained Earnings, AOCI
```

### Cash Flow Statement
```
Operating Activities: Net Income + D&A - ΔNW
Investing Activities: - CapEx - Acquisitions + Asset Sales
Financing Activities: + Debt Issued - Debt Repaid +/- Equity
= Change in Cash
```

---

## Excel Modeling Best Practices

### 1. Structure & Layout
- **Color Coding**: Blue = inputs, Black = formulas, Green = links
- **One Formula per Row**: Avoid nested logic; break into steps
- **Consistent Time Periods**: Annual left-to-right, clearly labeled
- **Error Checks**: #REF!, #DIV/0!, #N/A should flag RED

### 2. Formula Standards
- **Use Named Ranges**: `=Revenue_Growth_Rate` not `=B5`
- **Avoid Hardcoding**: Put constants in Assumptions tab
- **Flexible Ranges**: Use `OFFSET()` or Tables for dynamic data
- **Audit Trail**: `=A1+B1 "Growth Rate 5%"` in comments

### 3. Sensitivity Tables
- **1-Way**: Single variable (e.g., revenue growth 0-10%)
- **2-Way**: Two variables (e.g., WACC vs. Terminal Growth)
- **Use Data Tables**: Excel's built-in tool for auto-calculation

### 4. Formatting
- **Thousands Separator**: `#,##0` for readability
- **Percentages**: `0.0%` not `0.05` in cells
- **Conditional Formatting**: Highlight negative cash, EPS dilution RED

---

## Python Implementation Guidelines

### Project Structure
```
src/
├── models/
│   ├── dcf.py           # DCFModel class
│   ├── wacc.py          # WACCCalculator
│   ├── comps.py         # CompsAnalysis
│   ├── precedents.py    # PrecedentTransactions
│   ├── lbo.py           # LBOModel
│   └── merger.py        # MergerModel
├── data/
│   ├── fetcher.py       # API calls (yfinance, FRED)
│   ├── parser.py        # Extract from PDFs, filings
│   └── cache.py         # Local data storage
├── excel/
│   ├── generator.py     # Create Excel files
│   ├── formatter.py     # Apply IB-standard formatting
│   └── templates/       # Base templates
└── utils/
    ├── validators.py    # Input validation
    └── helpers.py       # Common calculations
```

### Excel Generation Strategy
1. **Template-Based**: Start with blank workbook, add sheets programmatically
2. **Formatting First**: Define styles upfront (`openpyxl.styles`)
3. **Data Then Formulas**: Write raw data, then Excel formulas (not Python calculations)
4. **Named Ranges**: Use `workbook.define_name()` for key inputs
5. **Freeze Panes**: Lock headers for easier navigation
6. **Data Validation**: Dropdown lists, input constraints

### Key Libraries
```python
import pandas as pd              # Data manipulation
import numpy as np               # Numerical operations
import yfinance as yf            # Market data
from fredapi import Fred         # Risk-free rate
import openpyxl                  # Excel writing
from openpyxl.styles import Font, PatternFill, Border
from openpyxl.utils.dataframe import dataframe_to_rows
import numpy_financial as npf    # IRR, NPV
```

### Error Handling
- **Validate Inputs**: Check for negative debt, unrealistic growth (>50%), missing data
- **Graceful Degradation**: If API fails, use cached data or prompt user for manual input
- **Logging**: Record all assumptions, data sources, calculation steps

---

## Data Sources & APIs

### Market Data
- **Yahoo Finance** (`yfinance`): Stock prices, beta, market cap
- **Alpha Vantage**: Fundamental data, alternative to Yahoo
- **FRED** (`fredapi`): Treasury rates, macro indicators

### Company Financials
- **SEC EDGAR**: 10-K, 10-Q filings (free)
- **Financial Modeling Prep**: Structured financial data (freemium)
- **Manual Input**: User uploads Excel/PDF of financials

### Comps/Precedent Transactions
- **Manual Research**: Most reliable for precedents
- **Bloomberg/Capital IQ**: Premium (not accessible)
- **Fallback**: User-provided spreadsheet of comps

---

## Validation & Testing

### Unit Tests
- **DCF**: Test with known company (AAPL), verify EV matches Bloomberg ±5%
- **WACC**: Validate components sum correctly, WACC in reasonable range
- **LBO**: Ensure debt schedule balances, IRR > 0%

### Integration Tests
- **End-to-End**: Upload financial data → Generate DCF → Export Excel
- **Error Cases**: Missing revenue, negative EBITDA, zero shares outstanding

### Regression Tests
- **Template Integrity**: Generated Excel matches IB standards
- **Formula Accuracy**: Excel formulas calculate correctly when user changes inputs

---

## Advanced Topics (Future Enhancements)

### Monte Carlo Simulation
- Run 10,000 scenarios with randomized inputs (revenue growth, margins)
- Output probability distribution of valuations

### Real Options Analysis
- Value flexibility (e.g., option to expand, abandon)
- Use Black-Scholes framework

### Credit Analysis
- Interest coverage ratio, leverage ratios
- Predict credit rating (AAA → D)

### Trading Comps Dashboard
- Auto-refresh market data daily
- Alert when target multiple deviates >2 std dev from peers

---

## Notes
- All formulas assume **fiscal year-end consistency** (adjust for calendar mismatches)
- **Private company adjustments**: Apply 20-35% DLOM (Discount for Lack of Marketability)
- **Control premium**: Precedents include 20-40% premium vs. trading multiples
- **Synergy assumptions**: Be conservative; typical realization is 50-70% of projected