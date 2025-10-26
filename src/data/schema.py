"""
Standard financial data schema for ValuationPro.

All extractors must convert their data into these standardized formats.
This ensures consistency across Excel, PDF, and Web API sources.

Units:
    - All monetary values in millions (USD unless specified)
    - All percentages as decimals (0.15 for 15%)
    - All dates as strings in YYYY-MM-DD format
"""

from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any
from datetime import datetime
import json


@dataclass
class CompanyInfo:
    """Company identification and basic information."""

    name: str
    ticker: Optional[str] = None
    industry: Optional[str] = None
    sector: Optional[str] = None
    fiscal_year_end: Optional[str] = None  # "December 31" or "FY ends Q4"
    description: Optional[str] = None

    def __repr__(self) -> str:
        ticker_str = f" ({self.ticker})" if self.ticker else ""
        return f"CompanyInfo: {self.name}{ticker_str}"


@dataclass
class IncomeStatement:
    """
    Income statement data.

    All values in millions (USD unless specified).
    Lists should have same length as FinancialData.years.
    """

    # Core metrics (required)
    revenue: List[float]

    # Profitability metrics (optional but recommended)
    cogs: Optional[List[float]] = None
    gross_profit: Optional[List[float]] = None
    operating_expenses: Optional[List[float]] = None
    rd_expense: Optional[List[float]] = None
    sga_expense: Optional[List[float]] = None

    # Operating profit
    ebitda: Optional[List[float]] = None
    depreciation_amortization: Optional[List[float]] = None
    ebit: Optional[List[float]] = None

    # Below operating line
    interest_expense: Optional[List[float]] = None
    interest_income: Optional[List[float]] = None
    other_income_expense: Optional[List[float]] = None
    pretax_income: Optional[List[float]] = None

    # After-tax
    income_tax: Optional[List[float]] = None
    net_income: Optional[List[float]] = None

    # Per share metrics
    eps_basic: Optional[List[float]] = None
    eps_diluted: Optional[List[float]] = None

    def __post_init__(self):
        """Validate that revenue is not empty."""
        if not self.revenue or len(self.revenue) == 0:
            raise ValueError("IncomeStatement must have at least one revenue value")


@dataclass
class BalanceSheet:
    """
    Balance sheet data.

    All values in millions.
    Lists should have same length as FinancialData.years.
    """

    # Assets
    cash: Optional[List[float]] = None
    marketable_securities: Optional[List[float]] = None
    accounts_receivable: Optional[List[float]] = None
    inventory: Optional[List[float]] = None
    other_current_assets: Optional[List[float]] = None
    current_assets: Optional[List[float]] = None

    ppe_gross: Optional[List[float]] = None
    accumulated_depreciation: Optional[List[float]] = None
    ppe_net: Optional[List[float]] = None
    goodwill: Optional[List[float]] = None
    intangible_assets: Optional[List[float]] = None
    other_longterm_assets: Optional[List[float]] = None
    total_assets: Optional[List[float]] = None

    # Liabilities
    accounts_payable: Optional[List[float]] = None
    accrued_expenses: Optional[List[float]] = None
    short_term_debt: Optional[List[float]] = None
    current_portion_longterm_debt: Optional[List[float]] = None
    other_current_liabilities: Optional[List[float]] = None
    current_liabilities: Optional[List[float]] = None

    long_term_debt: Optional[List[float]] = None
    deferred_tax_liabilities: Optional[List[float]] = None
    other_longterm_liabilities: Optional[List[float]] = None
    total_liabilities: Optional[List[float]] = None

    # Equity
    common_stock: Optional[List[float]] = None
    retained_earnings: Optional[List[float]] = None
    accumulated_other_comprehensive_income: Optional[List[float]] = None
    treasury_stock: Optional[List[float]] = None
    shareholders_equity: Optional[List[float]] = None

    # Non-controlling interests
    minority_interest: Optional[List[float]] = None
    total_equity: Optional[List[float]] = None

    # Derived metrics
    net_working_capital: Optional[List[float]] = None  # Current Assets - Current Liabilities


@dataclass
class CashFlowStatement:
    """
    Cash flow statement data.

    All values in millions.
    Lists should have same length as FinancialData.years.
    """

    # Operating activities
    operating_cash_flow: Optional[List[float]] = None
    depreciation_amortization: Optional[List[float]] = None
    stock_based_compensation: Optional[List[float]] = None
    change_in_accounts_receivable: Optional[List[float]] = None
    change_in_inventory: Optional[List[float]] = None
    change_in_accounts_payable: Optional[List[float]] = None
    change_in_nwc: Optional[List[float]] = None

    # Investing activities
    capex: Optional[List[float]] = None
    acquisitions: Optional[List[float]] = None
    asset_sales: Optional[List[float]] = None
    investing_cash_flow: Optional[List[float]] = None

    # Financing activities
    debt_issued: Optional[List[float]] = None
    debt_repaid: Optional[List[float]] = None
    equity_issued: Optional[List[float]] = None
    equity_repurchased: Optional[List[float]] = None
    dividends_paid: Optional[List[float]] = None
    financing_cash_flow: Optional[List[float]] = None

    # Summary
    net_change_in_cash: Optional[List[float]] = None
    free_cash_flow: Optional[List[float]] = None

    # Beginning/ending cash (for reconciliation)
    beginning_cash: Optional[List[float]] = None
    ending_cash: Optional[List[float]] = None


