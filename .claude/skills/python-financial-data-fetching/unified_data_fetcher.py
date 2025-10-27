"""
Unified Data Fetcher for ValuationPro

Orchestrates multiple data sources with intelligent fallback strategy.
Provides a single interface for fetching financial data with caching.
"""

from pathlib import Path
from typing import Optional
import logging
from dataclasses import dataclass, field

# Import individual extractors
# Note: In production, these would be imported from their respective modules
# from yfinance_extractor import YFinanceExtractor, FinancialData, DataFetchError, DataUnavailableError
# from alpha_vantage_extractor import AlphaVantageExtractor, RateLimitError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class FinancialData:
    """Standardized financial data structure (placeholder for import)."""
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
    """Raised when data cannot be fetched from any source."""
    pass


class UnifiedDataFetcher:
    """
    Unified interface for fetching financial data from multiple sources.
    
    Implements intelligent fallback strategy:
    1. Try yfinance (fastest, free, extensive coverage)
    2. Fallback to Alpha Vantage (reliable, official)
    3. (Future) Fallback to SEC EDGAR (US companies only)
    
    Features:
    - Automatic failover between sources
    - Data caching with TTL
    - Validation and quality scoring
    - Parallel fetching for batch requests
    """
    
    def __init__(
        self,
        yf_enabled: bool = True,
        av_api_key: Optional[str] = None,
        cache_dir: Optional[Path] = None,
        cache_ttl_hours: int = 24,
    ):
        """
        Initialize unified data fetcher.
        
        Args:
            yf_enabled: Enable yfinance (default True)
            av_api_key: Alpha Vantage API key (optional)
            cache_dir: Directory for caching data (optional, disables cache if None)
            cache_ttl_hours: Cache time-to-live in hours (default 24)
        """
        self.yf_enabled = yf_enabled
        self.av_enabled = av_api_key is not None
        
        # Initialize extractors
        if self.yf_enabled:
            try:
                from yfinance_extractor import YFinanceExtractor
                self.yf_extractor = YFinanceExtractor()
                logger.info("✓ yfinance extractor initialized")
            except ImportError:
                logger.warning("yfinance not available")
                self.yf_enabled = False
        
        if self.av_enabled:
            try:
                from alpha_vantage_extractor import AlphaVantageExtractor
                self.av_extractor = AlphaVantageExtractor(av_api_key)
                logger.info("✓ Alpha Vantage extractor initialized")
            except ImportError:
                logger.warning("Alpha Vantage extractor not available")
                self.av_enabled = False
        
        # Initialize cache
        self.cache_enabled = cache_dir is not None
        if self.cache_enabled:
            self.cache_dir = Path(cache_dir)
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            self.cache_ttl_hours = cache_ttl_hours
            logger.info(f"✓ Cache enabled: {self.cache_dir} (TTL: {cache_ttl_hours}h)")
        
        # Statistics
        self.stats = {
            'total_fetches': 0,
            'cache_hits': 0,
            'yf_success': 0,
            'av_success': 0,
            'failures': 0,
        }
    
    def get_company_data(self, ticker: str, years: int = 5, use_cache: bool = True) -> FinancialData:
        """
        Fetch financial data for a company ticker.
        
        This is the main entry point. Tries multiple sources with fallback.
        
        Args:
            ticker: Stock ticker symbol (e.g., 'AAPL')
            years: Number of historical years to fetch (default 5)
            use_cache: Use cached data if available (default True)
        
        Returns:
            FinancialData object with normalized data
        
        Raises:
            DataUnavailableError: If all sources fail
        """
        self.stats['total_fetches'] += 1
        ticker = ticker.upper()
        
        # Check cache first
        if use_cache and self.cache_enabled:
            cached_data = self._get_from_cache(ticker)
            if cached_data:
                logger.info(f"✓ Cache hit for {ticker}")
                self.stats['cache_hits'] += 1
                return cached_data
        
        # Try fetching from sources with fallback
        errors = []
        
        # Source 1: yfinance
        if self.yf_enabled:
            try:
                logger.info(f"Trying yfinance for {ticker}")
                data = self.yf_extractor.fetch(ticker, years)
                self._save_to_cache(ticker, data)
                self.stats['yf_success'] += 1
                logger.info(f"✓ Successfully fetched {ticker} from yfinance")
                return data
            except Exception as e:
                errors.append(f"yfinance: {str(e)}")
                logger.warning(f"yfinance failed for {ticker}: {e}")
        
        # Source 2: Alpha Vantage
        if self.av_enabled:
            try:
                logger.info(f"Trying Alpha Vantage for {ticker}")
                data = self.av_extractor.fetch(ticker, years)
                self._save_to_cache(ticker, data)
                self.stats['av_success'] += 1
                logger.info(f"✓ Successfully fetched {ticker} from Alpha Vantage")
                return data
            except Exception as e:
                errors.append(f"Alpha Vantage: {str(e)}")
                logger.warning(f"Alpha Vantage failed for {ticker}: {e}")
        
        # All sources failed
        self.stats['failures'] += 1
        error_msg = f"All sources failed for {ticker}:\n" + "\n".join(f"  - {e}" for e in errors)
        logger.error(error_msg)
        raise DataUnavailableError(error_msg)
    
    def batch_fetch(self, tickers: list[str], max_workers: int = 5) -> dict[str, FinancialData]:
        """
        Fetch data for multiple tickers in parallel.
        
        Args:
            tickers: List of ticker symbols
            max_workers: Maximum parallel workers (default 5)
        
        Returns:
            Dict mapping ticker → FinancialData (excludes failed tickers)
        """
        from concurrent.futures import ThreadPoolExecutor, as_completed
        
        results = {}
        failed = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_ticker = {
                executor.submit(self.get_company_data, ticker): ticker
                for ticker in tickers
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_ticker):
                ticker = future_to_ticker[future]
                try:
                    data = future.result()
                    results[ticker] = data
                    logger.info(f"✓ Batch fetch succeeded: {ticker}")
                except Exception as e:
                    failed.append(ticker)
                    logger.error(f"✗ Batch fetch failed: {ticker} - {e}")
        
        logger.info(f"Batch fetch complete: {len(results)} succeeded, {len(failed)} failed")
        if failed:
            logger.warning(f"Failed tickers: {', '.join(failed)}")
        
        return results
    
    def validate_data(self, data: FinancialData) -> list[str]:
        """
        Validate financial data quality.
        
        Args:
            data: FinancialData object to validate
        
        Returns:
            List of validation warnings (empty if all checks pass)
        """
        warnings = []
        
        # Check critical fields
        if not data.income_statement.get('revenue'):
            warnings.append("❌ Critical: Missing revenue data")
        elif any(r is not None and r <= 0 for r in data.income_statement['revenue']):
            warnings.append("⚠️  Negative revenue detected")
        
        if not data.balance_sheet.get('total_assets'):
            warnings.append("❌ Critical: Missing total assets")
        
        if not data.balance_sheet.get('total_equity'):
            warnings.append("❌ Critical: Missing total equity")
        
        # Check balance sheet equation: Assets = Liabilities + Equity
        if (data.balance_sheet.get('total_assets') and
            data.balance_sheet.get('total_liabilities') and
            data.balance_sheet.get('total_equity')):
            
            for i in range(len(data.balance_sheet['total_assets'])):
                assets = data.balance_sheet['total_assets'][i]
                liabilities = data.balance_sheet['total_liabilities'][i]
                equity = data.balance_sheet['total_equity'][i]
                
                if all(x is not None for x in [assets, liabilities, equity]):
                    difference = abs(assets - (liabilities + equity)) / assets
                    if difference > 0.01:  # More than 1% difference
                        warnings.append(
                            f"⚠️  Balance sheet equation violation in year {i}: "
                            f"{difference:.1%} difference"
                        )
        
        # Check beta range
        if data.market_data.get('beta'):
            beta = data.market_data['beta']
            if abs(beta) > 3.0:
                warnings.append(f"⚠️  Unusual beta value: {beta:.2f} (expected -3 to 3)")
        
        # Check market cap consistency
        if (data.market_data.get('market_cap') and
            data.market_data.get('current_price') and
            data.market_data.get('shares_outstanding')):
            
            calculated_mc = data.market_data['current_price'] * data.market_data['shares_outstanding']
            reported_mc = data.market_data['market_cap']
            
            difference = abs(calculated_mc - reported_mc) / reported_mc
            if difference > 0.05:  # More than 5% difference
                warnings.append(
                    f"⚠️  Market cap mismatch: Reported ${reported_mc/1e9:.2f}B, "
                    f"Calculated ${calculated_mc/1e9:.2f}B ({difference:.1%} diff)"
                )
        
        return warnings
    
    def get_stats(self) -> dict:
        """Get fetcher statistics."""
        stats = self.stats.copy()
        if stats['total_fetches'] > 0:
            stats['cache_hit_rate'] = f"{100 * stats['cache_hits'] / stats['total_fetches']:.1f}%"
            stats['success_rate'] = f"{100 * (1 - stats['failures'] / stats['total_fetches']):.1f}%"
        return stats
    
    def _get_from_cache(self, ticker: str) -> Optional[FinancialData]:
        """Get data from cache if available and not expired."""
        import pickle
        from datetime import datetime, timedelta
        
        cache_file = self.cache_dir / f"{ticker}.pkl"
        if not cache_file.exists():
            return None
        
        # Check age
        age = datetime.now() - datetime.fromtimestamp(cache_file.stat().st_mtime)
        if age > timedelta(hours=self.cache_ttl_hours):
            logger.debug(f"Cache expired for {ticker} (age: {age})")
            cache_file.unlink()
            return None
        
        try:
            with open(cache_file, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            logger.warning(f"Cache read error for {ticker}: {e}")
            return None
    
    def _save_to_cache(self, ticker: str, data: FinancialData):
        """Save data to cache."""
        if not self.cache_enabled:
            return
        
        import pickle
        
        try:
            cache_file = self.cache_dir / f"{ticker}.pkl"
            with open(cache_file, 'wb') as f:
                pickle.dump(data, f, protocol=4)
            logger.debug(f"Saved {ticker} to cache")
        except Exception as e:
            logger.warning(f"Cache write error for {ticker}: {e}")
    
    def clear_cache(self):
        """Clear all cached data."""
        if not self.cache_enabled:
            return
        
        count = 0
        for cache_file in self.cache_dir.glob("*.pkl"):
            cache_file.unlink()
            count += 1
        
        logger.info(f"Cleared {count} cached files")


# Example usage
if __name__ == '__main__':
    import os
    
    # Initialize fetcher with both sources
    fetcher = UnifiedDataFetcher(
        yf_enabled=True,
        av_api_key=os.getenv('ALPHA_VANTAGE_KEY'),  # Optional
        cache_dir=Path('./cache'),
        cache_ttl_hours=24
    )
    
    print("\n" + "="*60)
    print("UNIFIED DATA FETCHER - EXAMPLE USAGE")
    print("="*60 + "\n")
    
    # Example 1: Single ticker fetch
    print("1. Fetching single ticker (AAPL)...")
    try:
        data = fetcher.get_company_data('AAPL')
        print(f"   ✓ Company: {data.company_name}")
        print(f"   ✓ Source: {data.data_quality['source']}")
        print(f"   ✓ Completeness: {data.data_quality['completeness_score']}")
        
        # Validate
        warnings = fetcher.validate_data(data)
        if warnings:
            print("\n   Validation warnings:")
            for warning in warnings:
                print(f"   {warning}")
        else:
            print("   ✓ All validation checks passed")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # Example 2: Batch fetch
    print("\n2. Batch fetching multiple tickers...")
    comp_tickers = ['MSFT', 'GOOGL', 'META']
    try:
        results = fetcher.batch_fetch(comp_tickers, max_workers=3)
        print(f"   ✓ Successfully fetched {len(results)}/{len(comp_tickers)} tickers")
        for ticker in results:
            print(f"     - {ticker}: {results[ticker].company_name}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # Example 3: Show statistics
    print("\n3. Fetcher statistics:")
    stats = fetcher.get_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    print("\n" + "="*60 + "\n")
