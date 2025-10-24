"""
Formula Builder - Excel Formula Construction Utilities

Helper functions for building Excel formulas programmatically.
Ensures consistent formula syntax and proper cell/sheet references.

Key Principles:
1. All formulas start with '='
2. Sheet references use 'SheetName'!CellAddress format
3. Absolute references use $ for fixed rows/columns
4. Relative references allow fill-across/fill-down
"""

from openpyxl.utils import get_column_letter
from typing import Union, List


class FormulaBuilder:
    """Helper class for building Excel formulas."""

    @staticmethod
    def cell_ref(row: int, col: Union[int, str], absolute_row: bool = False, absolute_col: bool = False) -> str:
        """
        Build cell reference (e.g., 'A1', '$A$1', 'A$1', '$A1').

        Args:
            row: Row number (1-indexed)
            col: Column number (1-indexed) or letter
            absolute_row: Make row absolute with $
            absolute_col: Make column absolute with $

        Returns:
            Cell reference string

        Examples:
            >>> cell_ref(1, 1) -> 'A1'
            >>> cell_ref(1, 1, absolute_row=True) -> 'A$1'
            >>> cell_ref(1, 1, absolute_row=True, absolute_col=True) -> '$A$1'
        """
        # Convert column to letter if needed
        if isinstance(col, int):
            col_letter = get_column_letter(col)
        else:
            col_letter = col

        # Add $ for absolute references
        if absolute_col:
            col_letter = f"${col_letter}"
        if absolute_row:
            row = f"${row}"

        return f"{col_letter}{row}"

    @staticmethod
    def range_ref(start_row: int, start_col: int, end_row: int, end_col: int) -> str:
        """
        Build range reference (e.g., 'A1:D10').

        Args:
            start_row: Starting row (1-indexed)
            start_col: Starting column (1-indexed)
            end_row: Ending row (1-indexed)
            end_col: Ending column (1-indexed)

        Returns:
            Range reference string
        """
        start_cell = FormulaBuilder.cell_ref(start_row, start_col)
        end_cell = FormulaBuilder.cell_ref(end_row, end_col)
        return f"{start_cell}:{end_cell}"

    @staticmethod
    def sheet_ref(sheet_name: str, cell_ref: str) -> str:
        """
        Build cross-sheet reference (e.g., 'Income Statement'!A1).

        Args:
            sheet_name: Name of sheet
            cell_ref: Cell or range reference

        Returns:
            Sheet reference string

        Examples:
            >>> sheet_ref('Income Statement', 'H89') -> "'Income Statement'!H89"
            >>> sheet_ref('DCF', 'A1:D10') -> "'DCF'!A1:D10"
        """
        # Add quotes if sheet name contains spaces
        if ' ' in sheet_name:
            return f"'{sheet_name}'!{cell_ref}"
        else:
            return f"{sheet_name}!{cell_ref}"

    @staticmethod
    def sum_formula(range_ref: str) -> str:
        """
        Build SUM formula.

        Args:
            range_ref: Range reference

        Returns:
            Formula string with =
        """
        return f"=SUM({range_ref})"

    @staticmethod
    def choose_formula(index_ref: str, values: List[str], absolute_index: bool = True) -> str:
        """
        Build CHOOSE formula for scenario switching.

        Args:
            index_ref: Cell reference for index (e.g., 'B2')
            values: List of values/references for each scenario
            absolute_index: Make index reference absolute (default True)

        Returns:
            Formula string with =

        Example:
            >>> choose_formula('B2', ['H14', 'H15', 'H16'])
            '=CHOOSE($B$2, H14, H15, H16)'
        """
        # Make index absolute if requested
        if absolute_index and '$' not in index_ref:
            # Parse cell ref and make it absolute
            # Simple approach: if it's like 'B2', convert to '$B$2'
            if index_ref[0] != '$':
                index_ref = f"${index_ref[0]}${index_ref[1:]}"

        values_str = ', '.join(values)
        return f"=CHOOSE({index_ref}, {values_str})"

    @staticmethod
    def growth_formula(current_ref: str, prior_ref: str) -> str:
        """
        Build growth % formula (Current / Prior - 1).

        Args:
            current_ref: Current period cell reference
            prior_ref: Prior period cell reference

        Returns:
            Formula string with =
        """
        return f"={current_ref}/{prior_ref}-1"

    @staticmethod
    def if_formula(condition: str, value_if_true: str, value_if_false: str) -> str:
        """
        Build IF formula.

        Args:
            condition: Condition to test
            value_if_true: Value if condition is true
            value_if_false: Value if condition is false

        Returns:
            Formula string with =
        """
        return f"=IF({condition}, {value_if_true}, {value_if_false})"

    @staticmethod
    def simple_formula(expression: str) -> str:
        """
        Build simple arithmetic formula.

        Args:
            expression: Formula expression (without =)

        Returns:
            Formula string with =

        Examples:
            >>> simple_formula('A1+A2') -> '=A1+A2'
            >>> simple_formula('B5*C5') -> '=B5*C5'
        """
        if expression.startswith('='):
            return expression
        return f"={expression}"

    @staticmethod
    def multiply(*refs: str) -> str:
        """
        Build multiplication formula.

        Args:
            *refs: Cell references to multiply

        Returns:
            Formula string with =
        """
        return f"={'*'.join(refs)}"

    @staticmethod
    def divide(numerator: str, denominator: str) -> str:
        """
        Build division formula.

        Args:
            numerator: Numerator cell reference
            denominator: Denominator cell reference

        Returns:
            Formula string with =
        """
        return f"={numerator}/{denominator}"

    @staticmethod
    def subtract(*refs: str) -> str:
        """
        Build subtraction formula.

        Args:
            *refs: Cell references to subtract (first - second - third...)

        Returns:
            Formula string with =
        """
        return f"={'-'.join(refs)}"

    @staticmethod
    def add(*refs: str) -> str:
        """
        Build addition formula.

        Args:
            *refs: Cell references to add

        Returns:
            Formula string with =
        """
        return f"={'+'.join(refs)}"