@dataclass
class MarketData:
    """
    Market and valuation data.

    All values as of latest date (point-in-time, not time series).
    """

    # Current market data
    share_price: Optional[float] = None
    shares_outstanding: Optional[float] = None  # In millions
    shares_diluted: Optional[float] = None  # In millions
    market_cap: Optional[float] = None  # In millions

    # Debt and enterprise value
    total_debt: Optional[float] = None  # In millions
    cash_and_equivalents: Optional[float] = None  # In millions
    net_debt: Optional[float] = None  # In millions
    enterprise_value: Optional[float] = None  # In millions

    # Valuation multiples
    pe_ratio: Optional[float] = None
    ev_ebitda: Optional[float] = None
    ev_revenue: Optional[float] = None
    price_to_book: Optional[float] = None

    # Risk metrics
    beta: Optional[float] = None

    # Dividend info
    dividend_per_share: Optional[float] = None
    dividend_yield: Optional[float] = None


@dataclass
class ExtractionMetadata:
    """
    Metadata about the extraction process.

    Tracks source, quality, and any issues found.
    """

    source: str  # "excel", "pdf", "web_yfinance", "web_sec", etc.
    source_path: Optional[str] = None  # File path or URL
    extraction_date: datetime = field(default_factory=datetime.now)

    # Data quality metrics
    completeness_score: float = 0.0  # 0.0 to 1.0
    quality_flags: List[str] = field(default_factory=list)

    # Processing notes
    notes: Optional[str] = None
    warnings: List[str] = field(default_factory=list)

    # Conversion tracking
    unit_conversions_applied: List[str] = field(default_factory=list)
    derived_fields_calculated: List[str] = field(default_factory=list)

    def add_flag(self, flag: str):
        """Add a quality flag."""
        if flag not in self.quality_flags:
            self.quality_flags.append(flag)

    def add_warning(self, warning: str):
        """Add a warning message."""
        if warning not in self.warnings:
            self.warnings.append(warning)

    def add_unit_conversion(self, conversion: str):
        """Track a unit conversion that was applied."""
        if conversion not in self.unit_conversions_applied:
            self.unit_conversions_applied.append(conversion)

    def add_derived_field(self, field: str):
        """Track a field that was calculated from other data."""
        if field not in self.derived_fields_calculated:
            self.derived_fields_calculated.append(field)


