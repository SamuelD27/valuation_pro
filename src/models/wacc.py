"""
WACC (Weighted Average Cost of Capital) Calculator

Calculates the weighted average cost of capital using market data.
Follows standard investment banking methodology.
"""

import yfinance as yf
from typing import Dict, Optional
import warnings


class WACCCalculator:
    """
    Calculate weighted average cost of capital (WACC) for a company.

    WACC = (E/V × Re) + (D/V × Rd × (1-T))

    Where:
        E = Market value of equity
        D = Market value of debt
        V = E + D (total firm value)
        Re = Cost of equity
        Rd = Cost of debt
        T = Tax rate
    """

    # Standard market risk premium used in investment banking
    MARKET_RISK_PREMIUM = 0.06  # 6%

    # Reasonable WACC range for validation
    MIN_WACC = 0.05  # 5%
    MAX_WACC = 0.25  # 25%

    def __init__(
        self,
        ticker: str,
        debt: float,
        equity: float,
        tax_rate: float,
        risk_free_rate: Optional[float] = None
    ):
        """
        Initialize WACC Calculator.

        Args:
            ticker: Company stock ticker symbol (e.g., 'AAPL')
            debt: Market value of debt in millions ($M)
            equity: Market value of equity in millions ($M)
            tax_rate: Corporate tax rate as decimal (e.g., 0.21 for 21%)
            risk_free_rate: Optional risk-free rate override (otherwise fetched from market)

        Raises:
            ValueError: If tax_rate is negative or debt/equity are not positive
        """
        if tax_rate < 0:
            raise ValueError(f"Tax rate cannot be negative: {tax_rate}")
        if debt < 0:
            raise ValueError(f"Debt cannot be negative: {debt}")
        if equity <= 0:
            raise ValueError(f"Equity must be positive: {equity}")

        self.ticker = ticker.upper()
        self.debt = debt
        self.equity = equity
        self.tax_rate = tax_rate
        self._risk_free_rate = risk_free_rate
        self._beta = None

    def get_risk_free_rate(self) -> float:
        """
        Fetch current 10-Year U.S. Treasury yield as risk-free rate.

        Uses yfinance to get ^TNX (10-Year Treasury Note Yield).
        Falls back to standard 4% if data unavailable.

        Returns:
            Risk-free rate as decimal (e.g., 0.04 for 4%)
        """
        if self._risk_free_rate is not None:
            return self._risk_free_rate

        try:
            # Fetch 10-year Treasury yield
            treasury = yf.Ticker("^TNX")
            hist = treasury.history(period="5d")

            if not hist.empty:
                # TNX is already in percentage form, convert to decimal
                rf_rate = hist['Close'].iloc[-1] / 100
                return rf_rate
            else:
                warnings.warn(
                    "Could not fetch Treasury rate from yfinance. Using default 4%."
                )
                return 0.04

        except Exception as e:
            warnings.warn(
                f"Error fetching risk-free rate: {e}. Using default 4%."
            )
            return 0.04

    def get_beta(self) -> float:
        """
        Fetch company beta from yfinance.

        Beta measures systematic risk relative to the market.
        Falls back to 1.0 (market beta) if unavailable.

        Returns:
            Beta coefficient
        """
        if self._beta is not None:
            return self._beta

        try:
            stock = yf.Ticker(self.ticker)
            info = stock.info

            # yfinance provides beta in the info dict
            beta = info.get('beta')

            if beta is not None and beta > 0:
                self._beta = beta
                return beta
            else:
                warnings.warn(
                    f"Beta not available for {self.ticker}. Using market beta of 1.0."
                )
                self._beta = 1.0
                return 1.0

        except Exception as e:
            warnings.warn(
                f"Error fetching beta for {self.ticker}: {e}. Using default 1.0."
            )
            self._beta = 1.0
            return 1.0

    def calculate_cost_of_equity(self) -> float:
        """
        Calculate cost of equity using Capital Asset Pricing Model (CAPM).

        Re = Rf + β × (Rm - Rf)

        Where:
            Rf = Risk-free rate
            β = Beta (systematic risk)
            Rm - Rf = Market risk premium (typically 6%)

        Returns:
            Cost of equity as decimal (e.g., 0.10 for 10%)
        """
        rf = self.get_risk_free_rate()
        beta = self.get_beta()

        cost_of_equity = rf + (beta * self.MARKET_RISK_PREMIUM)

        return cost_of_equity

    def calculate_cost_of_debt(self, interest_expense: float) -> float:
        """
        Calculate after-tax cost of debt.

        Rd = Interest Expense / Debt
        After-tax Rd = Rd × (1 - Tax Rate)

        Args:
            interest_expense: Annual interest expense in millions ($M)

        Returns:
            After-tax cost of debt as decimal

        Raises:
            ValueError: If interest expense is negative
        """
        if interest_expense < 0:
            raise ValueError(f"Interest expense cannot be negative: {interest_expense}")

        if self.debt == 0:
            return 0.0

        # Pre-tax cost of debt
        rd_pretax = interest_expense / self.debt

        # Apply tax shield
        rd_aftertax = rd_pretax * (1 - self.tax_rate)

        return rd_aftertax

    def calculate_wacc(self, interest_expense: Optional[float] = None) -> Dict[str, float]:
        """
        Calculate weighted average cost of capital and all components.

        WACC = (E/V × Re) + (D/V × Rd × (1-T))

        Args:
            interest_expense: Annual interest expense ($M). If None, estimated as 5% of debt.

        Returns:
            Dictionary containing:
                - wacc: Weighted average cost of capital
                - cost_of_equity: Cost of equity (Re)
                - cost_of_debt: After-tax cost of debt (Rd)
                - weight_equity: E/V
                - weight_debt: D/V
                - risk_free_rate: Rf
                - beta: β
                - market_risk_premium: Market risk premium used
        """
        # Calculate components
        re = self.calculate_cost_of_equity()

        # Estimate interest expense if not provided (5% of debt is typical)
        if interest_expense is None:
            interest_expense = self.debt * 0.05

        rd = self.calculate_cost_of_debt(interest_expense)

        # Calculate weights
        total_value = self.equity + self.debt
        weight_equity = self.equity / total_value
        weight_debt = self.debt / total_value

        # Calculate WACC
        wacc = (weight_equity * re) + (weight_debt * rd)

        # Validate WACC is in reasonable range
        self.validate(wacc)

        return {
            'wacc': wacc,
            'cost_of_equity': re,
            'cost_of_debt': rd,
            'weight_equity': weight_equity,
            'weight_debt': weight_debt,
            'risk_free_rate': self.get_risk_free_rate(),
            'beta': self.get_beta(),
            'market_risk_premium': self.MARKET_RISK_PREMIUM,
            'tax_rate': self.tax_rate,
        }

    def validate(self, wacc: float) -> bool:
        """
        Validate that WACC is within reasonable bounds.

        Typical WACC ranges from 5% to 25%. Values outside this range
        trigger a warning but don't raise an error.

        Args:
            wacc: Calculated WACC value

        Returns:
            True if WACC is in valid range, False otherwise
        """
        if wacc < self.MIN_WACC or wacc > self.MAX_WACC:
            warnings.warn(
                f"WACC of {wacc:.2%} is outside typical range "
                f"({self.MIN_WACC:.0%}-{self.MAX_WACC:.0%}). "
                f"Please verify inputs."
            )
            return False
        return True

    def __repr__(self) -> str:
        """String representation of WACCCalculator."""
        return (
            f"WACCCalculator(ticker='{self.ticker}', "
            f"debt=${self.debt:,.0f}M, "
            f"equity=${self.equity:,.0f}M, "
            f"tax_rate={self.tax_rate:.1%})"
        )
