"""
Unit tests for WACC Calculator

Tests cover:
- Normal operation with real market data
- Edge cases (100% equity, negative inputs)
- Validation logic
- Component calculations
"""

import pytest
from src.models.wacc import WACCCalculator


class TestWACCCalculator:
    """Test suite for WACC Calculator"""

    def test_initialization_valid(self):
        """Test valid initialization"""
        calc = WACCCalculator(
            ticker="AAPL",
            debt=100000,
            equity=2500000,
            tax_rate=0.21
        )

        assert calc.ticker == "AAPL"
        assert calc.debt == 100000
        assert calc.equity == 2500000
        assert calc.tax_rate == 0.21

    def test_initialization_negative_tax_rate(self):
        """Test that negative tax rate raises ValueError"""
        with pytest.raises(ValueError, match="Tax rate cannot be negative"):
            WACCCalculator(
                ticker="AAPL",
                debt=100000,
                equity=2500000,
                tax_rate=-0.1
            )

    def test_initialization_negative_debt(self):
        """Test that negative debt raises ValueError"""
        with pytest.raises(ValueError, match="Debt cannot be negative"):
            WACCCalculator(
                ticker="AAPL",
                debt=-100000,
                equity=2500000,
                tax_rate=0.21
            )

    def test_initialization_zero_equity(self):
        """Test that zero equity raises ValueError"""
        with pytest.raises(ValueError, match="Equity must be positive"):
            WACCCalculator(
                ticker="AAPL",
                debt=100000,
                equity=0,
                tax_rate=0.21
            )

    def test_risk_free_rate_override(self):
        """Test manual risk-free rate override"""
        calc = WACCCalculator(
            ticker="AAPL",
            debt=100000,
            equity=2500000,
            tax_rate=0.21,
            risk_free_rate=0.045  # 4.5%
        )

        rf = calc.get_risk_free_rate()
        assert rf == 0.045

    def test_risk_free_rate_fetch(self):
        """Test fetching risk-free rate from market"""
        calc = WACCCalculator(
            ticker="AAPL",
            debt=100000,
            equity=2500000,
            tax_rate=0.21
        )

        rf = calc.get_risk_free_rate()

        # Should be a reasonable rate (0-10%)
        assert 0 <= rf <= 0.10
        assert isinstance(rf, float)

    def test_beta_fetch(self):
        """Test fetching beta from yfinance for AAPL"""
        calc = WACCCalculator(
            ticker="AAPL",
            debt=100000,
            equity=2500000,
            tax_rate=0.21
        )

        beta = calc.get_beta()

        # AAPL beta should be positive and reasonable (0.5-2.0)
        assert 0.5 <= beta <= 2.0
        assert isinstance(beta, float)

    def test_beta_invalid_ticker(self):
        """Test beta defaults to 1.0 for invalid ticker"""
        calc = WACCCalculator(
            ticker="INVALIDTICKER12345",
            debt=100000,
            equity=2500000,
            tax_rate=0.21
        )

        beta = calc.get_beta()

        # Should default to market beta of 1.0
        assert beta == 1.0

    def test_cost_of_equity_calculation(self):
        """Test CAPM cost of equity calculation"""
        calc = WACCCalculator(
            ticker="AAPL",
            debt=100000,
            equity=2500000,
            tax_rate=0.21,
            risk_free_rate=0.04  # 4%
        )

        # Set beta manually for testing
        calc._beta = 1.2

        re = calc.calculate_cost_of_equity()

        # Re = 0.04 + 1.2 × 0.06 = 0.04 + 0.072 = 0.112 = 11.2%
        expected_re = 0.04 + (1.2 * 0.06)
        assert abs(re - expected_re) < 0.0001

    def test_cost_of_debt_calculation(self):
        """Test after-tax cost of debt calculation"""
        calc = WACCCalculator(
            ticker="AAPL",
            debt=100000,
            equity=2500000,
            tax_rate=0.21
        )

        # Interest expense = $5,000M
        interest_expense = 5000

        rd = calc.calculate_cost_of_debt(interest_expense)

        # Rd = (5000 / 100000) × (1 - 0.21) = 0.05 × 0.79 = 0.0395 = 3.95%
        expected_rd = (5000 / 100000) * (1 - 0.21)
        assert abs(rd - expected_rd) < 0.0001

    def test_cost_of_debt_zero_debt(self):
        """Test cost of debt when debt is zero"""
        calc = WACCCalculator(
            ticker="AAPL",
            debt=0,
            equity=2500000,
            tax_rate=0.21
        )

        rd = calc.calculate_cost_of_debt(0)
        assert rd == 0.0

    def test_cost_of_debt_negative_interest(self):
        """Test that negative interest expense raises ValueError"""
        calc = WACCCalculator(
            ticker="AAPL",
            debt=100000,
            equity=2500000,
            tax_rate=0.21
        )

        with pytest.raises(ValueError, match="Interest expense cannot be negative"):
            calc.calculate_cost_of_debt(-1000)

    def test_wacc_calculation_manual_inputs(self):
        """Test full WACC calculation with manual inputs"""
        calc = WACCCalculator(
            ticker="AAPL",
            debt=100000,  # $100B
            equity=2500000,  # $2.5T
            tax_rate=0.21,
            risk_free_rate=0.04
        )

        # Set beta manually
        calc._beta = 1.2

        # Interest expense = $5B
        interest_expense = 5000

        result = calc.calculate_wacc(interest_expense)

        # Verify all components are returned
        assert 'wacc' in result
        assert 'cost_of_equity' in result
        assert 'cost_of_debt' in result
        assert 'weight_equity' in result
        assert 'weight_debt' in result
        assert 'risk_free_rate' in result
        assert 'beta' in result
        assert 'market_risk_premium' in result
        assert 'tax_rate' in result

        # Verify weights sum to 1
        assert abs(result['weight_equity'] + result['weight_debt'] - 1.0) < 0.0001

        # Calculate expected WACC manually
        # E = 2,500,000, D = 100,000, V = 2,600,000
        # Weight_E = 2,500,000 / 2,600,000 = 0.9615
        # Weight_D = 100,000 / 2,600,000 = 0.0385
        # Re = 0.04 + 1.2 × 0.06 = 0.112
        # Rd = (5000/100000) × (1-0.21) = 0.0395
        # WACC = 0.9615 × 0.112 + 0.0385 × 0.0395 = 0.1077 + 0.0015 = 0.1092

        expected_wacc = (2500000/2600000) * 0.112 + (100000/2600000) * 0.0395
        assert abs(result['wacc'] - expected_wacc) < 0.001

    def test_wacc_100_percent_equity(self):
        """Test WACC with 100% equity financing (no debt)"""
        calc = WACCCalculator(
            ticker="AAPL",
            debt=0,
            equity=2500000,
            tax_rate=0.21,
            risk_free_rate=0.04
        )

        calc._beta = 1.0

        result = calc.calculate_wacc(interest_expense=0)

        # WACC should equal cost of equity when no debt
        # Re = 0.04 + 1.0 × 0.06 = 0.10
        expected_wacc = 0.04 + 1.0 * 0.06
        assert abs(result['wacc'] - expected_wacc) < 0.0001
        assert result['weight_debt'] == 0.0
        assert result['weight_equity'] == 1.0

    def test_wacc_real_world_aapl(self):
        """Test WACC calculation with real AAPL data"""
        calc = WACCCalculator(
            ticker="AAPL",
            debt=100000,  # Approximate debt
            equity=2500000,  # Approximate market cap
            tax_rate=0.21
        )

        result = calc.calculate_wacc(interest_expense=3000)

        # AAPL WACC should be in reasonable range (7-12%)
        assert 0.07 <= result['wacc'] <= 0.12
        assert result['beta'] > 0
        assert result['risk_free_rate'] > 0

    def test_validate_wacc_in_range(self):
        """Test validation passes for WACC in normal range"""
        calc = WACCCalculator(
            ticker="AAPL",
            debt=100000,
            equity=2500000,
            tax_rate=0.21
        )

        # Normal WACC
        is_valid = calc.validate(0.10)
        assert is_valid is True

    def test_validate_wacc_too_low(self):
        """Test validation warns for WACC below 5%"""
        calc = WACCCalculator(
            ticker="AAPL",
            debt=100000,
            equity=2500000,
            tax_rate=0.21
        )

        # WACC too low
        with pytest.warns(UserWarning, match="outside typical range"):
            is_valid = calc.validate(0.02)
            assert is_valid is False

    def test_validate_wacc_too_high(self):
        """Test validation warns for WACC above 25%"""
        calc = WACCCalculator(
            ticker="AAPL",
            debt=100000,
            equity=2500000,
            tax_rate=0.21
        )

        # WACC too high
        with pytest.warns(UserWarning, match="outside typical range"):
            is_valid = calc.validate(0.30)
            assert is_valid is False

    def test_repr(self):
        """Test string representation"""
        calc = WACCCalculator(
            ticker="AAPL",
            debt=100000,
            equity=2500000,
            tax_rate=0.21
        )

        repr_str = repr(calc)
        assert "AAPL" in repr_str
        assert "100,000" in repr_str
        assert "2,500,000" in repr_str
        assert "21" in repr_str
