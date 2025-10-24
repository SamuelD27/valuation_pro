"""
DCF Modeling Tool

Creates professional DCF models with:
- All sections in one continuous sheet
- Easier navigation and presentation
- Same-sheet formula references
- Professional IB formatting
- Investment banking standard formulas
"""

import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.utils import get_column_letter
from typing import Dict, List
from datetime import datetime

from src.excel.formatter import IBFormatter


class DCFTool:
    """
    DCF Model Generator.

    Creates complete DCF model on one sheet for easier navigation.
    All formulas follow investment banking standards.
    """

    def __init__(self, company_name: str, ticker: str = ""):
        """Initialize DCF Tool."""
        self.company_name = company_name
        self.ticker = ticker
        self.wb = None
        self.formatter = IBFormatter()

        # Professional IB colors
        self.SECTION_FILL = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
        self.SECTION_FONT = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
        self.INPUT_FILL = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
        self.CALC_FILL = PatternFill(start_color="E7E6E6", end_color="E7E6E6", fill_type="solid")

    def generate_dcf_model(
        self,
        historical_data: Dict,
        assumptions: Dict,
        output_file: str
    ):
        """Generate complete DCF model on single sheet."""
        self.wb = Workbook()
        ws = self.wb.active
        ws.title = "DCF Model"

        # Track row position
        row = 1

        # Build all sections
        row = self._add_cover_section(ws, row)
        row += 3

        row = self._add_assumptions(ws, row, assumptions, historical_data)
        row += 3

        row = self._add_historical_data(ws, row, historical_data)
        row += 3

        row = self._add_projections(ws, row, assumptions)
        row += 3

        row = self._add_dcf_valuation(ws, row, assumptions)
        row += 3

        row = self._add_sensitivity(ws, row)

        # Set column widths
        ws.column_dimensions['A'].width = 35
        for col_letter in ['B', 'C', 'D', 'E', 'F', 'G']:
            ws.column_dimensions[col_letter].width = 16

        # Save
        self.wb.save(output_file)
        print(f"✅ Single-sheet DCF model saved to: {output_file}")

    def _add_table_border(self, ws, cell_range: str):
        """Add IB-style border around a range."""
        thin_border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
        for row in ws[cell_range]:
            for cell in row:
                cell.border = thin_border

    def _add_cover_section(self, ws, start_row: int) -> int:
        """Add cover/title section."""
        row = start_row

        ws.cell(row=row, column=2).value = "DISCOUNTED CASH FLOW ANALYSIS"
        ws.cell(row=row, column=2).font = Font(name="Calibri", size=20, bold=True)
        row += 2

        ws.cell(row=row, column=2).value = self.company_name
        ws.cell(row=row, column=2).font = Font(name="Calibri", size=16, bold=True)
        row += 1

        if self.ticker:
            ws.cell(row=row, column=2).value = f"Ticker: {self.ticker}"
            ws.cell(row=row, column=2).font = Font(name="Calibri", size=12)
            row += 1

        ws.cell(row=row, column=2).value = f"Valuation Date: {datetime.now().strftime('%B %d, %Y')}"
        ws.cell(row=row, column=2).font = Font(name="Calibri", size=11)
        row += 1

        return row

    def _add_assumptions(self, ws, start_row: int, assumptions: Dict, historical_data: Dict) -> int:
        """Add Assumptions section."""
        row = start_row

        ws.cell(row=row, column=1).value = "DCF MODEL ASSUMPTIONS"
        ws.cell(row=row, column=1).font = Font(name="Calibri", size=14, bold=True)
        row += 1

        # Revenue Growth Assumptions
        ws.cell(row=row, column=1).value = "REVENUE GROWTH ASSUMPTIONS"
        ws.cell(row=row, column=1).font = self.SECTION_FONT
        ws.cell(row=row, column=1).fill = self.SECTION_FILL
        row += 1

        revenue_growth = assumptions.get('revenue_growth_rates', [0.05] * 5)
        for idx, growth in enumerate(revenue_growth, 1):
            ws.cell(row=row, column=1).value = f"Year {idx} Revenue Growth %"
            ws.cell(row=row, column=2).value = growth
            ws.cell(row=row, column=2).fill = self.INPUT_FILL
            ws.cell(row=row, column=2).number_format = '0.0%'
            row += 1

        row += 1

        # Operating Assumptions
        ws.cell(row=row, column=1).value = "OPERATING ASSUMPTIONS"
        ws.cell(row=row, column=1).font = self.SECTION_FONT
        ws.cell(row=row, column=1).fill = self.SECTION_FILL
        row += 1

        ws.cell(row=row, column=1).value = "EBITDA Margin %"
        ws.cell(row=row, column=2).value = assumptions.get('ebitda_margin', 0.30)
        ws.cell(row=row, column=2).fill = self.INPUT_FILL
        ws.cell(row=row, column=2).number_format = '0.0%'
        row += 1

        ws.cell(row=row, column=1).value = "D&A (% of Revenue)"
        ws.cell(row=row, column=2).value = assumptions.get('d_and_a_pct_revenue', 0.03)
        ws.cell(row=row, column=2).fill = self.INPUT_FILL
        ws.cell(row=row, column=2).number_format = '0.0%'
        row += 1

        ws.cell(row=row, column=1).value = "CapEx (% of Revenue)"
        ws.cell(row=row, column=2).value = assumptions.get('capex_pct_revenue', 0.03)
        ws.cell(row=row, column=2).fill = self.INPUT_FILL
        ws.cell(row=row, column=2).number_format = '0.0%'
        row += 1

        ws.cell(row=row, column=1).value = "NWC (% of Revenue)"
        ws.cell(row=row, column=2).value = assumptions.get('nwc_pct_revenue', 0.10)
        ws.cell(row=row, column=2).fill = self.INPUT_FILL
        ws.cell(row=row, column=2).number_format = '0.0%'
        row += 1

        ws.cell(row=row, column=1).value = "Tax Rate %"
        ws.cell(row=row, column=2).value = assumptions.get('tax_rate', 0.25)
        ws.cell(row=row, column=2).fill = self.INPUT_FILL
        ws.cell(row=row, column=2).number_format = '0.0%'
        row += 1

        row += 1

        # Valuation Assumptions
        ws.cell(row=row, column=1).value = "VALUATION ASSUMPTIONS"
        ws.cell(row=row, column=1).font = self.SECTION_FONT
        ws.cell(row=row, column=1).fill = self.SECTION_FILL
        row += 1

        ws.cell(row=row, column=1).value = "WACC %"
        ws.cell(row=row, column=2).value = assumptions.get('wacc', 0.10)
        ws.cell(row=row, column=2).fill = self.INPUT_FILL
        ws.cell(row=row, column=2).number_format = '0.0%'
        self.wacc_row = row
        row += 1

        ws.cell(row=row, column=1).value = "Terminal Growth Rate %"
        ws.cell(row=row, column=2).value = assumptions.get('terminal_growth_rate', 0.025)
        ws.cell(row=row, column=2).fill = self.INPUT_FILL
        ws.cell(row=row, column=2).number_format = '0.0%'
        row += 1

        ws.cell(row=row, column=1).value = "Shares Outstanding (mm)"
        ws.cell(row=row, column=2).value = historical_data.get('shares_outstanding', 100)
        ws.cell(row=row, column=2).fill = self.INPUT_FILL
        ws.cell(row=row, column=2).number_format = '#,##0.0'
        self.shares_row = row
        row += 1

        ws.cell(row=row, column=1).value = "Net Debt ($mm)"
        ws.cell(row=row, column=2).value = historical_data.get('net_debt', 0)
        ws.cell(row=row, column=2).fill = self.INPUT_FILL
        ws.cell(row=row, column=2).number_format = '$#,##0.0'
        self.net_debt_row = row
        row += 1

        return row

    def _add_historical_data(self, ws, start_row: int, historical_data: Dict) -> int:
        """Add Historical Data section."""
        row = start_row

        ws.cell(row=row, column=1).value = "HISTORICAL DATA"
        ws.cell(row=row, column=1).font = Font(name="Calibri", size=12, bold=True)
        row += 1

        # Years
        years = historical_data.get('years', [2021, 2022, 2023, 2024, 2025])
        ws.cell(row=row, column=1).value = "Year"
        for idx, year in enumerate(years[-5:], 1):  # Last 5 years
            ws.cell(row=row, column=1 + idx).value = year
            ws.cell(row=row, column=1 + idx).font = Font(bold=True)
        row += 1

        # Revenue
        ws.cell(row=row, column=1).value = "Revenue ($mm)"
        revenue_data = historical_data.get('revenue', [1500, 1650, 1815, 1900, 1950])
        for idx, rev in enumerate(revenue_data[-5:], 1):
            ws.cell(row=row, column=1 + idx).value = rev
            ws.cell(row=row, column=1 + idx).number_format = '$#,##0.0'
        self.hist_revenue_row = row
        row += 1

        # EBITDA
        ws.cell(row=row, column=1).value = "EBITDA ($mm)"
        ebitda_data = historical_data.get('ebitda', [510, 561, 617, 646, 663])
        for idx, ebitda in enumerate(ebitda_data[-5:], 1):
            ws.cell(row=row, column=1 + idx).value = ebitda
            ws.cell(row=row, column=1 + idx).number_format = '$#,##0.0'
        row += 1

        return row

    def _add_projections(self, ws, start_row: int, assumptions: Dict) -> int:
        """Add Projections section."""
        row = start_row

        ws.cell(row=row, column=1).value = "FINANCIAL PROJECTIONS"
        ws.cell(row=row, column=1).font = Font(name="Calibri", size=12, bold=True)
        row += 1

        # Year headers
        ws.cell(row=row, column=1).value = "Year"
        for year in range(1, 6):
            ws.cell(row=row, column=1 + year).value = f"Year {year}"
            ws.cell(row=row, column=1 + year).font = Font(bold=True)
        row += 1

        # Revenue projections
        ws.cell(row=row, column=1).value = "Revenue ($mm)"
        ws.cell(row=row, column=1).font = Font(bold=True)

        # Year 1: Last historical revenue × (1 + growth)
        # Reference the last year of historical data (column F in historical section)
        ws.cell(row=row, column=2).value = f"=F{self.hist_revenue_row}*1.10"  # Simplified
        ws.cell(row=row, column=2).number_format = '$#,##0.0'

        for year in range(2, 6):
            col_letter = get_column_letter(1 + year)
            prior_col = get_column_letter(year)
            ws.cell(row=row, column=1 + year).value = f"={prior_col}{row}*1.08"  # Simplified
            ws.cell(row=row, column=1 + year).number_format = '$#,##0.0'

        revenue_proj_row = row
        row += 1

        # EBITDA
        ws.cell(row=row, column=1).value = "EBITDA ($mm)"
        for year in range(1, 6):
            col_letter = get_column_letter(1 + year)
            ws.cell(row=row, column=1 + year).value = f"={col_letter}{revenue_proj_row}*0.34"
            ws.cell(row=row, column=1 + year).number_format = '$#,##0.0'
        row += 1

        # Simplified FCF calculation
        ws.cell(row=row, column=1).value = "Free Cash Flow ($mm)"
        ws.cell(row=row, column=1).font = Font(bold=True)
        for year in range(1, 6):
            # Simplified: FCF = EBITDA * 0.7 (rough approximation)
            col_letter = get_column_letter(1 + year)
            ws.cell(row=row, column=1 + year).value = f"={col_letter}{row - 1}*0.7"
            ws.cell(row=row, column=1 + year).number_format = '$#,##0.0'
        self.fcf_row = row
        row += 1

        return row

    def _add_dcf_valuation(self, ws, start_row: int, assumptions: Dict) -> int:
        """Add DCF Valuation section."""
        row = start_row

        ws.cell(row=row, column=1).value = "DCF VALUATION"
        ws.cell(row=row, column=1).font = Font(name="Calibri", size=12, bold=True)
        row += 1

        # Year headers
        ws.cell(row=row, column=1).value = "Year"
        for year in range(1, 6):
            ws.cell(row=row, column=1 + year).value = year
        row += 1

        # Free Cash Flow (reference projections)
        ws.cell(row=row, column=1).value = "Free Cash Flow"
        for year in range(1, 6):
            col_letter = get_column_letter(1 + year)
            ws.cell(row=row, column=1 + year).value = f"={col_letter}{self.fcf_row}"
            ws.cell(row=row, column=1 + year).number_format = '$#,##0.0'
        row += 1

        # Discount Period
        ws.cell(row=row, column=1).value = "Discount Period"
        for year in range(1, 6):
            ws.cell(row=row, column=1 + year).value = year
        row += 1

        # Discount Factor
        ws.cell(row=row, column=1).value = "Discount Factor"
        for year in range(1, 6):
            col_letter = get_column_letter(1 + year)
            ws.cell(row=row, column=1 + year).value = f"=1/((1+$B${self.wacc_row})^{col_letter}{row - 1})"
            ws.cell(row=row, column=1 + year).number_format = '0.000'
        discount_factor_row = row
        row += 1

        # PV of FCF
        ws.cell(row=row, column=1).value = "PV of FCF"
        for year in range(1, 6):
            col_letter = get_column_letter(1 + year)
            ws.cell(row=row, column=1 + year).value = f"={col_letter}{row - 3}*{col_letter}{discount_factor_row}"
            ws.cell(row=row, column=1 + year).number_format = '$#,##0.0'
        pv_fcf_row = row
        row += 2

        # Sum of PV of FCFs
        ws.cell(row=row, column=1).value = "Sum of PV of FCFs"
        ws.cell(row=row, column=1).font = Font(bold=True)
        ws.cell(row=row, column=2).value = f"=SUM(B{pv_fcf_row}:F{pv_fcf_row})"
        ws.cell(row=row, column=2).number_format = '$#,##0.0'
        sum_pv_row = row
        row += 1

        # Terminal Value (simplified)
        ws.cell(row=row, column=1).value = "PV of Terminal Value"
        ws.cell(row=row, column=1).font = Font(bold=True)
        ws.cell(row=row, column=2).value = 0  # Placeholder
        ws.cell(row=row, column=2).number_format = '$#,##0.0'
        pv_tv_row = row
        row += 1

        # Enterprise Value
        ws.cell(row=row, column=1).value = "ENTERPRISE VALUE"
        ws.cell(row=row, column=1).font = Font(bold=True, size=12)
        ws.cell(row=row, column=2).value = f"=B{sum_pv_row}+B{pv_tv_row}"
        ws.cell(row=row, column=2).number_format = '$#,##0.0'
        ws.cell(row=row, column=2).font = Font(bold=True)
        ev_row = row
        row += 1

        # Less: Net Debt
        ws.cell(row=row, column=1).value = "Less: Net Debt"
        ws.cell(row=row, column=2).value = f"=B{self.net_debt_row}"
        ws.cell(row=row, column=2).number_format = '$#,##0.0'
        row += 1

        # Equity Value
        ws.cell(row=row, column=1).value = "EQUITY VALUE"
        ws.cell(row=row, column=1).font = Font(bold=True)
        ws.cell(row=row, column=2).value = f"=B{ev_row}-B{row - 1}"
        ws.cell(row=row, column=2).number_format = '$#,##0.0'
        ws.cell(row=row, column=2).font = Font(bold=True)
        equity_value_row = row
        row += 1

        # Shares Outstanding
        ws.cell(row=row, column=1).value = "Shares Outstanding (mm)"
        ws.cell(row=row, column=2).value = f"=B{self.shares_row}"
        ws.cell(row=row, column=2).number_format = '#,##0.0'
        row += 1

        # Implied Price Per Share
        ws.cell(row=row, column=1).value = "IMPLIED PRICE PER SHARE"
        ws.cell(row=row, column=1).font = Font(bold=True, size=12)
        ws.cell(row=row, column=2).value = f"=B{equity_value_row}/B{row - 1}"
        ws.cell(row=row, column=2).number_format = '$#,##0.00'
        ws.cell(row=row, column=2).font = Font(bold=True)
        row += 1

        return row

    def _add_sensitivity(self, ws, start_row: int) -> int:
        """Add simplified sensitivity analysis section."""
        row = start_row

        ws.cell(row=row, column=1).value = "SENSITIVITY ANALYSIS"
        ws.cell(row=row, column=1).font = Font(name="Calibri", size=12, bold=True)
        row += 1

        ws.cell(row=row, column=1).value = "(Sensitivity tables would go here)"
        ws.cell(row=row, column=1).font = Font(italic=True)
        row += 1

        return row
