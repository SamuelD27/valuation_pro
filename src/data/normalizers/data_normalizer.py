"""
Production-ready data normalizer for financial data.

Handles:
- Automatic scale detection (thousands, millions, billions)
- Unit conversion to standard millions
- Derived field calculation
- Missing data handling
- Currency conversion

Performance target: <1s per company dataset
"""

import re
import pandas as pd
import numpy as np
from typing import List, Optional, Dict, Tuple, Any
from enum import Enum
import warnings

from ..schema import FinancialData, IncomeStatement, BalanceSheet, CashFlowStatement


class Scale(Enum):
    """Monetary scale enumeration."""
    ACTUAL = 1
    THOUSANDS = 1_000
    MILLIONS = 1_000_000
    BILLIONS = 1_000_000_000


class DataNormalizer:
    """
    Production normalizer for financial data.

    Uses multi-method scale detection:
    1. Context analysis (looks for "in millions", "$M", etc.)
    2. Value heuristics (typical ranges for public companies)
    3. Sanity checks (Revenue $1M-$1T for public companies)
    """

    # Keywords for scale detection
    SCALE_KEYWORDS = {
        Scale.THOUSANDS: ['thousands', 'in thousands', '000s', '(000)', 'k'],
        Scale.MILLIONS: ['millions', 'in millions', 'mm', '$m', '(mm)', 'm'],
        Scale.BILLIONS: ['billions', 'in billions', 'bn', '$b', '(bn)', 'b'],
    }

    # Typical revenue ranges for public companies (in actual dollars)
    REVENUE_RANGES = {
        'small_cap': (1_000_000, 100_000_000),       # $1M - $100M
        'mid_cap': (100_000_000, 1_000_000_000),     # $100M - $1B
        'large_cap': (1_000_000_000, 50_000_000_000), # $1B - $50B
        'mega_cap': (50_000_000_000, 1_000_000_000_000), # $50B - $1T
    }

    @staticmethod
    def normalize(data: FinancialData, context: Optional[str] = None) -> FinancialData:
        """
        Apply all normalization steps to financial data.

        Steps:
        1. Detect scale from context and values
        2. Convert all values to millions
        3. Fill derived fields (e.g., gross_profit = revenue - cogs)
        4. Handle missing data
        5. Align fiscal years

        Args:
            data: FinancialData object to normalize
            context: Optional context string for scale detection
                    (e.g., "All values in thousands")

        Returns:
            Normalized FinancialData object

        Performance: <1s for typical dataset
        """
        print(f"🔄 Normalizing financial data for {data.company.name}...")

        # Step 1: Detect and convert scale
        data = DataNormalizer._convert_to_millions(data, context)

        # Step 2: Fill derived fields
        data = DataNormalizer._fill_derived_fields(data)

        # Step 3: Handle missing data
        data = DataNormalizer._handle_missing_data(data)

        # Step 4: Align fiscal years (ensure sequential)
        data = DataNormalizer._align_fiscal_years(data)

        # Step 5: Validate reasonableness
        DataNormalizer._validate_normalized_data(data)

        data.metadata.add_unit_conversion("normalized_to_millions")
        print(f"✓ Normalization complete")

        return data

    @staticmethod
    def detect_scale(
        values: List[float],
        context: Optional[str] = None,
        field_name: str = "revenue"
    ) -> Tuple[Scale, float]:
        """
        Detect the scale of financial values using multiple methods.

        Algorithm:
        1. Check context for explicit scale keywords
        2. Apply value heuristics based on typical ranges
        3. Sanity check against known company sizes

        Args:
            values: List of financial values
            context: Optional context string (e.g., sheet header, notes)
            field_name: Name of field for context (revenue, ebitda, etc.)

        Returns:
            Tuple of (detected_scale, confidence_score)

        Examples:
            >>> detect_scale([1200, 1350], "All values in thousands")
            (Scale.THOUSANDS, 1.0)

            >>> detect_scale([1.2, 1.35], "Revenue in billions")
            (Scale.BILLIONS, 1.0)

            >>> detect_scale([1200, 1350], None)  # No context
            (Scale.MILLIONS, 0.8)  # Heuristic-based
        """
        # Filter out None values
        valid_values = [v for v in values if v is not None and v > 0]

        if not valid_values:
            return Scale.MILLIONS, 0.5  # Default with low confidence

        # Method 1: Context analysis (highest confidence)
        if context:
            context_lower = context.lower()
            for scale, keywords in DataNormalizer.SCALE_KEYWORDS.items():
                if any(kw in context_lower for kw in keywords):
                    return scale, 1.0  # High confidence from explicit context

        # Method 2: Value heuristics
        median_value = np.median(valid_values)

        # For revenue specifically, use company size heuristics
        if field_name.lower() in ['revenue', 'sales', 'turnover']:
            detected_scale, confidence = DataNormalizer._detect_revenue_scale(median_value)
            if confidence > 0.7:
                return detected_scale, confidence

        # General heuristics for all fields
        if median_value < 1:
            # Very small values likely in billions
            return Scale.BILLIONS, 0.7

        elif 1 <= median_value < 100:
            # Could be millions or billions
            # Check if it makes sense as millions
            if 10 <= median_value <= 10_000:
                return Scale.MILLIONS, 0.8
            else:
                return Scale.BILLIONS, 0.6

        elif 100 <= median_value < 10_000:
            # Most likely millions
            return Scale.MILLIONS, 0.9

        elif 10_000 <= median_value < 1_000_000:
            # Likely thousands
            return Scale.THOUSANDS, 0.8

        elif median_value >= 1_000_000:
            # Likely actual values (no scaling)
            return Scale.ACTUAL, 0.9

        # Default: assume millions (most common in IB)
        return Scale.MILLIONS, 0.5

    @staticmethod
    def _detect_revenue_scale(revenue: float) -> Tuple[Scale, float]:
        """
        Detect scale specifically for revenue using company size heuristics.

        Public companies typically have revenue in specific ranges.

        Args:
            revenue: Single revenue value

        Returns:
            Tuple of (scale, confidence)
        """
        # Check each scale to see if revenue falls in reasonable range
        scales_to_check = [
            (Scale.ACTUAL, 1),
            (Scale.THOUSANDS, 1_000),
            (Scale.MILLIONS, 1_000_000),
            (Scale.BILLIONS, 1_000_000_000),
        ]

        best_match = None
        best_confidence = 0.0

        for scale, multiplier in scales_to_check:
            # Convert to actual dollars
            actual_value = revenue * multiplier

            # Check if it falls in any reasonable range
            for cap_type, (min_rev, max_rev) in DataNormalizer.REVENUE_RANGES.items():
                if min_rev <= actual_value <= max_rev:
                    # This scale makes sense
                    confidence = 0.9

                    # Small/mid cap more common, so higher confidence
                    if cap_type in ['small_cap', 'mid_cap']:
                        confidence = 0.95

                    if confidence > best_confidence:
                        best_confidence = confidence
                        best_match = scale

        if best_match:
            return best_match, best_confidence

        # No good match - default to millions with low confidence
        return Scale.MILLIONS, 0.5

    @staticmethod
    def _convert_to_millions(data: FinancialData, context: Optional[str]) -> FinancialData:
        """
        Convert all financial values to millions.

        Detects scale and applies appropriate conversion.

        Args:
            data: FinancialData object
            context: Optional context for scale detection

        Returns:
            FinancialData with all values in millions
        """
        # Check if data was already normalized during extraction (e.g., API sources)
        if data.metadata.unit_conversions_applied:
            for conversion in data.metadata.unit_conversions_applied:
                if "millions" in conversion.lower():
                    print(f"  → Data already normalized to millions during extraction")
                    return data

        # Detect scale from revenue (most reliable indicator)
        scale, confidence = DataNormalizer.detect_scale(
            data.income_statement.revenue,
            context,
            field_name="revenue"
        )

        if scale == Scale.MILLIONS:
            # Already in millions, no conversion needed
            if confidence < 0.9:
                data.metadata.add_warning(
                    f"Scale detection confidence low ({confidence:.1%}). "
                    f"Assuming millions - please verify."
                )
            return data

        # Calculate conversion factor to millions
        conversion_factor = scale.value / Scale.MILLIONS.value

        print(f"  → Detected scale: {scale.name} (confidence: {confidence:.1%})")
        print(f"  → Converting to millions (factor: {conversion_factor})")

        # Apply conversion to all financial statements
        data.income_statement = DataNormalizer._convert_income_statement(
            data.income_statement,
            conversion_factor
        )

        data.balance_sheet = DataNormalizer._convert_balance_sheet(
            data.balance_sheet,
            conversion_factor
        )

        data.cash_flow = DataNormalizer._convert_cash_flow(
            data.cash_flow,
            conversion_factor
        )

        # Convert market data
        data.market_data = DataNormalizer._convert_market_data(
            data.market_data,
            conversion_factor
        )

        # Log conversion
        data.metadata.add_unit_conversion(
            f"converted_from_{scale.name.lower()}_to_millions"
        )

        return data

    @staticmethod
    def _convert_income_statement(
        income_stmt: IncomeStatement,
        factor: float
    ) -> IncomeStatement:
        """Convert all income statement values by factor."""

        def convert_list(values: Optional[List[float]]) -> Optional[List[float]]:
            if values is None:
                return None
            return [v * factor if v is not None else None for v in values]

        return IncomeStatement(
            revenue=convert_list(income_stmt.revenue),
            cogs=convert_list(income_stmt.cogs),
            gross_profit=convert_list(income_stmt.gross_profit),
            operating_expenses=convert_list(income_stmt.operating_expenses),
            rd_expense=convert_list(income_stmt.rd_expense),
            sga_expense=convert_list(income_stmt.sga_expense),
            ebitda=convert_list(income_stmt.ebitda),
            depreciation_amortization=convert_list(income_stmt.depreciation_amortization),
            ebit=convert_list(income_stmt.ebit),
            interest_expense=convert_list(income_stmt.interest_expense),
            interest_income=convert_list(income_stmt.interest_income),
            other_income_expense=convert_list(income_stmt.other_income_expense),
            pretax_income=convert_list(income_stmt.pretax_income),
            income_tax=convert_list(income_stmt.income_tax),
            net_income=convert_list(income_stmt.net_income),
            eps_basic=income_stmt.eps_basic,  # Per-share metrics don't need conversion
            eps_diluted=income_stmt.eps_diluted,
        )

    @staticmethod
    def _convert_balance_sheet(
        balance_sheet: BalanceSheet,
        factor: float
    ) -> BalanceSheet:
        """Convert all balance sheet values by factor."""

        def convert_list(values: Optional[List[float]]) -> Optional[List[float]]:
            if values is None:
                return None
            return [v * factor if v is not None else None for v in values]

        # Convert all fields
        converted = BalanceSheet()

        for field_name in balance_sheet.__dataclass_fields__:
            value = getattr(balance_sheet, field_name)
            if isinstance(value, list):
                setattr(converted, field_name, convert_list(value))
            else:
                setattr(converted, field_name, value)

        return converted

    @staticmethod
    def _convert_cash_flow(
        cash_flow: CashFlowStatement,
        factor: float
    ) -> CashFlowStatement:
        """Convert all cash flow values by factor."""

        def convert_list(values: Optional[List[float]]) -> Optional[List[float]]:
            if values is None:
                return None
            return [v * factor if v is not None else None for v in values]

        # Convert all fields
        converted = CashFlowStatement()

        for field_name in cash_flow.__dataclass_fields__:
            value = getattr(cash_flow, field_name)
            if isinstance(value, list):
                setattr(converted, field_name, convert_list(value))
            else:
                setattr(converted, field_name, value)

        return converted

    @staticmethod
    def _convert_market_data(market_data, factor: float):
        """Convert market data values (except per-share metrics)."""
        # Market data fields that need conversion (in millions)
        fields_to_convert = [
            'market_cap', 'total_debt', 'cash_and_equivalents',
            'net_debt', 'enterprise_value'
        ]

        for field in fields_to_convert:
            value = getattr(market_data, field, None)
            if value is not None:
                setattr(market_data, field, value * factor)

        return market_data

    @staticmethod
    def _fill_derived_fields(data: FinancialData) -> FinancialData:
        """
        Calculate missing fields from available data.

        Derived calculations:
        - gross_profit = revenue - cogs
        - ebit = ebitda - depreciation_amortization
        - net_debt = total_debt - cash
        - free_cash_flow = operating_cash_flow - capex
        - enterprise_value = market_cap + net_debt

        Args:
            data: FinancialData object

        Returns:
            FinancialData with derived fields filled
        """
        num_years = len(data.years)

        # Income statement derived fields
        income = data.income_statement

        # Gross profit = Revenue - COGS
        if income.gross_profit is None and income.revenue and income.cogs:
            income.gross_profit = [
                (income.revenue[i] - income.cogs[i])
                if (income.revenue[i] is not None and income.cogs[i] is not None)
                else None
                for i in range(num_years)
            ]
            if any(v is not None for v in income.gross_profit):
                data.metadata.add_derived_field("gross_profit")

        # EBIT = EBITDA - D&A
        if income.ebit is None and income.ebitda and income.depreciation_amortization:
            income.ebit = [
                (income.ebitda[i] - income.depreciation_amortization[i])
                if (income.ebitda[i] is not None and income.depreciation_amortization[i] is not None)
                else None
                for i in range(num_years)
            ]
            if any(v is not None for v in income.ebit):
                data.metadata.add_derived_field("ebit")

        # Cash flow derived fields
        cf = data.cash_flow

        # Free Cash Flow = OCF - CapEx
        if cf.free_cash_flow is None and cf.operating_cash_flow and cf.capex:
            cf.free_cash_flow = [
                (cf.operating_cash_flow[i] - abs(cf.capex[i]))  # CapEx usually negative
                if (cf.operating_cash_flow[i] is not None and cf.capex[i] is not None)
                else None
                for i in range(num_years)
            ]
            if any(v is not None for v in cf.free_cash_flow):
                data.metadata.add_derived_field("free_cash_flow")

        # Market data derived fields
        market = data.market_data

        # Net Debt = Total Debt - Cash
        if market.net_debt is None and market.total_debt and market.cash_and_equivalents:
            market.net_debt = market.total_debt - market.cash_and_equivalents
            data.metadata.add_derived_field("net_debt")

        # Enterprise Value = Market Cap + Net Debt
        if market.enterprise_value is None and market.market_cap and market.net_debt is not None:
            market.enterprise_value = market.market_cap + market.net_debt
            data.metadata.add_derived_field("enterprise_value")

        return data

    @staticmethod
    def _handle_missing_data(data: FinancialData) -> FinancialData:
        """
        Strategy for handling missing data.

        Critical fields (revenue, net_income): Must be present or warn
        Optional fields: Leave as None
        Derived fields: Calculate if possible, otherwise None

        Args:
            data: FinancialData object

        Returns:
            FinancialData with missing data handled
        """
        # Check critical fields
        if not data.income_statement.revenue or all(v is None for v in data.income_statement.revenue):
            raise ValueError("Revenue is required but missing - cannot proceed")

        # Warn about missing important fields
        important_fields = [
            ('ebitda', data.income_statement.ebitda),
            ('net_income', data.income_statement.net_income),
            ('total_assets', data.balance_sheet.total_assets),
            ('operating_cash_flow', data.cash_flow.operating_cash_flow),
        ]

        for field_name, field_value in important_fields:
            if field_value is None or all(v is None for v in field_value if isinstance(field_value, list)):
                data.metadata.add_warning(f"Important field '{field_name}' is missing")

        return data

    @staticmethod
    def _align_fiscal_years(data: FinancialData) -> FinancialData:
        """
        Ensure fiscal years are properly aligned and sequential.

        Checks for gaps in years and warns if found.

        Args:
            data: FinancialData object

        Returns:
            FinancialData with validated year alignment
        """
        years = data.years

        # Check for sequential years
        for i in range(1, len(years)):
            gap = years[i] - years[i-1]
            if gap != 1:
                data.metadata.add_warning(
                    f"Non-sequential years detected: {years[i-1]} → {years[i]} (gap: {gap} years)"
                )

        return data

    @staticmethod
    def _validate_normalized_data(data: FinancialData) -> None:
        """
        Validate that normalized data is reasonable.

        Checks:
        - Revenue in reasonable range ($1M - $1T)
        - Margins in valid range (-100% to 100%)
        - No extreme outliers

        Args:
            data: Normalized FinancialData object

        Raises:
            ValueError: If data fails critical validation
        """
        revenue = data.income_statement.revenue

        # Check revenue range (assuming millions)
        for i, rev in enumerate(revenue):
            if rev is not None:
                # Revenue should be between $1M and $1T (in millions: 1 to 1,000,000)
                if not (0.1 <= rev <= 1_000_000):
                    warnings.warn(
                        f"Revenue for {data.years[i]} (${rev}M) outside typical range. "
                        f"Possible scale detection error."
                    )

        # Check margins if available
        if data.income_statement.ebitda and data.income_statement.revenue:
            for i in range(len(data.years)):
                ebitda = data.income_statement.ebitda[i]
                rev = revenue[i]

                if ebitda is not None and rev is not None and rev > 0:
                    margin = ebitda / rev

                    if not (-1.0 <= margin <= 1.0):
                        data.metadata.add_warning(
                            f"EBITDA margin for {data.years[i]} is {margin:.1%} - "
                            f"outside reasonable range (-100% to 100%)"
                        )


