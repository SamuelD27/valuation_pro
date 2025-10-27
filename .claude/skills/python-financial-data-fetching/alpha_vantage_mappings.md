# Alpha Vantage Complete Field Mappings

Comprehensive guide to all fields returned by Alpha Vantage API for financial statements and company overview.

## API Endpoints

| Function | Description | Rate Limit (Free) |
|----------|-------------|-------------------|
| INCOME_STATEMENT | Annual & quarterly income statements | 25 calls/day |
| BALANCE_SHEET | Annual & quarterly balance sheets | 25 calls/day |
| CASH_FLOW | Annual & quarterly cash flows | 25 calls/day |
| OVERVIEW | Company fundamentals and ratios | 25 calls/day |
| TIME_SERIES_DAILY | Historical prices | 25 calls/day |

## Income Statement Fields

### API Response Structure
```json
{
  "symbol": "AAPL",
  "annualReports": [
    {
      "fiscalDateEnding": "2023-09-30",
      "reportedCurrency": "USD",
      "grossProfit": "169148000000",
      // ... more fields
    }
  ],
  "quarterlyReports": [...]
}
```

### Field Mappings

| Alpha Vantage Field | Standard Field | Type | Notes |
|---------------------|----------------|------|-------|
| fiscalDateEnding | metadata | date | Fiscal year/quarter end date |
| reportedCurrency | metadata | string | Usually "USD" |
| grossProfit | gross_profit | float | Revenue - COGS |
| totalRevenue | revenue | float | Top line revenue |
| costOfRevenue | cogs | float | Cost of goods sold |
| costofGoodsAndServicesSold | cogs | float | Alternative field for COGS |
| operatingIncome | operating_income | float | EBIT |
| sellingGeneralAndAdministrative | sg_and_a | float | Part of operating expenses |
| researchAndDevelopment | r_and_d | float | Part of operating expenses |
| operatingExpenses | operating_expenses | float | SG&A + R&D + other |
| investmentIncomeNet | investment_income | float | Non-operating income |
| netInterestIncome | net_interest_income | float | Interest income - expense |
| interestIncome | interest_income | float | Interest earned |
| interestExpense | interest_expense | float | Interest paid |
| nonInterestIncome | non_interest_income | float | For financial institutions |
| otherNonOperatingIncome | other_income | float | Misc non-operating items |
| depreciation | depreciation | float | D&A (sometimes separate) |
| depreciationAndAmortization | depreciation_amortization | float | Combined D&A |
| incomeBeforeTax | pre_tax_income | float | Income before tax provision |
| incomeTaxExpense | tax_expense | float | Tax provision |
| interestAndDebtExpense | interest_expense | float | Alternative field |
| netIncomeFromContinuingOperations | continuing_ops_income | float | Before discontinued ops |
| comprehensiveIncomeNetOfTax | comprehensive_income | float | Net income + OCI |
| ebit | ebit | float | Earnings before interest & tax |
| ebitda | ebitda | float | EBIT + D&A |
| netIncome | net_income | float | Bottom line |

### Derived Calculations

```python
# If fields are missing, calculate:
gross_profit = total_revenue - cost_of_revenue
operating_expenses = selling_general_admin + research_development
operating_income = gross_profit - operating_expenses
ebit = operating_income  # Usually equivalent
ebitda = ebit + depreciation_and_amortization
income_before_tax = operating_income + net_interest_income + other_income
net_income = income_before_tax - income_tax_expense
```

## Balance Sheet Fields

### API Response Structure
```json
{
  "symbol": "AAPL",
  "annualReports": [
    {
      "fiscalDateEnding": "2023-09-30",
      "reportedCurrency": "USD",
      "totalAssets": "352755000000",
      // ... more fields
    }
  ]
}
```

### Field Mappings

