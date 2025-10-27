#!/usr/bin/env python3
"""
LBO Model Validator

Validates LBO calculation results against private equity standards.
"""

import sys
from typing import Dict, List, Tuple
import warnings


class LBOValidator:
    """Validates LBO model outputs and returns."""
    
    def __init__(self, strict_mode: bool = False):
        """
        Initialize validator.
        
        Args:
            strict_mode: If True, warnings become errors
        """
        self.strict_mode = strict_mode
        self.errors = []
        self.warnings = []
    
    def validate(self, lbo_results: Dict) -> Tuple[bool, List[str], List[str]]:
        """
        Validate complete LBO model.
        
        Args:
            lbo_results: Dictionary containing:
                - total_sources: Total financing sources
                - total_uses: Total capital uses
                - ltm_ebitda: Last twelve months EBITDA
                - total_debt: Initial total debt
                - equity_investment: Sponsor equity investment
                - purchase_multiple: Entry EV/EBITDA multiple
                - exit_multiple: Exit EV/EBITDA multiple
                - debt_balances: List of debt balances over time
                - ebitda_projections: List of projected EBITDA
                - interest_expenses: List of interest payments
                - irr: Internal rate of return
                - moic: Multiple on invested capital
                - exit_proceeds: Gross proceeds at exit
                - entry_ev: Entry enterprise value
                - exit_ev: Exit enterprise value
        
        Returns:
            Tuple of (is_valid, errors_list, warnings_list)
        """
        self.errors = []
        self.warnings = []
        
        # Run all validation checks
        self._validate_sources_uses(lbo_results)
        self._validate_initial_structure(lbo_results)
        self._validate_debt_schedule(lbo_results)
        self._validate_returns(lbo_results)
        self._validate_value_creation(lbo_results)
        
        # Convert warnings to errors if in strict mode
        if self.strict_mode and self.warnings:
            self.errors.extend(self.warnings)
            self.warnings = []
        
        is_valid = len(self.errors) == 0
        return is_valid, self.errors, self.warnings
    
    def _validate_sources_uses(self, results: Dict):
        """Validate Sources & Uses balance."""
        total_sources = results.get('total_sources')
        total_uses = results.get('total_uses')
        
        if total_sources is None or total_uses is None:
            self.errors.append("Missing Sources or Uses data")
            return
        
        # Sources must equal Uses (within 0.1% tolerance)
        if not 0.999 <= (total_sources / total_uses) <= 1.001:
            self.errors.append(
                f"Sources ({total_sources:.1f}M) ≠ Uses ({total_uses:.1f}M)"
            )
    
    def _validate_initial_structure(self, results: Dict):
        """Validate initial capital structure."""
        ltm_ebitda = results.get('ltm_ebitda')
        total_debt = results.get('total_debt')
        equity_investment = results.get('equity_investment')
        purchase_multiple = results.get('purchase_multiple')
        total_sources = results.get('total_sources')
        
        # Leverage ratio check
        if ltm_ebitda and total_debt:
            leverage_ratio = total_debt / ltm_ebitda
            
            if leverage_ratio > 7.0:
                self.errors.append(
                    f"Leverage ratio {leverage_ratio:.1f}x exceeds typical maximum (6-7x)"
                )
            elif leverage_ratio < 3.0:
                self.warnings.append(
                    f"Leverage ratio {leverage_ratio:.1f}x is low for LBO (typically 4-6x)"
                )
        
        # Equity percentage check
        if equity_investment and total_sources:
            equity_percentage = equity_investment / total_sources
            
            if not 0.25 <= equity_percentage <= 0.50:
                self.warnings.append(
                    f"Equity is {equity_percentage:.1%} of capital (typical range: 30-40%)"
                )
        
        # Purchase multiple check
        if purchase_multiple:
            if not 6.0 <= purchase_multiple <= 15.0:
                self.warnings.append(
                    f"Purchase multiple {purchase_multiple:.1f}x outside typical range (8-12x)"
                )
    
    def _validate_debt_schedule(self, results: Dict):
        """Validate debt paydown schedule."""
        debt_balances = results.get('debt_balances', [])
        ebitda_projections = results.get('ebitda_projections', [])
        interest_expenses = results.get('interest_expenses', [])
        
        if not debt_balances:
            self.warnings.append("No debt schedule provided")
            return
        
        # Check for monotonically decreasing debt
        for i in range(len(debt_balances) - 1):
            if debt_balances[i+1] > debt_balances[i]:
                self.warnings.append(
                    f"Debt balance increased in Year {i+1} (should be paying down)"
                )
                break
        
        # Check for negative debt
        if any(balance < 0 for balance in debt_balances):
            self.errors.append("Debt balance cannot be negative")
        
        # Check if debt is paid off or nearly paid off
        if debt_balances:
            initial_debt = debt_balances[0]
            final_debt = debt_balances[-1]
            
            if initial_debt > 0:
                remaining_debt_ratio = final_debt / initial_debt
                
                if remaining_debt_ratio > 0.50:
                    self.warnings.append(
                        f"Still {remaining_debt_ratio:.1%} of debt remaining at exit"
                    )
        
        # Interest coverage checks
        if ebitda_projections and interest_expenses:
            for i, (ebitda, interest) in enumerate(zip(ebitda_projections, interest_expenses)):
                if interest > 0:
                    coverage = ebitda / interest
                    
                    if coverage < 2.0:
                        self.errors.append(
                            f"Year {i+1}: Interest coverage {coverage:.1f}x below covenant threshold (2.0x)"
                        )
    
    def _validate_returns(self, results: Dict):
        """Validate IRR and MOIC returns."""
        irr = results.get('irr')
        moic = results.get('moic')
        
        # IRR validation
        if irr is not None:
            if irr < 0.10:
                self.warnings.append(
                    f"IRR {irr:.1%} is very low (<10%)"
                )
            elif irr < 0.15:
                self.warnings.append(
                    f"IRR {irr:.1%} below typical PE hurdle rate (15-20%)"
                )
            elif irr > 0.40:
                self.warnings.append(
                    f"IRR {irr:.1%} is exceptionally high (>40%) - verify assumptions"
                )
        
        # MOIC validation
        if moic is not None:
            if moic < 2.0:
                self.warnings.append(
                    f"MOIC {moic:.1f}x is below target (2.0-3.0x minimum)"
                )
            elif moic > 6.0:
                self.warnings.append(
                    f"MOIC {moic:.1f}x is very high (>6x) - verify assumptions"
                )
    
    def _validate_value_creation(self, results: Dict):
        """Validate value creation metrics."""
        entry_ev = results.get('entry_ev')
        exit_ev = results.get('exit_ev')
        purchase_multiple = results.get('purchase_multiple')
        exit_multiple = results.get('exit_multiple')
        
        # Check for value creation
        if entry_ev and exit_ev:
            if exit_ev < entry_ev:
                self.warnings.append(
                    f"Exit EV (${exit_ev:.1f}M) < Entry EV (${entry_ev:.1f}M) - value destruction"
                )
        
        # Check multiple expansion reasonableness
        if purchase_multiple and exit_multiple:
            multiple_change = abs(exit_multiple - purchase_multiple)
            
            if multiple_change > 2.0:
                self.warnings.append(
                    f"Exit multiple {exit_multiple:.1f}x differs significantly from "
                    f"entry {purchase_multiple:.1f}x"
                )
    
    def print_results(self):
        """Print validation results to console."""
        if self.errors:
            print("\n❌ ERRORS:")
            for i, error in enumerate(self.errors, 1):
                print(f"  {i}. {error}")
        
        if self.warnings:
            print("\n⚠️  WARNINGS:")
            for i, warning in enumerate(self.warnings, 1):
                print(f"  {i}. {warning}")
        
        if not self.errors and not self.warnings:
            print("\n✅ All validations passed!")


def main():
    """Command-line interface for LBO validation."""
    # Example usage
    lbo_results = {
        'total_sources': 835,
        'total_uses': 835,
        'ltm_ebitda': 100,
        'total_debt': 600,
        'equity_investment': 235,
        'purchase_multiple': 10.0,
        'exit_multiple': 10.5,
        'debt_balances': [600, 550, 480, 380, 250, 150],
        'ebitda_projections': [100, 105, 112, 120, 130],
        'interest_expenses': [33, 30, 27, 22, 15],
        'irr': 0.24,
        'moic': 5.1,
        'exit_proceeds': 1197,
        'entry_ev': 1000,
        'exit_ev': 1365
    }
    
    validator = LBOValidator(strict_mode=False)
    is_valid, errors, warnings = validator.validate(lbo_results)
    
    validator.print_results()
    
    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()
