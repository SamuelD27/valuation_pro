# SEC EDGAR XBRL Tag Reference

Comprehensive guide to XBRL tags for parsing SEC filings (10-K, 10-Q).

## Overview

**XBRL (eXtensible Business Reporting Language)** is used by the SEC for electronic filing of financial statements. Each financial line item has a standardized tag.

### Namespace Prefixes
- `us-gaap:` - US GAAP standard taxonomy
- `dei:` - Document and Entity Information
- `company:` - Company-specific custom tags (e.g., `aapl:` for Apple)

## Core Financial Statement Tags

### Income Statement

| Standard Field | Primary XBRL Tag | Alternative Tags | Notes |
|----------------|------------------|------------------|-------|
| **Revenue** |
| Revenue | `us-gaap:Revenues` | `us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax` | Top line |
| | | `us-gaap:SalesRevenueNet` | Alternative |
| | | `us-gaap:SalesRevenueGoodsNet` | Goods only |
| | | `us-gaap:SalesRevenueServicesNet` | Services only |
| **Expenses** |
| COGS | `us-gaap:CostOfRevenue` | `us-gaap:CostOfGoodsAndServicesSold` | |
| Gross Profit | `us-gaap:GrossProfit` | Calculate: Revenue - COGS | |
| R&D | `us-gaap:ResearchAndDevelopmentExpense` | | |
| SG&A | `us-gaap:SellingGeneralAndAdministrativeExpense` | | |
| Operating Expenses | `us-gaap:OperatingExpenses` | `us-gaap:OperatingExpensesAbstract` | |
| **Operating Income** |
| Operating Income | `us-gaap:OperatingIncomeLoss` | `us-gaap:IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest` | EBIT |
| **Non-Operating** |
| Interest Expense | `us-gaap:InterestExpense` | `us-gaap:InterestExpenseDebt` | |
| Interest Income | `us-gaap:InterestIncomeExpenseNonoperatingNet` | `us-gaap:InvestmentIncomeInterest` | |
| Other Income | `us-gaap:OtherNonoperatingIncomeExpense` | | |
| **Taxes & Net Income** |
| Pre-Tax Income | `us-gaap:IncomeLossFromContinuingOperationsBeforeIncomeTaxes` | | |
| Tax Expense | `us-gaap:IncomeTaxExpenseBenefit` | `us-gaap:CurrentIncomeTaxExpenseBenefit` | |
| Net Income | `us-gaap:NetIncomeLoss` | `us-gaap:ProfitLoss` | Bottom line |
| | | `us-gaap:NetIncomeLossAvailableToCommonStockholdersBasic` | Excludes preferred |
| **Per Share** |
| EPS Basic | `us-gaap:EarningsPerShareBasic` | | |
| EPS Diluted | `us-gaap:EarningsPerShareDiluted` | | |
| Shares Outstanding | `us-gaap:WeightedAverageNumberOfSharesOutstandingBasic` | | |

### Balance Sheet

