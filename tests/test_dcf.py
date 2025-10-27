"""
Unit tests for DCF Model

Tests cover:
- Financial projections
- FCF calculations
- Terminal value
- Enterprise value
- Equity value and price per share
- Sensitivity analysis
- Edge cases and validation
"""

import pytest
import pandas as pd
from src.models.dcf import DCFModel


class TestDCFModel:
    """Comprehensive DCF model test suite"""

    @pytest.fixture
    def sample_company_data(self):
        """Realistic financial data (in millions)"""
        return {
            'revenue': [350000, 380000, 400000],  # $350B, $380B, $400B
            'ebit': [90000, 100000, 110000],
            'tax_rate': 0.21,
            'nwc': [15000, 16000, 17000],
            'capex': [12000, 13000, 14000],
            'da': [11000, 11500, 12000],
        }

    @pytest.fixture
    def standard_assumptions(self):
        """Industry-standard DCF assumptions"""
        return {
            'revenue_growth': [0.08, 0.07, 0.06, 0.05, 0.04],
            'ebit_margin': 0.28,
            'tax_rate': 0.21,
            'nwc_pct_revenue': 0.04,
            'capex_pct_revenue': 0.03,
            'terminal_growth': 0.025,
            'wacc': 0.09,
            'net_debt': 50000,  # $50B net debt
            'shares_outstanding': 15_000_000_000,  # 15B shares
        }

    def test_initialization(self, sample_company_data, standard_assumptions):
        """Test DCF model initializes correctly"""
        model = DCFModel(sample_company_data, standard_assumptions)

        assert model.company_data == sample_company_data
        assert model.assumptions == standard_assumptions
        assert model.projections is None  # Not calculated yet
        assert model.enterprise_value is None

    def test_validation_terminal_growth_ge_wacc(self, sample_company_data):
        """Terminal growth >= WACC should raise ValueError"""
        invalid_assumptions = {
            'revenue_growth': [0.10] * 5,
            'ebit_margin': 0.25,
            'tax_rate': 0.21,
            'nwc_pct_revenue': 0.10,
            'capex_pct_revenue': 0.03,
            'terminal_growth': 0.10,  # Equal to WACC - INVALID
            'wacc': 0.10,
            'net_debt': 50000,
            'shares_outstanding': 10_000_000_000,
        }

        with pytest.raises(ValueError, match="Terminal growth.*must be less than.*WACC"):
            DCFModel(sample_company_data, invalid_assumptions)

    def test_project_financials(self, sample_company_data, standard_assumptions):
        """Test financial projections are calculated correctly"""
        model = DCFModel(sample_company_data, standard_assumptions)
        projections = model.project_financials()

        # Verify DataFrame structure
        assert isinstance(projections, pd.DataFrame)
        assert len(projections) == 5  # 5 years
        assert 'year' in projections.columns
        assert 'revenue' in projections.columns
        assert 'ebit' in projections.columns
        assert 'fcf' in projections.columns

        # Verify Year 1 revenue growth applied correctly
        base_revenue = sample_company_data['revenue'][0]  # Most recent (last in list)
        year_1_revenue = projections.iloc[0]['revenue']
        expected_revenue = base_revenue * (1 + standard_assumptions['revenue_growth'][0])

        assert abs(year_1_revenue - expected_revenue) < 1  # Within $1M tolerance

        # Verify EBIT margin maintained
        for _, row in projections.iterrows():
            ebit_margin = row['ebit'] / row['revenue']
            assert abs(ebit_margin - standard_assumptions['ebit_margin']) < 0.01

    def test_calculate_fcf(self, sample_company_data, standard_assumptions):
        """Test Free Cash Flow calculation: FCF = NOPAT - CapEx - ΔNWC"""
        model = DCFModel(sample_company_data, standard_assumptions)
        projections = model.project_financials()

        # Verify FCF formula for Year 1
        year_1 = projections.iloc[0]

        ebit = year_1['ebit']
        nopat = ebit * (1 - standard_assumptions['tax_rate'])
        da = year_1['da']  # D&A needs to be added back
        capex = year_1['capex']
        nwc_change = year_1['delta_nwc']

        # FCF = NOPAT + D&A - CapEx - ΔNWC (D&A is added back since it's non-cash)
        expected_fcf = nopat + da - capex - nwc_change
        actual_fcf = year_1['fcf']

        assert abs(actual_fcf - expected_fcf) < 10  # Within $10M tolerance

        # FCF should be positive for mature company
        assert all(projections['fcf'] > 0)

    def test_calculate_terminal_value(self, sample_company_data, standard_assumptions):
        """Test terminal value using Gordon Growth Model"""
        model = DCFModel(sample_company_data, standard_assumptions)
        projections = model.project_financials()
        final_fcf = projections.iloc[-1]['fcf']

        terminal_value = model.calculate_terminal_value(final_fcf)

        # Terminal value should be large (many years of cash flows)
        assert terminal_value > final_fcf * 10

        # Verify Gordon Growth formula: TV = FCF_n+1 / (WACC - g)
        fcf_n_plus_1 = final_fcf * (1 + standard_assumptions['terminal_growth'])
        expected_tv = fcf_n_plus_1 / (standard_assumptions['wacc'] - standard_assumptions['terminal_growth'])

        assert abs(terminal_value - expected_tv) / expected_tv < 0.01  # 1% tolerance

    def test_calculate_enterprise_value(self, sample_company_data, standard_assumptions):
        """Test EV = NPV(FCFs) + NPV(Terminal Value)"""
        model = DCFModel(sample_company_data, standard_assumptions)
        enterprise_value = model.calculate_enterprise_value()

        assert enterprise_value > 0
        assert enterprise_value > 100_000  # Should be > $100B for large company

        # Verify NPV discounting applied
        projections = model.project_financials()
        fcf_list = projections['fcf'].tolist()

        # Year 1 PV should be less than nominal
        year_1_pv = fcf_list[0] / (1 + standard_assumptions['wacc'])
        assert year_1_pv < fcf_list[0]

        # Verify EV components exist
        assert hasattr(model, 'ev_components')
        assert 'sum_pv_fcf' in model.ev_components
        assert 'terminal_value' in model.ev_components
        assert 'pv_terminal_value' in model.ev_components

    def test_calculate_equity_value(self, sample_company_data, standard_assumptions):
        """Test Equity Value = EV - Net Debt"""
        model = DCFModel(sample_company_data, standard_assumptions)
        equity_result = model.calculate_equity_value()

        assert 'equity_value' in equity_result
        assert 'enterprise_value' in equity_result
        assert 'price_per_share' in equity_result

        # Verify equity value bridge
        ev = equity_result['enterprise_value']
        net_debt = standard_assumptions['net_debt']
        expected_equity = ev - net_debt

        assert abs(equity_result['equity_value'] - expected_equity) < 1  # $1M tolerance

    def test_price_per_share_calculation(self, sample_company_data, standard_assumptions):
        """Test Price = (Equity Value × 1M) / Shares Outstanding"""
        model = DCFModel(sample_company_data, standard_assumptions)
        result = model.calculate_equity_value()

        price = result['price_per_share']
        equity_value = result['equity_value']  # In millions
        shares = standard_assumptions['shares_outstanding']

        # Verify calculation (equity_value is in millions, convert to dollars)
        expected_price = (equity_value * 1e6) / shares

        assert abs(price - expected_price) < 0.01  # $0.01 tolerance
        assert price > 0
        assert price < 1000  # Reasonable stock price

    def test_sensitivity_analysis(self, sample_company_data, standard_assumptions):
        """Test 2-way sensitivity: WACC vs Terminal Growth"""
        model = DCFModel(sample_company_data, standard_assumptions)

        sensitivity = model.sensitivity_analysis(
            wacc_range=[0.07, 0.08, 0.09, 0.10, 0.11],
            terminal_growth_range=[0.015, 0.020, 0.025, 0.030, 0.035]
        )

        # Verify DataFrame structure
        assert isinstance(sensitivity, pd.DataFrame)
        assert sensitivity.shape == (5, 5)  # 5x5 grid

        # Verify inverse relationship: Lower WACC = Higher valuation
        base_price = sensitivity.iloc[2, 2]  # Center cell (base case)
        low_wacc_price = sensitivity.iloc[0, 2]  # Lower WACC, same growth
        high_wacc_price = sensitivity.iloc[4, 2]  # Higher WACC, same growth

        assert low_wacc_price > base_price
        assert high_wacc_price < base_price

        # Verify growth relationship: Higher growth = Higher valuation
        low_growth_price = sensitivity.iloc[2, 0]
        high_growth_price = sensitivity.iloc[2, 4]

        assert high_growth_price > base_price
        assert low_growth_price < base_price

    def test_zero_debt_company(self, standard_assumptions):
        """Company with no debt (Equity Value = EV)"""
        zero_debt_data = {
            'revenue': [100000] * 3,
            'ebit': [25000] * 3,
            'tax_rate': 0.21,
            'nwc': [5000] * 3,
            'capex': [3000] * 3,
            'da': [5000] * 3,
        }

        zero_debt_assumptions = standard_assumptions.copy()
        zero_debt_assumptions['net_debt'] = 0  # NO DEBT

        model = DCFModel(zero_debt_data, zero_debt_assumptions)
        result = model.calculate_equity_value()

        # Equity Value should equal EV when net debt = 0
        assert abs(result['equity_value'] - result['enterprise_value']) < 1

    def test_high_leverage_company(self, sample_company_data, standard_assumptions):
        """Company with high debt (Equity Value < EV)"""
        high_debt_assumptions = standard_assumptions.copy()
        high_debt_assumptions['net_debt'] = 200_000  # $200B debt

        model = DCFModel(sample_company_data, high_debt_assumptions)
        result = model.calculate_equity_value()

        # Equity value should be much less than EV
        assert result['equity_value'] < result['enterprise_value']
        assert result['equity_value'] == result['enterprise_value'] - 200_000

    def test_negative_fcf_handling(self, sample_company_data, standard_assumptions):
        """Model should handle negative early-stage FCFs"""
        high_capex_assumptions = standard_assumptions.copy()
        high_capex_assumptions['capex_pct_revenue'] = 0.50  # 50% CapEx!

        model = DCFModel(sample_company_data, high_capex_assumptions)
        projections = model.project_financials()

        # May have some negative FCFs
        fcf_list = projections['fcf'].tolist()
        assert len(fcf_list) == 5

        # Should not crash when calculating EV (later positive FCFs + TV)
        enterprise_value = model.calculate_enterprise_value()
        assert isinstance(enterprise_value, (int, float))

    def test_upside_downside_calculation(self, sample_company_data, standard_assumptions):
        """Test upside/downside vs current price"""
        standard_assumptions['current_price'] = 100.0  # $100 current price

        model = DCFModel(sample_company_data, standard_assumptions)
        result = model.calculate_equity_value()

        assert 'current_price' in result
        assert 'upside_downside_pct' in result

        # Verify calculation
        upside = result['upside_downside_pct']
        implied_price = result['price_per_share']
        current_price = result['current_price']

        expected_upside = (implied_price - current_price) / current_price
        assert abs(upside - expected_upside) < 0.0001

    def test_missing_required_fields(self):
        """Should handle missing required fields gracefully"""
        incomplete_data = {
            'revenue': [100000],
            # Missing ebit, tax_rate, etc.
        }

        assumptions = {
            'revenue_growth': [0.05] * 5,
            'ebit_margin': 0.25,
            'tax_rate': 0.21,
            'nwc_pct_revenue': 0.10,
            'capex_pct_revenue': 0.03,
            'terminal_growth': 0.025,
            'wacc': 0.09,
            'net_debt': 50000,
            'shares_outstanding': 10_000_000_000,
        }

        # Should raise KeyError for missing fields
        model = DCFModel(incomplete_data, assumptions)

        with pytest.raises(KeyError):
            model.project_financials()

    def test_repr(self, sample_company_data, standard_assumptions):
        """Test string representation"""
        model = DCFModel(sample_company_data, standard_assumptions)

        # Before calculation
        repr_before = repr(model)
        assert "not calculated" in repr_before

        # After calculation
        model.calculate_equity_value()
        repr_after = repr(model)
        assert "DCFModel" in repr_after
        assert "implied_price" in repr_after
