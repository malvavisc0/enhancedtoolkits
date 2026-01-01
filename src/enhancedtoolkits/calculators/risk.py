"""
Risk Metrics Calculator

Provides risk metrics calculations including Sharpe ratio and volatility calculations.
"""

import statistics
from typing import List

from .base import (
    BaseCalculatorTools,
    FinancialComputationError,
    FinancialValidationError,
)


class RiskMetricsCalculatorTools(BaseCalculatorTools):
    """Calculator for risk metrics calculations."""

    def __init__(self, add_instructions: bool = True, **kwargs):
        """Initialize the risk metrics calculator and register all methods."""
        instructions = (
            self.get_llm_usage_instructions() if add_instructions else ""
        )
        super().__init__(
            name="risk_metrics_calculator",
            add_instructions=add_instructions,
            instructions=instructions,
            **kwargs,
        )

        self.register(self.calculate_sharpe_ratio)
        self.register(self.calculate_volatility)
        self.register(self.calculate_beta)
        self.register(self.calculate_value_at_risk)

    def calculate_sharpe_ratio(
        self, returns: List[float], risk_free_rate: float
    ) -> str:
        """
        Calculate the Sharpe ratio for an investment.

        Args:
            returns: List of periodic returns (as decimals)
            risk_free_rate: Risk-free rate per period (as decimal)

        Returns:
            JSON string containing Sharpe ratio calculation
        """
        try:
            returns = self._validate_returns_list(returns)
            risk_free_rate = self._validate_rate(risk_free_rate)

            if len(returns) < 2:
                raise FinancialValidationError(
                    "At least 2 return observations required"
                )

            mean_return = statistics.mean(returns)
            std_deviation = statistics.stdev(returns)

            if std_deviation == 0:
                raise FinancialComputationError(
                    "Cannot calculate Sharpe ratio with zero volatility"
                )

            excess_return = mean_return - risk_free_rate
            sharpe_ratio = excess_return / std_deviation

            result = {
                "operation": "sharpe_ratio",
                "result": round(sharpe_ratio, 4),
                "inputs": {
                    "returns": returns,
                    "risk_free_rate": risk_free_rate,
                    "observations": len(returns),
                },
                "summary": {
                    "sharpe_ratio": round(sharpe_ratio, 4),
                    "mean_return": round(mean_return, 4),
                    "volatility": round(std_deviation, 4),
                    "excess_return": round(excess_return, 4),
                },
                "metadata": self._base_metadata("sharpe_ratio_formula"),
            }

            return self._format_json_response(result)

        except (TypeError, ValueError, OverflowError, ZeroDivisionError) as e:
            self._log_unexpected_error("Failed to calculate Sharpe ratio", e)
            raise FinancialComputationError(
                f"Failed to calculate Sharpe ratio: {e}"
            ) from e

    def calculate_volatility(self, returns: List[float]) -> str:
        """
        Calculate the volatility (standard deviation) of returns.

        Args:
            returns: List of periodic returns (as decimals)

        Returns:
            JSON string containing volatility calculation
        """
        try:
            returns = self._validate_returns_list(returns)

            if len(returns) < 2:
                raise FinancialValidationError(
                    "At least 2 return observations required"
                )

            mean_return = statistics.mean(returns)
            volatility = statistics.stdev(returns)
            variance = statistics.variance(returns)

            result = {
                "operation": "volatility",
                "result": round(volatility, 6),
                "result_percentage": round(volatility * 100, 4),
                "inputs": {"returns": returns, "observations": len(returns)},
                "summary": {
                    "volatility_decimal": round(volatility, 6),
                    "volatility_percentage": round(volatility * 100, 4),
                    "variance": round(variance, 6),
                    "mean_return": round(mean_return, 4),
                },
                "metadata": self._base_metadata("standard_deviation"),
            }

            return self._format_json_response(result)

        except (TypeError, ValueError, OverflowError, ZeroDivisionError) as e:
            self._log_unexpected_error("Failed to calculate volatility", e)
            raise FinancialComputationError(
                f"Failed to calculate volatility: {e}"
            ) from e

    def calculate_beta(
        self, asset_returns: List[float], market_returns: List[float]
    ) -> str:
        """Calculate beta of an asset vs a market benchmark."""
        asset_returns = self._validate_returns_list(asset_returns)
        market_returns = self._validate_returns_list(market_returns)

        if len(asset_returns) != len(market_returns):
            raise FinancialValidationError(
                "asset_returns and market_returns must have the same length"
            )
        if len(asset_returns) < 2:
            raise FinancialValidationError("At least 2 observations required")

        mean_asset = statistics.mean(asset_returns)
        mean_market = statistics.mean(market_returns)

        cov = sum(
            (a - mean_asset) * (m - mean_market)
            for a, m in zip(asset_returns, market_returns)
        ) / (len(asset_returns) - 1)

        var_market = statistics.variance(market_returns)
        if var_market == 0:
            raise FinancialComputationError(
                "Cannot compute beta with zero market variance"
            )

        beta = cov / var_market

        return self._format_json_response(
            {
                "operation": "beta",
                "result": round(beta, 6),
                "inputs": {
                    "observations": len(asset_returns),
                },
                "summary": {
                    "beta": round(beta, 6),
                    "asset_mean": round(mean_asset, 6),
                    "market_mean": round(mean_market, 6),
                },
                "metadata": self._base_metadata("covariance_over_variance"),
            }
        )

    def calculate_value_at_risk(
        self, returns: List[float], confidence_level: float = 0.95
    ) -> str:
        """Historical Value-at-Risk (VaR).

        Returns are decimals (e.g. -0.02 for -2%).
        """
        returns = self._validate_returns_list(returns)

        if len(returns) < 2:
            raise FinancialValidationError("At least 2 observations required")
        if not 0 < confidence_level < 1:
            raise FinancialValidationError(
                "confidence_level must be between 0 and 1"
            )

        sorted_returns = sorted(returns)
        # VaR at 95% uses the 5th percentile loss.
        idx = max(0, int((1 - confidence_level) * len(sorted_returns)) - 1)
        var_return = sorted_returns[idx]

        return self._format_json_response(
            {
                "operation": "value_at_risk",
                "result": round(var_return, 6),
                "result_percentage": round(var_return * 100, 4),
                "inputs": {
                    "observations": len(returns),
                    "confidence_level": confidence_level,
                },
                "metadata": self._base_metadata("historical_var"),
            }
        )

    @staticmethod
    def get_llm_usage_instructions() -> str:
        """Return short, text-first usage instructions for risk tools."""
        return """
<risk_metrics_calculator>
Risk metrics (Sharpe/volatility/beta/VaR)

GOAL
- Compute portfolio risk metrics from small return series and return JSON.

Risk metrics. Tools return JSON strings.

Tools:
- calculate_sharpe_ratio(returns, risk_free_rate)
- calculate_volatility(returns)
- calculate_beta(asset_returns, market_returns)
- calculate_value_at_risk(returns, confidence_level=0.95)

Notes:
- `returns` are decimals per period (e.g. 0.01 for +1%).
- VaR is historical (quantile of returns).

CONTEXT-SIZE RULES (IMPORTANT)
- Keep returns lists reasonably small; do not pass huge arrays.
- In final user responses, summarize the metric(s) instead of pasting full JSON.
</risk_metrics_calculator>
"""
