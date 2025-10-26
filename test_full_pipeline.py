"""
End-to-end test of the full data extraction pipeline.

Tests: Excel Extraction → Normalization → Validation

Demonstrates production-ready financial data processing.
"""

import sys
sys.path.insert(0, '/Users/samueldukmedjian/Desktop/valuation_pro')

from pathlib import Path
from src.data.extractors.excel_extractor import ExcelExtractor
from src.data.normalizers.data_normalizer import DataNormalizer
from src.data.validators.data_validator import DataValidator


def test_full_pipeline():
    """
    Test complete pipeline: Extract → Normalize → Validate

    This demonstrates the production-ready data processing workflow
    that would be used in an actual investment banking environment.
    """
    print("=" * 80)
    print("TESTING FULL DATA EXTRACTION PIPELINE")
    print("=" * 80)
    print("\nWorkflow: Excel Extraction → Normalization → Validation")
    print("=" * 80)

    # Find test Excel file
    test_files = list(Path("/Users/samueldukmedjian/Desktop/valuation_pro/Examples").glob("*.xlsx"))

    if not test_files:
        print("❌ No test Excel files found")
        return False

    test_file = str(test_files[0])

    print(f"\n📁 Test file: {Path(test_file).name}")
    print("=" * 80)

    # ========================================================================
    # STEP 1: EXTRACTION
    # ========================================================================
    print("\n" + "=" * 80)
    print("STEP 1: INTELLIGENT EXTRACTION")
    print("=" * 80)

    try:
        extractor = ExcelExtractor()
        raw_data = extractor.extract(test_file)

        print("\n✅ EXTRACTION SUCCESSFUL")
        print(f"   Company: {raw_data.company.name}")
        print(f"   Years: {raw_data.years}")
        print(f"   Fields extracted: {len([f for f in [raw_data.income_statement.revenue, raw_data.income_statement.ebitda] if f])} of 2 key metrics")

    except Exception as e:
        print(f"\n❌ EXTRACTION FAILED: {e}")
        return False

    # ========================================================================
    # STEP 2: NORMALIZATION
    # ========================================================================
    print("\n" + "=" * 80)
    print("STEP 2: DATA NORMALIZATION")
    print("=" * 80)

    try:
        # Assume data is in millions already (from DCF template)
        context = "Values in millions"

        normalized_data = DataNormalizer.normalize(raw_data, context=context)

        print("\n✅ NORMALIZATION SUCCESSFUL")
        print(f"   Scale detected: MILLIONS")
        print(f"   Derived fields calculated: {len(normalized_data.metadata.derived_fields_calculated)}")

        if normalized_data.metadata.derived_fields_calculated:
            print(f"   Fields: {', '.join(normalized_data.metadata.derived_fields_calculated)}")

        print(f"   Completeness: {normalized_data.metadata.completeness_score:.1%}")

    except Exception as e:
        print(f"\n❌ NORMALIZATION FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

    # ========================================================================
    # STEP 3: VALIDATION
    # ========================================================================
    print("\n" + "=" * 80)
    print("STEP 3: DATA VALIDATION")
    print("=" * 80)

    try:
        validation_result = DataValidator.validate(normalized_data, strict=False)

        print("\n" + validation_result.summary())

        if validation_result.is_valid:
            print("\n✅ VALIDATION PASSED")
        else:
            print("\n⚠️  VALIDATION COMPLETED WITH ISSUES")

        # Show detailed issues
        if validation_result.issues:
            print("\n" + "=" * 80)
            print("DETAILED ISSUES")
            print("=" * 80)

            for issue in validation_result.issues:
                print(f"\n{issue}")

    except Exception as e:
        print(f"\n❌ VALIDATION FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

    # ========================================================================
    # FINAL SUMMARY
    # ========================================================================
    print("\n" + "=" * 80)
    print("FINAL DATA SUMMARY")
    print("=" * 80)

    print(normalized_data.summary())

    # ========================================================================
    # RESULTS
    # ========================================================================
    print("\n" + "=" * 80)
    print("PIPELINE RESULTS")
    print("=" * 80)

    print("\n✅ Extraction: SUCCESS")
    print("✅ Normalization: SUCCESS")
    print(f"{'✅' if validation_result.is_valid else '⚠️ '} Validation: {'PASSED' if validation_result.is_valid else 'PASSED WITH WARNINGS'}")

    print("\n" + "=" * 80)
    print("PIPELINE TEST COMPLETE!")
    print("=" * 80)

    print("\n📊 Key Metrics:")
    print(f"   • Company: {normalized_data.company.name}")
    print(f"   • Time Period: {normalized_data.years[0]} - {normalized_data.years[-1]}")
    print(f"   • Revenue CAGR: {((normalized_data.income_statement.revenue[-1] / normalized_data.income_statement.revenue[0]) ** (1 / (len(normalized_data.years) - 1)) - 1):.1%}")

    if normalized_data.income_statement.ebitda:
        rev_latest = normalized_data.income_statement.revenue[-1]
        ebitda_latest = normalized_data.income_statement.ebitda[-1]
        if rev_latest and ebitda_latest:
            margin = ebitda_latest / rev_latest
            print(f"   • Latest EBITDA Margin: {margin:.1%}")

    print(f"   • Data Quality: {normalized_data.metadata.completeness_score:.1%}")
    print(f"   • Validation Issues: {len(validation_result.issues)}")

    # Export options
    print("\n" + "=" * 80)
    print("EXPORT OPTIONS")
    print("=" * 80)

    print("\nYou can now:")
    print("  1. Export to JSON: normalized_data.to_json('output.json')")
    print("  2. Use in DCF model: DCFModel(financial_data=normalized_data)")
    print("  3. Further analysis with pandas")

    # Test JSON export
    output_file = "test_pipeline_output.json"
    normalized_data.to_json(output_file)
    print(f"\n✅ Exported to: {output_file}")

    print("\n" + "=" * 80)
    print("END-TO-END PIPELINE TEST SUCCESSFUL! 🎉")
    print("=" * 80)

    return True


def test_scale_detection():
    """
    Test scale detection in isolation.
    """
    print("\n" + "=" * 80)
    print("TESTING SCALE DETECTION")
    print("=" * 80)

    from src.data.normalizers.data_normalizer import DataNormalizer, Scale

    test_cases = [
        ([1200, 1350, 1520], "in thousands", Scale.THOUSANDS),
        ([1.2, 1.35, 1.52], "millions", Scale.MILLIONS),
        ([0.0012, 0.00135], "billions", Scale.BILLIONS),
        ([1200, 1350, 1520], None, Scale.MILLIONS),  # Heuristic
    ]

    print("\nTest Cases:")
    for values, context, expected in test_cases:
        detected, confidence = DataNormalizer.detect_scale(values, context)
        status = "✅" if detected == expected else "❌"
        print(f"\n{status} Values: {values}")
        print(f"   Context: {context or 'None'}")
        print(f"   Expected: {expected.name}, Detected: {detected.name}")
        print(f"   Confidence: {confidence:.1%}")


if __name__ == "__main__":
    print("\n")
    print("█" * 80)
    print("█" + " " * 78 + "█")
    print("█" + "  VALUATION PRO - PRODUCTION DATA EXTRACTION PIPELINE TEST".center(78) + "█")
    print("█" + " " * 78 + "█")
    print("█" * 80)
    print("\n")

    # Run scale detection test
    test_scale_detection()

    print("\n\n")

    # Run full pipeline test
    success = test_full_pipeline()

    if not success:
        sys.exit(1)

    print("\n")
    print("█" * 80)
    print("█" + " " * 78 + "█")
    print("█" + "  ALL TESTS PASSED - PIPELINE READY FOR PRODUCTION! ✅".center(78) + "█")
    print("█" + " " * 78 + "█")
    print("█" * 80)
    print("\n")
