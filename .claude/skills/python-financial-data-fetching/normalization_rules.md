# Financial Data Normalization Rules

Complete field mapping guide for standardizing data across yfinance, Alpha Vantage, and SEC EDGAR.

## Standard Schema Structure

```python
FinancialData = {
    'income_statement': {
        'revenue': list[float],
        'cogs': list[float],
        'gross_profit': list[float],
        'operating_expenses': list[float],
        'operating_income': list[float],
        'interest_expense': list[float],
        'tax_expense': list[float],
        'net_income': list[float],
        'ebitda': list[float],
        'ebit': list[float],
    },
    'balance_sheet': {
        'total_assets': list[float],
        'current_assets': list[float],
        'cash': list[float],
        'accounts_receivable': list[float],
        'inventory': list[float],
        'total_liabilities': list[float],
        'current_liabilities': list[float],
        'total_debt': list[float],
        'long_term_debt': list[float],
        'short_term_debt': list[float],
        'accounts_payable': list[float],
        'total_equity': list[float],
    },
    'cash_flow': {
        'operating_cash_flow': list[float],
        'investing_cash_flow': list[float],
        'financing_cash_flow': list[float],
        'free_cash_flow': list[float],
        'capex': list[float],
        'dividends_paid': list[float],
    },
    'market_data': {
        'market_cap': float,
        'shares_outstanding': float,
        'current_price': float,
        'beta': float,
        '52_week_high': float,
        '52_week_low': float,
        'avg_volume': float,
        'enterprise_value': float,
        'trailing_pe': float,
        'forward_pe': float,
    }
}
```

## Income Statement Field Mappings

| Standard Field | yfinance | Alpha Vantage | SEC EDGAR XBRL |
|----------------|----------|---------------|----------------|
| revenue | Total Revenue | totalRevenue | us-gaap:Revenues |
| cogs | Cost Of Revenue | costOfRevenue | us-gaap:CostOfRevenue |
| gross_profit | Gross Profit | grossProfit | us-gaap:GrossProfit |
| operating_expenses | Operating Expense | operatingExpenses | us-gaap:OperatingExpenses |
| operating_income | Operating Income | operatingIncome | us-gaap:OperatingIncomeLoss |
| interest_expense | Interest Expense | interestExpense | us-gaap:InterestExpense |
| tax_expense | Tax Provision | incomeTaxExpense | us-gaap:IncomeTaxExpenseBenefit |
| net_income | Net Income | netIncome | us-gaap:NetIncomeLoss |
| ebitda | EBITDA | ebitda | Calculated |
| ebit | EBIT | ebit | us-gaap:OperatingIncomeLoss |

## Balance Sheet Field Mappings

| Standard Field | yfinance | Alpha Vantage | SEC EDGAR XBRL |
|----------------|----------|---------------|----------------|
| total_assets | Total Assets | totalAssets | us-gaap:Assets |
| current_assets | Current Assets | totalCurrentAssets | us-gaap:AssetsCurrent |
| cash | Cash And Cash Equivalents | cashAndCashEquivalentsAtCarryingValue | us-gaap:CashAndCashEquivalentsAtCarryingValue |
| accounts_receivable | Accounts Receivable | currentNetReceivables | us-gaap:AccountsReceivableNetCurrent |
| inventory | Inventory | inventory | us-gaap:InventoryNet |
| total_liabilities | Total Liabilities Net Minority Interest | totalLiabilities | us-gaap:Liabilities |
| current_liabilities | Current Liabilities | totalCurrentLiabilities | us-gaap:LiabilitiesCurrent |
| long_term_debt | Long Term Debt | longTermDebt | us-gaap:LongTermDebt |
| short_term_debt | Current Debt | shortTermDebt | us-gaap:ShortTermBorrowings |
| accounts_payable | Accounts Payable | currentAccountsPayable | us-gaap:AccountsPayableCurrent |
| total_equity | Total Equity Gross Minority Interest | totalShareholderEquity | us-gaap:StockholdersEquity |

**Calculated Fields:**
- `total_debt` = `long_term_debt` + `short_term_debt`

## Cash Flow Statement Field Mappings

