---
name: python-financial-data-fetching
description: Standardized financial data extraction from yfinance, Alpha Vantage, and SEC EDGAR for investment banking valuations. Use when building data fetchers, normalizing financial statements, handling API rate limits, or implementing fallback strategies for missing data.
---

# Python Financial Data Fetching

Comprehensive toolkit for extracting and standardizing financial data from multiple sources for investment banking-grade valuation models (DCF, LBO, Comps).

## Core Principles

1. **Multi-source strategy**: Primary + fallback sources to handle API failures
2. **Standardized output**: All sources return consistent FinancialData schema
3. **Graceful degradation**: Missing fields marked as None, not errors
4. **Caching**: 24-hour cache for API responses to respect rate limits
5. **Validation**: Check data quality before returning to caller

## Data Sources Overview

| Source | Best For | Rate Limits | Data Quality | Cost |
|--------|----------|-------------|--------------|------|
| yfinance | Quick prototyping, market data | 2000/hr/IP | Medium | Free |
| Alpha Vantage | Backup, international stocks | 25/day free, 500/day premium | High | Free tier available |
| SEC EDGAR | US public companies, official filings | 10/sec | Highest | Free |

**Recommended strategy**: yfinance primary → Alpha Vantage fallback → SEC EDGAR for validation

## Quick Start

```python
from data_fetcher import UnifiedDataFetcher

fetcher = UnifiedDataFetcher(cache_enabled=True)
data = fetcher.get_company_data('AAPL')

# Access standardized fields
print(data.income_statement['revenue'])  # List of annual revenues
print(data.balance_sheet['total_debt'])  # Total debt
print(data.market_data['beta'])          # Beta
```

## Implementation Patterns

### Pattern 1: Multi-Source Fetch with Fallback

```python
def get_with_fallback(self, ticker: str) -> FinancialData:
    """Try primary source, fallback to secondary if fails."""
    try:
        return self.yfinance_fetcher.fetch(ticker)
    except (DataUnavailableError, RateLimitError) as e:
        logger.warning(f"yfinance failed: {e}, trying Alpha Vantage")
        try:
            return self.alpha_vantage_fetcher.fetch(ticker)
        except Exception as e2:
            raise DataUnavailableError(
                f"All sources failed for {ticker}: yfinance={e}, av={e2}"
            )
```

### Pattern 2: Data Normalization

See `references/normalization_rules.md` for complete field mapping.

```python
def normalize_income_statement(self, raw_data: dict) -> dict:
    """Convert source-specific fields to standard schema."""
    return {
        'revenue': self._extract_field(raw_data, ['totalRevenue', 'Total Revenue']),
        'cogs': self._extract_field(raw_data, ['costOfRevenue', 'Cost Of Goods Sold']),
        'gross_profit': self._extract_field(raw_data, ['grossProfit', 'Gross Profit']),
        'operating_income': self._extract_field(raw_data, ['operatingIncome', 'EBIT']),
        'net_income': self._extract_field(raw_data, ['netIncome', 'Net Income']),
    }
```

### Pattern 3: Rate Limit Management

```python
import time
from functools import wraps

def rate_limit(calls_per_second: float):
    min_interval = 1.0 / calls_per_second
    last_call = [0.0]
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_call[0]
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            last_call[0] = time.time()
            return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limit(2.0)  # Max 2 calls/second for SEC EDGAR
def fetch_from_edgar(cik: str):
    # ... implementation
```

### Pattern 4: Caching Strategy

```python
import pickle
from pathlib import Path
from datetime import datetime, timedelta

class DataCache:
    def __init__(self, cache_dir: Path, ttl_hours: int = 24):
        self.cache_dir = cache_dir
        self.ttl = timedelta(hours=ttl_hours)
    
    def get(self, key: str) -> Optional[dict]:
        cache_file = self.cache_dir / f"{key}.pkl"
        if not cache_file.exists():
            return None
        
        # Check age
        age = datetime.now() - datetime.fromtimestamp(cache_file.stat().st_mtime)
        if age > self.ttl:
            cache_file.unlink()  # Delete stale cache
            return None
        
        with open(cache_file, 'rb') as f:
            return pickle.load(f)
    
    def set(self, key: str, value: dict):
        with open(self.cache_dir / f"{key}.pkl", 'wb') as f:
            pickle.dump(value, f)
```