| Alpha Vantage Field | Standard Field | Type | Notes |
|---------------------|----------------|------|-------|
| **Assets** |
| totalAssets | total_assets | float | Total assets |
| totalCurrentAssets | current_assets | float | Assets < 1 year |
| cashAndCashEquivalentsAtCarryingValue | cash | float | Cash and equivalents |
| cashAndShortTermInvestments | cash_and_st_investments | float | Cash + marketable securities |
| inventory | inventory | float | Inventory value |
| currentNetReceivables | accounts_receivable | float | A/R net of allowances |
| totalNonCurrentAssets | non_current_assets | float | Assets >= 1 year |
| propertyPlantEquipment | ppe | float | Net PP&E |
| accumulatedDepreciationAmortizationPPE | accumulated_depreciation | float | Contra-asset |
| intangibleAssets | intangible_assets | float | Patents, trademarks, etc |
| intangibleAssetsExcludingGoodwill | intangibles_ex_goodwill | float | Excludes goodwill |
| goodwill | goodwill | float | From acquisitions |
| investments | investments | float | Long-term investments |
| longTermInvestments | long_term_investments | float | Investments > 1 year |
| shortTermInvestments | short_term_investments | float | Marketable securities |
| otherCurrentAssets | other_current_assets | float | Misc current assets |
| otherNonCurrentAssets | other_non_current_assets | float | Misc non-current |
| **Liabilities** |
| totalLiabilities | total_liabilities | float | Total liabilities |
| totalCurrentLiabilities | current_liabilities | float | Liabilities < 1 year |
| currentAccountsPayable | accounts_payable | float | A/P to suppliers |
| deferredRevenue | deferred_revenue | float | Unearned revenue |
| currentDebt | short_term_debt | float | Debt due < 1 year |
| shortTermDebt | short_term_debt | float | Alternative field |
| totalNonCurrentLiabilities | non_current_liabilities | float | Liabilities >= 1 year |
| capitalLeaseObligations | capital_leases | float | Lease obligations |
| longTermDebt | long_term_debt | float | Debt due > 1 year |
| currentLongTermDebt | current_portion_lt_debt | float | LT debt due this year |
| longTermDebtNoncurrent | long_term_debt | float | Alternative field |
| shortLongTermDebtTotal | total_debt | float | All debt |
| otherCurrentLiabilities | other_current_liabilities | float | Misc current |
| otherNonCurrentLiabilities | other_non_current_liabilities | float | Misc non-current |
| **Equity** |
| totalShareholderEquity | total_equity | float | Assets - Liabilities |
| treasuryStock | treasury_stock | float | Repurchased shares (negative) |
| retainedEarnings | retained_earnings | float | Cumulative earnings |
| commonStock | common_stock | float | Par value of shares |
| commonStockSharesOutstanding | shares_outstanding | float | Number of shares |

### Balance Sheet Equation Validation

```python
# Must hold (within 1% tolerance):
total_assets ≈ total_liabilities + total_shareholder_equity

# Current ratio:
current_ratio = total_current_assets / total_current_liabilities

# Debt-to-equity:
debt_to_equity = total_debt / total_shareholder_equity
```

## Cash Flow Statement Fields

### API Response Structure
```json
{
  "symbol": "AAPL",
  "annualReports": [
    {
      "fiscalDateEnding": "2023-09-30",
      "reportedCurrency": "USD",
      "operatingCashflow": "110543000000",
      // ... more fields
    }
  ]
}
```

### Field Mappings

