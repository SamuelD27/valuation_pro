"""
Example: Using the DCF Tool

Demonstrates how to use the focused DCF tool to create
pixel-perfect DCF models with proper IB formatting.
"""

from src.tools.dcf_tool import DCFTool
from src.data.excel_extractor import FinancialStatementExtractor

def run_dcf_tool_example():
    """Run DCF tool example."""

    print("="*80)
    print("DCF TOOL - Pixel-Perfect DCF Model Generator")
    print("="*80)

    # Step 1: Extract historical data from Excel files
    print("\n📊 Step 1: Extracting historical financial data...")

    extractor = FinancialStatementExtractor()

    try:
        is_data = extractor.extract_income_statement('income-statement.xlsx')
        bs_data = extractor.extract_balance_sheet('balance-sheet.xlsx')
        cf_data = extractor.extract_cash_flow_statement('cash-flow-statement.xlsx')
        print("   ✓ Data extracted from Excel files")
    except Exception as e:
        print(f"   ! Using example data: {e}")
        is_data = {
            'years': [2019, 2020],
            'revenue': [157000, 180000],
            'ebit': [45000, 52000],
        }
        bs_data = {
            'years': [2019, 2020],
            'cash': [10000, 11874],
        }

    revenue_val = is_data.get('revenue', {}).get('Total Revenues', [0])[0] if isinstance(is_data.get('revenue'), dict) else is_data.get('revenue', [180000])[0] if is_data.get('revenue') else 180000
    print(f"   Revenue: ${revenue_val:,.0f}")

    # Step 2: Set up DCF assumptions
    print("\n⚙️  Step 2: Setting up DCF assumptions...")

    assumptions = {
        # Revenue growth for 5 projection years
        'revenue_growth': [0.08, 0.07, 0.06, 0.05, 0.04],

        # Operating assumptions
        'ebit_margin': 0.28,          # 28% EBIT margin
        'tax_rate': 0.21,             # 21% tax rate
        'capex_pct_revenue': 0.03,    # 3% CapEx
        'nwc_pct_revenue': 0.02,      # 2% NWC

        # Valuation assumptions
        'wacc': 0.095,                # 9.5% WACC
        'terminal_growth': 0.025,     # 2.5% terminal growth
        'shares_outstanding': 100,     # 100mm shares
        'net_debt': 5000,             # $5B net debt
    }

    print(f"   WACC: {assumptions['wacc']:.1%}")
    print(f"   Terminal Growth: {assumptions['terminal_growth']:.1%}")
    print(f"   Avg Revenue Growth: {sum(assumptions['revenue_growth'])/5:.1%}")

    # Step 3: Create DCF model
    print("\n🔧 Step 3: Generating DCF model...")

    dcf_tool = DCFTool(
        company_name="Example Company Inc.",
        ticker="EXMPL"
    )

    # Historical data for the tool
    # Extract total revenues if dict, else use as list
    total_rev = is_data.get('revenue', {}).get('Total Revenues', [157000, 180000]) if isinstance(is_data.get('revenue'), dict) else [157000, 180000]

    historical_data = {
        'years': is_data.get('years', [2019, 2020]),
        'revenue': total_rev,
        'ebit': [45000, 52000],
    }

    output_file = "DCF_Model_Example.xlsx"

    dcf_tool.generate_dcf_model(
        historical_data=historical_data,
        assumptions=assumptions,
        output_file=output_file
    )

    print(f"\n✅ DCF model created: {output_file}")

    # Summary
    print("\n" + "="*80)
    print("MODEL FEATURES")
    print("="*80)
    print("✓ 6 Sheets: Cover | Assumptions | Historical | Projections | DCF | Sensitivity")
    print("✓ All calculations use FORMULAS (no hardcoded values)")
    print("✓ Proper IB-style table borders and formatting")
    print("✓ Blue cells = inputs (editable)")
    print("✓ Clean, professional layout")
    print("✓ Sensitivity analysis included")
    print("\nOpen the Excel file to see the pixel-perfect DCF model!")
    print("="*80)


if __name__ == "__main__":
    run_dcf_tool_example()
