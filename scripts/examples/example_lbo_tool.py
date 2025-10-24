"""
Example: Using the LBO Tool

Demonstrates how to use the focused LBO tool to create
pixel-perfect LBO models with proper IB formatting.

Uses Financial_Model_Data_Source.xlsx (AcmeTech Holdings)
"""

from src.tools.lbo_tool import LBOTool
from src.data.comprehensive_extractor import ComprehensiveDataExtractor


def run_lbo_tool_example():
    """Run LBO tool example."""

    print("="*80)
    print("LBO TOOL - Pixel-Perfect LBO Model Generator")
    print("="*80)
    print("Data Source: AcmeTech Holdings Ltd. (Financial_Model_Data_Source.xlsx)")
    print("="*80)

    # Step 1: Extract historical data from comprehensive data source
    print("\n📊 Step 1: Extracting financial data from comprehensive source...")

    with ComprehensiveDataExtractor() as extractor:
        ltm = extractor.get_ltm_metrics()

        ltm_revenue = ltm['revenue']
        ltm_ebitda = ltm['ebitda']

        print("   ✓ Data extracted from Financial_Model_Data_Source.xlsx")
        print(f"   Company: AcmeTech Holdings Ltd.")
        print(f"   Fiscal Year: {ltm['year']}")
        print(f"   LTM Revenue: ${ltm_revenue:,.1f}M")
        print(f"   LTM EBITDA: ${ltm_ebitda:,.1f}M")
        print(f"   LTM EBITDA Margin: {(ltm_ebitda/ltm_revenue)*100:.1f}%")

    # Step 2: Set up transaction data
    print("\n💼 Step 2: Setting up transaction assumptions...")

    transaction_data = {
        'ltm_revenue': ltm_revenue,
        'ltm_ebitda': ltm_ebitda,
        'transaction_date': '2026-01-01',
    }

    # Step 3: Set up LBO assumptions
    print("\n⚙️  Step 3: Setting up LBO assumptions...")

    assumptions = {
        # Transaction assumptions
        'entry_multiple': 8.5,               # 8.5x EBITDA entry multiple
        'exit_multiple': 9.5,                # 9.5x EBITDA exit multiple
        'holding_period': 5,                 # 5-year hold
        'transaction_fees_pct': 0.015,       # 1.5% transaction fees
        'financing_fees_pct': 0.025,         # 2.5% financing fees

        # Sources of funds
        'senior_debt_pct': 0.45,             # 45% senior debt
        'subordinated_debt_pct': 0.15,       # 15% sub debt
        'equity_contribution_pct': 0.40,     # 40% equity

        # Debt assumptions
        'senior_debt_rate': 0.065,           # 6.5% senior rate
        'sub_debt_rate': 0.105,              # 10.5% sub debt rate
        'senior_amortization_pct': 0.06,     # 6% annual amortization

        # Operating assumptions (5-year projections)
        'revenue_growth': [0.08, 0.07, 0.06, 0.06, 0.05],
        'ebitda_margin': 0.34,               # 34% EBITDA margin (actual is 34%)
        'depreciation_pct_revenue': 0.032,   # 3.2% D&A
        'capex_pct_revenue': 0.045,          # 4.5% CapEx
        'nwc_pct_revenue': 0.12,             # 12% NWC
        'tax_rate': 0.25,                    # 25% tax rate
    }

    print(f"   Entry Multiple: {assumptions['entry_multiple']:.1f}x")
    print(f"   Exit Multiple: {assumptions['exit_multiple']:.1f}x")
    print(f"   Holding Period: {assumptions['holding_period']} years")

    print(f"   Senior Debt: {assumptions['senior_debt_pct']:.0%}")
    print(f"   Sub Debt: {assumptions['subordinated_debt_pct']:.0%}")
    print(f"   Equity: {assumptions['equity_contribution_pct']:.0%}")
    print(f"   EBITDA Margin: {assumptions['ebitda_margin']:.0%}")

    # Step 4: Create LBO model
    print("\n🔧 Step 4: Generating LBO model...")

    lbo_tool = LBOTool(
        company_name="AcmeTech Holdings Ltd.",
        sponsor="Private Equity Partners"
    )

    output_file = "Examples/LBO_Model_AcmeTech.xlsx"

    lbo_tool.generate_lbo_model(
        transaction_data=transaction_data,
        assumptions=assumptions,
        output_file=output_file
    )

    print(f"\n✅ LBO model created: {output_file}")

    # Summary
    print("\n" + "="*80)
    print("MODEL FEATURES")
    print("="*80)
    print("✓ 8 Sheets: Cover | Transaction | S&U | Assumptions | Operating | Debt | CF | Returns")
    print("✓ All calculations use FORMULAS (no hardcoded values)")
    print("✓ Proper IB-style table borders and formatting")
    print("✓ Dark blue headers with white text (professional)")
    print("✓ Yellow cells = inputs (editable)")
    print("✓ Sources & Uses table")
    print("✓ Debt schedule with amortization")
    print("✓ Returns analysis (IRR & MOIC)")
    print("\nOpen the Excel file to see the pixel-perfect LBO model!")
    print("="*80)


if __name__ == "__main__":
    run_lbo_tool_example()
