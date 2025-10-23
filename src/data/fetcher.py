"""
Data Fetcher Module

Handles fetching financial data from external sources:
- yfinance: Stock data, financial statements, market data
- FRED: Risk-free rates and economic data

Includes error handling, caching, and fallback mechanisms.
"""

import yfinance as yf
import pandas as pd
from typing import Dict, List, Optional
import warnings
from datetime import datetime, timedelta


class DataUnavailableError(Exception):
    """Raised when data cannot be fetched from any source."""
    pass


class DataFetcher:
    """
    Fetch financial and market data for valuation models.

    Supports:
    - Financial statements (income statement, balance sheet, cash flow)
    - Market data (price, beta, market cap)
    - Risk-free rates (10Y Treasury)
    - Batch fetching for comparable companies
    """

    def __init__(self, cache_duration_hours: int = 24):
        """
        Initialize DataFetcher.

        Args:
            cache_duration_hours: How long to cache data (default 24 hours)
        """
        self.cache_duration = timedelta(hours=cache_duration_hours)
        self._cache = {}

    def get_financial_statements(self, ticker: str) -> Dict:
        """
        Fetch complete financial statements for a company.

        Returns standardized dict with:
        - Income statement (revenue, EBIT, net income, etc.)
        - Balance sheet (assets, liabilities, equity)
        - Cash flow statement (operating, investing, financing CF)

        Args:
            ticker: Stock ticker symbol

        Returns:
            Dictionary with financial statement data

        Raises:
            DataUnavailableError: If data cannot be fetched
        """
        ticker = ticker.upper()

        try:
            stock = yf.Ticker(ticker)

            # Fetch financial statements
            income_stmt = stock.financials  # Annual income statement
            balance_sheet = stock.balance_sheet
            cash_flow = stock.cashflow

            if income_stmt.empty:
                raise DataUnavailableError(
                    f"No financial data available for {ticker}. "
                    f"Please upload data manually."
                )

            # Standardize the data structure
            data = {
                'ticker': ticker,
                'currency': stock.info.get('currency', 'USD'),
                'fetch_date': datetime.now().isoformat(),
            }

            # Extract income statement items (most recent year first)
            if not income_stmt.empty:
                # Get most recent 3-5 years
                years = min(5, len(income_stmt.columns))

                data['income_statement'] = {
                    'dates': [col.strftime('%Y-%m-%d') for col in income_stmt.columns[:years]],
                    'revenue': self._safe_extract(income_stmt, 'Total Revenue', years),
                    'cost_of_revenue': self._safe_extract(income_stmt, 'Cost Of Revenue', years),
                    'gross_profit': self._safe_extract(income_stmt, 'Gross Profit', years),
                    'operating_expense': self._safe_extract(income_stmt, 'Operating Expense', years),
                    'ebit': self._safe_extract(income_stmt, 'EBIT', years),
                    'interest_expense': self._safe_extract(income_stmt, 'Interest Expense', years),
                    'pretax_income': self._safe_extract(income_stmt, 'Pretax Income', years),
                    'tax_provision': self._safe_extract(income_stmt, 'Tax Provision', years),
                    'net_income': self._safe_extract(income_stmt, 'Net Income', years),
                }

            # Extract balance sheet items
            if not balance_sheet.empty:
                years = min(5, len(balance_sheet.columns))

                data['balance_sheet'] = {
                    'dates': [col.strftime('%Y-%m-%d') for col in balance_sheet.columns[:years]],
                    'cash': self._safe_extract(balance_sheet, 'Cash And Cash Equivalents', years),
                    'total_assets': self._safe_extract(balance_sheet, 'Total Assets', years),
                    'current_assets': self._safe_extract(balance_sheet, 'Current Assets', years),
                    'current_liabilities': self._safe_extract(balance_sheet, 'Current Liabilities', years),
                    'total_debt': self._safe_extract(balance_sheet, 'Total Debt', years),
                    'long_term_debt': self._safe_extract(balance_sheet, 'Long Term Debt', years),
                    'stockholders_equity': self._safe_extract(balance_sheet, 'Stockholders Equity', years),
                }

                # Calculate Net Working Capital
                current_assets = data['balance_sheet']['current_assets']
                current_liabilities = data['balance_sheet']['current_liabilities']
                data['balance_sheet']['nwc'] = [
                    ca - cl if ca and cl else None
                    for ca, cl in zip(current_assets, current_liabilities)
                ]

            # Extract cash flow items
            if not cash_flow.empty:
                years = min(5, len(cash_flow.columns))

                data['cash_flow'] = {
                    'dates': [col.strftime('%Y-%m-%d') for col in cash_flow.columns[:years]],
                    'operating_cf': self._safe_extract(cash_flow, 'Operating Cash Flow', years),
                    'capex': self._safe_extract(cash_flow, 'Capital Expenditure', years),
                    'free_cash_flow': self._safe_extract(cash_flow, 'Free Cash Flow', years),
                    'depreciation': self._safe_extract(cash_flow, 'Depreciation And Amortization', years),
                }

            return data

        except Exception as e:
            raise DataUnavailableError(
                f"Failed to fetch financial statements for {ticker}: {str(e)}\n"
                f"Please verify the ticker symbol or upload data manually."
            )

    def _safe_extract(self, df: pd.DataFrame, key: str, years: int) -> List[Optional[float]]:
        """
        Safely extract data from DataFrame, handling missing keys.

        Args:
            df: DataFrame to extract from
            key: Row key to extract
            years: Number of years to extract

        Returns:
            List of values (None if key doesn't exist)
        """
        if key in df.index:
            values = df.loc[key].head(years).tolist()
            # Convert NaN to None
            return [float(v) if pd.notna(v) else None for v in values]
        else:
            return [None] * years

    def get_market_data(self, ticker: str) -> Dict:
        """
        Fetch current market data for a company.

        Args:
            ticker: Stock ticker symbol

        Returns:
            Dictionary with:
                - current_price: Current stock price
                - market_cap: Market capitalization
                - beta: Beta coefficient
                - shares_outstanding: Number of shares
                - 52_week_high: 52-week high price
                - 52_week_low: 52-week low price
                - avg_volume: Average trading volume

        Raises:
            DataUnavailableError: If data cannot be fetched
        """
        ticker = ticker.upper()

        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            # Validate we have data
            if not info or 'regularMarketPrice' not in info:
                raise DataUnavailableError(
                    f"No market data available for {ticker}"
                )

            market_data = {
                'ticker': ticker,
                'current_price': info.get('regularMarketPrice') or info.get('currentPrice'),
                'market_cap': info.get('marketCap'),
                'beta': info.get('beta'),
                'shares_outstanding': info.get('sharesOutstanding'),
                '52_week_high': info.get('fiftyTwoWeekHigh'),
                '52_week_low': info.get('fiftyTwoWeekLow'),
                'avg_volume': info.get('averageVolume'),
                'sector': info.get('sector'),
                'industry': info.get('industry'),
                'fetch_date': datetime.now().isoformat(),
            }

            return market_data

        except Exception as e:
            raise DataUnavailableError(
                f"Failed to fetch market data for {ticker}: {str(e)}"
            )

    def get_risk_free_rate(self) -> float:
        """
        Fetch current 10-Year U.S. Treasury yield as risk-free rate.

        Uses ^TNX ticker for 10-Year Treasury Note Yield.

        Returns:
            Risk-free rate as decimal (e.g., 0.04 for 4%)

        Raises:
            DataUnavailableError: If rate cannot be fetched
        """
        try:
            treasury = yf.Ticker("^TNX")
            hist = treasury.history(period="5d")

            if not hist.empty:
                # TNX is in percentage form, convert to decimal
                rf_rate = hist['Close'].iloc[-1] / 100
                return rf_rate
            else:
                warnings.warn(
                    "Could not fetch Treasury rate. Using default 4%."
                )
                return 0.04

        except Exception as e:
            warnings.warn(
                f"Error fetching risk-free rate: {e}. Using default 4%."
            )
            return 0.04

    def get_comps_data(self, tickers: List[str]) -> pd.DataFrame:
        """
        Batch fetch financial data for multiple companies (comps analysis).

        Args:
            tickers: List of ticker symbols

        Returns:
            DataFrame with rows = companies, columns = financial metrics

        Raises:
            DataUnavailableError: If no data can be fetched for any ticker
        """
        comps_data = []
        failed_tickers = []

        for ticker in tickers:
            try:
                # Get market data
                market = self.get_market_data(ticker)

                # Get financial statements for revenue, EBITDA, etc.
                financials = self.get_financial_statements(ticker)

                # Extract most recent year data
                revenue = financials['income_statement']['revenue'][0] if \
                    financials['income_statement']['revenue'] else None

                ebit = financials['income_statement']['ebit'][0] if \
                    financials['income_statement']['ebit'] else None

                net_income = financials['income_statement']['net_income'][0] if \
                    financials['income_statement']['net_income'] else None

                # Calculate EBITDA (EBIT + D&A)
                da = financials['cash_flow']['depreciation'][0] if \
                    financials['cash_flow']['depreciation'] else 0
                ebitda = (ebit + abs(da)) if ebit and da else ebit

                # Calculate net debt
                debt = financials['balance_sheet']['total_debt'][0] if \
                    financials['balance_sheet']['total_debt'] else 0
                cash = financials['balance_sheet']['cash'][0] if \
                    financials['balance_sheet']['cash'] else 0
                net_debt = (debt - cash) if debt and cash else debt

                # Calculate EV
                market_cap = market['market_cap']
                enterprise_value = market_cap + net_debt if market_cap and net_debt else market_cap

                comp = {
                    'ticker': ticker,
                    'company_name': ticker,  # Could fetch full name from info
                    'market_cap': market_cap,
                    'net_debt': net_debt,
                    'enterprise_value': enterprise_value,
                    'revenue': revenue,
                    'ebitda': ebitda,
                    'ebit': ebit,
                    'net_income': net_income,
                    'current_price': market['current_price'],
                    'shares_outstanding': market['shares_outstanding'],
                }

                comps_data.append(comp)

            except Exception as e:
                warnings.warn(f"Failed to fetch data for {ticker}: {e}")
                failed_tickers.append(ticker)
                continue

        if not comps_data:
            raise DataUnavailableError(
                f"Could not fetch data for any tickers. Failed: {failed_tickers}"
            )

        if failed_tickers:
            warnings.warn(
                f"Failed to fetch data for: {', '.join(failed_tickers)}"
            )

        return pd.DataFrame(comps_data)

    def clear_cache(self):
        """Clear the data cache."""
        self._cache = {}
