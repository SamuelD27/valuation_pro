"""
Probability Distributions

Provides probability distribution models for Monte Carlo simulations.

Supported Distributions:
- Normal (Gaussian)
- Lognormal
- Triangular
- Uniform
- Beta
- Custom empirical distributions

Example:
    >>> from src.analytics.distributions import NormalDistribution
    >>> revenue_dist = NormalDistribution(mean=100, std=10)
    >>> samples = revenue_dist.sample(1000)
"""

import numpy as np
from abc import ABC, abstractmethod
from typing import Optional


class Distribution(ABC):
    """Base class for probability distributions."""

    @abstractmethod
    def sample(self, n: int) -> np.ndarray:
        """Generate n random samples from distribution."""
        pass

    @abstractmethod
    def pdf(self, x: np.ndarray) -> np.ndarray:
        """Probability density function."""
        pass


class NormalDistribution(Distribution):
    """Normal (Gaussian) distribution."""

    def __init__(self, mean: float, std: float):
        self.mean = mean
        self.std = std

    def sample(self, n: int) -> np.ndarray:
        """Generate n samples from normal distribution."""
        return np.random.normal(self.mean, self.std, n)

    def pdf(self, x: np.ndarray) -> np.ndarray:
        """Normal probability density function."""
        # Placeholder
        raise NotImplementedError()


class TriangularDistribution(Distribution):
    """Triangular distribution for optimistic/base/pessimistic scenarios."""

    def __init__(self, low: float, mode: float, high: float):
        self.low = low
        self.mode = mode
        self.high = high

    def sample(self, n: int) -> np.ndarray:
        """Generate n samples from triangular distribution."""
        return np.random.triangular(self.low, self.mode, self.high, n)

    def pdf(self, x: np.ndarray) -> np.ndarray:
        """Triangular probability density function."""
        raise NotImplementedError()


# TODO: Implement LogNormalDistribution
# TODO: Implement BetaDistribution
# TODO: Implement UniformDistribution
# TODO: Add distribution fitting from historical data