| Standard Field | yfinance | Alpha Vantage | SEC EDGAR XBRL |
|----------------|----------|---------------|----------------|
| operating_cash_flow | Operating Cash Flow | operatingCashflow | us-gaap:NetCashProvidedByUsedInOperatingActivities |
| investing_cash_flow | Investing Cash Flow | cashflowFromInvestment | us-gaap:NetCashProvidedByUsedInInvestingActivities |
| financing_cash_flow | Financing Cash Flow | cashflowFromFinancing | us-gaap:NetCashProvidedByUsedInFinancingActivities |
| capex | Capital Expenditure | capitalExpenditures | us-gaap:PaymentsToAcquirePropertyPlantAndEquipment |
| dividends_paid | Cash Dividends Paid | dividendPayout | us-gaap:PaymentsOfDividends |

**Calculated Fields:**
- `free_cash_flow` = `operating_cash_flow` - abs(`capex`)
  - Note: yfinance returns capex as negative, Alpha Vantage as positive

## Market Data Field Mappings

| Standard Field | yfinance | Alpha Vantage | Notes |
|----------------|----------|---------------|-------|
| market_cap | marketCap | MarketCapitalization | |
| shares_outstanding | sharesOutstanding | SharesOutstanding | |
| current_price | currentPrice or regularMarketPrice | Price | |
| beta | beta | Beta | Range: -3 to 3 typically |
| 52_week_high | fiftyTwoWeekHigh | 52WeekHigh | |
| 52_week_low | fiftyTwoWeekLow | 52WeekLow | |
| avg_volume | averageVolume | Not available | yfinance only |
| trailing_pe | trailingPE | TrailingPE | |
| forward_pe | forwardPE | ForwardPE | |

**Calculated Fields:**
- `enterprise_value` = `market_cap` + `total_debt` - `cash`

## Normalization Rules

### 1. Unit Standardization

All monetary values should be in **native currency units** (usually USD):
- yfinance: Already in native units
- Alpha Vantage: Already in native units
- SEC EDGAR: Already in native units

**No unit conversion needed** unless dealing with international stocks reporting in foreign currencies.

### 2. Sign Conventions

Standardize signs across sources:
- **Revenue, Assets, Equity**: Always positive
- **Expenses, Liabilities**: Always positive
- **CapEx**: Store as **positive** value (opposite of cash outflow)
  - yfinance returns negative → Convert to positive
  - Alpha Vantage returns positive → Keep as-is
- **Debt**: Always positive

### 3. Missing Data Handling

Priority levels for missing fields:

**Level 1 - Critical (Raise error if missing):**
- revenue
- total_assets
- total_equity
- net_income

**Level 2 - Important (Calculate if possible, warn if not):**
- ebitda: Calculate from `ebit` + D&A if available
- ebit: Calculate from `operating_income` or `net_income` + taxes + interest
- free_cash_flow: Calculate from `operating_cash_flow` - `capex`
- total_debt: Calculate from `long_term_debt` + `short_term_debt`
- enterprise_value: Calculate from `market_cap` + `total_debt` - `cash`

**Level 3 - Optional (Set to None with debug log):**
- Segment data
- Quarterly data
- Non-GAAP metrics

### 4. Time Series Alignment

All time series data should be:
- **Annual** (not quarterly)
- **Most recent first** (descending order)
- **Same length** for all fields in a category
- **Fiscal year-aligned** (not calendar year)

Example:
```python
revenue = [100.0, 90.0, 85.0, 80.0, 75.0]  # 2024, 2023, 2022, 2021, 2020
```

### 5. Fiscal Year Handling

Companies have different fiscal year ends:
- Apple: September 30
- Microsoft: June 30
- Walmart: January 31

**Standard approach:**
1. Store fiscal year end in metadata
2. Label data points by fiscal year (not calendar year)
3. Align all calculations to fiscal year

### 6. Data Type Standardization

- **Floats**: All numeric values as `float` (not int, Decimal, or string)
- **None**: Missing values as Python `None` (not 0, NaN, or empty string)
- **Lists**: Time series as Python `list[float]` (not pandas Series or numpy array)
- **Dicts**: Structured data as Python `dict` (not DataFrame or custom objects)

### 7. Field Name Fallbacks

When a field has multiple possible names in source data, try in order:

