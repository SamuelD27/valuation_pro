"""
Example: Generate LBO Model

Demonstrates how to create an LBO model for leveraged buyout analysis.
"""

from src.tools.lbo_tool import LBOTool
from src.data.comprehensive_extractor import ComprehensiveDataExtractor


def main():
    """Generate example LBO model."""

    # Extract data from comprehensive source
    with ComprehensiveDataExtractor() as extractor:
        ltm = extractor.get_ltm_metrics()

    # Create LBO model
    lbo = LBOTool(
        company_name="AcmeTech Holdings Ltd.",
        sponsor="Apollo Global Management"
    )

    # Transaction data
    transaction_data = {
        'company_name': 'AcmeTech Holdings Ltd.',
        'ltm_revenue': ltm['revenue'],
        'ltm_ebitda': ltm['ebitda'],
    }

    # LBO assumptions
    assumptions = {
        'holding_period': 5,
        'entry_multiple': 8.5,
        'exit_multiple': 8.0,
        'transaction_fees_pct': 0.02,
        'equity_contribution_pct': 0.50,
        'revolver': 0,
        'revolver_rate': 0.055,
        'senior_debt_pct': 0.40,
        'senior_debt_rate': 0.055,
        'senior_amortization_pct': 0.05,
        'subordinated_debt_pct': 0.10,
        'sub_debt_rate': 0.095,
        'revenue_growth': [0.10, 0.10, 0.08, 0.08, 0.06],
        'ebitda_margin': 0.34,
        'da_pct': 0.03,
        'capex_pct': 0.02,
        'nwc_pct': 0.10,
        'tax_rate': 0.25,
    }

    # Generate LBO model
    lbo.generate_lbo_model(
        transaction_data=transaction_data,
        assumptions=assumptions,
        output_file='Examples/LBO_Model_AcmeTech.xlsx'
    )

    print("\n✅ LBO model generated successfully!")
    print("📄 File: Examples/LBO_Model_AcmeTech.xlsx")
    print("\n📊 Model includes:")
    print("   - Cover section")
    print("   - Transaction Summary")
    print("   - Sources & Uses")
    print("   - Assumptions")
    print("   - Operating Model (5-year projections)")
    print("   - Debt Schedule")
    print("   - Cash Flow Waterfall")
    print("   - Returns Analysis")
    print("\n💡 All sections on one sheet for easier navigation!")


if __name__ == "__main__":
    main()
