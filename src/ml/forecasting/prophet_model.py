"""
Facebook Prophet Forecasting

Time series forecasting using Facebook's Prophet algorithm.

Features:
- Automatic seasonality detection
- Holiday effects
- Changepoint detection
- Uncertainty intervals

Example:
    >>> from src.ml.forecasting.prophet_model import ProphetForecaster
    >>> forecaster = ProphetForecaster()
    >>> forecaster.fit(dates, revenue)
    >>> forecast = forecaster.predict(periods=12)
"""

from typing import Dict, List, Optional
import pandas as pd


class ProphetForecaster:
    """
    Prophet-based revenue forecasting.

    Wrapper around Facebook Prophet for time series forecasting
    with automatic seasonality and trend detection.
    """

    def __init__(
        self,
        yearly_seasonality: bool = True,
        weekly_seasonality: bool = False,
        daily_seasonality: bool = False
    ):
        """
        Initialize Prophet forecaster.

        Args:
            yearly_seasonality: Include yearly seasonal component
            weekly_seasonality: Include weekly seasonal component
            daily_seasonality: Include daily seasonal component
        """
        self.yearly_seasonality = yearly_seasonality
        self.weekly_seasonality = weekly_seasonality
        self.daily_seasonality = daily_seasonality
        self.model = None

    def fit(
        self,
        dates: pd.DatetimeIndex,
        values: pd.Series,
        holidays: Optional[pd.DataFrame] = None
    ):
        """
        Fit Prophet model to historical data.

        Args:
            dates: Datetime index
            values: Revenue or metric values
            holidays: Optional holiday dataframe
        """
        # Placeholder - requires prophet package
        raise NotImplementedError(
            "Prophet forecasting requires prophet package. "
            "Install with: pip install prophet"
        )

    def predict(self, periods: int, freq: str = 'M') -> pd.DataFrame:
        """
        Generate forecast.

        Args:
            periods: Number of periods to forecast
            freq: Frequency ('D', 'W', 'M', 'Q', 'Y')

        Returns:
            DataFrame with predictions and confidence intervals
        """
        raise NotImplementedError()

    def plot_components(self):
        """Plot trend, seasonality, and holiday components."""
        raise NotImplementedError()


# TODO: Implement Prophet integration
# TODO: Add custom seasonality
# TODO: Implement growth cap (saturation)
# TODO: Add external regressors support