| Alpha Vantage Field | Standard Field | Type | Notes |
|---------------------|----------------|------|-------|
| **Operating Activities** |
| operatingCashflow | operating_cash_flow | float | Cash from operations |
| paymentsForOperatingActivities | operating_payments | float | Cash paid for ops |
| proceedsFromOperatingActivities | operating_proceeds | float | Cash received |
| changeInOperatingLiabilities | change_operating_liabilities | float | Working capital change |
| changeInOperatingAssets | change_operating_assets | float | Working capital change |
| depreciationDepletionAndAmortization | depreciation_amortization | float | Non-cash expense |
| capitalExpenditures | capex | float | CapEx (often positive) |
| changeInReceivables | change_receivables | float | A/R change |
| changeInInventory | change_inventory | float | Inventory change |
| profitLoss | net_income | float | Starting point for OCF |
| **Investing Activities** |
| cashflowFromInvestment | investing_cash_flow | float | Net investing CF |
| cashflowFromInvestmentNet | investing_cash_flow | float | Alternative field |
| paymentsForInvestingActivities | investing_payments | float | Cash paid |
| proceedsFromInvestingActivities | investing_proceeds | float | Cash received |
| capitalExpenditures | capex | float | Purchase of PP&E |
| paymentsToAcquirePropertyPlantAndEquipment | capex | float | Alternative field |
| proceedsFromSaleOfPropertyPlantAndEquipment | ppe_sales | float | Asset disposals |
| paymentsToAcquireBusinessesNetOfCash | acquisitions | float | M&A cash paid |
| paymentsForRepaymentsOfShortTermDebt | st_debt_payments | float | Debt repayment |
| **Financing Activities** |
| cashflowFromFinancing | financing_cash_flow | float | Net financing CF |
| paymentsForFinancingActivities | financing_payments | float | Cash paid |
| proceedsFromFinancingActivities | financing_proceeds | float | Cash received |
| proceedsFromRepaymentsOfShortTermDebt | st_debt_proceeds | float | Debt issued |
| proceedsFromRepaymentsOfLongTermDebt | lt_debt_proceeds | float | Debt issued |
| paymentsForRepaymentsOfLongTermDebt | lt_debt_payments | float | Debt repaid |
| proceedsFromIssuanceOfCommonStock | stock_issued | float | Equity raised |
| paymentsForRepurchaseOfCommonStock | stock_repurchased | float | Buybacks |
| dividendPayout | dividends_paid | float | Cash dividends |
| dividendPayoutCommonStock | common_dividends | float | Common stock only |
| dividendPayoutPreferredStock | preferred_dividends | float | Preferred stock |
| **Summary** |
| changeInCashAndCashEquivalents | change_in_cash | float | Total cash change |
| beginningCashPosition | beginning_cash | float | Cash at start |
| endingCashPosition | ending_cash | float | Cash at end |

### Cash Flow Calculations

```python
# Free Cash Flow:
fcf = operating_cashflow - abs(capital_expenditures)

# Cash flow statement validation:
change_in_cash = (operating_cashflow + 
                  cashflow_from_investment + 
                  cashflow_from_financing)

# Alternatively:
ending_cash = beginning_cash + change_in_cash
```

## Company Overview (OVERVIEW) Fields

### API Response Structure
```json
{
  "Symbol": "AAPL",
  "Name": "Apple Inc",
  "Exchange": "NASDAQ",
  "Currency": "USD",
  "Country": "USA",
  // ... 50+ fields
}
```

### Field Mappings

| Alpha Vantage Field | Standard Field | Type | Notes |
|---------------------|----------------|------|-------|
| **Company Info** |
| Symbol | ticker | string | Stock ticker |
| Name | company_name | string | Full company name |
| Description | description | string | Business description |
| Exchange | exchange | string | Listed exchange |
| Currency | currency | string | Reporting currency |
| Country | country | string | Country of domicile |
| Sector | sector | string | GICS sector |
| Industry | industry | string | GICS industry |
| Address | address | string | HQ address |
| FiscalYearEnd | fiscal_year_end | string | Month (e.g., "September") |
| LatestQuarter | latest_quarter | date | Most recent quarter |
| **Market Data** |
| MarketCapitalization | market_cap | float | Market cap |
| EBITDA | ebitda | float | Trailing 12m EBITDA |
| PERatio | trailing_pe | float | Price/earnings |
| PEGRatio | peg_ratio | float | PE to growth |
| BookValue | book_value_per_share | float | Equity/share |
| DividendPerShare | dividend_per_share | float | Annual dividend |
| DividendYield | dividend_yield | float | Yield % |
| EPS | eps | float | Earnings per share |
| RevenuePerShareTTM | revenue_per_share | float | Revenue/share (TTM) |
| ProfitMargin | profit_margin | float | Net margin |
| OperatingMarginTTM | operating_margin | float | Operating margin |
| ReturnOnAssetsTTM | roa | float | ROA |
| ReturnOnEquityTTM | roe | float | ROE |
| RevenueTTM | revenue_ttm | float | Trailing 12m revenue |
| GrossProfitTTM | gross_profit_ttm | float | Trailing 12m GP |
| DilutedEPSTTM | diluted_eps_ttm | float | Diluted EPS |
| QuarterlyEarningsGrowthYOY | earnings_growth_yoy | float | YoY growth % |
| QuarterlyRevenueGrowthYOY | revenue_growth_yoy | float | YoY growth % |
| AnalystTargetPrice | analyst_target | float | Consensus target |
| TrailingPE | trailing_pe | float | Trailing P/E |
| ForwardPE | forward_pe | float | Forward P/E |
| PriceToSalesRatioTTM | price_to_sales | float | P/S ratio |
| PriceToBookRatio | price_to_book | float | P/B ratio |
| EVToRevenue | ev_to_revenue | float | EV/Revenue |
| EVToEBITDA | ev_to_ebitda | float | EV/EBITDA |
| **Stock Data** |
| SharesOutstanding | shares_outstanding | float | Total shares |
| DividendDate | dividend_date | date | Last dividend date |
| ExDividendDate | ex_dividend_date | date | Ex-dividend date |
| **Risk Metrics** |
| Beta | beta | float | Market correlation |
| 52WeekHigh | 52_week_high | float | 52w high price |
| 52WeekLow | 52_week_low | float | 52w low price |
| 50DayMovingAverage | ma_50 | float | 50-day MA |
| 200DayMovingAverage | ma_200 | float | 200-day MA |

