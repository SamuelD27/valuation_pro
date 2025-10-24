"""
Example: Complete DCF Valuation for Apple Inc. (AAPL)

This script demonstrates the full ValuationPro workflow:
1. Fetch financial data using DataFetcher
2. Calculate WACC using WACCCalculator
3. Run DCF model with projections
4. Generate investment banking-quality Excel output

Run this script to see the system in action!
"""

from src.models.wacc import WACCCalculator
from src.models.dcf import DCFModel
from src.data.fetcher import DataFetcher
from src.excel.three_statement_generator import ThreeStatementGenerator


def run_aapl_dcf():
    """Run complete DCF valuation for Apple Inc."""

    print("=" * 80)
    print("ValuationPro - DCF Valuation Example")
    print("Company: Apple Inc. (AAPL)")
    print("=" * 80)
    print()

    # Step 1: Fetch Financial Data
    print("Step 1: Fetching financial data from yfinance...")
    fetcher = DataFetcher()

    try:
        financials = fetcher.get_financial_statements("AAPL")
        market_data = fetcher.get_market_data("AAPL")
        print("  ✓ Financial data fetched successfully")
    except Exception as e:
        print(f"  ✗ Error fetching data: {e}")
        print("\nUsing example data instead...")

        # Fallback to example data
        financials = {
            'income_statement': {
                'revenue': [394328000000, 383285000000, 365817000000, 274515000000, 260174000000],
                'ebit': [119437000000, 114301000000, 108949000000, 76311000000, 71230000000],
            },
            'balance_sheet': {
                'nwc': [10000000000, 9500000000, 9000000000, 8500000000, 8000000000],
                'total_debt': [111088000000, 120069000000, 112436000000, 108047000000, 93735000000],
                'cash': [61555000000, 48304000000, 51224000000, 38016000000, 25913000000],
            },
            'cash_flow': {
                'capex': [-10959000000, -10708000000, -11085000000, -7309000000, -13313000000],
                'depreciation': [11519000000, 11104000000, 11284000000, 12547000000, 10903000000],
            }
        }

        market_data = {
            'current_price': 175.0,
            'market_cap': 2700000000000,  # $2.7T
            'shares_outstanding': 15400000000,  # 15.4B shares
            'beta': 1.2,
        }

    print(f"  Current Price: ${market_data.get('current_price', 'N/A')}")
    print(f"  Market Cap: ${market_data.get('market_cap', 0) / 1e9:.1f}B")
    print()

    # Step 2: Calculate WACC
    print("Step 2: Calculating WACC...")

    # Extract debt and equity values
    debt = financials['balance_sheet']['total_debt'][0] / 1e6  # Convert to millions
    equity = market_data['market_cap'] / 1e6  # Convert to millions
    tax_rate = 0.21  # U.S. corporate tax rate

    wacc_calc = WACCCalculator(
        ticker="AAPL",
        debt=debt,
        equity=equity,
        tax_rate=tax_rate
    )

    wacc_results = wacc_calc.calculate_wacc()

    print(f"  WACC: {wacc_results['wacc']:.2%}")
    print(f"  Cost of Equity: {wacc_results['cost_of_equity']:.2%}")
    print(f"  Cost of Debt: {wacc_results['cost_of_debt']:.2%}")
    print(f"  Risk-free Rate: {wacc_results['risk_free_rate']:.2%}")
    print(f"  Beta: {wacc_results['beta']:.2f}")
    print()

    # Step 3: Set up DCF assumptions
    print("Step 3: Setting up DCF assumptions...")

    # Historical data (convert to millions for consistency)
    company_data = {
        'revenue': [x / 1e6 if x else 0 for x in financials['income_statement']['revenue'][:3]],  # Convert to millions
        'ebit': [x / 1e6 if x else 0 for x in financials['income_statement']['ebit'][:3]],
        'tax_rate': tax_rate,
        'nwc': [x / 1e6 if x else 0 for x in financials['balance_sheet']['nwc'][:3]],
        'capex': [abs(x) / 1e6 if x else 0 for x in financials['cash_flow']['capex'][:3]],
        'da': [x / 1e6 if x else 0 for x in financials['cash_flow']['depreciation'][:3]],
    }

    # Projection assumptions
    assumptions = {
        # 5-year revenue growth projection
        'revenue_growth': [0.08, 0.07, 0.06, 0.05, 0.04],

        # Operating assumptions
        'ebit_margin': 0.30,  # Target 30% EBIT margin
        'tax_rate': tax_rate,
        'nwc_pct_revenue': 0.025,  # 2.5% of revenue
        'capex_pct_revenue': 0.03,  # 3% of revenue

        # Valuation assumptions
        'terminal_growth': 0.025,  # 2.5% perpetual growth
        'wacc': wacc_results['wacc'],

        # Capital structure (already in millions from WACC calc)
        'net_debt': debt - (financials['balance_sheet']['cash'][0] / 1e6 if financials['balance_sheet']['cash'][0] else 0),
        'cash': financials['balance_sheet']['cash'][0] / 1e6 if financials['balance_sheet']['cash'][0] else 0,
        'shares_outstanding': market_data['shares_outstanding'],
        'current_price': market_data.get('current_price'),
    }

    print("  Revenue Growth (Y1-Y5):", [f"{g:.1%}" for g in assumptions['revenue_growth']])
    print(f"  EBIT Margin: {assumptions['ebit_margin']:.1%}")
    print(f"  Terminal Growth: {assumptions['terminal_growth']:.1%}")
    print(f"  WACC: {assumptions['wacc']:.2%}")
    print()

    # Step 4: Run DCF Model
    print("Step 4: Running DCF valuation...")

    dcf = DCFModel(company_data, assumptions)

    # Project financials
    projections = dcf.project_financials()
    print("  ✓ Projected 5-year financials")

    # Calculate enterprise value (values are in millions)
    ev = dcf.calculate_enterprise_value()
    print(f"  Enterprise Value: ${ev / 1e3:.1f}B (${ev:,.0f}M)")

    # Calculate equity value and price
    equity_result = dcf.calculate_equity_value()
    print(f"  Equity Value: ${equity_result['equity_value'] / 1e3:.1f}B")
    print(f"  Implied Price per Share: ${equity_result['price_per_share']:.2f}")

    if 'current_price' in equity_result:
        print(f"  Current Price: ${equity_result['current_price']:.2f}")
        print(f"  Upside/(Downside): {equity_result['upside_downside_pct']:.1%}")

    print()

    # Step 5: Sensitivity Analysis
    print("Step 5: Running sensitivity analysis...")
    sensitivity = dcf.sensitivity_analysis()
    print("  ✓ Generated 5x5 sensitivity table (WACC vs Terminal Growth)")
    print()
    print("Sample sensitivity results (Price per Share):")
    print(sensitivity.head())
    print()

    # Step 6: Generate Excel Output
    print("Step 6: Generating Excel output with FORMULAS (not values)...")

    generator = ThreeStatementGenerator(ticker="AAPL")

    output_file = "AAPL_DCF_Valuation.xlsx"

    # Prepare WACC data for generator
    wacc_generator_data = {
        'risk_free_rate': wacc_results['risk_free_rate'],
        'beta': wacc_results['beta'],
        'market_risk_premium': wacc_results['market_risk_premium'],
        'cost_of_debt': wacc_results['cost_of_debt'],
        'market_cap': equity,
        'total_debt': debt,
    }

    generator.generate_full_model(
        company_data=company_data,
        assumptions=assumptions,
        wacc_data=wacc_generator_data,
        filepath=output_file
    )

    print(f"  ✓ Excel file created: {output_file}")
    print()

    # Summary
    print("=" * 80)
    print("VALUATION SUMMARY")
    print("=" * 80)
    print(f"Target Price: ${equity_result['price_per_share']:.2f}")

    if 'upside_downside_pct' in equity_result:
        upside = equity_result['upside_downside_pct']
        if upside > 0:
            print(f"Rating: BUY (Upside: {upside:.1%})")
        elif upside > -0.10:
            print(f"Rating: HOLD (Downside: {upside:.1%})")
        else:
            print(f"Rating: SELL (Downside: {upside:.1%})")

    print()
    print("Key Assumptions:")
    print(f"  - WACC: {assumptions['wacc']:.2%}")
    print(f"  - Terminal Growth: {assumptions['terminal_growth']:.1%}")
    print(f"  - Avg Revenue Growth: {sum(assumptions['revenue_growth'])/len(assumptions['revenue_growth']):.1%}")
    print(f"  - EBIT Margin: {assumptions['ebit_margin']:.1%}")
    print()
    print("=" * 80)


if __name__ == "__main__":
    run_aapl_dcf()
