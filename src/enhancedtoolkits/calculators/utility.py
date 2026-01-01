"""
Utility Calculator

Provides utility calculations including currency conversion and inflation adjustments.
"""

from .base import BaseCalculatorTools


class UtilityCalculatorTools(BaseCalculatorTools):
    """Calculator for utility calculations."""

    def __init__(self, add_instructions: bool = True, **kwargs):
        """Initialize the utility calculator and register all methods."""
        instructions = (
            self.get_llm_usage_instructions() if add_instructions else ""
        )
        super().__init__(
            name="utility_calculator",
            add_instructions=add_instructions,
            instructions=instructions,
            **kwargs,
        )

        # Register all utility methods
        self.register(self.convert_currency)
        self.register(self.adjust_for_inflation)

    def convert_currency(self, amount: float, rate: float) -> str:
        """Convert an amount using an exchange rate."""
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
            "metadata": self._base_metadata("simple_multiplication"),
        }

        return self._format_json_response(result)

    def adjust_for_inflation(
        self, amount: float, rate: float, periods: int
    ) -> str:
        """
        Adjust an amount for inflation over a number of periods.

        Args:
            amount: Initial amount
            rate: Inflation rate per period (as decimal)
            periods: Number of periods

        Returns:
            JSON string containing inflation adjustment
        """
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
                "purchasing_power_loss": round(
                    (inflation_impact / amount) * 100, 2
                ),
            },
            "metadata": self._base_metadata("compound_inflation"),
        }

        return self._format_json_response(result)

    @staticmethod
    def get_llm_usage_instructions() -> str:
        """Return short, text-first usage instructions for utility tools."""
        return """
<utility_calculator>
Simple utilities (currency conversion, inflation adjustment)

GOAL
- Convert/adjust values with simple formulas and return JSON.

Simple utilities. Tools return JSON strings.

Tools:
- convert_currency(amount, rate)
- adjust_for_inflation(amount, rate, periods)

Notes:
- `rate` is a decimal (e.g., 0.03 for 3%).

CONTEXT-SIZE RULES (IMPORTANT)
- In final user responses, present the converted/adjusted amount and assumptions; avoid dumping full JSON.
</utility_calculator>
"""
