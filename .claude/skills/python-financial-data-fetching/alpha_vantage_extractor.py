"""
Alpha Vantage Data Extractor for ValuationPro

Extracts financial data from Alpha Vantage API and normalizes to standard schema.
Implements rate limiting and handles API errors gracefully.
"""

import requests
import time
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
import logging
from functools import wraps

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class FinancialData:
    """Standardized financial data structure."""
    ticker: str
    company_name: str
    fiscal_year_end: str
    income_statement: dict[str, list[float]] = field(default_factory=dict)
    balance_sheet: dict[str, list[float]] = field(default_factory=dict)
    cash_flow: dict[str, list[float]] = field(default_factory=dict)
    market_data: dict[str, float] = field(default_factory=dict)
    data_quality: dict[str, str] = field(default_factory=dict)


class DataFetchError(Exception):
    """Base exception for data fetching errors."""
    pass


class RateLimitError(DataFetchError):
    """Raised when API rate limit is exceeded."""
    pass


class DataUnavailableError(DataFetchError):
    """Raised when data cannot be fetched."""
    pass


def rate_limit(calls_per_minute: int = 5):
    """
    Rate limiting decorator.
    
    Alpha Vantage free tier: 25 calls/day, 5 calls/minute
    """
    min_interval = 60.0 / calls_per_minute
    last_call = [0.0]
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_call[0]
            if elapsed < min_interval:
                sleep_time = min_interval - elapsed
                logger.debug(f"Rate limiting: sleeping {sleep_time:.2f}s")
                time.sleep(sleep_time)
            last_call[0] = time.time()
            return func(*args, **kwargs)
        return wrapper
    return decorator