# Convenience functions for common patterns

def year_increment_formula(prior_year_cell: str) -> str:
    """
    Create formula for incrementing year (e.g., =D4+1).

    Args:
        prior_year_cell: Previous year cell reference

    Returns:
        Formula string
    """
    return f"={prior_year_cell}+1"


def revenue_formula(volume_ref: str, price_ref: str) -> str:
    """
    Create revenue formula (Volume × Price).

    Args:
        volume_ref: Volume cell reference
        price_ref: Price cell reference

    Returns:
        Formula string
    """
    return FormulaBuilder.multiply(volume_ref, price_ref)


def margin_formula(numerator_ref: str, denominator_ref: str) -> str:
    """
    Create margin % formula (Item / Revenue).

    Args:
        numerator_ref: Numerator (e.g., EBIT) cell reference
        denominator_ref: Denominator (revenue) cell reference

    Returns:
        Formula string
    """
    return FormulaBuilder.divide(numerator_ref, denominator_ref)


def working_capital_formula(days: str, annual_value: str) -> str:
    """
    Create working capital formula (Days/365 × Annual Value).

    Args:
        days: Days cell reference (DSO, DIO, or DPO)
        annual_value: Annual value cell reference (Revenue or COGS)

    Returns:
        Formula string
    """
    return f"={days}/365*{annual_value}"


def fcf_formula(ebit: str, tax: str, da: str, capex: str, nwc_change: str) -> str:
    """
    Create Free Cash Flow formula.

    FCF = EBIT × (1 - Tax Rate) + D&A - CapEx - ΔNWC

    Args:
        ebit: EBIT cell reference
        tax: Tax rate cell reference
        da: D&A cell reference
        capex: CapEx cell reference
        nwc_change: NWC change cell reference

    Returns:
        Formula string
    """
    return f"={ebit}*(1-{tax})+{da}-{capex}-{nwc_change}"


def discount_factor_formula(period: str, wacc: str) -> str:
    """
    Create discount factor formula: 1/(1+WACC)^Period.

    Args:
        period: Period number cell reference
        wacc: WACC cell reference (should be absolute)

    Returns:
        Formula string
    """
    return f"=1/(1+{wacc})^{period}"


def terminal_value_formula(final_fcf: str, growth: str, wacc: str) -> str:
    """
    Create terminal value formula: FCF × (1+g) / (WACC - g).

    Args:
        final_fcf: Final year FCF cell reference
        growth: Terminal growth rate cell reference
        wacc: WACC cell reference

    Returns:
        Formula string
    """
    return f"={final_fcf}*(1+{growth})/({wacc}-{growth})"