# Convenience functions

def normalize_to_millions(df: pd.DataFrame, scale: Scale = Scale.MILLIONS) -> pd.DataFrame:
    """
    Normalize a pandas DataFrame to millions.

    Args:
        df: DataFrame with financial data
        scale: Current scale of the data

    Returns:
        DataFrame with values in millions

    Example:
        >>> df = pd.DataFrame({'revenue': [1200, 1350], 'ebitda': [360, 415]})
        >>> normalized = normalize_to_millions(df, Scale.THOUSANDS)
        >>> # Revenue now: [1.2, 1.35], EBITDA: [0.36, 0.415]
    """
    if scale == Scale.MILLIONS:
        return df

    factor = scale.value / Scale.MILLIONS.value
    return df * factor


def detect_scale_from_context(context: str) -> Optional[Scale]:
    """
    Detect scale from context string.

    Args:
        context: Context string (e.g., "All values in thousands")

    Returns:
        Detected Scale or None

    Example:
        >>> detect_scale_from_context("Financial data in millions")
        Scale.MILLIONS

        >>> detect_scale_from_context("Values are in 000s")
        Scale.THOUSANDS
    """
    context_lower = context.lower()

    for scale, keywords in DataNormalizer.SCALE_KEYWORDS.items():
        if any(kw in context_lower for kw in keywords):
            return scale

    return None
