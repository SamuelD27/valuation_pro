"""
Risk Metrics Calculation

Provides risk measurement and quantification tools.

Metrics Supported:
- Value at Risk (VaR)
- Conditional Value at Risk (CVaR / Expected Shortfall)
- Volatility measures
- Downside risk metrics
- Risk-adjusted returns

Example:
    >>> from src.analytics.risk_metrics import calculate_var
    >>> var_95 = calculate_var(returns, confidence=0.95)
    >>> cvar_95 = calculate_cvar(returns, confidence=0.95)
"""

import numpy as np
from typing import Optional


def calculate_var(
    returns: np.ndarray,
    confidence: float = 0.95,
    method: str = 'historical'
) -> float:
    """
    Calculate Value at Risk.

    Args:
        returns: Array of returns or outcomes
        confidence: Confidence level (e.g., 0.95 for 95%)
        method: Calculation method ('historical', 'parametric', 'monte_carlo')

    Returns:
        VaR value at specified confidence level
    """
    if method == 'historical':
        return np.percentile(returns, (1 - confidence) * 100)
    else:
        raise NotImplementedError(f"Method '{method}' not yet implemented")


def calculate_cvar(
    returns: np.ndarray,
    confidence: float = 0.95
) -> float:
    """
    Calculate Conditional Value at Risk (Expected Shortfall).

    CVaR is the expected loss given that the loss exceeds VaR.

    Args:
        returns: Array of returns or outcomes
        confidence: Confidence level

    Returns:
        CVaR value
    """
    var = calculate_var(returns, confidence)
    # CVaR is the mean of losses beyond VaR
    tail_losses = returns[returns <= var]
    return tail_losses.mean() if len(tail_losses) > 0 else var


def calculate_downside_deviation(
    returns: np.ndarray,
    target_return: float = 0.0
) -> float:
    """
    Calculate downside deviation (semi-deviation).

    Measures volatility of negative returns only.

    Args:
        returns: Array of returns
        target_return: Minimum acceptable return

    Returns:
        Downside deviation
    """
    downside_returns = returns[returns < target_return]
    if len(downside_returns) == 0:
        return 0.0
    return np.std(downside_returns - target_return)


def calculate_sortino_ratio(
    returns: np.ndarray,
    risk_free_rate: float = 0.0,
    target_return: float = 0.0
) -> float:
    """
    Calculate Sortino ratio (risk-adjusted return using downside deviation).

    Args:
        returns: Array of returns
        risk_free_rate: Risk-free rate
        target_return: Minimum acceptable return

    Returns:
        Sortino ratio
    """
    excess_return = returns.mean() - risk_free_rate
    downside_dev = calculate_downside_deviation(returns, target_return)

    if downside_dev == 0:
        return np.inf if excess_return > 0 else 0

    return excess_return / downside_dev


# TODO: Implement parametric VaR
# TODO: Add Maximum Drawdown calculation
# TODO: Implement Sharpe ratio variants
# TODO: Add stress VaR calculation
