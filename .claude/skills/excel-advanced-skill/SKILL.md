# Excel Advanced Skills for Dynamic Financial Model Generation

## Purpose
Enable **AI-driven, dynamic Excel generation** for ValuationPro where each model is intelligently constructed based on available inputs. This skill provides frameworks for deciding WHAT to generate, HOW to build it with industry-grade quality, and WHEN each analysis is appropriate.

## Core Philosophy: Intelligence-Based Generation

**Traditional Approach:** `template + data → Excel`  
**ValuationPro Approach:** `analyze inputs → determine capabilities → build custom model → validate quality`

Each generation must:
1. Assess input completeness and quality
2. Determine which analyses are feasible  
3. Select appropriate methodologies
4. Generate industry-grade outputs
5. Validate results meet IB standards

---

## Part 1: Input Analysis & Capability Mapping

### 1.1 The Input Inventory System

**Before generating ANY Excel model, perform complete input analysis:**

```python
class InputAnalyzer:
    """Analyzes available data and determines what can be generated"""
    
    # Define capability requirements
    ANALYSIS_REQUIREMENTS = {
        'dcf_basic': {
            'required': ['revenue', 'ebitda', 'tax_rate', 'capex'],
            'optional': ['nwc_change', 'da'],
            'enables': ['fcf_projection', 'terminal_value', 'enterprise_value']
        },
        'dcf_advanced': {
            'required': ['revenue', 'ebitda', 'da', 'capex', 'nwc_change', 'tax_rate', 'debt', 'cash'],
            'optional': ['interest_expense', 'preferred_stock'],
            'enables': ['fcf_projection', 'wacc_calculation', 'equity_value', 'price_per_share', 'sensitivity']
        },
        'lbo_basic': {
            'required': ['ebitda', 'enterprise_value', 'debt', 'cash'],
            'optional': ['ebitda_growth'],
            'enables': ['sources_uses', 'returns_summary']
        },
        'lbo_advanced': {
            'required': ['ebitda', 'revenue', 'margins', 'capex_pct', 'nwc_pct', 'debt_tranches'],
            'optional': ['management_equity', 'transaction_fees'],
            'enables': ['debt_schedule', 'waterfall', 'irr_moic', 'sensitivity', 'exit_analysis']
        },
        'comps': {
            'required': ['comparable_companies', 'revenue', 'ebitda'],
            'optional': ['ebit', 'net_income', 'growth_rates'],
            'enables': ['multiple_analysis', 'valuation_range', 'percentile_analysis']
        },
        'precedent_tx': {
            'required': ['transactions', 'ev', 'ebitda'],
            'optional': ['revenue', 'synergies', 'premium_paid'],
            'enables': ['transaction_multiples', 'premium_analysis', 'time_series']
        }
    }
    
    def analyze_and_map_capabilities(self, input_data: dict) -> dict:
        """
        Main entry point: Analyze inputs and return capability map
        
        Returns:
            {
                'analyses': {
                    'dcf': {'feasible': True, 'level': 'advanced', 'confidence': 0.95},
                    'lbo': {'feasible': True, 'level': 'basic', 'confidence': 0.80},
                    'comps': {'feasible': False, 'reason': 'missing_comparables'}
                },
                'components': ['fcf_projection', 'wacc', 'terminal_value', ...],
                'quality_score': 0.87,
                'recommendations': ['Add debt schedule for advanced LBO', ...]
            }
        """
```

### 1.2 Capability Decision Logic

**Decision Tree for Dynamic Generation:**