**Example: Revenue**
1. 'Total Revenue'
2. 'totalRevenue'
3. 'Revenue'
4. 'Sales'
5. 'Net Sales'

**Example: Total Debt**
1. 'Total Debt'
2. Calculate: 'Long Term Debt' + 'Short Term Debt'
3. 'Debt'
4. 'Borrowings'

### 8. Validation Rules

After normalization, validate:

**Balance Sheet Equation:**
```python
abs(total_assets - (total_liabilities + total_equity)) / total_assets < 0.01
```

**Cash Flow Check:**
```python
operating_cash_flow + investing_cash_flow + financing_cash_flow ≈ change_in_cash
```

**Revenue Sanity:**
```python
revenue > 0 for all years
```

**Beta Range:**
```python
-3.0 <= beta <= 3.0 (typically)
```

**Market Cap Consistency:**
```python
abs(market_cap - (current_price * shares_outstanding)) / market_cap < 0.05
```

## Edge Cases

### Case 1: Negative Equity

Some companies have negative equity (losses exceed assets):
- Don't raise error
- Flag in warnings
- Handle carefully in valuation models (can't use P/B ratio)

### Case 2: Multiple Share Classes

Companies like Google (GOOGL vs GOOG):
- Use primary trading class (usually Class A)
- Adjust shares outstanding if needed
- Note in metadata

### Case 3: Foreign Currency

For non-USD companies:
- Store currency in metadata
- Optionally convert to USD using exchange rates
- Maintain consistency within dataset

### Case 4: Fiscal Year Transitions

If company changes fiscal year end:
- Note transition year in warnings
- May have partial year data
- Handle in time series alignment

### Case 5: Acquisitions/Divestitures

Major M&A can cause discontinuities:
- Flag unusual growth rates
- Consider pro forma adjustments
- Note in metadata

## Implementation Pattern

```python
def normalize_field(raw_data: dict, field_mapping: list[str], 
                    validation_func: Optional[Callable] = None) -> Optional[list[float]]:
    """
    Extract and normalize a field from raw source data.
    
    Args:
        raw_data: Raw data from source (DataFrame or dict)
        field_mapping: List of possible field names to try (priority order)
        validation_func: Optional function to validate extracted values
    
    Returns:
        Normalized list of float values, or None if field not found
    """
    for field_name in field_mapping:
        if field_name in raw_data:
            values = extract_values(raw_data[field_name])
            
            # Clean values
            values = [float(v) if pd.notna(v) else None for v in values]
            
            # Validate if function provided
            if validation_func and not validation_func(values):
                continue  # Try next field name
            
            return values
    
    return None  # Field not found


def validate_revenue(values: list[float]) -> bool:
    """Validate revenue values are positive."""
    return all(v is None or v > 0 for v in values)


def validate_beta(value: float) -> bool:
    """Validate beta is in reasonable range."""
    return value is None or -3.0 <= value <= 3.0
```

## Testing Normalization

```python
def test_normalization():
    """Test data normalization across sources."""
    
    # Fetch same company from all sources
    yf_data = yf_extractor.fetch('AAPL')
    av_data = av_extractor.fetch('AAPL')
    
    # Check revenue consistency (within 1%)
    yf_rev = yf_data.income_statement['revenue'][0]
    av_rev = av_data.income_statement['revenue'][0]
    
    assert abs(yf_rev - av_rev) / yf_rev < 0.01
    
    # Check balance sheet equation
    for data in [yf_data, av_data]:
        assets = data.balance_sheet['total_assets'][0]
        liabilities = data.balance_sheet['total_liabilities'][0]
        equity = data.balance_sheet['total_equity'][0]
        
        assert abs(assets - (liabilities + equity)) / assets < 0.01
```

## Common Normalization Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Values off by 1000x | Thousands vs millions | Check source documentation |
| Negative cash | Different sign conventions | Standardize signs |
| Missing EBITDA | Not all sources report | Calculate from EBIT + D&A |
| Beta = None | Not calculated for some stocks | Acceptable for non-traded companies |
| Fiscal year mismatch | Different fiscal year ends | Store fiscal year end in metadata |
| Outliers in time series | Acquisitions, accounting changes | Flag in warnings, don't filter |
| Zero total debt | Company has no debt | This is valid (e.g., Apple in 2000s) |