## Data Quality Notes

### Common Issues

1. **Missing Fields**: Not all companies have all fields (e.g., no dividends for growth stocks)
2. **"None" String**: Alpha Vantage returns "None" as string, not Python None
3. **Currency Variations**: Check `reportedCurrency` field
4. **Fiscal vs Calendar Year**: Use `fiscalDateEnding` for alignment
5. **Rate Limits**: Free tier = 25 calls/day (5 calls/minute)

### Validation Checks

```python
def validate_alpha_vantage_response(data: dict) -> bool:
    """Validate API response quality."""
    
    # Check for error messages
    if 'Error Message' in data:
        raise DataUnavailableError(data['Error Message'])
    
    # Check for rate limit
    if 'Note' in data:
        raise RateLimitError("API rate limit exceeded")
    
    # Check for annual reports
    if 'annualReports' not in data or len(data['annualReports']) == 0:
        return False
    
    # Check for required fields in first report
    first_report = data['annualReports'][0]
    required_fields = ['fiscalDateEnding', 'reportedCurrency']
    
    return all(field in first_report for field in required_fields)
```

### Field Extraction Pattern

```python
def safe_extract(data: dict, field: str, default=None) -> Optional[float]:
    """Safely extract and convert field."""
    value = data.get(field, default)
    
    # Handle "None" string
    if value in [None, "None", ""]:
        return None
    
    try:
        return float(value)
    except (ValueError, TypeError):
        return None
```

## Example API Calls

### Fetching Income Statement
```python
import requests

url = "https://www.alphavantage.co/query"
params = {
    'function': 'INCOME_STATEMENT',
    'symbol': 'AAPL',
    'apikey': 'YOUR_API_KEY'
}

response = requests.get(url, params=params)
data = response.json()

# Extract revenue from most recent year
latest_report = data['annualReports'][0]
revenue = float(latest_report['totalRevenue'])
```

### Batch Fetching with Rate Limiting
```python
import time

def fetch_all_statements(ticker: str, api_key: str) -> dict:
    """Fetch all financial statements with rate limiting."""
    
    functions = ['INCOME_STATEMENT', 'BALANCE_SHEET', 'CASH_FLOW', 'OVERVIEW']
    results = {}
    
    for func in functions:
        params = {
            'function': func,
            'symbol': ticker,
            'apikey': api_key
        }
        
        response = requests.get(BASE_URL, params=params)
        results[func] = response.json()
        
        # Rate limit: wait 12 seconds between calls (5 calls/minute)
        if func != functions[-1]:  # Don't wait after last call
            time.sleep(12)
    
    return results
```

## Rate Limit Management

### Free Tier Limits
- **25 API calls per day** (resets at midnight UTC)
- **5 API calls per minute**
- Total = 4 API calls needed per ticker (Income/Balance/Cash/Overview)
- Max tickers per day = 25 / 4 = **6 tickers/day**

### Premium Tier ($49.99/month)
- **500 API calls per day**
- **10 API calls per minute**
- Max tickers per day = 500 / 4 = **125 tickers/day**

### Optimization Strategies

1. **Aggressive caching**: Cache for 24h minimum
2. **Batch requests**: Fetch all statements at once
3. **Use yfinance as primary**: Reserve Alpha Vantage for fallback
4. **Track usage**: Monitor daily call count