## Data Schema

Standard output format across all sources:

```python
@dataclass
class FinancialData:
    ticker: str
    company_name: str
    fiscal_year_end: str  # 'December' or 'MM-DD'
    
    # Income Statement (5 years historical)
    income_statement: dict[str, list[float]] = field(default_factory=dict)
    # Keys: revenue, cogs, gross_profit, operating_expenses, operating_income,
    #       interest_expense, tax_expense, net_income, ebitda, ebit
    
    # Balance Sheet (5 years historical)
    balance_sheet: dict[str, list[float]] = field(default_factory=dict)
    # Keys: total_assets, current_assets, cash, accounts_receivable, inventory,
    #       total_liabilities, current_liabilities, total_debt, long_term_debt,
    #       short_term_debt, accounts_payable, total_equity
    
    # Cash Flow Statement (5 years historical)
    cash_flow: dict[str, list[float]] = field(default_factory=dict)
    # Keys: operating_cash_flow, investing_cash_flow, financing_cash_flow,
    #       free_cash_flow, capex, dividends_paid
    
    # Market Data (point-in-time)
    market_data: dict[str, float] = field(default_factory=dict)
    # Keys: market_cap, shares_outstanding, current_price, beta, 
    #       52_week_high, 52_week_low, avg_volume
    
    # Metadata
    data_quality: dict[str, str] = field(default_factory=dict)
    # Keys: source, fetch_timestamp, completeness_score, warnings
```

**Validation Rules**:
- Revenue must be positive for all years (or None if missing)
- Assets = Liabilities + Equity (within 1% tolerance)
- Operating Cash Flow should correlate with Net Income
- Beta should be between -3.0 and 3.0
- Market cap should match shares × price (within 5%)

## Source-Specific Implementation

### yfinance

**Pros**: Fast, free, extensive coverage  
**Cons**: Unofficial API (can break), missing some fields  
**Best for**: Prototyping, US stocks, market data

```python
import yfinance as yf

ticker = yf.Ticker("AAPL")

# Financial statements (already in standardized format)
income_stmt = ticker.financials  # Annual by default
balance = ticker.balance_sheet
cashflow = ticker.cashflow

# Market data
info = ticker.info
beta = info.get('beta')
market_cap = info.get('marketCap')
```

**Common Issues**:
1. `None` values for missing data → Fill with interpolation or raise warning
2. Quarterly vs Annual data → Always use `.financials` not `.quarterly_financials`
3. Currency mismatches → Check `info['currency']` and convert if needed

See `scripts/yfinance_extractor.py` for complete implementation.

### Alpha Vantage

**Pros**: Reliable, official API, JSON format  
**Cons**: Strict rate limits (25/day free), requires API key  
**Best for**: Fallback, international stocks

```python
import requests

API_KEY = "your_key_here"  # Get from https://www.alphavantage.co/support/#api-key
url = f"https://www.alphavantage.co/query"

# Income statement
params = {
    'function': 'INCOME_STATEMENT',
    'symbol': 'AAPL',
    'apikey': API_KEY
}
response = requests.get(url, params=params)
data = response.json()

# Extract annual reports
annual_reports = data['annualReports']  # List of dicts, most recent first
```

**Field Mappings** (Alpha Vantage → Standard):
- `totalRevenue` → `revenue`
- `costOfRevenue` → `cogs`
- `operatingIncome` → `operating_income`
- `netIncome` → `net_income`

See `references/alpha_vantage_mappings.md` for complete field list.

### SEC EDGAR

**Pros**: Official source, highest accuracy, includes full 10-K text  
**Cons**: US companies only, complex parsing, rate limits  
**Best for**: Validation, detailed analysis, regulatory data