```
INPUT DATA RECEIVED
    │
    ├─→ Has Historical Financials? (3+ years)
    │   ├─→ YES: Enable projection models (DCF, LBO)
    │   │   ├─→ Has Debt Details?
    │   │   │   ├─→ YES: Advanced LBO with debt schedule
    │   │   │   └─→ NO: Basic LBO with aggregate debt
    │   │   │
    │   │   ├─→ Has Market Data (Beta, Market Cap)?
    │   │   │   ├─→ YES: Full DCF with WACC, equity value
    │   │   │   └─→ NO: Simplified DCF with assumed discount rate
    │   │   │
    │   │   └─→ Has Industry Comparables?
    │   │       ├─→ YES: Add comps section + valuation football field
    │   │       └─→ NO: Standalone DCF/LBO
    │   │
    │   └─→ NO: Focus on current valuation only
    │       ├─→ Has Comparables? → Comps analysis
    │       └─→ Has Transaction Data? → Precedent transactions
    │
    ├─→ Data Quality Check
    │   ├─→ Missing < 10% of key fields? → Proceed with warnings
    │   ├─→ Missing 10-30%? → Request critical data or use estimates
    │   └─→ Missing > 30%? → Abort with specific requirements
    │
    └─→ Generate Component List
        └─→ Build Excel Model
```

### 1.3 Quality Scoring System

```python
def calculate_generation_confidence(self, input_data: dict, capabilities: dict) -> float:
    """
    Calculate confidence score for generation quality (0.0 to 1.0)
    
    Factors:
    - Data completeness (40%)
    - Data consistency (30%) - e.g., FCF ties to components
    - Historical depth (15%) - more years = better projections
    - Market data availability (15%)
    """
    
    completeness = self._score_completeness(input_data)
    consistency = self._score_consistency(input_data)
    depth = self._score_historical_depth(input_data)
    market = self._score_market_data(input_data)
    
    confidence = (
        completeness * 0.40 +
        consistency * 0.30 +
        depth * 0.15 +
        market * 0.15
    )
    
    return confidence
```

**Confidence Thresholds:**
- `0.90-1.00`: Investment-grade model, all analyses feasible
- `0.75-0.89`: High quality, minor estimates acceptable  
- `0.60-0.74`: Moderate quality, flag key assumptions
- `< 0.60`: Low confidence, warn user about limitations

---

## Part 2: Component Library Architecture

### 2.1 Modular Building Blocks

**Every Excel model is assembled from reusable components:**

```python
COMPONENTS = {
    # Core Financial Components
    'assumptions_panel': {
        'requires': [],
        'generates': ['assumption_cells', 'input_section'],
        'cells_used': 20,
        'formatting': 'blue_header_white_text'
    },
    
    'fcf_projection': {
        'requires': ['revenue', 'ebitda_margin', 'tax_rate', 'capex', 'nwc'],
        'generates': ['5yr_fcf_projection', 'fcf_formulas'],
        'cells_used': 50,
        'formulas': ['revenue_growth', 'ebitda_calc', 'nopat_calc', 'fcf_calc']
    },
    
    'wacc_calculation': {
        'requires': ['beta', 'risk_free_rate', 'market_risk_premium', 'debt', 'equity', 'tax_rate'],
        'generates': ['cost_of_equity', 'cost_of_debt', 'wacc'],
        'cells_used': 30,
        'formulas': ['capm', 'weighted_average']
    },
    
    'dcf_valuation': {
        'requires': ['fcf_projection', 'wacc', 'terminal_growth'],
        'generates': ['pv_fcf', 'terminal_value', 'enterprise_value', 'equity_value'],
        'cells_used': 40,
        'formulas': ['npv', 'terminal_value', 'ev_to_equity_bridge']
    },
    
    'sensitivity_table': {
        'requires': ['dcf_valuation'],
        'generates': ['2way_sensitivity', 'conditional_formatting'],
        'cells_used': 100,
        'dimensions': ['wacc', 'terminal_growth']
    },
    
    'debt_schedule': {
        'requires': ['debt_tranches', 'ebitda_projection', 'cash_sweep'],
        'generates': ['quarterly_debt_balance', 'interest_expense', 'paydown_priority'],
        'cells_used': 200,
        'formulas': ['debt_paydown_waterfall', 'interest_calc', 'cash_sweep']
    },
    
    'lbo_returns': {
        'requires': ['entry_ev', 'exit_ev', 'equity_invested', 'distributions'],
        'generates': ['moic', 'irr', 'cash_on_cash'],
        'cells_used': 25,
        'formulas': ['xirr', 'moic_calc']
    },
    
    'comps_table': {
        'requires': ['comparable_companies', 'metrics'],
        'generates': ['trading_multiples', 'statistics', 'implied_valuation'],
        'cells_used': 150,
        'formulas': ['percentile', 'average', 'median']
    }
}
```

