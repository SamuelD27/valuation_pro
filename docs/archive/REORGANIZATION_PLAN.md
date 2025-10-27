# File Reorganization Plan

## Goal
Keep only single-sheet versions and rename them (remove "_single_sheet" suffix).

## Files to Rename

### Tools (src/tools/)
- `dcf_tool_single_sheet.py` → `dcf_tool.py` (replace old)
- `lbo_tool_single_sheet.py` → `lbo_tool.py` (replace old)

### Example Scripts (scripts/examples/)
- `example_dcf_single_sheet.py` → `example_dcf.py` (replace old)
- `example_lbo_single_sheet.py` → `example_lbo.py` (replace old)

## Files to Remove
- `src/tools/dcf_tool.py` (old multi-sheet version)
- `src/tools/lbo_tool.py` (old multi-sheet version)
- `scripts/examples/example_dcf_tool.py` (old version)
- `scripts/examples/example_lbo_tool.py` (old version)
- `scripts/examples/example_dcf.py` (old version - will be replaced)

## Execution Steps
1. Backup old files (to OLD_VERSIONS folder)
2. Rename single_sheet versions to standard names
3. Update import statements in all files
4. Update class names (remove "SingleSheet")
5. Test all example scripts