class AlphaVantageExtractor:
    """Extracts and normalizes financial data from Alpha Vantage API."""
    
    BASE_URL = "https://www.alphavantage.co/query"
    
    def __init__(self, api_key: str):
        """
        Initialize extractor with API key.
        
        Args:
            api_key: Alpha Vantage API key (get from alphavantage.co)
        """
        if not api_key:
            raise ValueError("Alpha Vantage API key required")
        self.api_key = api_key
        self.warnings = []
    
    def fetch(self, ticker: str, years: int = 5) -> FinancialData:
        """
        Fetch financial data for a ticker.
        
        Args:
            ticker: Stock ticker symbol (e.g., 'AAPL')
            years: Number of historical years to fetch (default 5)
        
        Returns:
            FinancialData object with normalized data
        
        Raises:
            RateLimitError: If API rate limit exceeded
            DataUnavailableError: If ticker not found or data unavailable
        """
        self.warnings = []
        logger.info(f"Fetching data for {ticker} from Alpha Vantage")
        
        try:
            # Fetch all financial statements
            income_data = self._fetch_income_statement(ticker)
            balance_data = self._fetch_balance_sheet(ticker)
            cashflow_data = self._fetch_cash_flow(ticker)
            overview_data = self._fetch_company_overview(ticker)
            
            # Extract and normalize
            income_stmt = self._normalize_income_statement(income_data, years)
            balance = self._normalize_balance_sheet(balance_data, years)
            cashflow = self._normalize_cash_flow(cashflow_data, years)
            market = self._extract_market_data(overview_data)
            
            # Get company info
            company_name = overview_data.get('Name', ticker)
            fiscal_year_end = overview_data.get('FiscalYearEnd', 'December')
            
            # Create FinancialData object
            data = FinancialData(
                ticker=ticker.upper(),
                company_name=company_name,
                fiscal_year_end=fiscal_year_end,
                income_statement=income_stmt,
                balance_sheet=balance,
                cash_flow=cashflow,
                market_data=market,
                data_quality={
                    'source': 'alpha_vantage',
                    'fetch_timestamp': datetime.now().isoformat(),
                    'completeness_score': self._calculate_completeness(
                        income_stmt, balance, cashflow
                    ),
                    'warnings': ', '.join(self.warnings) if self.warnings else 'None'
                }
            )
            
            logger.info(f"Successfully fetched {ticker} with completeness {data.data_quality['completeness_score']}")
            return data
            
        except RateLimitError:
            raise
        except Exception as e:
            logger.error(f"Error fetching {ticker}: {e}")
            raise DataUnavailableError(f"Failed to fetch {ticker}: {str(e)}")
    
    @rate_limit(calls_per_minute=5)
    def _api_call(self, function: str, symbol: str) -> dict:
        """
        Make API call with rate limiting.
        
        Args:
            function: API function name (e.g., 'INCOME_STATEMENT')
            symbol: Stock ticker
        
        Returns:
            API response as dict
        """
        params = {
            'function': function,
            'symbol': symbol,
            'apikey': self.api_key
        }
        
        response = requests.get(self.BASE_URL, params=params, timeout=30)
        
        if response.status_code != 200:
            raise DataFetchError(f"API returned status {response.status_code}")
        
        data = response.json()
        
        # Check for API errors
        if 'Error Message' in data:
            raise DataUnavailableError(data['Error Message'])
        
        if 'Note' in data:
            # Rate limit message
            raise RateLimitError("API rate limit exceeded. Wait 1 minute or upgrade to premium.")
        
        return data
    
    def _fetch_income_statement(self, ticker: str) -> dict:
        """Fetch income statement from API."""
        return self._api_call('INCOME_STATEMENT', ticker)
    
    def _fetch_balance_sheet(self, ticker: str) -> dict:
        """Fetch balance sheet from API."""
        return self._api_call('BALANCE_SHEET', ticker)
    
    def _fetch_cash_flow(self, ticker: str) -> dict:
        """Fetch cash flow statement from API."""
        return self._api_call('CASH_FLOW', ticker)
    
    def _fetch_company_overview(self, ticker: str) -> dict:
        """Fetch company overview (includes market data)."""
        return self._api_call('OVERVIEW', ticker)
    
    def _normalize_income_statement(self, data: dict, years: int) -> dict[str, list[float]]:
        """Normalize income statement to standard schema."""
        if 'annualReports' not in data:
            self.warnings.append("No annual income statement reports found")
            return {}
        
        reports = data['annualReports'][:years]  # Most recent first
        
        return {
            'revenue': self._extract_field(reports, 'totalRevenue'),
            'cogs': self._extract_field(reports, 'costOfRevenue'),
            'gross_profit': self._extract_field(reports, 'grossProfit'),
            'operating_expenses': self._extract_field(reports, 'operatingExpenses'),
            'operating_income': self._extract_field(reports, 'operatingIncome'),
            'interest_expense': self._extract_field(reports, 'interestExpense'),
            'tax_expense': self._extract_field(reports, 'incomeTaxExpense'),
            'net_income': self._extract_field(reports, 'netIncome'),
            'ebitda': self._extract_field(reports, 'ebitda'),
            'ebit': self._extract_field(reports, 'ebit'),
        }
    
    def _normalize_balance_sheet(self, data: dict, years: int) -> dict[str, list[float]]:
        """Normalize balance sheet to standard schema."""
        if 'annualReports' not in data:
            self.warnings.append("No annual balance sheet reports found")
            return {}
        
        reports = data['annualReports'][:years]
        
        # Calculate total debt
        long_term_debt = self._extract_field(reports, 'longTermDebt')
        short_term_debt = self._extract_field(reports, 'shortTermDebt')
        
        total_debt = []
        if long_term_debt and short_term_debt:
            total_debt = [
                (ltd + std) if (ltd is not None and std is not None) else None
                for ltd, std in zip(long_term_debt, short_term_debt)
            ]
        
        return {
            'total_assets': self._extract_field(reports, 'totalAssets'),
            'current_assets': self._extract_field(reports, 'totalCurrentAssets'),
            'cash': self._extract_field(reports, 'cashAndCashEquivalentsAtCarryingValue'),
            'accounts_receivable': self._extract_field(reports, 'currentNetReceivables'),
            'inventory': self._extract_field(reports, 'inventory'),
            'total_liabilities': self._extract_field(reports, 'totalLiabilities'),
            'current_liabilities': self._extract_field(reports, 'totalCurrentLiabilities'),
            'total_debt': total_debt,
            'long_term_debt': long_term_debt,
            'short_term_debt': short_term_debt,
            'accounts_payable': self._extract_field(reports, 'currentAccountsPayable'),
            'total_equity': self._extract_field(reports, 'totalShareholderEquity'),
        }
    
    def _normalize_cash_flow(self, data: dict, years: int) -> dict[str, list[float]]:
        """Normalize cash flow statement to standard schema."""
        if 'annualReports' not in data:
            self.warnings.append("No annual cash flow reports found")
            return {}
        
        reports = data['annualReports'][:years]
        
        # Calculate FCF if not present
        ocf = self._extract_field(reports, 'operatingCashflow')
        capex = self._extract_field(reports, 'capitalExpenditures')
        
        fcf = []
        if ocf and capex:
            fcf = [
                (o - abs(c)) if (o is not None and c is not None) else None
                for o, c in zip(ocf, capex)
            ]
        
        return {
            'operating_cash_flow': ocf,
            'investing_cash_flow': self._extract_field(reports, 'cashflowFromInvestment'),
            'financing_cash_flow': self._extract_field(reports, 'cashflowFromFinancing'),
            'free_cash_flow': fcf,
            'capex': capex,
            'dividends_paid': self._extract_field(reports, 'dividendPayout'),
        }
    
    def _extract_market_data(self, overview: dict) -> dict[str, float]:
        """Extract market data from company overview."""
        def safe_float(value, default=None):
            try:
                return float(value) if value and value != 'None' else default
            except (ValueError, TypeError):
                return default
        
        return {
            'market_cap': safe_float(overview.get('MarketCapitalization')),
            'shares_outstanding': safe_float(overview.get('SharesOutstanding')),
            'current_price': safe_float(overview.get('Price')),
            'beta': safe_float(overview.get('Beta')),
            '52_week_high': safe_float(overview.get('52WeekHigh')),
            '52_week_low': safe_float(overview.get('52WeekLow')),
            'avg_volume': None,  # Not provided by overview
            'enterprise_value': None,  # Calculate: Market Cap + Debt - Cash
            'trailing_pe': safe_float(overview.get('TrailingPE')),
            'forward_pe': safe_float(overview.get('ForwardPE')),
            'peg_ratio': safe_float(overview.get('PEGRatio')),
            'price_to_book': safe_float(overview.get('PriceToBookRatio')),
        }
    
    def _extract_field(self, reports: list[dict], field_name: str) -> Optional[list[float]]:
        """
        Extract field from list of annual reports.
        
        Args:
            reports: List of annual report dicts
            field_name: Field name to extract
        
        Returns:
            List of values or None if field missing from all reports
        """
        values = []
        for report in reports:
            value = report.get(field_name)
            try:
                values.append(float(value) if value and value != 'None' else None)
            except (ValueError, TypeError):
                values.append(None)
        
        # Return None if all values are None
        if all(v is None for v in values):
            self.warnings.append(f"Missing field: {field_name}")
            return None
        
        return values
    
    def _calculate_completeness(self, income: dict, balance: dict, cashflow: dict) -> str:
        """Calculate data completeness score."""
        critical_fields = [
            income.get('revenue'),
            income.get('net_income'),
            balance.get('total_assets'),
            balance.get('total_equity'),
            cashflow.get('operating_cash_flow'),
        ]
        
        available = sum(1 for field in critical_fields if field is not None)
        score = available / len(critical_fields)
        
        if score >= 0.9:
            return 'High (>90%)'
        elif score >= 0.7:
            return 'Medium (70-90%)'
        else:
            return f'Low ({score:.0%})'


