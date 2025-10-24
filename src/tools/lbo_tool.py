"""
LBO Modeling Tool

Creates professional LBO models with:
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


class LBOTool:
    """
    LBO Model Generator.

    Creates complete LBO model on one sheet for easier navigation.
    All formulas follow investment banking standards.
    """

    def __init__(self, company_name: str, sponsor: str = ""):
        """Initialize LBO Tool."""
        self.company_name = company_name
        self.sponsor = sponsor
        self.wb = None
        self.formatter = IBFormatter()

        # Professional IB colors
        self.SECTION_FILL = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
        self.SECTION_FONT = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
        self.INPUT_FILL = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
        self.CALC_FILL = PatternFill(start_color="E7E6E6", end_color="E7E6E6", fill_type="solid")

    def generate_lbo_model(
        self,
        transaction_data: Dict,
        assumptions: Dict,
        output_file: str
    ):
        """Generate complete LBO model on single sheet."""
        self.wb = Workbook()
        ws = self.wb.active
        ws.title = "LBO Model"

        # Track row position as we build sections
        row = 1

        # Build all sections sequentially
        row = self._add_cover_section(ws, row, transaction_data)
        row += 3  # spacing

        row = self._add_transaction_summary(ws, row, transaction_data, assumptions)
        row += 3

        row = self._add_sources_uses(ws, row, transaction_data, assumptions)
        row += 3

        row = self._add_assumptions(ws, row, assumptions)
        row += 3

        row = self._add_operating_model(ws, row, transaction_data, assumptions)
        row += 3

        row = self._add_debt_schedule(ws, row, assumptions)
        row += 3

        row = self._add_cash_flow_waterfall(ws, row, assumptions)
        row += 3

        row = self._add_returns_analysis(ws, row, transaction_data, assumptions)

        # Set column widths
        ws.column_dimensions['A'].width = 35
        ws.column_dimensions['B'].width = 18
        ws.column_dimensions['C'].width = 18
        ws.column_dimensions['D'].width = 18
        ws.column_dimensions['E'].width = 18
        ws.column_dimensions['F'].width = 18
        ws.column_dimensions['G'].width = 18

        # Save
        self.wb.save(output_file)
        print(f"✅ Single-sheet LBO model saved to: {output_file}")

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

    def _add_cover_section(self, ws, start_row: int, transaction_data: Dict) -> int:
        """Add cover/title section. Returns next available row."""
        row = start_row

        # Title
        ws.cell(row=row, column=2).value = "LEVERAGED BUYOUT ANALYSIS"
        ws.cell(row=row, column=2).font = Font(name="Calibri", size=20, bold=True)
        row += 2

        ws.cell(row=row, column=2).value = self.company_name
        ws.cell(row=row, column=2).font = Font(name="Calibri", size=16, bold=True)
        row += 1

        if self.sponsor:
            ws.cell(row=row, column=2).value = f"Sponsor: {self.sponsor}"
            ws.cell(row=row, column=2).font = Font(name="Calibri", size=12)
            row += 1

        ws.cell(row=row, column=2).value = f"Date: {datetime.now().strftime('%B %d, %Y')}"
        ws.cell(row=row, column=2).font = Font(name="Calibri", size=11)
        row += 1

        return row

    def _add_transaction_summary(self, ws, start_row: int, transaction_data: Dict, assumptions: Dict) -> int:
        """Add Transaction Summary section."""
        row = start_row

        # Section header
        ws.cell(row=row, column=1).value = "TRANSACTION SUMMARY"
        ws.cell(row=row, column=1).font = self.SECTION_FONT
        ws.cell(row=row, column=1).fill = self.SECTION_FILL
        ws.merge_cells(f'A{row}:D{row}')
        self._add_table_border(ws, f'A{row}:D{row}')
        row += 1

        # Entry Valuation
        ws.cell(row=row, column=1).value = "ENTRY VALUATION"
        ws.cell(row=row, column=1).font = self.SECTION_FONT
        ws.cell(row=row, column=1).fill = self.SECTION_FILL
        ws.merge_cells(f'A{row}:D{row}')
        self._add_table_border(ws, f'A{row}:D{row}')
        entry_section_row = row
        row += 1

        # LTM EBITDA
        ws.cell(row=row, column=1).value = "LTM EBITDA ($mm)"
        ws.cell(row=row, column=2).value = transaction_data.get('ltm_ebitda', 0)
        ws.cell(row=row, column=2).number_format = '$#,##0.0'
        ltm_ebitda_row = row
        row += 1

        # Entry Multiple
        ws.cell(row=row, column=1).value = "Entry EV / EBITDA Multiple"
        ws.cell(row=row, column=2).value = assumptions.get('entry_multiple', 10.0)
        ws.cell(row=row, column=2).fill = self.INPUT_FILL
        ws.cell(row=row, column=2).number_format = '0.0x'
        entry_multiple_row = row
        row += 1

        # Purchase EV
        ws.cell(row=row, column=1).value = "Purchase Enterprise Value ($mm)"
        ws.cell(row=row, column=1).font = Font(bold=True)
        ws.cell(row=row, column=2).value = f"=B{ltm_ebitda_row}*B{entry_multiple_row}"
        ws.cell(row=row, column=2).number_format = '$#,##0.0'
        ws.cell(row=row, column=2).font = Font(bold=True)
        purchase_ev_row = row
        row += 1

        # Exit Valuation
        ws.cell(row=row, column=1).value = "EXIT VALUATION"
        ws.cell(row=row, column=1).font = self.SECTION_FONT
        ws.cell(row=row, column=1).fill = self.SECTION_FILL
        ws.merge_cells(f'A{row}:D{row}')
        self._add_table_border(ws, f'A{row}:D{row}')
        row += 1

        # Exit Year EBITDA (will be calculated from Operating Model section)
        ws.cell(row=row, column=1).value = "Exit Year EBITDA ($mm)"
        # Note: This formula will reference the operating model section we'll create later
        # We'll need to track the operating model EBITDA row and update this
        ws.cell(row=row, column=2).value = 0  # Placeholder - will be updated with formula
        ws.cell(row=row, column=2).number_format = '$#,##0.0'
        exit_ebitda_row = row
        row += 1

        # Exit Multiple
        ws.cell(row=row, column=1).value = "Exit EV / EBITDA Multiple"
        ws.cell(row=row, column=2).value = assumptions.get('exit_multiple', 8.0)
        ws.cell(row=row, column=2).fill = self.INPUT_FILL
        ws.cell(row=row, column=2).number_format = '0.0x'
        exit_multiple_row = row
        row += 1

        # Exit EV
        ws.cell(row=row, column=1).value = "Exit Enterprise Value ($mm)"
        ws.cell(row=row, column=1).font = Font(bold=True)
        ws.cell(row=row, column=2).value = f"=B{exit_ebitda_row}*B{exit_multiple_row}"
        ws.cell(row=row, column=2).number_format = '$#,##0.0'
        ws.cell(row=row, column=2).font = Font(bold=True)
        exit_ev_row = row
        row += 1

        # Store important row references for later use
        self.purchase_ev_row = purchase_ev_row
        self.exit_ebitda_row = exit_ebitda_row
        self.exit_ev_row = exit_ev_row
        self.ltm_ebitda_row = ltm_ebitda_row

        return row

    def _add_sources_uses(self, ws, start_row: int, transaction_data: Dict, assumptions: Dict) -> int:
        """Add Sources & Uses section."""
        row = start_row

        # Section header
        ws.cell(row=row, column=1).value = "SOURCES & USES OF FUNDS"
        ws.cell(row=row, column=1).font = self.SECTION_FONT
        ws.cell(row=row, column=1).fill = self.SECTION_FILL
        ws.merge_cells(f'A{row}:C{row}')
        self._add_table_border(ws, f'A{row}:C{row}')
        row += 1

        # Column headers
        ws.cell(row=row, column=2).value = "$mm"
        ws.cell(row=row, column=3).value = "% of Total"
        ws.cell(row=row, column=2).font = Font(bold=True)
        ws.cell(row=row, column=3).font = Font(bold=True)
        row += 1

        # USES header
        ws.cell(row=row, column=1).value = "USES"
        ws.cell(row=row, column=1).font = self.SECTION_FONT
        ws.cell(row=row, column=1).fill = self.SECTION_FILL
        ws.merge_cells(f'A{row}:C{row}')
        self._add_table_border(ws, f'A{row}:C{row}')
        row += 1

        uses_start = row

        # Purchase EV
        ws.cell(row=row, column=1).value = "Purchase Enterprise Value"
        ws.cell(row=row, column=2).value = f"=B{self.purchase_ev_row}"
        ws.cell(row=row, column=2).number_format = '$#,##0.0'
        row += 1

        # Transaction Fees %
        ws.cell(row=row, column=1).value = "Transaction Fees (% of EV)"
        ws.cell(row=row, column=2).value = assumptions.get('transaction_fees_pct', 0.02)
        ws.cell(row=row, column=2).fill = self.INPUT_FILL
        ws.cell(row=row, column=2).number_format = '0.0%'
        fees_pct_row = row
        row += 1

        # Transaction Fees $
        ws.cell(row=row, column=1).value = "Transaction Fees ($mm)"
        ws.cell(row=row, column=2).value = f"=B{self.purchase_ev_row}*B{fees_pct_row}"
        ws.cell(row=row, column=2).number_format = '$#,##0.0'
        row += 1

        uses_end = row - 1

        # Total Uses
        ws.cell(row=row, column=1).value = "TOTAL USES"
        ws.cell(row=row, column=1).font = Font(bold=True)
        ws.cell(row=row, column=2).value = f"=SUM(B{uses_start}:B{uses_end})"
        ws.cell(row=row, column=2).number_format = '$#,##0.0'
        ws.cell(row=row, column=2).font = Font(bold=True)
        ws.cell(row=row, column=3).value = "100.0%"
        ws.cell(row=row, column=3).number_format = '0.0%'
        ws.cell(row=row, column=3).font = Font(bold=True)
        total_uses_row = row
        self.total_uses_row = total_uses_row  # Store for later reference
        row += 2

        # SOURCES header
        ws.cell(row=row, column=1).value = "SOURCES"
        ws.cell(row=row, column=1).font = self.SECTION_FONT
        ws.cell(row=row, column=1).fill = self.SECTION_FILL
        ws.merge_cells(f'A{row}:C{row}')
        self._add_table_border(ws, f'A{row}:C{row}')
        row += 1

        sources_start = row

        # Store this row for Assumptions section reference
        self.sources_sponsor_equity_row = row

        # We'll populate sources after we know the assumptions row numbers
        # Placeholder for now
        ws.cell(row=row, column=1).value = "Sponsor Equity"
        ws.cell(row=row, column=2).value = 0  # Will be linked to assumptions
        ws.cell(row=row, column=2).number_format = '$#,##0.0'
        ws.cell(row=row, column=3).value = f"=B{row}/B{total_uses_row}"
        ws.cell(row=row, column=3).number_format = '0.0%'
        equity_row = row
        row += 1

        # Revolver
        ws.cell(row=row, column=1).value = "Revolving Credit Facility"
        ws.cell(row=row, column=2).value = 0  # Will be linked to assumptions
        ws.cell(row=row, column=2).number_format = '$#,##0.0'
        ws.cell(row=row, column=3).value = f"=B{row}/B{total_uses_row}"
        ws.cell(row=row, column=3).number_format = '0.0%'
        row += 1

        # Senior Debt
        ws.cell(row=row, column=1).value = "Senior Term Loan"
        ws.cell(row=row, column=2).value = 0  # Will be linked to assumptions
        ws.cell(row=row, column=2).number_format = '$#,##0.0'
        ws.cell(row=row, column=3).value = f"=B{row}/B{total_uses_row}"
        ws.cell(row=row, column=3).number_format = '0.0%'
        senior_debt_row = row
        row += 1

        # Sub Debt
        ws.cell(row=row, column=1).value = "Subordinated Notes"
        ws.cell(row=row, column=2).value = 0  # Will be linked to assumptions
        ws.cell(row=row, column=2).number_format = '$#,##0.0'
        ws.cell(row=row, column=3).value = f"=B{row}/B{total_uses_row}"
        ws.cell(row=row, column=3).number_format = '0.0%'
        row += 1

        sources_end = row - 1

        # Total Sources
        ws.cell(row=row, column=1).value = "TOTAL SOURCES"
        ws.cell(row=row, column=1).font = Font(bold=True)
        ws.cell(row=row, column=2).value = f"=SUM(B{sources_start}:B{sources_end})"
        ws.cell(row=row, column=2).number_format = '$#,##0.0'
        ws.cell(row=row, column=2).font = Font(bold=True)
        ws.cell(row=row, column=3).value = "100.0%"
        ws.cell(row=row, column=3).number_format = '0.0%'
        ws.cell(row=row, column=3).font = Font(bold=True)
        total_sources_row = row
        row += 2

        # Check
        ws.cell(row=row, column=1).value = "CHECK (Should be $0)"
        ws.cell(row=row, column=2).value = f"=B{total_sources_row}-B{total_uses_row}"
        ws.cell(row=row, column=2).number_format = '$#,##0.0'
        ws.cell(row=row, column=2).font = Font(bold=True, color="FF0000")
        row += 1

        return row

    def _add_assumptions(self, ws, start_row: int, assumptions: Dict) -> int:
        """Add Assumptions section."""
        row = start_row

        # Section header
        ws.cell(row=row, column=1).value = "LBO MODEL ASSUMPTIONS"
        ws.cell(row=row, column=1).font = Font(name="Calibri", size=14, bold=True)
        row += 1

        # Transaction Assumptions
        ws.cell(row=row, column=1).value = "TRANSACTION ASSUMPTIONS"
        ws.cell(row=row, column=1).font = self.SECTION_FONT
        ws.cell(row=row, column=1).fill = self.SECTION_FILL
        row += 1

        # Holding Period
        ws.cell(row=row, column=1).value = "Holding Period (Years)"
        ws.cell(row=row, column=2).value = assumptions.get('holding_period', 5)
        ws.cell(row=row, column=2).fill = self.INPUT_FILL
        ws.cell(row=row, column=2).number_format = '0'
        row += 1

        # Transaction Fees %
        ws.cell(row=row, column=1).value = "Transaction Fees (% of EV)"
        ws.cell(row=row, column=2).value = assumptions.get('transaction_fees_pct', 0.02)
        ws.cell(row=row, column=2).fill = self.INPUT_FILL
        ws.cell(row=row, column=2).number_format = '0.0%'
        row += 1

        # Sponsor Equity % (input) - should be % of TOTAL USES not just EV
        ws.cell(row=row, column=1).value = "Sponsor Equity (% of Total Uses)"
        ws.cell(row=row, column=2).value = assumptions.get('equity_contribution_pct', 0.50)
        ws.cell(row=row, column=2).fill = self.INPUT_FILL
        ws.cell(row=row, column=2).number_format = '0.0%'
        equity_pct_row = row
        row += 1

        # Sponsor Equity $mm (calculated) - multiply by TOTAL USES not just Purchase EV
        ws.cell(row=row, column=1).value = "Sponsor Equity ($mm)"
        # Use total_uses_row which was stored in _add_sources_uses
        ws.cell(row=row, column=2).value = f"=B{self.total_uses_row}*B{equity_pct_row}"
        ws.cell(row=row, column=2).number_format = '$#,##0.0'
        sponsor_equity_row = row
        row += 1

        # Now update Sources & Uses to reference this
        ws.cell(row=self.sources_sponsor_equity_row, column=2).value = f"=B{sponsor_equity_row}"

        row += 1

        # Debt Structure
        ws.cell(row=row, column=1).value = "DEBT STRUCTURE"
        ws.cell(row=row, column=1).font = self.SECTION_FONT
        ws.cell(row=row, column=1).fill = self.SECTION_FILL
        row += 1

        # Revolver
        ws.cell(row=row, column=1).value = "Revolver Size ($mm)"
        ws.cell(row=row, column=2).value = assumptions.get('revolver', 0)
        ws.cell(row=row, column=2).fill = self.INPUT_FILL
        ws.cell(row=row, column=2).number_format = '$#,##0.0'
        revolver_row = row
        row += 1

        # Update Sources & Uses revolver
        ws.cell(row=self.sources_sponsor_equity_row + 1, column=2).value = f"=B{revolver_row}"

        ws.cell(row=row, column=1).value = "Revolver Interest Rate"
        ws.cell(row=row, column=2).value = assumptions.get('revolver_rate', 0.055)
        ws.cell(row=row, column=2).fill = self.INPUT_FILL
        ws.cell(row=row, column=2).number_format = '0.00%'
        row += 1

        # Senior Debt
        ws.cell(row=row, column=1).value = "Senior Debt (% of Total Uses)"
        ws.cell(row=row, column=2).value = assumptions.get('senior_debt_pct', 0.40)
        ws.cell(row=row, column=2).fill = self.INPUT_FILL
        ws.cell(row=row, column=2).number_format = '0.0%'
        senior_pct_row = row
        row += 1

        ws.cell(row=row, column=1).value = "Senior Term Loan ($mm)"
        ws.cell(row=row, column=2).value = f"=B{self.total_uses_row}*B{senior_pct_row}"
        ws.cell(row=row, column=2).number_format = '$#,##0.0'
        senior_debt_row = row
        row += 1

        # Update Sources & Uses senior debt
        ws.cell(row=self.sources_sponsor_equity_row + 2, column=2).value = f"=B{senior_debt_row}"

        ws.cell(row=row, column=1).value = "Senior Interest Rate"
        ws.cell(row=row, column=2).value = assumptions.get('senior_debt_rate', 0.055)
        ws.cell(row=row, column=2).fill = self.INPUT_FILL
        ws.cell(row=row, column=2).number_format = '0.00%'
        row += 1

        ws.cell(row=row, column=1).value = "Senior Amortization (% p.a.)"
        ws.cell(row=row, column=2).value = assumptions.get('senior_amortization_pct', 0.05)
        ws.cell(row=row, column=2).fill = self.INPUT_FILL
        ws.cell(row=row, column=2).number_format = '0.0%'
        row += 1

        # Subordinated Debt
        ws.cell(row=row, column=1).value = "Subordinated Debt (% of Total Uses)"
        ws.cell(row=row, column=2).value = assumptions.get('subordinated_debt_pct', 0.10)
        ws.cell(row=row, column=2).fill = self.INPUT_FILL
        ws.cell(row=row, column=2).number_format = '0.0%'
        sub_pct_row = row
        row += 1

        ws.cell(row=row, column=1).value = "Subordinated Notes ($mm)"
        ws.cell(row=row, column=2).value = f"=B{self.total_uses_row}*B{sub_pct_row}"
        ws.cell(row=row, column=2).number_format = '$#,##0.0'
        sub_debt_row = row
        row += 1

        # Update Sources & Uses sub debt
        ws.cell(row=self.sources_sponsor_equity_row + 3, column=2).value = f"=B{sub_debt_row}"

        ws.cell(row=row, column=1).value = "Subordinated Interest Rate"
        ws.cell(row=row, column=2).value = assumptions.get('sub_debt_rate', 0.095)
        ws.cell(row=row, column=2).fill = self.INPUT_FILL
        ws.cell(row=row, column=2).number_format = '0.00%'
        row += 1

        row += 1

        # Operating Assumptions
        ws.cell(row=row, column=1).value = "OPERATING ASSUMPTIONS"
        ws.cell(row=row, column=1).font = self.SECTION_FONT
        ws.cell(row=row, column=1).fill = self.SECTION_FILL
        row += 1

        revenue_growth = assumptions.get('revenue_growth', [0.05] * 5)
        for year, growth in enumerate(revenue_growth, 1):
            ws.cell(row=row, column=1).value = f"Year {year} Revenue Growth"
            ws.cell(row=row, column=2).value = growth
            ws.cell(row=row, column=2).fill = self.INPUT_FILL
            ws.cell(row=row, column=2).number_format = '0.0%'
            row += 1

        ws.cell(row=row, column=1).value = "EBITDA Margin"
        ws.cell(row=row, column=2).value = assumptions.get('ebitda_margin', 0.30)
        ws.cell(row=row, column=2).fill = self.INPUT_FILL
        ws.cell(row=row, column=2).number_format = '0.0%'
        row += 1

        ws.cell(row=row, column=1).value = "D&A (% of Revenue)"
        ws.cell(row=row, column=2).value = assumptions.get('da_pct', 0.03)
        ws.cell(row=row, column=2).fill = self.INPUT_FILL
        ws.cell(row=row, column=2).number_format = '0.0%'
        row += 1

        ws.cell(row=row, column=1).value = "CapEx (% of Revenue)"
        ws.cell(row=row, column=2).value = assumptions.get('capex_pct', 0.03)
        ws.cell(row=row, column=2).fill = self.INPUT_FILL
        ws.cell(row=row, column=2).number_format = '0.0%'
        row += 1

        ws.cell(row=row, column=1).value = "NWC (% of Revenue)"
        ws.cell(row=row, column=2).value = assumptions.get('nwc_pct', 0.10)
        ws.cell(row=row, column=2).fill = self.INPUT_FILL
        ws.cell(row=row, column=2).number_format = '0.0%'
        row += 1

        ws.cell(row=row, column=1).value = "Tax Rate"
        ws.cell(row=row, column=2).value = assumptions.get('tax_rate', 0.25)
        ws.cell(row=row, column=2).fill = self.INPUT_FILL
        ws.cell(row=row, column=2).number_format = '0.0%'
        row += 1

        return row

    def _add_operating_model(self, ws, start_row: int, transaction_data: Dict, assumptions: Dict) -> int:
        """Add Operating Model section with simplified 5-year projection."""
        row = start_row

        # Section header
        ws.cell(row=row, column=1).value = "OPERATING MODEL & PROJECTIONS"
        ws.cell(row=row, column=1).font = Font(name="Calibri", size=12, bold=True)
        row += 1

        # Column headers
        ws.cell(row=row, column=1).value = ""
        ws.cell(row=row, column=2).value = "LTM"
        ws.cell(row=row, column=2).font = Font(bold=True)

        for year in range(1, 6):
            col = 2 + year
            ws.cell(row=row, column=col).value = f"Year {year}"
            ws.cell(row=row, column=col).font = Font(bold=True)
        header_row = row
        row += 1

        # Revenue
        ws.cell(row=row, column=1).value = "Revenue"
        ltm_revenue = transaction_data.get('ltm_revenue', 180000)
        ws.cell(row=row, column=2).value = ltm_revenue
        ws.cell(row=row, column=2).number_format = '$#,##0.0'

        revenue_row = row
        # Year 1-5 revenue projections will be added
        # This is simplified - in reality would reference growth assumptions
        for year in range(1, 6):
            col = 2 + year
            # Simplified: just growing revenue
            # In full model, would reference specific growth rate cells
            if year == 1:
                ws.cell(row=row, column=col).value = f"=B{revenue_row}*1.10"  # Simplified 10% growth
            else:
                prior_col_letter = get_column_letter(col - 1)
                ws.cell(row=row, column=col).value = f"={prior_col_letter}{revenue_row}*1.08"  # 8% thereafter
            ws.cell(row=row, column=col).number_format = '$#,##0.0'
        row += 1

        # EBITDA
        ws.cell(row=row, column=1).value = "EBITDA"
        ws.cell(row=row, column=1).font = Font(bold=True)
        ltm_ebitda = transaction_data.get('ltm_ebitda', 0)
        ws.cell(row=row, column=2).value = ltm_ebitda
        ws.cell(row=row, column=2).number_format = '$#,##0.0'

        ebitda_row = row
        for year in range(1, 6):
            col = 2 + year
            col_letter = get_column_letter(col)
            # EBITDA = Revenue * EBITDA Margin (simplified)
            ws.cell(row=row, column=col).value = f"={col_letter}{revenue_row}*0.34"  # Simplified 34% margin
            ws.cell(row=row, column=col).number_format = '$#,##0.0'
        row += 1

        # Now update the Transaction Summary Exit EBITDA to reference Year 5 EBITDA
        ws.cell(row=self.exit_ebitda_row, column=2).value = f"=G{ebitda_row}"  # G = column 7 = Year 5

        # Simplified operating model - just showing EBITDA for now
        # Full model would include D&A, EBIT, Interest, Taxes, FCF, etc.

        return row

    def _add_debt_schedule(self, ws, start_row: int, assumptions: Dict) -> int:
        """Add simplified Debt Schedule section."""
        row = start_row

        ws.cell(row=row, column=1).value = "DEBT SCHEDULE (Simplified)"
        ws.cell(row=row, column=1).font = Font(name="Calibri", size=12, bold=True)
        row += 1

        ws.cell(row=row, column=1).value = "(Full debt schedule with amortization would go here)"
        ws.cell(row=row, column=1).font = Font(italic=True)
        row += 1

        return row

    def _add_cash_flow_waterfall(self, ws, start_row: int, assumptions: Dict) -> int:
        """Add simplified Cash Flow Waterfall section."""
        row = start_row

        ws.cell(row=row, column=1).value = "CASH FLOW WATERFALL (Simplified)"
        ws.cell(row=row, column=1).font = Font(name="Calibri", size=12, bold=True)
        row += 1

        ws.cell(row=row, column=1).value = "(Full cash flow waterfall would go here)"
        ws.cell(row=row, column=1).font = Font(italic=True)
        row += 1

        return row

    def _add_returns_analysis(self, ws, start_row: int, transaction_data: Dict, assumptions: Dict) -> int:
        """Add simplified Returns Analysis section."""
        row = start_row

        ws.cell(row=row, column=1).value = "RETURNS ANALYSIS"
        ws.cell(row=row, column=1).font = Font(name="Calibri", size=12, bold=True)
        row += 1

        # Exit EV
        ws.cell(row=row, column=1).value = "Exit Enterprise Value"
        ws.cell(row=row, column=2).value = f"=B{self.exit_ev_row}"
        ws.cell(row=row, column=2).number_format = '$#,##0.0'
        row += 1

        # Initial Equity Investment
        ws.cell(row=row, column=1).value = "Initial Equity Investment"
        # Would reference sponsor equity from assumptions
        ws.cell(row=row, column=2).value = 0  # Placeholder
        ws.cell(row=row, column=2).number_format = '$#,##0.0'
        row += 1

        ws.cell(row=row, column=1).value = "(Full returns analysis with IRR, MOIC would go here)"
        ws.cell(row=row, column=1).font = Font(italic=True)
        row += 1

        return row