| Standard Field | Primary XBRL Tag | Alternative Tags | Notes |
|----------------|------------------|------------------|-------|
| **Assets - Current** |
| Current Assets | `us-gaap:AssetsCurrent` | | |
| Cash | `us-gaap:CashAndCashEquivalentsAtCarryingValue` | `us-gaap:Cash` | |
| | | `us-gaap:CashCashEquivalentsAndShortTermInvestments` | Includes ST investments |
| Marketable Securities | `us-gaap:MarketableSecurities` | `us-gaap:AvailableForSaleSecuritiesCurrent` | |
| Accounts Receivable | `us-gaap:AccountsReceivableNetCurrent` | `us-gaap:AccountsReceivableNet` | |
| Inventory | `us-gaap:InventoryNet` | | |
| Prepaid Expenses | `us-gaap:PrepaidExpenseCurrent` | | |
| Other Current Assets | `us-gaap:OtherAssetsCurrent` | | |
| **Assets - Non-Current** |
| PP&E (Gross) | `us-gaap:PropertyPlantAndEquipmentGross` | | |
| Accumulated Depreciation | `us-gaap:AccumulatedDepreciationDepletionAndAmortizationPropertyPlantAndEquipment` | | Contra-asset |
| PP&E (Net) | `us-gaap:PropertyPlantAndEquipmentNet` | Calculate: Gross - Accumulated | |
| Goodwill | `us-gaap:Goodwill` | | From acquisitions |
| Intangible Assets | `us-gaap:IntangibleAssetsNetExcludingGoodwill` | `us-gaap:FiniteLivedIntangibleAssetsNet` | |
| Long-term Investments | `us-gaap:LongTermInvestments` | | |
| Deferred Tax Assets | `us-gaap:DeferredTaxAssetsNetNoncurrent` | | |
| Other Assets | `us-gaap:OtherAssetsNoncurrent` | | |
| **Total Assets** |
| Total Assets | `us-gaap:Assets` | | Must equal L + E |
| **Liabilities - Current** |
| Current Liabilities | `us-gaap:LiabilitiesCurrent` | | |
| Accounts Payable | `us-gaap:AccountsPayableCurrent` | | |
| Accrued Expenses | `us-gaap:AccruedLiabilitiesCurrent` | | |
| Short-term Debt | `us-gaap:ShortTermBorrowings` | `us-gaap:DebtCurrent` | |
| | | `us-gaap:LongTermDebtCurrent` | Current portion of LT debt |
| Deferred Revenue | `us-gaap:DeferredRevenueCurrent` | `us-gaap:ContractWithCustomerLiabilityCurrent` | Unearned revenue |
| Other Current Liabilities | `us-gaap:OtherLiabilitiesCurrent` | | |
| **Liabilities - Non-Current** |
| Long-term Debt | `us-gaap:LongTermDebt` | `us-gaap:LongTermDebtNoncurrent` | |
| | | `us-gaap:LongTermDebtAndCapitalLeaseObligations` | Includes leases |
| Deferred Tax Liabilities | `us-gaap:DeferredTaxLiabilitiesNoncurrent` | | |
| Pension Liabilities | `us-gaap:PensionAndOtherPostretirementDefinedBenefitPlansLiabilitiesNoncurrent` | | |
| Other Liabilities | `us-gaap:OtherLiabilitiesNoncurrent` | | |
| **Total Liabilities** |
| Total Liabilities | `us-gaap:Liabilities` | | |
| **Equity** |
| Common Stock | `us-gaap:CommonStockValue` | | Par value |
| Additional Paid-in Capital | `us-gaap:AdditionalPaidInCapital` | | |
| Retained Earnings | `us-gaap:RetainedEarningsAccumulatedDeficit` | | Cumulative |
| Treasury Stock | `us-gaap:TreasuryStockValue` | | Negative (repurchased shares) |
| AOCI | `us-gaap:AccumulatedOtherComprehensiveIncomeLossNetOfTax` | | OCI cumulative |
| **Total Equity** |
| Total Equity | `us-gaap:StockholdersEquity` | `us-gaap:StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest` | |

### Cash Flow Statement

| Standard Field | Primary XBRL Tag | Alternative Tags | Notes |
|----------------|------------------|------------------|-------|
| **Operating Activities** |
| Net Income | `us-gaap:NetIncomeLoss` | | Starting point |
| D&A | `us-gaap:DepreciationDepletionAndAmortization` | `us-gaap:Depreciation` | Non-cash |
| Stock-based Comp | `us-gaap:ShareBasedCompensation` | | Non-cash |
| Deferred Taxes | `us-gaap:DeferredIncomeTaxExpenseBenefit` | | |
| Change in A/R | `us-gaap:IncreaseDecreaseInAccountsReceivable` | | Negative = increase |
| Change in Inventory | `us-gaap:IncreaseDecreaseInInventories` | | |
| Change in A/P | `us-gaap:IncreaseDecreaseInAccountsPayable` | | Positive = increase |
| Operating Cash Flow | `us-gaap:NetCashProvidedByUsedInOperatingActivities` | | Total OCF |
| **Investing Activities** |
| CapEx | `us-gaap:PaymentsToAcquirePropertyPlantAndEquipment` | | Negative |
| Asset Sales | `us-gaap:ProceedsFromSaleOfPropertyPlantAndEquipment` | | Positive |
| Acquisition | `us-gaap:PaymentsToAcquireBusinessesNetOfCashAcquired` | | Negative |
| Investment Purchase | `us-gaap:PaymentsToAcquireInvestments` | | Negative |
| Investment Sale | `us-gaap:ProceedsFromSaleOfInvestments` | | Positive |
| Investing Cash Flow | `us-gaap:NetCashProvidedByUsedInInvestingActivities` | | Total ICF |
| **Financing Activities** |
| Debt Issued | `us-gaap:ProceedsFromIssuanceOfLongTermDebt` | | Positive |
| Debt Repaid | `us-gaap:RepaymentsOfLongTermDebt` | | Negative |
| Stock Issued | `us-gaap:ProceedsFromIssuanceOfCommonStock` | | Positive |
| Stock Repurchased | `us-gaap:PaymentsForRepurchaseOfCommonStock` | | Negative (buybacks) |
| Dividends Paid | `us-gaap:PaymentsOfDividends` | `us-gaap:PaymentsOfDividendsCommonStock` | Negative |
| Financing Cash Flow | `us-gaap:NetCashProvidedByUsedInFinancingActivities` | | Total FCF |
| **Net Change** |
| Change in Cash | `us-gaap:CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalentsPeriodIncreaseDecreaseIncludingExchangeRateEffect` | | OCF + ICF + FCF |