```python
import requests
from bs4 import BeautifulSoup

# 1. Get CIK from ticker (use SEC company tickers JSON)
# 2. Get filing list for CIK
# 3. Extract XBRL data or parse HTML

headers = {'User-Agent': 'YourCompany support@yourcompany.com'}
url = f"https://data.sec.gov/submissions/CIK{cik:010d}.json"
response = requests.get(url, headers=headers)
filings = response.json()
```

**XBRL Tag Extraction**:
- Revenue: `us-gaap:Revenues`, `us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax`
- Total Assets: `us-gaap:Assets`
- Net Income: `us-gaap:NetIncomeLoss`

See `scripts/edgar_extractor.py` and `references/xbrl_tags.md` for complete implementation.

## Error Handling

### Error Hierarchy

```python
class DataFetchError(Exception):
    """Base exception for data fetching."""
    pass

class DataUnavailableError(DataFetchError):
    """Data not found for ticker."""
    pass

class RateLimitError(DataFetchError):
    """API rate limit exceeded."""
    pass

class ValidationError(DataFetchError):
    """Data failed quality checks."""
    pass
```

### Handling Missing Data

**Priority levels**:
1. **Critical fields** (revenue, assets, equity): Raise error if missing
2. **Important fields** (EBITDA, FCF): Calculate from other fields if possible
3. **Optional fields** (segment data): Set to None with warning

```python
def validate_data(data: FinancialData) -> list[str]:
    """Return list of warnings (empty if all good)."""
    warnings = []
    
    # Critical field checks
    if not data.income_statement.get('revenue'):
        raise ValidationError("Missing critical field: revenue")
    
    # Derived field calculations
    if not data.income_statement.get('ebitda'):
        # Calculate: EBITDA = Operating Income + D&A
        if 'operating_income' in data.income_statement:
            warnings.append("EBITDA missing, calculated from operating income")
            # ... calculation
    
    return warnings
```

## Usage Examples

### Example 1: Basic Data Fetch

```python
fetcher = UnifiedDataFetcher(
    yf_enabled=True,
    av_api_key=os.getenv('ALPHA_VANTAGE_KEY'),
    cache_dir=Path('./cache')
)

# Fetch data with automatic fallback
data = fetcher.get_company_data('AAPL')

# Check data quality
print(f"Source: {data.data_quality['source']}")
print(f"Completeness: {data.data_quality['completeness_score']}")

if data.data_quality['warnings']:
    for warning in data.data_quality['warnings']:
        print(f"⚠️  {warning}")
```

### Example 2: Batch Fetch for Comps

```python
comp_tickers = ['AAPL', 'MSFT', 'GOOGL', 'META', 'NVDA']
comp_data = {}

for ticker in comp_tickers:
    try:
        comp_data[ticker] = fetcher.get_company_data(ticker)
    except DataFetchError as e:
        print(f"❌ Failed to fetch {ticker}: {e}")
        continue

# Calculate median multiples
ev_ebitda_multiples = [
    calculate_ev_ebitda(data) for data in comp_data.values()
]
median_multiple = np.median(ev_ebitda_multiples)
```

### Example 3: Historical Data with Validation

```python
# Fetch 10 years of historical data
data = fetcher.get_company_data('AAPL', years=10)

# Validate data quality
revenue_list = data.income_statement['revenue']

# Check for consistent growth
if all(revenue_list[i] <= revenue_list[i+1] for i in range(len(revenue_list)-1)):
    print("✅ Revenue shows consistent growth")

# Check for anomalies (using simple z-score)
growth_rates = [
    (revenue_list[i+1] - revenue_list[i]) / revenue_list[i]
    for i in range(len(revenue_list)-1)
]
mean_growth = np.mean(growth_rates)
std_growth = np.std(growth_rates)

anomalies = [
    (i, rate) for i, rate in enumerate(growth_rates)
    if abs(rate - mean_growth) > 2 * std_growth
]

if anomalies:
    print(f"⚠️  Detected unusual growth rates: {anomalies}")
```

