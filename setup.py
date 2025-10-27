from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="valuationpro",
    version="0.1.0",
    author="ValuationPro Team",
    description="Investment banking-quality company valuation models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "yfinance>=0.2.0",
        "fredapi>=0.5.0",
        "openpyxl>=3.1.0",
        "numpy-financial>=1.0.0",
        "python-dotenv>=1.0.0",
        "requests>=2.31.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
        "ml": [
            "scikit-learn>=1.3.0",
            "xgboost>=2.0.0",
            "tensorflow>=2.13.0",  # For LSTM models
            "prophet>=1.1.0",  # For time series forecasting
        ],
        "llm": [
            "anthropic>=0.18.0",  # Claude API
            "pypdf>=3.0.0",  # PDF processing
            "tiktoken>=0.5.0",  # Token counting
        ],
        "viz": [
            "matplotlib>=3.7.0",
            "seaborn>=0.12.0",
            "plotly>=5.14.0",
            "streamlit>=1.28.0",  # Interactive dashboards
        ],
        "all": [
            # All optional dependencies
            "scikit-learn>=1.3.0",
            "xgboost>=2.0.0",
            "tensorflow>=2.13.0",
            "prophet>=1.1.0",
            "anthropic>=0.18.0",
            "pypdf>=3.0.0",
            "tiktoken>=0.5.0",
            "matplotlib>=3.7.0",
            "seaborn>=0.12.0",
            "plotly>=5.14.0",
            "streamlit>=1.28.0",
        ],
    },
)