## Document and Entity Information (DEI)

| Field | XBRL Tag | Notes |
|-------|----------|-------|
| Company Name | `dei:EntityRegistrantName` | Legal name |
| Ticker | `dei:TradingSymbol` | Stock ticker |
| CIK | `dei:EntityCentralIndexKey` | SEC identifier |
| Fiscal Year End | `dei:CurrentFiscalYearEndDate` | MM-DD format |
| Document Type | `dei:DocumentType` | 10-K, 10-Q, etc. |
| Reporting Period | `dei:DocumentPeriodEndDate` | Date of report |

## Parsing Strategies

### Strategy 1: Element-Level Parsing

```python
from lxml import etree

def parse_xbrl_fact(xml_root, tag_name: str, namespace: str = 'us-gaap') -> float:
    """
    Extract a single fact from XBRL.
    
    Args:
        xml_root: Parsed XML tree
        tag_name: XBRL tag name (e.g., 'Revenues')
        namespace: Namespace prefix (default 'us-gaap')
    
    Returns:
        Float value or None if not found
    """
    # Define namespace
    ns = {'us-gaap': 'http://fasb.org/us-gaap/2021-01-31'}
    
    # Find element
    elements = xml_root.findall(f'.//{{{ns[namespace]}}}{tag_name}')
    
    if not elements:
        return None
    
    # Get most recent value (if multiple periods)
    # Usually the first element is most recent
    value = elements[0].text
    
    try:
        return float(value)
    except (ValueError, TypeError):
        return None
```

### Strategy 2: Context-Based Parsing

XBRL uses contexts to specify time periods:

```python
def parse_annual_values(xml_root, tag_name: str, years: int = 5) -> list[float]:
    """
    Extract historical annual values for a tag.
    
    Returns:
        List of values (most recent first)
    """
    # Find all instances of the tag
    elements = xml_root.findall(f'.//{tag_name}')
    
    # Group by context (fiscal year)
    values_by_year = {}
    
    for elem in elements:
        context_ref = elem.get('contextRef')
        value = float(elem.text)
        
        # Extract year from context
        year = extract_year_from_context(xml_root, context_ref)
        values_by_year[year] = value
    
    # Sort by year (descending) and return
    sorted_years = sorted(values_by_year.keys(), reverse=True)
    return [values_by_year[year] for year in sorted_years[:years]]
```

### Strategy 3: Table-Based Extraction

Financial statements are often in structured tables:

```python
from bs4 import BeautifulSoup

def extract_financial_table(html: str, statement_type: str) -> dict:
    """
    Extract financial statement from HTML rendering.
    
    Args:
        html: HTML content of 10-K
        statement_type: 'income', 'balance', or 'cash_flow'
    
    Returns:
        Dict mapping field names to lists of annual values
    """
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find table with financial data
    # Usually has specific class or id
    table = soup.find('table', {'class': 'financial-statements'})
    
    # Parse table rows
    data = {}
    for row in table.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) > 1:
            field_name = cells[0].text.strip()
            values = [float(cell.text.replace(',', '')) 
                     for cell in cells[1:]]
            data[field_name] = values
    
    return normalize_fields(data, statement_type)
```

## Common Challenges

### Challenge 1: Missing Tags

Not all companies use all standard tags. Implement fallbacks:

```python
REVENUE_TAGS = [
    'us-gaap:Revenues',
    'us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax',
    'us-gaap:SalesRevenueNet',
    'us-gaap:SalesRevenueGoodsNet',
]

def get_revenue(xml_root) -> Optional[float]:
    """Try multiple revenue tags."""
    for tag in REVENUE_TAGS:
        value = parse_xbrl_fact(xml_root, tag)
        if value is not None:
            return value
    return None
```

### Challenge 2: Custom Tags

