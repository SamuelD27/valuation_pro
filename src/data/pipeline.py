"""
Main data extraction pipeline orchestrator.

Provides unified interface for extracting financial data from any source,
with automatic source routing, normalization, and validation.

Uses Strategy pattern for flexible source handling.

Example usage:
    >>> pipeline = FinancialDataPipeline()
    >>>
    >>> # Extract from Excel
    >>> result = pipeline.execute("company_financials.xlsx")
    >>>
    >>> # Extract from API
    >>> result = pipeline.execute("AAPL")
    >>>
    >>> # Access clean data
    >>> data = result['data']
    >>> print(data.summary())
"""

from typing import Dict, Any, List, Optional, Callable
from pathlib import Path
import time
from datetime import datetime

from .extractors import BaseExtractor, ExcelExtractor, APIExtractor
from .normalizers.data_normalizer import DataNormalizer
from .validators.data_validator import DataValidator, ValidationResult
from .schema import FinancialData


class FinancialDataPipeline:
    """
    Main orchestrator for financial data extraction pipeline.

    Automatically:
    1. Detects source type (Excel, API, PDF, etc.)
    2. Routes to appropriate extractor
    3. Normalizes data (scale detection, derived fields)
    4. Validates data (outliers, reconciliation, sanity checks)
    5. Returns clean, standardized data

    Features:
    - Automatic source detection
    - Pluggable extractors (Strategy pattern)
    - Configurable transformers and validators
    - Performance tracking
    - Error handling with detailed reporting

    Performance target: <30s per company
    """

    def __init__(self, api_keys: Optional[Dict[str, str]] = None):
        """
        Initialize pipeline with default extractors.

        Args:
            api_keys: Optional API keys for providers
                     {'alpha_vantage': 'key', 'fmp': 'key'}
        """
        # Registered extractors (Strategy pattern)
        self.extractors: List[BaseExtractor] = []

        # Register default extractors
        self._register_default_extractors(api_keys)

        # Pipeline transformers (applied in order)
        self.transformers: List[Callable[[FinancialData], FinancialData]] = []

        # Add default normalizer
        self.add_transformer(self._normalize_data)

        # Validators
        self.validators: List[Callable[[FinancialData], ValidationResult]] = []

        # Add default validator
        self.add_validator(DataValidator.validate)

        # Performance tracking
        self.stats = {
            'total_executions': 0,
            'total_time': 0.0,
            'successful': 0,
            'failed': 0,
            'by_source': {}
        }

    def _register_default_extractors(self, api_keys: Optional[Dict[str, str]]) -> None:
        """Register default extractors in priority order."""
        # Priority 1: Excel (fast, local)
        self.register_extractor(ExcelExtractor())

        # Priority 2: API (real-time data)
        self.register_extractor(APIExtractor(api_keys))

        # Priority 3: PDF (future)
        # self.register_extractor(PDFExtractor())

    def register_extractor(self, extractor: BaseExtractor) -> None:
        """
        Register a new data source extractor.

        Extractors are tried in registration order.

        Args:
            extractor: BaseExtractor implementation

        Example:
            >>> pipeline = FinancialDataPipeline()
            >>> pipeline.register_extractor(CustomExtractor())
        """
        self.extractors.append(extractor)

    def add_transformer(self, transformer: Callable[[FinancialData], FinancialData]) -> None:
        """
        Add a data transformer to the pipeline.

        Transformers are applied in registration order after extraction.

        Args:
            transformer: Function that takes FinancialData and returns FinancialData

        Example:
            >>> def custom_transform(data: FinancialData) -> FinancialData:
            ...     # Apply custom transformation
            ...     return data
            >>>
            >>> pipeline.add_transformer(custom_transform)
        """
        self.transformers.append(transformer)

    def add_validator(self, validator: Callable[[FinancialData], ValidationResult]) -> None:
        """
        Add a validator to the pipeline.

        Args:
            validator: Function that validates FinancialData

        Example:
            >>> def custom_validator(data: FinancialData) -> ValidationResult:
            ...     # Perform custom validation
            ...     return result
            >>>
            >>> pipeline.add_validator(custom_validator)
        """
        self.validators.append(validator)

    def execute(
        self,
        source: Any,
        context: Optional[str] = None,
        strict_validation: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Execute complete extraction pipeline.

        Steps:
        1. Auto-detect source type and route to extractor
        2. Extract raw data
        3. Apply transformers (normalization, etc.)
        4. Run validators
        5. Return results with metadata

        Args:
            source: Data source (file path, ticker, URL, etc.)
            context: Optional context for extraction (e.g., "values in thousands")
            strict_validation: If True, warnings are treated as errors
            **kwargs: Additional arguments passed to extractor

        Returns:
            Dict with:
                - 'data': FinancialData object
                - 'validation': ValidationResult object
                - 'metadata': Dict with extraction metadata
                - 'performance': Dict with timing info

        Raises:
            ValueError: If no extractor can handle the source
            Exception: If extraction, transformation, or validation fails critically

        Example:
            >>> pipeline = FinancialDataPipeline()
            >>>
            >>> # Excel file
            >>> result = pipeline.execute("financials.xlsx")
            >>>
            >>> # API ticker
            >>> result = pipeline.execute("AAPL", years=5)
            >>>
            >>> # Check results
            >>> if result['validation'].is_valid:
            ...     data = result['data']
            ...     data.to_json("output.json")
        """
        start_time = time.time()

        print(f"\n{'='*80}")
        print(f"FINANCIAL DATA PIPELINE")
        print(f"{'='*80}")
        print(f"Source: {source}")
        print(f"{'='*80}\n")

        # Step 1: Route to appropriate extractor
        print("📍 Step 1: Source Detection & Routing")
        extractor = self._select_extractor(source)

        if not extractor:
            raise ValueError(
                f"No extractor found for source: {source}\n"
                f"Registered extractors: {[e.__class__.__name__ for e in self.extractors]}"
            )

        print(f"   ✓ Using {extractor.__class__.__name__}")

        # Step 2: Extract raw data
        print(f"\n📥 Step 2: Data Extraction")

        try:
            extraction_start = time.time()
            raw_data = extractor.extract(source, **kwargs)
            extraction_time = time.time() - extraction_start

            print(f"   ✓ Extracted {raw_data.company.name}")
            print(f"   ✓ Years: {raw_data.years[0]}-{raw_data.years[-1]} ({len(raw_data.years)} years)")
            print(f"   ✓ Time: {extraction_time:.2f}s")

        except Exception as e:
            self._record_failure(source, extractor.__class__.__name__)
            raise ValueError(f"Extraction failed: {e}") from e

        # Step 3: Apply transformers
        print(f"\n⚙️  Step 3: Data Transformation")

        transformed_data = raw_data

        for i, transformer in enumerate(self.transformers, 1):
            try:
                transform_name = transformer.__name__
                print(f"   → Applying {transform_name}...")

                # Pass context if it's the normalizer
                if transform_name == '_normalize_data' and context:
                    transformed_data = transformer(transformed_data, context)
                else:
                    transformed_data = transformer(transformed_data)

            except Exception as e:
                print(f"   ⚠️  Transformer {transform_name} failed: {e}")
                # Continue with other transformers

        print(f"   ✓ Transformation complete")

        # Step 4: Run validators
        print(f"\n🔍 Step 4: Data Validation")

        validation_results = []

        for validator in self.validators:
            try:
                validator_name = validator.__name__ if hasattr(validator, '__name__') else str(validator)
                print(f"   → Running {validator_name}...")

                # Pass strict flag if it's the default validator
                if validator_name == 'validate':
                    result = validator(transformed_data, strict=strict_validation)
                else:
                    result = validator(transformed_data)

                validation_results.append(result)

            except Exception as e:
                print(f"   ⚠️  Validator {validator_name} failed: {e}")

        # Combine validation results
        if validation_results:
            combined_validation = validation_results[0]  # Use first as primary

            # Check if any validator failed
            is_valid = all(v.is_valid for v in validation_results)
            combined_validation.is_valid = is_valid

            print(f"   ✓ Validation complete: {'PASSED' if is_valid else 'ISSUES FOUND'}")
        else:
            # No validators ran - create dummy result
            from .validators.data_validator import ValidationResult
            combined_validation = ValidationResult(
                is_valid=True,
                issues=[],
                outliers_detected={},
                completeness_score=transformed_data.metadata.completeness_score,
                reconciliation_checks={}
            )

        # Step 5: Compile results
        total_time = time.time() - start_time

        print(f"\n{'='*80}")
        print(f"PIPELINE COMPLETE")
        print(f"{'='*80}")
        print(f"Status: {'✅ SUCCESS' if combined_validation.is_valid else '⚠️  SUCCESS WITH WARNINGS'}")
        print(f"Total time: {total_time:.2f}s")
        print(f"Data quality: {transformed_data.metadata.completeness_score:.1%}")
        print(f"{'='*80}\n")

        # Record stats
        self._record_success(source, extractor.__class__.__name__, total_time)

        # Build result
        result = {
            'data': transformed_data,
            'validation': combined_validation,
            'metadata': {
                'source': source,
                'source_type': extractor.__class__.__name__,
                'extraction_date': datetime.now().isoformat(),
                'pipeline_version': '1.0.0',
                'context': context,
            },
            'performance': {
                'total_time': total_time,
                'extraction_time': extraction_time,
                'stages': {
                    'extraction': extraction_time,
                    'transformation': total_time - extraction_time,
                }
            }
        }

        return result

    def _select_extractor(self, source: Any) -> Optional[BaseExtractor]:
        """
        Select appropriate extractor for source.

        Tries extractors in registration order.

        Args:
            source: Input source

        Returns:
            Extractor that can handle source, or None
        """
        for extractor in self.extractors:
            if extractor.can_handle(source):
                return extractor

        return None

    @staticmethod
    def _normalize_data(data: FinancialData, context: Optional[str] = None) -> FinancialData:
        """Default normalizer transformer."""
        return DataNormalizer.normalize(data, context=context)

    def _record_success(self, source: str, extractor_name: str, time_elapsed: float) -> None:
        """Record successful execution stats."""
        self.stats['total_executions'] += 1
        self.stats['successful'] += 1
        self.stats['total_time'] += time_elapsed

        if extractor_name not in self.stats['by_source']:
            self.stats['by_source'][extractor_name] = {
                'count': 0,
                'total_time': 0.0,
                'successful': 0,
                'failed': 0
            }

        self.stats['by_source'][extractor_name]['count'] += 1
        self.stats['by_source'][extractor_name]['total_time'] += time_elapsed
        self.stats['by_source'][extractor_name]['successful'] += 1

    def _record_failure(self, source: str, extractor_name: str) -> None:
        """Record failed execution stats."""
        self.stats['total_executions'] += 1
        self.stats['failed'] += 1

        if extractor_name not in self.stats['by_source']:
            self.stats['by_source'][extractor_name] = {
                'count': 0,
                'total_time': 0.0,
                'successful': 0,
                'failed': 0
            }

        self.stats['by_source'][extractor_name]['count'] += 1
        self.stats['by_source'][extractor_name]['failed'] += 1

    def get_stats(self) -> Dict[str, Any]:
        """
        Get pipeline execution statistics.

        Returns:
            Dict with execution stats

        Example:
            >>> pipeline = FinancialDataPipeline()
            >>> pipeline.execute("AAPL")
            >>> pipeline.execute("financials.xlsx")
            >>>
            >>> stats = pipeline.get_stats()
            >>> print(f"Success rate: {stats['success_rate']:.1%}")
            >>> print(f"Avg time: {stats['avg_time']:.2f}s")
        """
        total = self.stats['total_executions']
        successful = self.stats['successful']

        return {
            'total_executions': total,
            'successful': successful,
            'failed': self.stats['failed'],
            'success_rate': successful / total if total > 0 else 0,
            'total_time': self.stats['total_time'],
            'avg_time': self.stats['total_time'] / total if total > 0 else 0,
            'by_source': self.stats['by_source']
        }

    def print_stats(self) -> None:
        """Print formatted execution statistics."""
        stats = self.get_stats()

        print("\n" + "="*80)
        print("PIPELINE STATISTICS")
        print("="*80)

        print(f"\nTotal executions: {stats['total_executions']}")
        print(f"Successful: {stats['successful']} ({stats['success_rate']:.1%})")
        print(f"Failed: {stats['failed']}")
        print(f"Total time: {stats['total_time']:.2f}s")
        print(f"Average time: {stats['avg_time']:.2f}s")

        if stats['by_source']:
            print("\nBy Source Type:")
            for source_type, source_stats in stats['by_source'].items():
                avg_time = source_stats['total_time'] / source_stats['count'] if source_stats['count'] > 0 else 0
                print(f"\n  {source_type}:")
                print(f"    Count: {source_stats['count']}")
                print(f"    Success: {source_stats['successful']}")
                print(f"    Failed: {source_stats['failed']}")
                print(f"    Avg time: {avg_time:.2f}s")

        print("="*80 + "\n")


# Convenience function for quick extraction
def extract_financial_data(
    source: Any,
    api_keys: Optional[Dict[str, str]] = None,
    **kwargs
) -> FinancialData:
    """
    Quick extraction function without creating pipeline object.

    Args:
        source: Data source (file, ticker, etc.)
        api_keys: Optional API keys
        **kwargs: Additional arguments for extractor

    Returns:
        FinancialData object

    Example:
        >>> from src.data.pipeline import extract_financial_data
        >>>
        >>> # Excel
        >>> data = extract_financial_data("financials.xlsx")
        >>>
        >>> # API
        >>> data = extract_financial_data("AAPL", years=5)
        >>>
        >>> print(data.summary())
    """
    pipeline = FinancialDataPipeline(api_keys=api_keys)
    result = pipeline.execute(source, **kwargs)
    return result['data']