# Example usage
if __name__ == '__main__':
    import os
    
    # Get API key from environment variable
    api_key = os.getenv('ALPHA_VANTAGE_KEY')
    if not api_key:
        print("Error: Set ALPHA_VANTAGE_KEY environment variable")
        print("Get your free key at: https://www.alphavantage.co/support/#api-key")
        exit(1)
    
    extractor = AlphaVantageExtractor(api_key)
    
    # Test with Apple
    try:
        data = extractor.fetch('AAPL')
        print(f"\n{'='*60}")
        print(f"Company: {data.company_name} ({data.ticker})")
        print(f"Fiscal Year End: {data.fiscal_year_end}")
        print(f"Data Source: {data.data_quality['source']}")
        print(f"Completeness: {data.data_quality['completeness_score']}")
        print(f"{'='*60}\n")
        
        # Show revenue trend
        if data.income_statement.get('revenue'):
            print("Revenue (last 5 years, most recent first):")
            for i, rev in enumerate(data.income_statement['revenue'][:5]):
                if rev:
                    print(f"  Year {i}: ${rev / 1e9:.2f}B")
        
        # Show market metrics
        if data.market_data.get('market_cap'):
            print(f"\nMarket Cap: ${data.market_data['market_cap'] / 1e9:.2f}B")
        if data.market_data.get('beta'):
            print(f"Beta: {data.market_data['beta']:.2f}")
        if data.market_data.get('trailing_pe'):
            print(f"P/E Ratio: {data.market_data['trailing_pe']:.2f}")
        
        if data.data_quality['warnings'] != 'None':
            print(f"\n⚠️  Warnings: {data.data_quality['warnings']}")
    
    except RateLimitError as e:
        print(f"❌ Rate limit error: {e}")
        print("Wait 1 minute or upgrade to premium tier")
    except DataUnavailableError as e:
        print(f"❌ Data unavailable: {e}")