Companies create custom tags for unique line items:

```xml
<aapl:iPhoneRevenue>100000000000</aapl:iPhoneRevenue>
```

Solution: Inspect company filings to identify custom tags.

### Challenge 3: Unit Scaling

Values may be in different units:
- `unitRef="USD"` → Dollars
- `unitRef="USD_per_share"` → Per-share
- `decimals="-6"` → Millions

```python
def apply_unit_scaling(value: float, decimals: str) -> float:
    """Apply decimal scaling."""
    if decimals:
        scale = int(decimals)
        return value * (10 ** scale)
    return value
```

### Challenge 4: Negative Signs

Some items are naturally negative (expenses, contra-assets):
- Look for `negative="true"` attribute
- Apply sign conventions per field type

## Tools & Libraries

### Python Libraries for XBRL Parsing

| Library | Purpose | Pros | Cons |
|---------|---------|------|------|
| `lxml` | XML parsing | Fast, standard | Manual extraction |
| `BeautifulSoup` | HTML/XML parsing | Easy to use | Slower |
| `xbrl` | XBRL-specific | Purpose-built | Less maintained |
| `arelle` | SEC-approved XBRL processor | Comprehensive | Complex |
| `secedgar` | SEC EDGAR API wrapper | Easy filing access | Limited parsing |

### Recommended Approach

```python
import requests
from lxml import etree

def fetch_10k_xbrl(cik: str, filing_date: str) -> dict:
    """
    Fetch and parse 10-K XBRL filing.
    
    Args:
        cik: Company CIK (10 digits, zero-padded)
        filing_date: Date of filing (YYYY-MM-DD)
    
    Returns:
        Dict with financial data
    """
    # 1. Get filing index
    url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    headers = {'User-Agent': 'YourCompany support@yourcompany.com'}
    response = requests.get(url, headers=headers)
    submissions = response.json()
    
    # 2. Find 10-K filing URL
    filings = submissions['filings']['recent']
    for i, form in enumerate(filings['form']):
        if form == '10-K' and filings['filingDate'][i] == filing_date:
            accession = filings['accessionNumber'][i]
            break
    
    # 3. Fetch XBRL instance document
    # Format: https://www.sec.gov/cgi-bin/viewer?action=view&cik={cik}&accession_number={accession}
    xbrl_url = construct_xbrl_url(cik, accession)
    xbrl_content = requests.get(xbrl_url, headers=headers).content
    
    # 4. Parse XBRL
    root = etree.fromstring(xbrl_content)
    
    # 5. Extract financial data
    data = {
        'income_statement': extract_income_statement(root),
        'balance_sheet': extract_balance_sheet(root),
        'cash_flow': extract_cash_flow(root),
    }
    
    return data
```

## Rate Limits

SEC EDGAR enforces strict rate limits:
- **10 requests per second**
- Must include `User-Agent` header with contact info
- Violators are blocked

```python
import time
from functools import wraps

def sec_rate_limit(func):
    """Rate limit decorator for SEC requests (10/sec)."""
    last_call = [0.0]
    min_interval = 0.1  # 100ms between calls
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        elapsed = time.time() - last_call[0]
        if elapsed < min_interval:
            time.sleep(min_interval - elapsed)
        last_call[0] = time.time()
        return func(*args, **kwargs)
    return wrapper

@sec_rate_limit
def fetch_from_edgar(url: str):
    # ... implementation
```

## Additional Resources

- **SEC XBRL Taxonomy**: https://www.sec.gov/structureddata/osd-inline-xbrl.html
- **US GAAP Taxonomy**: https://www.fasb.org/standards
- **EDGAR Search**: https://www.sec.gov/edgar/searchedgar/companysearch.html
- **CIK Lookup**: https://www.sec.gov/cgi-bin/browse-edgar?company=&CIK=

## Example: Complete Revenue Extraction

```python
def extract_revenue_history(cik: str, years: int = 5) -> list[float]:
    """
    Extract revenue for past N years from 10-K filings.
    
    Args:
        cik: Company CIK
        years: Number of years
    
    Returns:
        List of revenue values (most recent first)
    """
    # 1. Get list of 10-K filings
    filings = get_10k_filings(cik, years)
    
    # 2. Extract revenue from each filing
    revenues = []
    for filing in filings:
        xbrl = fetch_xbrl(filing['accession_number'])
        revenue = extract_tag_value(xbrl, REVENUE_TAGS)
        revenues.append(revenue)
    
    return revenues
```