---

## Part 3: openpyxl Best Practices

### 3.1 Formula Generation - The Critical Skill

```python
class FormulaBuilder:
    """Generates error-free Excel formulas with proper references"""
    
    def build_formula(self, formula_type: str, params: dict) -> str:
        """
        Central formula builder - returns Excel formula string
        
        Example:
            build_formula('fcf', {
                'ebitda_cell': 'F10',
                'da_cell': 'F11', 
                'tax_rate': 'B5',
                'capex_cell': 'F15',
                'nwc_cell': 'F20'
            })
            
            Returns: "=(F10-F11)*(1-B5)-F15-F20"
        """
        
        if formula_type == 'fcf':
            return self._fcf_formula(params)
        elif formula_type == 'wacc':
            return self._wacc_formula(params)
        elif formula_type == 'npv':
            return self._npv_formula(params)
        elif formula_type == 'irr':
            return self._irr_formula(params)
    
    def _fcf_formula(self, p: dict) -> str:
        """FCF = NOPAT - CapEx - ΔNW"""
        # NOPAT = EBIT * (1 - tax_rate) = (EBITDA - D&A) * (1 - tax)
        nopat = f"(({p['ebitda_cell']}-{p['da_cell']})*(1-{p['tax_rate']}))"
        return f"={nopat}-{p['capex_cell']}-{p['nwc_cell']}"
    
    def _wacc_formula(self, p: dict) -> str:
        """WACC = (E/V)*Re + (D/V)*Rd*(1-T)"""
        re = f"({p['rf']}+{p['beta']}*{p['mrp']})"
        total_v = f"({p['equity']}+{p['debt']})"
        e_component = f"({p['equity']}/{total_v})*{re}"
        d_component = f"({p['debt']}/{total_v})*{p['rd']}*(1-{p['tax_rate']})"
        return f"={e_component}+{d_component}"
    
    def _npv_formula(self, p: dict) -> str:
        """NPV of cash flow range"""
        if 'cf0' in p:
            return f"=NPV({p['discount_rate']},{p['cf_range']})+{p['cf0']}"
        else:
            return f"=NPV({p['discount_rate']},{p['cf_range']})"
    
    def _irr_formula(self, p: dict) -> str:
        """IRR = XIRR(cash_flows, dates)"""
        if 'dates_range' in p:
            return f"=XIRR({p['cash_flows']},{p['dates_range']})"
        else:
            return f"=IRR({p['cash_flows']})"
```

### 3.2 Absolute vs Relative References

**CRITICAL RULE:** Use $ signs correctly or formulas break when copied.

```python
# WRONG - relative reference to growth assumption
ws['F10'].value = "=E10*(1+B5)"  # If copied right, becomes =F10*(1+C5) ❌

# CORRECT - absolute reference to assumption, relative to previous year
ws['F10'].value = "=E10*(1+$B$5)"  # If copied right, becomes =F10*(1+$B$5) ✓
```

**Reference Types Guide:**
- **Assumptions (growth rates, tax rates, WACC):** Always absolute `$B$5`
- **Previous period reference:** Relative `E10`
- **Same-row lookups:** Mixed `$B10` (absolute column, relative row)
- **Same-column lookups:** Mixed `B$10` (relative column, absolute row)

---

## Part 4: Industry-Grade Formatting

```python
class IBFormatter:
    """Apply investment banking standard formatting"""
    
    COLORS = {
        'header_bg': '002060',      # Dark blue
        'header_text': 'FFFFFF',     # White
        'input_bg': 'FFF2CC',        # Light yellow
        'output_bg': 'D9E1F2',       # Light blue
    }
    
    NUMBER_FORMATS = {
        'currency_millions': '$#,##0.0,,"M"',
        'percentage': '0.0%',
        'multiple': '0.0x',
    }
    
    def format_header(self, ws, cell_range: str, text: str):
        """Dark blue header, white bold text"""
        cells = ws[cell_range]
        for row in cells:
            for cell in row if isinstance(row, tuple) else [row]:
                cell.fill = PatternFill(start_color=self.COLORS['header_bg'],
                                       end_color=self.COLORS['header_bg'],
                                       fill_type='solid')
                cell.font = Font(color=self.COLORS['header_text'], bold=True)
```

