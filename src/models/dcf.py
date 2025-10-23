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
        Initialize DCF Model.

        Args:
            company_data: Historical financial data
                {
                    'revenue': [...],  # Historical 3-5 years
                    'ebit': [...],
                    'tax_rate': float,
                    'nwc': [...],      # Net working capital
                    'capex': [...],
                    'da': [...],       # Depreciation & amortization
                }

            assumptions: Projection assumptions
                {
                    'revenue_growth': [...],  # Growth rates for projection years
                    'ebit_margin': float,     # Target EBIT margin
                    'tax_rate': float,
                    'nwc_pct_revenue': float,
                    'capex_pct_revenue': float,
                    'terminal_growth': float,  # Must be < WACC
                    'wacc': float,
                    'net_debt': float,         # Current net debt
                    'cash': float,             # Current cash
                    'shares_outstanding': int,
                }

        Raises:
            ValueError: If terminal growth >= WACC or other invalid inputs
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
        """Validate model inputs."""
        # Terminal growth must be less than WACC
        if self.assumptions['terminal_growth'] >= self.assumptions['wacc']:
            raise ValueError(
                f"Terminal growth rate ({self.assumptions['terminal_growth']:.2%}) "
                f"must be less than WACC ({self.assumptions['wacc']:.2%})"
            )

        # WACC must be positive
        if self.assumptions['wacc'] <= 0:
            raise ValueError(f"WACC must be positive: {self.assumptions['wacc']}")

        # Shares outstanding must be positive
        if self.assumptions['shares_outstanding'] <= 0:
            raise ValueError(
                f"Shares outstanding must be positive: {self.assumptions['shares_outstanding']}"
            )

        # Revenue growth rates should match projection period
        if not self.assumptions['revenue_growth']:
            raise ValueError("Revenue growth rates cannot be empty")

    def project_financials(self) -> pd.DataFrame:
        """
        Project financial statements for forecast period.

        Projects:
        - Revenue (using growth rates)
        - EBIT (using margin assumption)
        - NOPAT (EBIT × (1 - Tax Rate))
        - Net Working Capital
        - CapEx
        - Free Cash Flow

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
                'nwc': nwc,
                'delta_nwc': delta_nwc,
                'capex': capex,
                'fcf': fcf,
            })

        self.projections = pd.DataFrame(projections)
        return self.projections

    def calculate_fcf(self, year_data: Dict) -> float:
        """
        Calculate Free Cash Flow for a given year.

        FCF = NOPAT - CapEx - ΔNWC

        Where:
            NOPAT = Net Operating Profit After Tax = EBIT × (1 - Tax Rate)
            CapEx = Capital Expenditures
            ΔNWC = Change in Net Working Capital

        Args:
            year_data: Dict with 'nopat', 'capex', 'delta_nwc'

        Returns:
            Free cash flow
        """
        fcf = year_data['nopat'] - year_data['capex'] - year_data['delta_nwc']
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

        EV = Σ(FCF_t / (1 + WACC)^t) + TV / (1 + WACC)^n

        Returns:
            Enterprise value
        """
        if self.projections is None:
            self.project_financials()

        wacc = self.assumptions['wacc']
        fcf_list = self.projections['fcf'].tolist()

        # Calculate terminal value
        final_fcf = fcf_list[-1]
        terminal_value = self.calculate_terminal_value(final_fcf)

        # Discount each year's FCF to present value
        pv_fcf = []
        for year, fcf in enumerate(fcf_list, start=1):
            pv = fcf / ((1 + wacc) ** year)
            pv_fcf.append(pv)

        # Discount terminal value to present value
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
