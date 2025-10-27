#!/usr/bin/env python3
"""DCF Model Validator - Works as CLI tool and reference code"""
import sys
import json
import argparse
from typing import Dict, List, Tuple

class DCFValidator:
    def __init__(self, strict_mode: bool = False):
        self.strict_mode = strict_mode
        self.errors = []
        self.warnings = []
    
    def validate(self, dcf_results: Dict) -> Tuple[bool, List[str], List[str]]:
        self.errors = []
        self.warnings = []
        
        self._validate_inputs(dcf_results)
        self._validate_fcf_projections(dcf_results)
        self._validate_terminal_value(dcf_results)
        self._validate_outputs(dcf_results)
        
        if self.strict_mode and self.warnings:
            self.errors.extend(self.warnings)
            self.warnings = []
        
        return len(self.errors) == 0, self.errors, self.warnings
    
    def _validate_inputs(self, r: Dict):
        wacc = r.get('wacc')
        tg = r.get('terminal_growth')
        
        if wacc and not 0.05 <= wacc <= 0.25:
            self.warnings.append(f"WACC {wacc:.1%} outside 5-25% range")
        
        if tg and not 0.015 <= tg <= 0.05:
            self.warnings.append(f"Terminal growth {tg:.1%} outside 1.5-5% range")
        
        if wacc and tg and wacc <= tg:
            self.errors.append(f"WACC ({wacc:.1%}) must exceed terminal growth ({tg:.1%})")
    
    def _validate_fcf_projections(self, r: Dict):
        fcf = r.get('fcf_projections', [])
        if not fcf:
            self.errors.append("No FCF projections")
            return
        
        if len(fcf) < 5 or len(fcf) > 15:
            self.warnings.append(f"Projection period {len(fcf)} years unusual (typical 5-10)")
        
        if fcf[-1] <= 0:
            self.errors.append("Terminal year FCF negative")
    
    def _validate_terminal_value(self, r: Dict):
        tv = r.get('pv_terminal_value')
        ev = r.get('enterprise_value')
        
        if tv and ev and ev > 0:
            pct = (tv / ev) * 100
            if pct > 90:
                self.warnings.append(f"Terminal value {pct:.1f}% of EV (target 50-75%)")
            elif pct < 40:
                self.warnings.append(f"Terminal value only {pct:.1f}% of EV")
    
    def _validate_outputs(self, r: Dict):
        ev = r.get('enterprise_value')
        eq = r.get('equity_value')
        ebitda = r.get('ltm_ebitda')
        
        if ev and ev <= 0:
            self.errors.append("Enterprise Value ≤ 0")
        
        if eq and eq <= 0:
            self.warnings.append("Equity Value negative (insolvency)")
        
        if ev and ebitda and ebitda > 0:
            mult = ev / ebitda
            if not 4.0 <= mult <= 25.0:
                self.warnings.append(f"EV/EBITDA {mult:.1f}x unusual")

def main():
    parser = argparse.ArgumentParser(description='Validate DCF model')
    parser.add_argument('--file', help='JSON file with DCF results')
    parser.add_argument('--strict', action='store_true', help='Treat warnings as errors')
    args = parser.parse_args()
    
    if args.file:
        with open(args.file) as f:
            data = json.load(f)
    else:
        # Example data
        data = {
            'wacc': 0.095, 'terminal_growth': 0.025,
            'fcf_projections': [100, 120, 140, 160, 180],
            'pv_terminal_value': 2200, 'enterprise_value': 3000,
            'equity_value': 2500, 'ltm_ebitda': 250
        }
    
    validator = DCFValidator(strict_mode=args.strict)
    is_valid, errors, warnings = validator.validate(data)
    
    if errors:
        print("\n❌ ERRORS:")
        for i, e in enumerate(errors, 1):
            print(f"  {i}. {e}")
    
    if warnings:
        print("\n⚠️  WARNINGS:")
        for i, w in enumerate(warnings, 1):
            print(f"  {i}. {w}")
    
    if not errors and not warnings:
        print("\n✅ All validations passed!")
    
    sys.exit(0 if is_valid else 1)

if __name__ == "__main__":
    main()
