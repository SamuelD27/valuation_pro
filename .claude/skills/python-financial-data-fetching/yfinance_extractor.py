"""
yfinance Data Extractor for ValuationPro

Extracts financial data from Yahoo Finance and normalizes to standard schema.
Handles missing data gracefully and validates output quality.
"""

import yfinance as yf
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
import pandas as pd
import logging

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


class DataUnavailableError(DataFetchError):
    """Raised when data cannot be fetched."""
    pass


class YFinanceExtractor:
    """Extracts and normalizes financial data from yfinance."""
    
    def __init__(self):
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
            DataUnavailableError: If ticker not found or data unavailable
        """
        self.warnings = []
        logger.info(f"Fetching data for {ticker} from yfinance")
        
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Check if ticker is valid
            if not info or 'longName' not in info:
                raise DataUnavailableError(f"Ticker {ticker} not found")
            
            # Extract components
            income_stmt = self._extract_income_statement(stock)
            balance = self._extract_balance_sheet(stock)
            cashflow = self._extract_cash_flow(stock)
            market = self._extract_market_data(stock, info)
            
            # Create FinancialData object
            data = FinancialData(
                ticker=ticker.upper(),
                company_name=info.get('longName', ticker),
                fiscal_year_end=self._get_fiscal_year_end(info),
                income_statement=income_stmt,
                balance_sheet=balance,
                cash_flow=cashflow,
                market_data=market,
                data_quality={
                    'source': 'yfinance',
                    'fetch_timestamp': datetime.now().isoformat(),
                    'completeness_score': self._calculate_completeness(
                        income_stmt, balance, cashflow
                    ),
                    'warnings': ', '.join(self.warnings) if self.warnings else 'None'
                }
            )
            
            logger.info(f"Successfully fetched {ticker} with completeness {data.data_quality['completeness_score']}")
            return data
            
        except Exception as e:
            logger.error(f"Error fetching {ticker}: {e}")
            raise DataUnavailableError(f"Failed to fetch {ticker}: {str(e)}")
    
    def _extract_income_statement(self, stock) -> dict[str, list[float]]:
        """Extract and normalize income statement."""
        try:
            financials = stock.financials  # Annual by default
            
            return {
                'revenue': self._safe_extract(financials, ['Total Revenue']),
                'cogs': self._safe_extract(financials, ['Cost Of Revenue']),
                'gross_profit': self._safe_extract(financials, ['Gross Profit']),
                'operating_expenses': self._safe_extract(financials, ['Operating Expense']),
                'operating_income': self._safe_extract(financials, ['Operating Income']),
                'interest_expense': self._safe_extract(financials, ['Interest Expense']),
                'tax_expense': self._safe_extract(financials, ['Tax Provision']),
                'net_income': self._safe_extract(financials, ['Net Income']),
                'ebitda': self._safe_extract(financials, ['EBITDA']),
                'ebit': self._safe_extract(financials, ['EBIT']),
            }
        except Exception as e:
            self.warnings.append(f"Incomplete income statement: {e}")
            return {}
    
    def _extract_balance_sheet(self, stock) -> dict[str, list[float]]:
        """Extract and normalize balance sheet."""
        try:
            balance = stock.balance_sheet
            
            # Total debt = Long-term + Short-term
            long_term_debt = self._safe_extract(balance, ['Long Term Debt'])
            short_term_debt = self._safe_extract(balance, ['Current Debt'])
            
            total_debt = []
            if long_term_debt and short_term_debt:
                total_debt = [lt + st for lt, st in zip(long_term_debt, short_term_debt)]
            
            return {
                'total_assets': self._safe_extract(balance, ['Total Assets']),
                'current_assets': self._safe_extract(balance, ['Current Assets']),
                'cash': self._safe_extract(balance, ['Cash And Cash Equivalents']),
                'accounts_receivable': self._safe_extract(balance, ['Accounts Receivable']),
                'inventory': self._safe_extract(balance, ['Inventory']),
                'total_liabilities': self._safe_extract(balance, ['Total Liabilities Net Minority Interest']),
                'current_liabilities': self._safe_extract(balance, ['Current Liabilities']),
                'total_debt': total_debt,
                'long_term_debt': long_term_debt,
                'short_term_debt': short_term_debt,
                'accounts_payable': self._safe_extract(balance, ['Accounts Payable']),
                'total_equity': self._safe_extract(balance, ['Total Equity Gross Minority Interest']),
            }
        except Exception as e:
            self.warnings.append(f"Incomplete balance sheet: {e}")
            return {}
    
    def _extract_cash_flow(self, stock) -> dict[str, list[float]]:
        """Extract and normalize cash flow statement."""
        try:
            cashflow = stock.cashflow
            
            # Calculate Free Cash Flow if not present
            ocf = self._safe_extract(cashflow, ['Operating Cash Flow'])
            capex = self._safe_extract(cashflow, ['Capital Expenditure'])
            
            fcf = []
            if ocf and capex:
                # Capex is usually negative in yfinance
                fcf = [o + c for o, c in zip(ocf, capex)]
            
            return {
                'operating_cash_flow': ocf,
                'investing_cash_flow': self._safe_extract(cashflow, ['Investing Cash Flow']),
                'financing_cash_flow': self._safe_extract(cashflow, ['Financing Cash Flow']),
                'free_cash_flow': fcf,
                'capex': capex,
                'dividends_paid': self._safe_extract(cashflow, ['Cash Dividends Paid']),
            }
        except Exception as e:
            self.warnings.append(f"Incomplete cash flow: {e}")
            return {}
    
    def _extract_market_data(self, stock, info: dict) -> dict[str, float]:
        """Extract market data from info dict."""
        return {
            'market_cap': info.get('marketCap'),
            'shares_outstanding': info.get('sharesOutstanding'),
            'current_price': info.get('currentPrice') or info.get('regularMarketPrice'),
            'beta': info.get('beta'),
            '52_week_high': info.get('fiftyTwoWeekHigh'),
            '52_week_low': info.get('fiftyTwoWeekLow'),
            'avg_volume': info.get('averageVolume'),
            'enterprise_value': info.get('enterpriseValue'),
            'trailing_pe': info.get('trailingPE'),
            'forward_pe': info.get('forwardPE'),
        }
    
    def _safe_extract(self, df: pd.DataFrame, field_names: list[str]) -> Optional[list[float]]:
        """
        Safely extract field from DataFrame, trying multiple field names.
        
        Args:
            df: DataFrame from yfinance
            field_names: List of possible field names to try
        
        Returns:
            List of values (most recent first) or None if not found
        """
        for field in field_names:
            if field in df.index:
                values = df.loc[field].tolist()
                # Remove NaN values
                values = [float(v) if pd.notna(v) else None for v in values]
                # Filter out all-None lists
                if any(v is not None for v in values):
                    return values
        
        self.warnings.append(f"Missing fields: {field_names}")
        return None
    
    def _get_fiscal_year_end(self, info: dict) -> str:
        """Extract fiscal year end from info dict."""
        # yfinance doesn't always provide this clearly
        # Default to December if not found
        return info.get('fiscalYearEnd', 'December')
    
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
    extractor = YFinanceExtractor()
    
    # Test with Apple
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
    print(f"\nMarket Cap: ${data.market_data['market_cap'] / 1e9:.2f}B")
    print(f"Beta: {data.market_data['beta']:.2f}")
    print(f"P/E Ratio: {data.market_data['trailing_pe']:.2f}")
    
    if data.data_quality['warnings'] != 'None':
        print(f"\n⚠️  Warnings: {data.data_quality['warnings']}")
