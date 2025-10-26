"""
Base extractor abstract class for ValuationPro.

All extractors (Excel, PDF, Web) inherit from this base class
and must implement the can_handle() and extract() methods.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict
from ..schema import FinancialData, IncomeStatement, BalanceSheet, CashFlowStatement


class BaseExtractor(ABC):
    """
    Abstract base class for all data extractors.

    Extractors are responsible for:
    1. Detecting if they can handle a given source
    2. Extracting raw data from the source
    3. Converting to standardized FinancialData format
    """

    @abstractmethod
    def can_handle(self, source: Any) -> bool:
        """
        Check if this extractor can handle the given source.

        Args:
            source: Input source (file path, URL, ticker, etc.)

        Returns:
            True if this extractor can process the source, False otherwise

        Examples:
            ExcelExtractor.can_handle("financials.xlsx") -> True
            ExcelExtractor.can_handle("financials.pdf") -> False
            WebExtractor.can_handle("AAPL") -> True
        """
        pass

    @abstractmethod
    def extract(self, source: Any, **kwargs) -> FinancialData:
        """
        Extract financial data from source and return standardized FinancialData.

        Args:
            source: Input source to extract from
            **kwargs: Additional extractor-specific arguments
                     e.g., sheet_name, year_range, api_key

        Returns:
            FinancialData object with normalized data

        Raises:
            ValueError: If extraction fails or data is invalid
            FileNotFoundError: If source file doesn't exist
            Exception: For other extractor-specific errors

        Examples:
            data = extractor.extract("financials.xlsx")
            data = extractor.extract("AAPL", years=5)
            data = extractor.extract("10k.pdf", use_llm=True)
        """
        pass

    def _calculate_completeness(self, data: FinancialData) -> float:
        """
        Calculate how complete the extracted data is (0.0 to 1.0).

        Checks both required and optional fields to give a completeness score.
        This helps users understand data quality.

        Args:
            data: FinancialData object to assess

        Returns:
            Float between 0.0 and 1.0 representing completeness

        Methodology:
            - Required fields (revenue, years, company name): Must be present
            - Important fields (EBITDA, net income, total assets): Weighted higher
            - Optional fields (detailed line items): Weighted lower
        """
        total_fields = 0
        present_fields = 0

        # Required fields (must be present, but don't count in score)
        # These are validated in FinancialData.__post_init__

        # Important income statement fields (weight: 3x)
        important_income_fields = [
            ('revenue', data.income_statement.revenue),
            ('ebitda', data.income_statement.ebitda),
            ('ebit', data.income_statement.ebit),
            ('net_income', data.income_statement.net_income),
        ]

        for field_name, field_value in important_income_fields:
            total_fields += 3
            if field_value and any(v is not None for v in field_value):
                present_fields += 3

        # Standard income statement fields (weight: 2x)
        standard_income_fields = [
            ('cogs', data.income_statement.cogs),
            ('gross_profit', data.income_statement.gross_profit),
            ('operating_expenses', data.income_statement.operating_expenses),
            ('depreciation_amortization', data.income_statement.depreciation_amortization),
            ('interest_expense', data.income_statement.interest_expense),
            ('income_tax', data.income_statement.income_tax),
        ]

        for field_name, field_value in standard_income_fields:
            total_fields += 2
            if field_value and any(v is not None for v in field_value):
                present_fields += 2

        # Important balance sheet fields (weight: 2x)
        important_bs_fields = [
            ('cash', data.balance_sheet.cash),
            ('total_assets', data.balance_sheet.total_assets),
            ('total_liabilities', data.balance_sheet.total_liabilities),
            ('shareholders_equity', data.balance_sheet.shareholders_equity),
            ('long_term_debt', data.balance_sheet.long_term_debt),
        ]

        for field_name, field_value in important_bs_fields:
            total_fields += 2
            if field_value and any(v is not None for v in field_value):
                present_fields += 2

        # Standard balance sheet fields (weight: 1x)
        standard_bs_fields = [
            ('accounts_receivable', data.balance_sheet.accounts_receivable),
            ('inventory', data.balance_sheet.inventory),
            ('current_assets', data.balance_sheet.current_assets),
            ('ppe_net', data.balance_sheet.ppe_net),
            ('accounts_payable', data.balance_sheet.accounts_payable),
            ('current_liabilities', data.balance_sheet.current_liabilities),
        ]

        for field_name, field_value in standard_bs_fields:
            total_fields += 1
            if field_value and any(v is not None for v in field_value):
                present_fields += 1

        # Important cash flow fields (weight: 2x)
        important_cf_fields = [
            ('operating_cash_flow', data.cash_flow.operating_cash_flow),
            ('capex', data.cash_flow.capex),
            ('free_cash_flow', data.cash_flow.free_cash_flow),
        ]

        for field_name, field_value in important_cf_fields:
            total_fields += 2
            if field_value and any(v is not None for v in field_value):
                present_fields += 2

        # Standard cash flow fields (weight: 1x)
        standard_cf_fields = [
            ('depreciation_amortization', data.cash_flow.depreciation_amortization),
            ('change_in_nwc', data.cash_flow.change_in_nwc),
        ]

        for field_name, field_value in standard_cf_fields:
            total_fields += 1
            if field_value and any(v is not None for v in field_value):
                present_fields += 1

        # Market data fields (weight: 1x each)
        market_fields = [
            ('share_price', data.market_data.share_price),
            ('shares_outstanding', data.market_data.shares_outstanding),
            ('market_cap', data.market_data.market_cap),
            ('total_debt', data.market_data.total_debt),
            ('net_debt', data.market_data.net_debt),
            ('enterprise_value', data.market_data.enterprise_value),
            ('beta', data.market_data.beta),
        ]

        for field_name, field_value in market_fields:
            total_fields += 1
            if field_value is not None:
                present_fields += 1

        # Calculate score
        if total_fields == 0:
            return 0.0

        completeness = present_fields / total_fields
        return min(completeness, 1.0)  # Cap at 1.0

    def _validate_basic_data(self, data: FinancialData) -> None:
        """
        Perform basic validation on extracted data.

        This is a lightweight validation that all extractors should run.
        More comprehensive validation is done by DataValidator.

        Args:
            data: FinancialData object to validate

        Raises:
            ValueError: If critical validation fails
        """
        # Check revenue is positive
        if any(r <= 0 for r in data.income_statement.revenue if r is not None):
            raise ValueError("Revenue must be positive for all years")

        # Check years are sequential
        for i in range(1, len(data.years)):
            if data.years[i] != data.years[i-1] + 1:
                data.metadata.add_warning(
                    f"Non-sequential years detected: {data.years[i-1]} -> {data.years[i]}"
                )

        # Warn if completeness is low
        if data.metadata.completeness_score < 0.5:
            data.metadata.add_warning(
                f"Low data completeness: {data.metadata.completeness_score:.1%}. "
                f"Many fields are missing."
            )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"
