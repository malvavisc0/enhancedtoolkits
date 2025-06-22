"""
Risk Metrics Calculator

Provides risk metrics calculations including Sharpe ratio and volatility calculations.
"""

import statistics
from datetime import datetime
from typing import List

from agno.utils.log import log_error, log_info

from .base import (
    BaseCalculatorTools,
    FinancialComputationError,
    FinancialValidationError,
)


class RiskMetricsCalculatorTools(BaseCalculatorTools):
    """Calculator for risk metrics calculations."""

    def __init__(self, **kwargs):
        """Initialize the risk metrics calculator and register all methods."""
        self.add_instructions = True
        self.instructions = RiskMetricsCalculatorTools.get_llm_usage_instructions()

        super().__init__(name="risk_metrics_calculator", **kwargs)

        # Register all risk metrics methods
        self.register(self.calculate_sharpe_ratio)
        self.register(self.calculate_volatility)

    def calculate_sharpe_ratio(self, returns: List[float], risk_free_rate: float) -> str:
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
                raise FinancialValidationError("At least 2 return observations required")

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
                "metadata": {
                    "calculation_method": "sharpe_ratio_formula",
                    "timestamp": datetime.now().isoformat(),
                },
            }

            log_info(f"Calculated Sharpe ratio: {sharpe_ratio:.4f}")
            return self._format_json_response(result)

        except (FinancialValidationError, FinancialComputationError):
            raise
        except Exception as e:
            log_error(f"Unexpected error in Sharpe ratio calculation: {e}")
            raise FinancialComputationError(f"Failed to calculate Sharpe ratio: {e}")

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
                raise FinancialValidationError("At least 2 return observations required")

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
                "metadata": {
                    "calculation_method": "standard_deviation",
                    "timestamp": datetime.now().isoformat(),
                },
            }

            log_info(f"Calculated volatility: {volatility:.4%}")
            return self._format_json_response(result)

        except (FinancialValidationError, FinancialComputationError):
            raise
        except Exception as e:
            log_error(f"Unexpected error in volatility calculation: {e}")
            raise FinancialComputationError(f"Failed to calculate volatility: {e}")

    @staticmethod
    def get_llm_usage_instructions() -> str:
        """
        Returns detailed instructions for LLMs on how to use risk metrics calculations.
        """
        return """
<risk_performance_calculations_tools_instructions>
**RISK AND PERFORMANCE METRICS CALCULATIONS TOOLS:**

- Use calculate_sharpe_ratio to calculate risk-adjusted returns.
   Parameters:
      - returns (List[float]): List of periodic returns as decimals, e.g., [0.10, 0.15, -0.05, 0.20]
      - risk_free_rate (float): Risk-free rate per period as decimal, e.g., 0.02

- Use calculate_volatility to calculate standard deviation of returns.
   Parameters:
      - returns (List[float]): List of periodic returns as decimals, e.g., [0.08, 0.12, -0.03, 0.18]

<risk_performance_calculations_tools_instructions>
"""
