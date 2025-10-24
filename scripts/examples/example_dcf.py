"""
Example: Generate DCF Model

Demonstrates how to create a DCF model for valuation analysis.
"""

from src.tools.dcf_tool import DCFTool
from src.data.comprehensive_extractor import ComprehensiveDataExtractor


def main():
    """Generate example DCF model."""

    # Extract data from comprehensive source
    with ComprehensiveDataExtractor() as extractor:
        ltm = extractor.get_ltm_metrics()
        historical = extractor.get_historical_data(years=5)

    # Create DCF model
    dcf = DCFTool(
        company_name="AcmeTech Holdings Ltd.",
        ticker="ACME"
    )

    # Historical data
    historical_data = {
        'company_name': 'AcmeTech Holdings Ltd.',
        'fiscal_year_end': 'June 30',
        'currency': 'USD',
        'years': historical['years'],
        'revenue': historical['income_statement']['revenue'],
        'ebitda': historical['income_statement']['ebitda'],
        'net_income': historical['cash_flow']['net_income'],
        'd_and_a': historical['cash_flow']['d_and_a'],
        'capex': historical['cash_flow']['capex'],
        'net_debt': ltm['net_debt'],
        'shares_outstanding': 100,
    }

    # DCF assumptions
    assumptions = {
        'projection_years': 5,
        'revenue_growth_rates': [0.10, 0.10, 0.08, 0.08, 0.06],
        'terminal_growth_rate': 0.025,
        'ebitda_margin': 0.34,
        'tax_rate': 0.25,
        'nwc_pct_revenue': 0.10,
        'capex_pct_revenue': 0.03,
        'd_and_a_pct_revenue': 0.03,
        'wacc': 0.09,
    }

    # Generate DCF model
    dcf.generate_dcf_model(
        historical_data=historical_data,
        assumptions=assumptions,
        output_file='Examples/DCF_Model_AcmeTech.xlsx'
    )

    print("\n✅ DCF model generated successfully!")
    print("📄 File: Examples/DCF_Model_AcmeTech.xlsx")
    print("\n📊 Model includes:")
    print("   - Cover section")
    print("   - Assumptions")
    print("   - Historical Data (5 years)")
    print("   - Financial Projections (5 years)")
    print("   - DCF Valuation")
    print("   - Sensitivity Analysis (simplified)")
    print("\n💡 All sections on one sheet for easier navigation!")


if __name__ == "__main__":
    main()
