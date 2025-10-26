"""
Example: Create DCF model using intelligent API extraction.

This demonstrates the complete workflow:
1. Extract financial data from yfinance
2. Normalize and validate
3. Build DCF model with intelligent data

No manual data entry required!
"""

import sys
sys.path.insert(0, '/Users/samueldukmedjian/Desktop/valuation_pro')

from src.data.pipeline import FinancialDataPipeline
from src.models.dcf import DCFModel


def create_dcf_from_api(ticker: str, output_file: str = None):
    """
    Create DCF model from API data.

    Args:
        ticker: Stock ticker (e.g., "AAPL")
        output_file: Optional output Excel file name
    """
    print("="*90)
    print(f"CREATING DCF MODEL FROM API DATA: {ticker}")
    print("="*90 + "\n")

    # Step 1: Extract data using pipeline
    print("STEP 1: INTELLIGENT DATA EXTRACTION")
    print("-"*90)

    pipeline = FinancialDataPipeline()
    result = pipeline.execute(ticker, years=5)

    data = result['data']

    print(f"\n✅ Extraction complete:")
    print(f"   Company: {data.company.name}")
    print(f"   Years: {data.years}")
    print(f"   Data quality: {data.metadata.completeness_score:.1%}")

    # Step 2: Prepare data for DCF model
    print(f"\nSTEP 2: PREPARING DCF INPUTS")
    print("-"*90)

    # Extract historical data
    historical_data = {
        'company_name': data.company.name,
        'ticker': data.company.ticker,
        'years': data.years,
        'revenue': data.income_statement.revenue,
        'ebit': data.income_statement.ebit if data.income_statement.ebit else [],
        'nwc': data.balance_sheet.net_working_capital if data.balance_sheet.net_working_capital else [],
        'tax_rate': 0.21,  # US federal rate (could extract from data)
    }

    # Get latest values for assumptions
    latest_revenue = data.income_statement.revenue[-1] if data.income_statement.revenue else 0

    # Calculate historical growth rate
    if len(data.income_statement.revenue) >= 2:
        first_rev = data.income_statement.revenue[0]
        last_rev = data.income_statement.revenue[-1]
        years_diff = len(data.years) - 1
        cagr = (last_rev / first_rev) ** (1 / years_diff) - 1
    else:
        cagr = 0.10  # Default

    print(f"\n✅ Historical metrics:")
    print(f"   Latest Revenue: ${latest_revenue:,.0f}M")
    print(f"   Revenue CAGR: {cagr:.1%}")

    # Step 3: Set DCF assumptions
    print(f"\nSTEP 3: DCF ASSUMPTIONS")
    print("-"*90)

    # Use intelligent defaults based on extracted data
    assumptions = {
        # Revenue growth (declining from historical CAGR)
        'revenue_growth': [
            min(cagr * 0.9, 0.15),  # Year 1: 90% of historical, max 15%
            min(cagr * 0.8, 0.12),  # Year 2: 80% of historical, max 12%
            min(cagr * 0.7, 0.10),  # Year 3: 70% of historical, max 10%
            min(cagr * 0.6, 0.08),  # Year 4: 60% of historical, max 8%
            min(cagr * 0.5, 0.06),  # Year 5: 50% of historical, max 6%
        ],

        # Operating assumptions
        'ebit_margin': 0.25,  # Conservative estimate
        'tax_rate': 0.21,  # US federal rate
        'nwc_pct_revenue': 0.10,
        'capex_pct_revenue': 0.03,
        'da_pct_revenue': 0.03,

        # Valuation assumptions
        'wacc': 0.09,  # Could use beta from market data
        'terminal_growth': 0.025,  # Long-term GDP growth

        # Market data
        'net_debt': data.market_data.net_debt if data.market_data.net_debt else 0,
        'shares_outstanding': data.market_data.shares_outstanding if data.market_data.shares_outstanding else 1000,

        # Use mid-year convention (IB standard)
        'use_midyear_convention': True,
    }

    print(f"\n   Revenue Growth: {[f'{g:.1%}' for g in assumptions['revenue_growth']]}")
    print(f"   EBIT Margin: {assumptions['ebit_margin']:.1%}")
    print(f"   WACC: {assumptions['wacc']:.1%}")
    print(f"   Terminal Growth: {assumptions['terminal_growth']:.1%}")

    # Step 4: Create DCF model
    print(f"\nSTEP 4: CREATING DCF MODEL")
    print("-"*90)

    model = DCFModel(historical_data, assumptions)

    # Project financials
    projections = model.project_financials()
    print(f"\n✅ Projected 5 years of financials")

    # Calculate valuation
    ev = model.calculate_enterprise_value()
    print(f"   Enterprise Value: ${ev:,.0f}M")

    equity_result = model.calculate_equity_value()
    print(f"   Equity Value: ${equity_result['equity_value']:,.0f}M")
    print(f"   Implied Price: ${equity_result['price_per_share']:.2f}")

    # Current price comparison
    if data.market_data.share_price:
        current_price = data.market_data.share_price
        implied_price = equity_result['price_per_share']
        upside = (implied_price / current_price - 1) * 100

        print(f"\n   Current Price: ${current_price:.2f}")
        print(f"   Implied Upside: {upside:+.1f}%")

    # Step 5: Generate sensitivity analysis
    print(f"\nSTEP 5: SENSITIVITY ANALYSIS")
    print("-"*90)

    sensitivity = model.sensitivity_analysis()
    print("\n" + str(sensitivity))

    # Step 6: Export (optional)
    if output_file:
        print(f"\nSTEP 6: EXPORTING RESULTS")
        print("-"*90)
        # Would export to Excel here
        print(f"   (Excel export not implemented in this example)")
        print(f"   Would export to: {output_file}")

    print("\n" + "="*90)
    print("DCF MODEL COMPLETE!")
    print("="*90)

    return model, data


if __name__ == "__main__":
    # Example: Apple Inc.
    ticker = "AAPL"

    model, data = create_dcf_from_api(ticker)

    print(f"\n{'='*90}")
    print("SUMMARY")
    print(f"{'='*90}")
    print(f"\n{data.company.name} ({ticker})")
    print(f"Current Market Cap: ${data.market_data.market_cap:,.0f}M")
    print(f"DCF Enterprise Value: ${model.enterprise_value:,.0f}M")
    print(f"\n✅ Complete DCF model created from API data with zero manual input!")
    print(f"{'='*90}\n")
