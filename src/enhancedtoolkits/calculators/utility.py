"""
Utility Calculator

Provides utility calculations including currency conversion and inflation adjustments.
"""

from datetime import datetime

from agno.utils.log import log_error, log_info

from .base import (
    BaseCalculatorTools,
    FinancialComputationError,
    FinancialValidationError,
)


class UtilityCalculatorTools(BaseCalculatorTools):
    """Calculator for utility calculations."""

    def __init__(self, **kwargs):
        """Initialize the utility calculator and register all methods."""
        self.add_instructions = True
        self.instructions = UtilityCalculatorTools.get_llm_usage_instructions()

        super().__init__(name="utility_calculator", **kwargs)

        # Register all utility methods
        self.register(self.convert_currency)
        self.register(self.adjust_for_inflation)

    def convert_currency(self, amount: float, rate: float) -> str:
        """
        Convert an amount from one currency to another using a given exchange rate.

        Args:
            amount: Amount to convert
            rate: Exchange rate (target per source)

        Returns:
            JSON string containing currency conversion
        """
        try:
            amount = self._validate_positive_amount(amount, "amount")
            rate = self._validate_positive_amount(rate, "rate")

            converted_amount = amount * rate

            result = {
                "operation": "currency_conversion",
                "result": round(converted_amount, 2),
                "inputs": {"amount": amount, "exchange_rate": rate},
                "summary": {
                    "original_amount": amount,
                    "converted_amount": round(converted_amount, 2),
                    "exchange_rate": rate,
                },
                "metadata": {
                    "calculation_method": "simple_multiplication",
                    "timestamp": datetime.now().isoformat(),
                },
            }

            log_info(f"Converted currency: {amount} -> {converted_amount:.2f}")
            return self._format_json_response(result)

        except (FinancialValidationError, FinancialComputationError):
            raise
        except Exception as e:
            log_error(f"Unexpected error in currency conversion: {e}")
            raise FinancialComputationError(f"Failed to convert currency: {e}")

    def adjust_for_inflation(self, amount: float, rate: float, periods: int) -> str:
        """
        Adjust an amount for inflation over a number of periods.

        Args:
            amount: Initial amount
            rate: Inflation rate per period (as decimal)
            periods: Number of periods

        Returns:
            JSON string containing inflation adjustment
        """
        try:
            amount = self._validate_positive_amount(amount, "amount")
            rate = self._validate_rate(rate)
            periods = self._validate_periods(periods)

            adjusted_amount = amount * ((1 + rate) ** periods)
            inflation_impact = adjusted_amount - amount

            result = {
                "operation": "inflation_adjustment",
                "result": round(adjusted_amount, 2),
                "inputs": {
                    "original_amount": amount,
                    "inflation_rate": rate,
                    "periods": periods,
                },
                "summary": {
                    "original_amount": amount,
                    "adjusted_amount": round(adjusted_amount, 2),
                    "inflation_impact": round(inflation_impact, 2),
                    "purchasing_power_loss": round((inflation_impact / amount) * 100, 2),
                },
                "metadata": {
                    "calculation_method": "compound_inflation",
                    "timestamp": datetime.now().isoformat(),
                },
            }

            log_info(f"Adjusted for inflation: {amount} -> {adjusted_amount:.2f}")
            return self._format_json_response(result)

        except (FinancialValidationError, FinancialComputationError):
            raise
        except Exception as e:
            log_error(f"Unexpected error in inflation adjustment: {e}")
            raise FinancialComputationError(f"Failed to adjust for inflation: {e}")

    @staticmethod
    def get_llm_usage_instructions() -> str:
        """
        Returns detailed instructions for LLMs on how to use utility calculations.
        """
        return """
<utility_calculator_tools_instructions>
**UTILITY Calculator FUNCTIONS:**

- Use convert_currency for simple currency conversion.
   Parameters:
      - amount (float): Amount to convert, e.g., 1000.0
      - rate (float): Exchange rate (target per source), e.g., 1.25

- Use adjust_for_inflation to adjust amounts for inflation.
   Parameters:
      - amount (float): Initial amount, e.g., 1000.0
      - rate (float): Inflation rate per period as decimal, e.g., 0.03
      - periods (int): Number of periods, e.g., 5

</utility_calculator_tools_instructions>
"""
