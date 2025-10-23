"""
Helper utilities for financial calculations and data manipulation
"""

from typing import List, Optional
import numpy as np


def calculate_cagr(beginning_value: float, ending_value: float, years: float) -> float:
    """
    Calculate Compound Annual Growth Rate (CAGR).

    CAGR = (Ending Value / Beginning Value)^(1/years) - 1

    Args:
        beginning_value: Starting value
        ending_value: Ending value
        years: Number of years

    Returns:
        CAGR as decimal (e.g., 0.10 for 10%)
    """
    if beginning_value <= 0:
        raise ValueError("Beginning value must be positive")

    if years <= 0:
        raise ValueError("Years must be positive")

    cagr = (ending_value / beginning_value) ** (1 / years) - 1
    return cagr


def calculate_average_growth(values: List[float]) -> float:
    """
    Calculate average year-over-year growth rate.

    Args:
        values: List of values (earliest to latest)

    Returns:
        Average growth rate as decimal
    """
    if len(values) < 2:
        raise ValueError("Need at least 2 values to calculate growth")

    growth_rates = []
    for i in range(1, len(values)):
        if values[i - 1] != 0:
            growth = (values[i] - values[i - 1]) / values[i - 1]
            growth_rates.append(growth)

    return np.mean(growth_rates)


def millions_to_billions(value: float) -> float:
    """Convert millions to billions."""
    return value / 1000


def billions_to_millions(value: float) -> float:
    """Convert billions to millions."""
    return value * 1000


def format_large_number(value: float, decimals: int = 1) -> str:
    """
    Format large numbers with B/M/T suffixes.

    Args:
        value: Number to format
        decimals: Decimal places

    Returns:
        Formatted string (e.g., "$2.5T", "$150.3B", "$50.0M")
    """
    abs_value = abs(value)

    if abs_value >= 1e12:
        formatted = f"${value / 1e12:.{decimals}f}T"
    elif abs_value >= 1e9:
        formatted = f"${value / 1e9:.{decimals}f}B"
    elif abs_value >= 1e6:
        formatted = f"${value / 1e6:.{decimals}f}M"
    elif abs_value >= 1e3:
        formatted = f"${value / 1e3:.{decimals}f}K"
    else:
        formatted = f"${value:.{decimals}f}"

    return formatted


def interpolate_growth_rates(
    start_rate: float,
    end_rate: float,
    years: int
) -> List[float]:
    """
    Linearly interpolate growth rates from start to end.

    Useful for creating smooth revenue growth projections.

    Args:
        start_rate: Starting growth rate
        end_rate: Ending growth rate
        years: Number of years

    Returns:
        List of interpolated growth rates
    """
    if years < 2:
        return [start_rate] * years

    rates = np.linspace(start_rate, end_rate, years)
    return rates.tolist()


def calculate_net_debt(
    total_debt: float,
    cash: float,
    short_term_investments: float = 0
) -> float:
    """
    Calculate net debt.

    Net Debt = Total Debt - Cash - Short-term Investments

    Args:
        total_debt: Total debt
        cash: Cash and cash equivalents
        short_term_investments: Short-term marketable securities

    Returns:
        Net debt (can be negative if cash > debt)
    """
    return total_debt - cash - short_term_investments


def calculate_working_capital(
    current_assets: float,
    current_liabilities: float
) -> float:
    """
    Calculate net working capital.

    NWC = Current Assets - Current Liabilities

    Args:
        current_assets: Current assets
        current_liabilities: Current liabilities

    Returns:
        Net working capital
    """
    return current_assets - current_liabilities
