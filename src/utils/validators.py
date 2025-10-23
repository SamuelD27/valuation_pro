"""
Validators for financial models

Provides validation functions to ensure data quality and
catch common errors in valuation models.
"""

from typing import List, Dict, Optional
import warnings


def validate_positive(value: float, name: str) -> bool:
    """
    Validate that a value is positive.

    Args:
        value: Value to check
        name: Name of the value (for error messages)

    Returns:
        True if valid

    Raises:
        ValueError: If value is not positive
    """
    if value <= 0:
        raise ValueError(f"{name} must be positive, got {value}")
    return True


def validate_percentage(value: float, name: str, allow_negative: bool = False) -> bool:
    """
    Validate that a value is a reasonable percentage.

    Args:
        value: Value to check (as decimal, e.g., 0.05 for 5%)
        name: Name of the value
        allow_negative: Whether to allow negative values

    Returns:
        True if valid

    Raises:
        ValueError: If value is outside reasonable bounds
    """
    if not allow_negative and value < 0:
        raise ValueError(f"{name} cannot be negative: {value}")

    if abs(value) > 2.0:  # 200%
        warnings.warn(
            f"{name} of {value:.1%} seems unusually high. Please verify."
        )

    return True


def validate_growth_rate(rate: float, name: str = "Growth rate") -> bool:
    """
    Validate growth rate is reasonable.

    Args:
        rate: Growth rate as decimal (e.g., 0.10 for 10%)
        name: Name of the rate

    Returns:
        True if valid
    """
    if rate < -0.50:
        warnings.warn(
            f"{name} of {rate:.1%} indicates severe decline. Please verify."
        )

    if rate > 0.50:
        warnings.warn(
            f"{name} of {rate:.1%} is very high. Please verify sustainability."
        )

    return True


def validate_wacc(wacc: float, terminal_growth: float) -> bool:
    """
    Validate WACC and terminal growth relationship.

    Terminal growth must be less than WACC for DCF to work.

    Args:
        wacc: Weighted average cost of capital
        terminal_growth: Terminal growth rate

    Returns:
        True if valid

    Raises:
        ValueError: If terminal growth >= WACC
    """
    if terminal_growth >= wacc:
        raise ValueError(
            f"Terminal growth ({terminal_growth:.2%}) must be less than "
            f"WACC ({wacc:.2%}) for Gordon Growth model."
        )

    # Warn if they're very close
    if wacc - terminal_growth < 0.01:  # Less than 1% spread
        warnings.warn(
            f"WACC ({wacc:.2%}) and terminal growth ({terminal_growth:.2%}) "
            f"are very close. This makes valuation highly sensitive."
        )

    return True


def validate_financial_data(data: Dict) -> bool:
    """
    Validate financial data structure and contents.

    Args:
        data: Dictionary of financial data

    Returns:
        True if valid

    Raises:
        ValueError: If data is missing or invalid
    """
    required_keys = ['revenue', 'ebit', 'tax_rate']

    for key in required_keys:
        if key not in data:
            raise ValueError(f"Missing required financial data: {key}")

    # Validate revenue is positive
    if isinstance(data['revenue'], list):
        for i, rev in enumerate(data['revenue']):
            if rev and rev <= 0:
                raise ValueError(f"Revenue in year {i} must be positive: {rev}")

    return True


def validate_dcf_assumptions(assumptions: Dict) -> bool:
    """
    Validate DCF model assumptions.

    Args:
        assumptions: Dictionary of assumptions

    Returns:
        True if valid

    Raises:
        ValueError: If assumptions are invalid
    """
    required_keys = [
        'revenue_growth', 'wacc', 'terminal_growth', 'shares_outstanding'
    ]

    for key in required_keys:
        if key not in assumptions:
            raise ValueError(f"Missing required assumption: {key}")

    # Validate WACC vs terminal growth
    validate_wacc(assumptions['wacc'], assumptions['terminal_growth'])

    # Validate shares outstanding
    validate_positive(assumptions['shares_outstanding'], "Shares outstanding")

    # Validate growth rates
    if isinstance(assumptions['revenue_growth'], list):
        for i, rate in enumerate(assumptions['revenue_growth']):
            validate_growth_rate(rate, f"Revenue growth year {i+1}")

    return True