---

## Part 5: Dynamic Generation Orchestration

```python
class DynamicModelGenerator:
    """Orchestrates entire dynamic Excel generation"""
    
    def generate_model(self, input_data: dict, company_name: str) -> Workbook:
        """
        Main entry point: Generate custom Excel model based on inputs
        
        Process:
        1. Analyze inputs → determine capabilities
        2. Select components → determine layout
        3. Generate Excel structure
        4. Populate with formulas
        5. Apply formatting
        6. Validate output
        """
        
        # STEP 1: Analyze inputs
        capabilities = self.input_analyzer.analyze_and_map_capabilities(input_data)
        confidence = self.input_analyzer.calculate_generation_confidence(input_data, capabilities)
        
        # STEP 2: Select components
        components = self.component_library.select_components(capabilities)
        layout = self.layout_engine.generate_layout(components)
        
        # STEP 3: Create workbook
        wb = Workbook()
        ws = wb.active
        ws.title = f"{company_name} Valuation"
        
        # STEP 4: Generate each component
        for component in components:
            self._generate_component(ws, component, layout[component], input_data, capabilities)
        
        # STEP 5: Apply formatting
        self._apply_formatting(ws, components, layout)
        
        # STEP 6: Validate
        errors = self._validate_output(ws, components, input_data)
        if errors:
            self._add_error_sheet(wb, errors)
        
        return wb
```

---

## Part 6: Top 10 openpyxl Mistakes to Avoid

1. **Using calculated values instead of formulas**
2. **Forgetting $ signs for absolute references**
3. **Cell reference off-by-one errors** (openpyxl is 1-indexed)
4. **Not handling cell merges properly**
5. **Creating circular references**
6. **Not setting column widths** (numbers appear as ###)
7. **Forgetting number formats** (0.15 displays as 0.15, not 15%)
8. **Incorrect formula string escaping**
9. **Not validating generated formulas**
10. **Performance issues with individual cell writes**

---

## Part 7: Quick Reference Formulas

```python
# Revenue growth
f"={prev_year_cell}*(1+${growth_assumption_cell})"

# EBITDA from margin
f"={revenue_cell}*${margin_cell}"

# NOPAT
f"=({ebitda_cell}-{da_cell})*(1-${tax_rate_cell})"

# Free Cash Flow
f"=({ebitda_cell}-{da_cell})*(1-${tax_cell})-{capex_cell}-{nwc_cell}"

# NPV
f"=NPV(${wacc_cell},{fcf_range})"

# Terminal Value (Gordon Growth)
f"={last_fcf_cell}*(1+${term_growth})/(${wacc_cell}-${term_growth})"

# Terminal Value (Exit Multiple)
f"={last_ebitda_cell}*${exit_multiple_cell}"

# EV to Equity Bridge
f"={ev_cell}-{debt_cell}+{cash_cell}"

# WACC
f"=(${equity}/(${equity}+${debt}))*${re}+(${debt}/(${equity}+${debt}))*${rd}*(1-${tax})"

# Cost of Equity (CAPM)
f"=${rf_cell}+${beta_cell}*${mrp_cell}"

# IRR
f"=XIRR({cash_flow_range},{date_range})"

# MOIC
f"={exit_value_cell}/{entry_value_cell}"
```

---

## Summary: Keys to Success

1. **Always analyze inputs first** - Don't assume what's available
2. **Build modularly** - Components that can be mixed and matched
3. **Use formulas, never hardcoded values** - Transparency is critical
4. **Get references right** - $ signs matter enormously
5. **Format like an investment banker** - Standards exist for a reason
6. **Validate output** - Check for errors, unrealistic values
7. **Handle edge cases gracefully** - Missing data, negative values
8. **Test each component** - Unit test every formula
9. **Document decisions** - Log what was generated and why
10. **Performance matters** - Batch operations where possible

This skill enables ValuationPro to generate ANY financial model configuration based on available inputs, maintaining investment banking quality standards across all scenarios.
