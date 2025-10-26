┌─────────────────────────────────────────────────────────────┐
│                    USER INPUT LAYER                          │
│  - Excel files (any structure)                               │
│  - PDF reports (10-K, technical reports, presentations)      │
│  - Web sources (yfinance, SEC EDGAR, company websites)       │
│  - User prompts/context (industry, special circumstances)    │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│           INTELLIGENT EXTRACTION ORCHESTRATOR                │
│  • Route to appropriate extractor based on file type         │
│  • Manage extraction workflow                                │
│  • Handle errors and fallbacks                               │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
┌───────▼──────┐  ┌───▼────────┐  ┌─▼──────────┐
│ Excel        │  │ PDF        │  │ Web API    │
│ Extractor    │  │ Extractor  │  │ Extractor  │
│              │  │            │  │            │
│ - Layout     │  │ - PyPDF2   │  │ - yfinance │
│   detection  │  │ - pdfplumber│  │ - SEC API  │
│ - Table      │  │ - Camelot  │  │ - FRED     │
│   finder     │  │ - OCR      │  │ - Alpha    │
│ - Smart      │  │ - LLM for  │  │   Vantage  │
│   mapping    │  │   parsing  │  │            │
└───────┬──────┘  └───┬────────┘  └─┬──────────┘
        │             │              │
        └─────────────┼──────────────┘
                      │
┌─────────────────────▼──────────────────────────────────────┐
│              DATA NORMALIZATION LAYER                        │
│  • Map extracted data to standard schema                     │
│  • Unit conversion (thousands, millions, billions)           │
│  • Currency conversion                                       │
│  • Date/period alignment (fiscal years, quarters)           │
│  • Handle missing data (mark as None, estimate, or fail)    │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│         DATA VALIDATION & QUALITY CHECKS                     │
│  • Sanity checks (revenue > 0, margins in range)            │
│  • Consistency checks (BS balances, CF reconciliation)       │
│  • Outlier detection (z-scores, IQR)                        │
│  • Completeness scoring (% of required fields present)      │
│  • Flag anomalies for user review                           │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│          INTELLIGENT REASONING ENGINE                        │
│  🧠 LLM-Powered Adjustment Layer                            │
│                                                              │
│  Input: Normalized data + Context (industry, news, etc.)    │
│  Output: Adjusted assumptions + Rationale                    │
│                                                              │
│  • Debt structure adjustments                               │
│  • WACC component adjustments (beta, risk premium)          │
│  • Industry-specific modifications                          │
│  • Company-specific events (M&A, restructuring, IPO)        │
│  • Macroeconomic considerations (rates, recession risk)     │
│  • Comparable selection and screening                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│             VALUATION MODEL INTERFACE                        │
│  • Standard FinancialData object                            │
│  • Feed into existing DCF/LBO/Comps tools                   │
│  • Include adjustment notes/audit trail                     │
└─────────────────────────────────────────────────────────────┘