@dataclass
class FinancialData:
    """
    Complete financial dataset in standardized format.

    This is the main data structure that all extractors produce
    and all valuation models consume.
    """

    company: CompanyInfo
    years: List[int]  # e.g., [2020, 2021, 2022, 2023, 2024]

    # Financial statements
    income_statement: IncomeStatement
    balance_sheet: BalanceSheet
    cash_flow: CashFlowStatement

    # Market data
    market_data: MarketData

    # Metadata
    metadata: ExtractionMetadata

    def __post_init__(self):
        """Validate data consistency."""
        # Ensure years list is not empty
        if not self.years or len(self.years) == 0:
            raise ValueError("FinancialData must have at least one year")

        # Ensure years are sorted
        if self.years != sorted(self.years):
            raise ValueError("Years must be in chronological order")

        # Validate that revenue list matches years length
        if len(self.income_statement.revenue) != len(self.years):
            raise ValueError(
                f"Revenue list length ({len(self.income_statement.revenue)}) "
                f"must match years length ({len(self.years)})"
            )

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary for JSON serialization.

        Returns:
            Dictionary representation of financial data
        """
        def convert_value(obj):
            """Helper to convert dataclass and datetime objects."""
            if isinstance(obj, datetime):
                return obj.isoformat()
            elif hasattr(obj, '__dataclass_fields__'):
                return asdict(obj)
            return obj

        data_dict = asdict(self)

        # Convert datetime objects to ISO format strings
        if 'metadata' in data_dict and 'extraction_date' in data_dict['metadata']:
            data_dict['metadata']['extraction_date'] = \
                self.metadata.extraction_date.isoformat()

        return data_dict

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FinancialData':
        """
        Create FinancialData from dictionary.

        Args:
            data: Dictionary representation (from to_dict or JSON)

        Returns:
            FinancialData object
        """
        # Convert extraction_date string back to datetime
        if 'metadata' in data and 'extraction_date' in data['metadata']:
            if isinstance(data['metadata']['extraction_date'], str):
                data['metadata']['extraction_date'] = datetime.fromisoformat(
                    data['metadata']['extraction_date']
                )

        # Build nested dataclass objects
        return cls(
            company=CompanyInfo(**data['company']),
            years=data['years'],
            income_statement=IncomeStatement(**data['income_statement']),
            balance_sheet=BalanceSheet(**data['balance_sheet']),
            cash_flow=CashFlowStatement(**data['cash_flow']),
            market_data=MarketData(**data['market_data']),
            metadata=ExtractionMetadata(**data['metadata']),
        )

    def to_json(self, filepath: Optional[str] = None) -> str:
        """
        Serialize to JSON string or file.

        Args:
            filepath: Optional path to save JSON file

        Returns:
            JSON string
        """
        json_str = json.dumps(self.to_dict(), indent=2)

        if filepath:
            with open(filepath, 'w') as f:
                f.write(json_str)

        return json_str

    @classmethod
    def from_json(cls, json_input: str) -> 'FinancialData':
        """
        Deserialize from JSON string or file.

        Args:
            json_input: JSON string or path to JSON file

        Returns:
            FinancialData object
        """
        # Check if input is a file path
        try:
            with open(json_input, 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, OSError):
            # Treat as JSON string
            data = json.loads(json_input)

        return cls.from_dict(data)

    def get_latest_year(self) -> int:
        """Get the most recent year in the dataset."""
        return max(self.years)

    def get_year_index(self, year: int) -> int:
        """
        Get array index for a specific year.

        Args:
            year: The year to find

        Returns:
            Index in the years list

        Raises:
            ValueError: If year not in dataset
        """
        try:
            return self.years.index(year)
        except ValueError:
            raise ValueError(f"Year {year} not found in dataset. Available years: {self.years}")

    def summary(self) -> str:
        """
        Generate a human-readable summary of the financial data.

        Returns:
            Multi-line string summary
        """
        lines = []
        lines.append("=" * 70)
        lines.append(f"FINANCIAL DATA SUMMARY: {self.company.name}")
        lines.append("=" * 70)

        if self.company.ticker:
            lines.append(f"Ticker: {self.company.ticker}")
        if self.company.industry:
            lines.append(f"Industry: {self.company.industry}")
        if self.company.sector:
            lines.append(f"Sector: {self.company.sector}")

        lines.append(f"\nYears: {self.years[0]} - {self.years[-1]} ({len(self.years)} years)")
        lines.append(f"Source: {self.metadata.source}")
        lines.append(f"Completeness: {self.metadata.completeness_score:.1%}")

        # Revenue summary
        lines.append("\nREVENUE:")
        for i, year in enumerate(self.years):
            rev = self.income_statement.revenue[i]
            lines.append(f"  {year}: ${rev:,.1f}M")

        # Calculate CAGR
        if len(self.years) > 1:
            first_rev = self.income_statement.revenue[0]
            last_rev = self.income_statement.revenue[-1]
            years_diff = self.years[-1] - self.years[0]
            cagr = (last_rev / first_rev) ** (1 / years_diff) - 1
            lines.append(f"  Revenue CAGR: {cagr:.1%}")

        # Net income if available
        if self.income_statement.net_income:
            lines.append("\nNET INCOME:")
            for i, year in enumerate(self.years):
                ni = self.income_statement.net_income[i]
                if ni is not None:
                    margin = ni / self.income_statement.revenue[i]
                    lines.append(f"  {year}: ${ni:,.1f}M ({margin:.1%} margin)")

        # Market data
        if self.market_data.market_cap:
            lines.append("\nMARKET DATA:")
            lines.append(f"  Market Cap: ${self.market_data.market_cap:,.1f}M")
            if self.market_data.enterprise_value:
                lines.append(f"  Enterprise Value: ${self.market_data.enterprise_value:,.1f}M")

        # Quality flags
        if self.metadata.quality_flags:
            lines.append("\nQUALITY FLAGS:")
            for flag in self.metadata.quality_flags:
                lines.append(f"  ⚠️  {flag}")

        # Warnings
        if self.metadata.warnings:
            lines.append("\nWARNINGS:")
            for warning in self.metadata.warnings:
                lines.append(f"  ⚠️  {warning}")

        lines.append("=" * 70)

        return "\n".join(lines)

    def __repr__(self) -> str:
        return (f"FinancialData({self.company.name}, "
                f"{len(self.years)} years, "
                f"completeness={self.metadata.completeness_score:.1%})")


# Helper functions for common operations

def create_empty_financial_data(
    company_name: str,
    years: List[int],
    source: str = "manual"
) -> FinancialData:
    """
    Create an empty FinancialData object with minimal required fields.

    Useful for testing or manual data entry.

    Args:
        company_name: Name of the company
        years: List of years
        source: Data source identifier

    Returns:
        FinancialData object with empty/None optional fields
    """
    num_years = len(years)

    return FinancialData(
        company=CompanyInfo(name=company_name),
        years=years,
        income_statement=IncomeStatement(
            revenue=[0.0] * num_years  # Placeholder, should be filled
        ),
        balance_sheet=BalanceSheet(),
        cash_flow=CashFlowStatement(),
        market_data=MarketData(),
        metadata=ExtractionMetadata(source=source)
    )
