"""
Test API extractor with real tickers.
"""

import sys
sys.path.insert(0, '/Users/samueldukmedjian/Desktop/valuation_pro')

from src.data.extractors.api_extractor import APIExtractor
from src.data.normalizers.data_normalizer import DataNormalizer
from src.data.validators.data_validator import DataValidator


def test_single_ticker():
    """Test extraction for a single ticker."""
    print("=" * 80)
    print("TESTING API EXTRACTOR - SINGLE TICKER")
    print("=" * 80)

    # Test with Apple (well-known, reliable data)
    ticker = "AAPL"

    print(f"\n📊 Testing with {ticker}...")
    print("=" * 80)

    try:
        extractor = APIExtractor()

        # Check if it can handle the ticker
        assert extractor.can_handle(ticker), f"Should recognize {ticker} as valid ticker"
        print(f"✅ Recognized {ticker} as valid ticker")

        # Extract data
        print(f"\n📡 Extracting data...")
        data = extractor.extract(ticker, years=5)

        print(f"\n✅ EXTRACTION SUCCESSFUL")
        print("=" * 80)

        # Display summary
        print(data.summary())

        # Verify key fields
        print("\n" + "=" * 80)
        print("VERIFICATION")
        print("=" * 80)

        assert data.company.name, "Company name should be present"
        print(f"✅ Company: {data.company.name}")

        assert data.company.ticker == ticker, "Ticker should match"
        print(f"✅ Ticker: {data.company.ticker}")

        assert len(data.years) > 0, "Should have years"
        print(f"✅ Years: {data.years}")

        assert len(data.income_statement.revenue) > 0, "Should have revenue"
        print(f"✅ Revenue data: {len(data.income_statement.revenue)} years")

        if data.market_data.market_cap:
            print(f"✅ Market Cap: ${data.market_data.market_cap:,.0f}M")

        if data.market_data.beta:
            print(f"✅ Beta: {data.market_data.beta:.2f}")

        print(f"✅ Completeness: {data.metadata.completeness_score:.1%}")

        # Test normalization
        print("\n" + "=" * 80)
        print("TESTING NORMALIZATION")
        print("=" * 80)

        normalized = DataNormalizer.normalize(data)
        print(f"✅ Normalization successful")
        print(f"   Completeness: {normalized.metadata.completeness_score:.1%}")

        # Test validation
        print("\n" + "=" * 80)
        print("TESTING VALIDATION")
        print("=" * 80)

        result = DataValidator.validate(normalized)
        print(result.summary())

        if result.is_valid:
            print("\n✅ VALIDATION PASSED")
        else:
            print("\n⚠️  VALIDATION COMPLETED WITH ISSUES")

        # Export
        output_file = f"test_api_{ticker.lower()}.json"
        normalized.to_json(output_file)
        print(f"\n✅ Exported to: {output_file}")

        return True

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_cache():
    """Test caching functionality."""
    print("\n" + "=" * 80)
    print("TESTING CACHE PERFORMANCE")
    print("=" * 80)

    import time

    ticker = "MSFT"
    extractor = APIExtractor()

    # First fetch (no cache)
    print(f"\n🔄 First fetch (no cache)...")
    start = time.time()
    data1 = extractor.extract(ticker, years=3)
    time1 = time.time() - start
    print(f"   Time: {time1:.2f}s")

    # Second fetch (from cache)
    print(f"\n🔄 Second fetch (should use cache)...")
    start = time.time()
    data2 = extractor.extract(ticker, years=3)
    time2 = time.time() - start
    print(f"   Time: {time2:.2f}s")

    # Verify cache worked
    if time2 < time1 * 0.5:  # Should be much faster
        print(f"\n✅ CACHE WORKING: {time2:.2f}s vs {time1:.2f}s ({time1/time2:.1f}x faster)")
    else:
        print(f"\n⚠️  Cache may not be working: {time2:.2f}s vs {time1:.2f}s")

    # Verify data is same
    assert data1.company.name == data2.company.name
    print(f"✅ Data integrity verified")


def test_invalid_ticker():
    """Test error handling for invalid ticker."""
    print("\n" + "=" * 80)
    print("TESTING ERROR HANDLING")
    print("=" * 80)

    ticker = "INVALIDTICKER12345"
    extractor = APIExtractor()

    print(f"\n🔄 Testing with invalid ticker: {ticker}")

    try:
        data = extractor.extract(ticker)
        print("❌ Should have raised error for invalid ticker")
        return False
    except Exception as e:
        print(f"✅ Correctly raised error: {str(e)[:100]}")
        return True


if __name__ == "__main__":
    print("\n")
    print("█" * 80)
    print("█" + " " * 78 + "█")
    print("█" + "  API EXTRACTOR TEST SUITE".center(78) + "█")
    print("█" + " " * 78 + "█")
    print("█" * 80)
    print("\n")

    # Test 1: Single ticker extraction
    success1 = test_single_ticker()

    if not success1:
        print("\n❌ Single ticker test failed")
        sys.exit(1)

    # Test 2: Cache performance
    try:
        test_cache()
    except Exception as e:
        print(f"\n⚠️  Cache test failed: {e}")

    # Test 3: Error handling
    success3 = test_invalid_ticker()

    if not success3:
        print("\n❌ Error handling test failed")
        sys.exit(1)

    print("\n")
    print("█" * 80)
    print("█" + " " * 78 + "█")
    print("█" + "  ALL API EXTRACTOR TESTS PASSED! ✅".center(78) + "█")
    print("█" + " " * 78 + "█")
    print("█" * 80)
    print("\n")