## Testing Strategy

**Unit tests** (test each source independently):
```python
def test_yfinance_extractor():
    """Test yfinance can fetch AAPL data."""
    extractor = YFinanceExtractor()
    data = extractor.fetch('AAPL')
    
    assert data.ticker == 'AAPL'
    assert data.company_name == 'Apple Inc.'
    assert len(data.income_statement['revenue']) >= 5
    assert all(r > 0 for r in data.income_statement['revenue'])
```

**Integration tests** (test fallback logic):
```python
def test_fallback_to_alpha_vantage():
    """Test fallback when yfinance fails."""
    fetcher = UnifiedDataFetcher()
    
    # Mock yfinance to fail
    with patch.object(fetcher.yf_extractor, 'fetch', side_effect=DataUnavailableError):
        data = fetcher.get_company_data('AAPL')
    
    assert data.data_quality['source'] == 'alpha_vantage'
```

**Validation tests** (test data quality):
```python
def test_balance_sheet_equation():
    """Assets = Liabilities + Equity."""
    data = fetcher.get_company_data('AAPL')
    
    for year_idx in range(len(data.balance_sheet['total_assets'])):
        assets = data.balance_sheet['total_assets'][year_idx]
        liabilities = data.balance_sheet['total_liabilities'][year_idx]
        equity = data.balance_sheet['total_equity'][year_idx]
        
        assert abs(assets - (liabilities + equity)) / assets < 0.01  # Within 1%
```

## Performance Optimization

1. **Parallel fetching**: Use `ThreadPoolExecutor` for batch requests
2. **Smart caching**: Cache normalized data, not raw API responses
3. **Lazy loading**: Only fetch statements when accessed
4. **Compression**: Use `pickle` with `protocol=4` for faster serialization

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def batch_fetch(tickers: list[str], max_workers: int = 5) -> dict[str, FinancialData]:
    results = {}
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_ticker = {
            executor.submit(fetcher.get_company_data, ticker): ticker
            for ticker in tickers
        }
        
        for future in as_completed(future_to_ticker):
            ticker = future_to_ticker[future]
            try:
                results[ticker] = future.result()
            except Exception as e:
                print(f"Failed {ticker}: {e}")
    
    return results
```

## Bundled Resources

- **`scripts/yfinance_extractor.py`**: Complete yfinance implementation
- **`scripts/alpha_vantage_extractor.py`**: Complete Alpha Vantage implementation
- **`scripts/edgar_extractor.py`**: Complete SEC EDGAR implementation
- **`scripts/unified_data_fetcher.py`**: Orchestration layer with fallback logic
- **`references/normalization_rules.md`**: Field mappings across all sources
- **`references/alpha_vantage_mappings.md`**: Complete Alpha Vantage field list
- **`references/xbrl_tags.md`**: Common XBRL tags for SEC EDGAR parsing
- **`assets/data_schema.json`**: JSON Schema for FinancialData validation

## Common Issues & Solutions

**Issue**: yfinance returns empty DataFrame  
**Solution**: Check if ticker is valid, try alternate ticker format (e.g., 'BRK.B' vs 'BRK-B')

**Issue**: Alpha Vantage 429 error  
**Solution**: Implement exponential backoff, cache aggressively, consider premium tier

**Issue**: SEC EDGAR XBRL tags vary by company  
**Solution**: Use multiple fallback tags per field (see `references/xbrl_tags.md`)

**Issue**: Data spans fiscal years, not calendar years  
**Solution**: Use fiscal year end from company metadata, align all dates

**Issue**: Currency conversions for international companies  
**Solution**: Fetch exchange rates from yfinance or use static conversion if USD-reporting

## Next Steps

After implementing this skill, consider:
1. **Real-time data**: Integrate websocket APIs for live market data
2. **Consensus estimates**: Add FactSet, Bloomberg Terminal access
3. **Alternative data**: Satellite imagery, credit card data, web scraping
4. **ML forecasting**: Train models on historical data for projections
