"""
DCF (Discounted Cash Flow) Model

Comprehensive DCF valuation following investment banking methodology:
1. Project free cash flows (FCF)
2. Calculate terminal value
3. Discount to present value
4. Calculate equity value and price per share
5. Sensitivity analysis

Formula:
    Enterprise Value = Σ(FCF_t / (1+WACC)^t) + Terminal Value / (1+WACC)^n
    Equity Value = EV + Cash - Debt
    Price per Share = Equity Value / Shares Outstanding
"""

import pandas as pd
import numpy as np
import numpy_financial as npf
from typing import Dict, List, Optional
import warnings


class DCFModel:
    """
    Discounted Cash Flow valuation model.

    Calculates enterprise value, equity value, and implied share price
    using projected free cash flows and terminal value.
    """

    def __init__(self, company_data: Dict, assumptions: Dict):
        """
        Initialize DCF Model following Investment Banking standards.

        Args:
            company_data: Historical financial data
                {
                    'revenue': [...],  # Historical 3-5 years (most recent first)
                    'ebit': [...],
                    'tax_rate': float,
                    'nwc': [...],      # Net working capital
                    'capex': [...],
                    'da': [...],       # Depreciation & amortization
                }

            assumptions: Projection assumptions
                {
                    'revenue_growth': [...],     # Growth rates for projection years
                    'ebit_margin': float,        # Target EBIT margin (0.0-1.0)
                    'tax_rate': float,           # Corporate tax rate (0.0-0.5)
                    'nwc_pct_revenue': float,    # NWC as % of revenue (typically 0.10-0.25)
                    'capex_pct_revenue': float,  # CapEx as % of revenue (typically 0.02-0.15)
                    'da_pct_revenue': float,     # D&A as % of revenue (optional, default 0.03)
                    'terminal_growth': float,    # Perpetual growth rate (must be < WACC, typically 0.02-0.03)
                    'wacc': float,               # Weighted avg cost of capital (typically 0.07-0.15)
                    'net_debt': float,           # Current net debt (Debt - Cash) in millions
                    'cash': float,               # Current cash (optional, for display)
                    'shares_outstanding': int,   # Diluted shares outstanding
                    'use_midyear_convention': bool,  # Use mid-year discounting (optional, default True)
                    'current_price': float,      # Current stock price (optional, for upside calc)
                }

        Raises:
            ValueError: If terminal growth >= WACC, tax rate invalid, or other input errors
            UserWarning: If WACC or terminal growth outside typical ranges

        Example:
            >>> company_data = {
            ...     'revenue': [500.0],  # $500M LTM revenue
            ...     'nwc': [50.0],
            ...     'ebit': [100.0],
            ...     'tax_rate': 0.25,
            ... }
            >>> assumptions = {
            ...     'revenue_growth': [0.10, 0.08, 0.06, 0.05, 0.04],  # 5-year projection
            ...     'ebit_margin': 0.20,
            ...     'tax_rate': 0.25,
            ...     'nwc_pct_revenue': 0.10,
            ...     'capex_pct_revenue': 0.03,
            ...     'da_pct_revenue': 0.03,
            ...     'terminal_growth': 0.025,  # 2.5% perpetual growth
            ...     'wacc': 0.09,  # 9% WACC
            ...     'net_debt': 200.0,  # $200M net debt
            ...     'shares_outstanding': 100_000_000,
            ... }
            >>> model = DCFModel(company_data, assumptions)
            >>> result = model.calculate_equity_value()

        Reference:
            Investment Banking Financial Modeling Guide Sections 2.1-2.9
        """
        self.company_data = company_data
        self.assumptions = assumptions

        # Validation
        self._validate_inputs()

        # Store calculated values
        self.projections = None
        self.enterprise_value = None
        self.equity_value_result = None

    def _validate_inputs(self):
        """
        Validate model inputs against investment banking standards.

        Checks:
        - WACC in reasonable range (5-25%)
        - Terminal growth < WACC and in reasonable range (1-4%)
        - Tax rate in valid range (0-50%)
        - All rates are positive
        - Shares outstanding is positive

        Reference: Guide Sections 2.3 (WACC), 2.5 (Tax), 2.6 (Terminal Growth)
        """
        wacc = self.assumptions['wacc']
        terminal_growth = self.assumptions['terminal_growth']
        tax_rate = self.assumptions['tax_rate']
        shares = self.assumptions['shares_outstanding']

        # WACC validation
        if wacc <= 0:
            raise ValueError(f"WACC must be positive: {wacc:.2%}")

        if wacc < 0.05 or wacc > 0.25:
            warnings.warn(
                f"WACC of {wacc:.2%} is outside typical range (5%-25%). "
                f"Please verify this is correct.\n"
                f"Typical ranges per IB standards:\n"
                f"  - Mature companies: 7-10%\n"
                f"  - Growth companies: 9-12%\n"
                f"  - High-risk companies: 12-15%+",
                UserWarning
            )

        # Terminal growth validation
        if terminal_growth >= wacc:
            raise ValueError(
                f"Terminal growth rate ({terminal_growth:.2%}) must be less than "
                f"WACC ({wacc:.2%}). A company cannot grow faster than its cost "
                f"of capital in perpetuity."
            )

        if terminal_growth < 0 or terminal_growth > 0.04:
            warnings.warn(
                f"Terminal growth rate of {terminal_growth:.2%} is outside typical "
                f"range (1%-4%). Conservative assumption is 2-3% (long-term GDP growth).\n"
                f"Terminal growth should not exceed long-term GDP growth + inflation.",
                UserWarning
            )

        # Tax rate validation
        if not 0 <= tax_rate <= 0.5:
            raise ValueError(
                f"Tax rate {tax_rate:.1%} is outside valid range (0%-50%).\n"
                f"US Federal rate: 21%\n"
                f"Typical effective rates: 23-28% (including state/local)"
            )

        # Shares outstanding validation
        if shares <= 0:
            raise ValueError(
                f"Shares outstanding must be positive: {shares:,.0f}"
            )

        # Revenue growth rates validation
        if not self.assumptions['revenue_growth']:
            raise ValueError("Revenue growth rates cannot be empty")

    def project_financials(self) -> pd.DataFrame:
        """
        Project financial statements for forecast period.

        Projects:
        - Revenue (using growth rates)
        - EBIT (using margin assumption)
        - NOPAT (EBIT × (1 - Tax Rate))
        - D&A (Depreciation & Amortization as % of revenue)
        - Net Working Capital
        - CapEx
        - Free Cash Flow (FCFF = NOPAT + D&A - CapEx - ΔNWC)

        Returns:
            DataFrame with projected financials by year
        """
        revenue_growth = self.assumptions['revenue_growth']
        projection_years = len(revenue_growth)

        # Get most recent historical revenue as base
        last_revenue = self.company_data['revenue'][0]

        projections = []

        for year_idx, growth_rate in enumerate(revenue_growth):
            year = year_idx + 1

            # Project revenue
            if year == 1:
                revenue = last_revenue * (1 + growth_rate)
            else:
                revenue = projections[year_idx - 1]['revenue'] * (1 + growth_rate)

            # Project EBIT using target margin
            ebit = revenue * self.assumptions['ebit_margin']

            # Calculate NOPAT (Net Operating Profit After Tax)
            nopat = ebit * (1 - self.assumptions['tax_rate'])

            # Project D&A as % of revenue
            # Typical range: 2-5% for asset-light, 5-10% for asset-heavy
            # Default to 3% if not specified
            da_pct = self.assumptions.get('da_pct_revenue', 0.03)
            da = revenue * da_pct

            # Project Net Working Capital as % of revenue
            nwc = revenue * self.assumptions['nwc_pct_revenue']

            # Calculate change in NWC
            if year == 1:
                # Compare to last historical NWC
                last_nwc = self.company_data['nwc'][0] if self.company_data['nwc'][0] else 0
                delta_nwc = nwc - last_nwc
            else:
                delta_nwc = nwc - projections[year_idx - 1]['nwc']

            # Project CapEx as % of revenue
            capex = revenue * self.assumptions['capex_pct_revenue']

            # Calculate Free Cash Flow
            fcf = self.calculate_fcf({
                'nopat': nopat,
                'da': da,
                'capex': capex,
                'delta_nwc': delta_nwc
            })

            projections.append({
                'year': year,
                'revenue': revenue,
                'revenue_growth': growth_rate,
                'ebit': ebit,
                'ebit_margin': ebit / revenue,
                'nopat': nopat,
                'da': da,
                'da_pct_revenue': da_pct,
                'nwc': nwc,
                'delta_nwc': delta_nwc,
                'capex': capex,
                'fcf': fcf,
            })

        self.projections = pd.DataFrame(projections)
        return self.projections

    def calculate_fcf(self, year_data: Dict) -> float:
        """
        Calculate Free Cash Flow to Firm (FCFF) for a given year.

        FCF = NOPAT + D&A - CapEx - ΔNWC

        Where:
            NOPAT = Net Operating Profit After Tax = EBIT × (1 - Tax Rate)
            D&A = Depreciation & Amortization (non-cash expense, add back)
            CapEx = Capital Expenditures (cash outflow)
            ΔNWC = Change in Net Working Capital (increase = cash outflow)

        Reference: Investment Banking Guide Section 2.2

        Args:
            year_data: Dict with 'nopat', 'da', 'capex', 'delta_nwc'

        Returns:
            Free cash flow to firm

        Note:
            D&A must be added back because it's a non-cash expense that was
            already subtracted from NOPAT. This is the standard FCFF formula
            used in investment banking.
        """
        fcf = year_data['nopat'] + year_data['da'] - year_data['capex'] - year_data['delta_nwc']
        return fcf

    def calculate_terminal_value(self, final_fcf: float) -> float:
        """
        Calculate terminal value using Gordon Growth Model.

        TV = FCF_final × (1 + g) / (WACC - g)

        Where:
            FCF_final = Free cash flow in final projection year
            g = Perpetual growth rate
            WACC = Weighted average cost of capital

        Args:
            final_fcf: Free cash flow in terminal year

        Returns:
            Terminal value
        """
        g = self.assumptions['terminal_growth']
        wacc = self.assumptions['wacc']

        terminal_value = (final_fcf * (1 + g)) / (wacc - g)

        return terminal_value

    def calculate_enterprise_value(self) -> float:
        """
        Calculate enterprise value by discounting FCFs and terminal value.

        End-of-Year Convention:
            EV = Σ(FCF_t / (1 + WACC)^t) + TV / (1 + WACC)^n

        Mid-Year Convention (IB Standard):
            EV = Σ(FCF_t / (1 + WACC)^(t-0.5)) + TV / (1 + WACC)^n

        Mid-year convention assumes cash flows occur throughout the year
        (not on Dec 31), which is more accurate and is the standard in
        investment banking.

        Reference: Guide Section 2.9

        Returns:
            Enterprise value
        """
        if self.projections is None:
            self.project_financials()

        wacc = self.assumptions['wacc']
        fcf_list = self.projections['fcf'].tolist()

        # Check if mid-year convention should be used (default = True per IB standards)
        use_midyear = self.assumptions.get('use_midyear_convention', True)

        # Calculate terminal value
        final_fcf = fcf_list[-1]
        terminal_value = self.calculate_terminal_value(final_fcf)

        # Discount each year's FCF to present value
        pv_fcf = []
        for year, fcf in enumerate(fcf_list, start=1):
            if use_midyear:
                # Mid-year convention: Cash flows occur at midpoint of year
                # Year 1 FCF discounted at 0.5 years, Year 2 at 1.5 years, etc.
                discount_period = year - 0.5
            else:
                # End-of-year convention: Cash flows occur on Dec 31
                discount_period = year

            pv = fcf / ((1 + wacc) ** discount_period)
            pv_fcf.append(pv)

        # Discount terminal value to present value
        # Terminal value is always discounted to end of final projection year
        n = len(fcf_list)
        pv_terminal = terminal_value / ((1 + wacc) ** n)

        # Enterprise Value = Sum of PV of FCFs + PV of Terminal Value
        enterprise_value = sum(pv_fcf) + pv_terminal

        self.enterprise_value = enterprise_value

        # Store components for reference
        self.ev_components = {
            'pv_fcf': pv_fcf,
            'sum_pv_fcf': sum(pv_fcf),
            'terminal_value': terminal_value,
            'pv_terminal_value': pv_terminal,
            'enterprise_value': enterprise_value,
            'use_midyear_convention': use_midyear,
        }

        return enterprise_value

    def calculate_equity_value(self) -> Dict:
        """
        Calculate equity value and implied share price.

        Equity Value = EV + Cash - Debt
        Price per Share = Equity Value / Shares Outstanding

        Also calculates upside/downside % vs current price if available.

        Returns:
            Dictionary with:
                - enterprise_value: Enterprise value
                - equity_value: Equity value
                - price_per_share: Implied share price
                - upside_downside: % upside/downside vs current (if available)
        """
        if self.enterprise_value is None:
            self.calculate_enterprise_value()

        cash = self.assumptions.get('cash', 0)
        net_debt = self.assumptions['net_debt']
        shares = self.assumptions['shares_outstanding']

        # Equity Value = EV - Net Debt (or EV + Cash - Debt)
        # Net Debt = Debt - Cash, so EV - Net Debt = EV - Debt + Cash
        equity_value = self.enterprise_value - net_debt

        # Price per share (equity_value is in millions, convert to dollars)
        price_per_share = (equity_value * 1e6) / shares

        result = {
            'enterprise_value': self.enterprise_value,
            'net_debt': net_debt,
            'equity_value': equity_value,
            'shares_outstanding': shares,
            'price_per_share': price_per_share,
        }

        # Calculate upside/downside if current price provided
        if 'current_price' in self.assumptions:
            current_price = self.assumptions['current_price']
            upside_pct = (price_per_share - current_price) / current_price
            result['current_price'] = current_price
            result['upside_downside_pct'] = upside_pct

        self.equity_value_result = result
        return result

    def sensitivity_analysis(
        self,
        wacc_range: Optional[List[float]] = None,
        terminal_growth_range: Optional[List[float]] = None
    ) -> pd.DataFrame:
        """
        Perform 2-way sensitivity analysis on price per share.

        Creates grid of WACC vs Terminal Growth Rate, calculating
        implied share price for each combination.

        Args:
            wacc_range: List of WACC values to test (default: ±2% around base)
            terminal_growth_range: List of terminal growth rates (default: ±1% around base)

        Returns:
            DataFrame with WACC as rows, terminal growth as columns
        """
        base_wacc = self.assumptions['wacc']
        base_terminal_growth = self.assumptions['terminal_growth']

        # Default ranges if not provided
        if wacc_range is None:
            wacc_range = [
                base_wacc - 0.02,
                base_wacc - 0.01,
                base_wacc,
                base_wacc + 0.01,
                base_wacc + 0.02,
            ]

        if terminal_growth_range is None:
            terminal_growth_range = [
                base_terminal_growth - 0.01,
                base_terminal_growth - 0.005,
                base_terminal_growth,
                base_terminal_growth + 0.005,
                base_terminal_growth + 0.01,
            ]

        # Create sensitivity grid
        sensitivity_grid = []

        for wacc in wacc_range:
            row = []
            for terminal_growth in terminal_growth_range:
                # Skip invalid combinations (terminal growth >= WACC)
                if terminal_growth >= wacc:
                    row.append(None)
                    continue

                # Temporarily modify assumptions
                original_wacc = self.assumptions['wacc']
                original_terminal = self.assumptions['terminal_growth']

                self.assumptions['wacc'] = wacc
                self.assumptions['terminal_growth'] = terminal_growth

                # Recalculate valuation
                self.enterprise_value = None  # Reset cache
                self.calculate_enterprise_value()
                result = self.calculate_equity_value()

                row.append(result['price_per_share'])

                # Restore original assumptions
                self.assumptions['wacc'] = original_wacc
                self.assumptions['terminal_growth'] = original_terminal

            sensitivity_grid.append(row)

        # Restore base case calculations
        self.enterprise_value = None
        self.calculate_enterprise_value()
        self.calculate_equity_value()

        # Create DataFrame
        sensitivity_df = pd.DataFrame(
            sensitivity_grid,
            index=[f"{w:.1%}" for w in wacc_range],
            columns=[f"{tg:.1%}" for tg in terminal_growth_range]
        )

        return sensitivity_df

    def get_summary(self) -> Dict:
        """
        Get complete valuation summary.

        Returns:
            Dictionary with all key metrics and results
        """
        if self.equity_value_result is None:
            self.calculate_equity_value()

        summary = {
            'valuation': self.equity_value_result,
            'assumptions': self.assumptions,
            'ev_components': self.ev_components if hasattr(self, 'ev_components') else None,
        }

        return summary

    def __repr__(self) -> str:
        """String representation of DCF Model."""
        if self.equity_value_result:
            price = self.equity_value_result['price_per_share']
            return f"DCFModel(implied_price=${price:.2f})"
        else:
            return "DCFModel(not calculated)"
