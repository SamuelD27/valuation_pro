"""
Decision Logic Example - Input Analysis & Capability Mapping

Shows how to intelligently decide what to generate based on available data
"""

from typing import Dict, List


def analyze_data_completeness(data: Dict) -> Dict:
    """
    Analyze input data and score completeness
    
    Returns scores and missing fields for each analysis type
    """
    
    analysis_requirements = {
        'dcf_basic': ['revenue', 'ebitda', 'tax_rate', 'capex'],
        'dcf_advanced': ['revenue', 'ebitda', 'd_and_a', 'capex', 'nwc_change', 
                        'tax_rate', 'debt', 'cash', 'beta'],
        'lbo_basic': ['ebitda', 'enterprise_value', 'debt', 'cash'],
        'lbo_advanced': ['ebitda', 'revenue', 'margins', 'capex_pct', 
                        'nwc_pct', 'debt_tranches'],
        'comps': ['comparable_companies', 'revenue', 'ebitda'],
    }
    
    results = {}
    
    for analysis, required_fields in analysis_requirements.items():
        available = [f for f in required_fields if f in data and data[f] is not None]
        missing = [f for f in required_fields if f not in available]
        
        completeness = len(available) / len(required_fields)
        
        results[analysis] = {
            'completeness': completeness,
            'available_fields': available,
            'missing_fields': missing,
            'feasible': completeness >= 0.8  # 80% threshold
        }
    
    return results


def determine_generation_strategy(data: Dict) -> Dict:
    """
    Main decision function: Determines what to generate
    
    Returns generation plan with components and confidence
    """
    
    completeness = analyze_data_completeness(data)
    
    strategy = {
        'components': [],
        'analyses': {},
        'confidence': 0.0,
        'warnings': [],
        'recommendations': []
    }
    
    # Decision tree for DCF
    if completeness['dcf_advanced']['feasible']:
        strategy['analyses']['dcf'] = 'advanced'
        strategy['components'].extend(['fcf_projection', 'wacc_calc', 'dcf_valuation', 'sensitivity'])
        strategy['confidence'] += 0.4
    elif completeness['dcf_basic']['feasible']:
        strategy['analyses']['dcf'] = 'basic'
        strategy['components'].extend(['fcf_projection', 'dcf_valuation'])
        strategy['confidence'] += 0.25
        strategy['warnings'].append("DCF is basic - missing market data for WACC")
        strategy['recommendations'].append("Add beta, debt, cash for advanced DCF")
    else:
        missing = completeness['dcf_basic']['missing_fields']
        strategy['warnings'].append(f"Cannot generate DCF - missing: {', '.join(missing)}")
    
    # Decision tree for LBO
    if completeness['lbo_advanced']['feasible']:
        strategy['analyses']['lbo'] = 'advanced'
        strategy['components'].extend(['debt_schedule', 'lbo_returns', 'waterfall'])
        strategy['confidence'] += 0.4
    elif completeness['lbo_basic']['feasible']:
        strategy['analyses']['lbo'] = 'basic'
        strategy['components'].append('lbo_returns')
        strategy['confidence'] += 0.2
        strategy['recommendations'].append("Add debt schedule for advanced LBO")
    
    # Decision tree for Comps
    if completeness['comps']['feasible']:
        num_comps = len(data.get('comparable_companies', []))
        if num_comps >= 5:
            strategy['analyses']['comps'] = 'full'
            strategy['components'].append('comps_table')
            strategy['confidence'] += 0.2
        elif num_comps >= 3:
            strategy['analyses']['comps'] = 'limited'
            strategy['components'].append('comps_table')
            strategy['confidence'] += 0.15
            strategy['warnings'].append(f"Only {num_comps} comparables - consider adding more")
    
    # Integrative components (if multiple analyses)
    if len(strategy['analyses']) > 1:
        strategy['components'].append('football_field')
    
    return strategy


# Example scenarios
if __name__ == "__main__":
    
    print("\n" + "="*70)
    print("SCENARIO 1: High-Quality Public Company Data")
    print("="*70)
    
    scenario1 = {
        'revenue': 1500,
        'ebitda': 450,
        'd_and_a': 75,
        'capex': 120,
        'nwc_change': 30,
        'tax_rate': 0.25,
        'debt': 500,
        'cash': 200,
        'beta': 1.2,
        'enterprise_value': 8000,
        'debt_tranches': [
            {'type': 'Senior', 'amount': 300},
            {'type': 'Sub', 'amount': 200}
        ],
        'comparable_companies': [{'name': f'Comp{i}'} for i in range(6)]
    }
    
    strategy1 = determine_generation_strategy(scenario1)
    print(f"\nAnalyses: {strategy1['analyses']}")
    print(f"Components: {strategy1['components']}")
    print(f"Confidence: {strategy1['confidence']:.0%}")
    
    
    print("\n" + "="*70)
    print("SCENARIO 2: Limited Private Company Data")
    print("="*70)
    
    scenario2 = {
        'revenue': 500,
        'ebitda': 100,
        'capex': 40,
        'tax_rate': 0.25,
        # Missing: market data, debt details, comparables
    }
    
    strategy2 = determine_generation_strategy(scenario2)
    print(f"\nAnalyses: {strategy2['analyses']}")
    print(f"Components: {strategy2['components']}")
    print(f"Confidence: {strategy2['confidence']:.0%}")
    print(f"Warnings: {strategy2['warnings']}")
    print(f"Recommendations: {strategy2['recommendations']}")
    
    
    print("\n" + "="*70)
    print("SCENARIO 3: Transaction Comps Only")
    print("="*70)
    
    scenario3 = {
        'revenue': 750,
        'ebitda': 200,
        'comparable_companies': [{'name': f'Comp{i}'} for i in range(4)]
        # Missing: most financial details
    }
    
    strategy3 = determine_generation_strategy(scenario3)
    print(f"\nAnalyses: {strategy3['analyses']}")
    print(f"Components: {strategy3['components']}")
    print(f"Confidence: {strategy3['confidence']:.0%}")
    if strategy3['warnings']:
        print(f"Warnings: {strategy3['warnings']}")
