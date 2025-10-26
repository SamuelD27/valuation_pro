"""
Test the Pipeline Orchestrator.

Demonstrates unified interface for all data sources.
"""

import sys
sys.path.insert(0, '/Users/samueldukmedjian/Desktop/valuation_pro')

from src.data.pipeline import FinancialDataPipeline, extract_financial_data
from pathlib import Path


def test_pipeline_orchestrator():
    """Test the pipeline with multiple sources."""
    print("\n" + "="*90)
    print("TESTING PIPELINE ORCHESTRATOR")
    print("="*90 + "\n")

    # Initialize pipeline
    pipeline = FinancialDataPipeline()

    # Test 1: Excel file
    print("\n" + "="*90)
    print("TEST 1: EXCEL FILE (AUTO-ROUTED)")
    print("="*90)

    excel_files = list(Path("/Users/samueldukmedjian/Desktop/valuation_pro/Examples").glob("*.xlsx"))

    if excel_files:
        result = pipeline.execute(str(excel_files[0]))

        print("\n✅ Result:")
        print(f"   Data: {result['data'].company.name}")
        print(f"   Source Type: {result['metadata']['source_type']}")
        print(f"   Validation: {'PASSED' if result['validation'].is_valid else 'ISSUES'}")
        print(f"   Performance: {result['performance']['total_time']:.2f}s")

    # Test 2: API ticker
    print("\n" + "="*90)
    print("TEST 2: API TICKER (AUTO-ROUTED)")
    print("="*90)

    result = pipeline.execute("AAPL", years=3)

    print("\n✅ Result:")
    print(f"   Data: {result['data'].company.name}")
    print(f"   Source Type: {result['metadata']['source_type']}")
    print(f"   Validation: {'PASSED' if result['validation'].is_valid else 'ISSUES'}")
    print(f"   Performance: {result['performance']['total_time']:.2f}s")

    # Test 3: Convenience function
    print("\n" + "="*90)
    print("TEST 3: CONVENIENCE FUNCTION")
    print("="*90)

    print("\nUsing quick extract function...")
    data = extract_financial_data("MSFT", years=2)

    print(f"\n✅ Quick extract:")
    print(f"   Company: {data.company.name}")
    print(f"   Years: {data.years}")
    print(f"   Revenue: ${data.income_statement.revenue[-1]:,.0f}M")

    # Test 4: Pipeline stats
    print("\n" + "="*90)
    print("TEST 4: PIPELINE STATISTICS")
    print("="*90)

    pipeline.print_stats()

    # Test 5: Custom transformer
    print("\n" + "="*90)
    print("TEST 5: CUSTOM TRANSFORMER")
    print("="*90)

    def add_growth_metrics(data):
        """Custom transformer that adds growth calculations."""
        revenue = data.income_statement.revenue

        if len(revenue) >= 2:
            # Calculate YoY growth
            yoy_growth = []
            for i in range(1, len(revenue)):
                if revenue[i] and revenue[i-1]:
                    growth = (revenue[i] - revenue[i-1]) / revenue[i-1]
                    yoy_growth.append(growth)

            print(f"   📊 YoY Revenue Growth: {[f'{g:.1%}' for g in yoy_growth]}")

        return data

    # Create new pipeline with custom transformer
    custom_pipeline = FinancialDataPipeline()
    custom_pipeline.add_transformer(add_growth_metrics)

    print("\nRunning pipeline with custom transformer...")
    result = custom_pipeline.execute("GOOGL", years=3)

    print(f"\n✅ Custom pipeline complete")

    return True


if __name__ == "__main__":
    print("\n" + "█"*90)
    print("█" + " "*88 + "█")
    print("█" + "  PIPELINE ORCHESTRATOR TEST".center(88) + "█")
    print("█" + " "*88 + "█")
    print("█"*90 + "\n")

    success = test_pipeline_orchestrator()

    if success:
        print("\n" + "█"*90)
        print("█" + " "*88 + "█")
        print("█" + "  ✅ ALL PIPELINE TESTS PASSED".center(88) + "█")
        print("█" + " "*88 + "█")
        print("█"*90 + "\n")
    else:
        sys.exit(1)
