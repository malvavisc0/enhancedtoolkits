"""
Depreciation Calculator

Provides depreciation calculations including straight-line and declining balance methods.
"""

from datetime import datetime

from agno.utils.log import log_error, log_info

from .base import (
    BaseCalculatorTools,
    FinancialComputationError,
    FinancialValidationError,
)


class DepreciationCalculatorTools(BaseCalculatorTools):
    """Calculator for depreciation calculations."""

    def __init__(self, **kwargs):
        """Initialize the depreciation calculator and register all methods."""
        self.add_instructions = True
        self.instructions = DepreciationCalculatorTools.get_llm_usage_instructions()

        super().__init__(name="depreciation_calculator", **kwargs)

        # Register all depreciation methods
        self.register(self.calculate_straight_line_depreciation)
        self.register(self.calculate_declining_balance_depreciation)

    def calculate_straight_line_depreciation(
        self, cost: float, salvage: float, life: int
    ) -> str:
        """
        Calculate annual depreciation using the straight-line method.

        Args:
            cost: Initial cost of the asset
            salvage: Salvage value at end of useful life
            life: Useful life in years

        Returns:
            JSON string containing depreciation calculation
        """
        try:
            cost = self._validate_positive_amount(cost, "cost")
            salvage = max(0, salvage)  # Salvage can be zero but not negative
            life = self._validate_periods(life)

            if salvage >= cost:
                raise FinancialValidationError(
                    "Salvage value cannot be greater than or equal to cost"
                )

            annual_depreciation = (cost - salvage) / life
            total_depreciation = cost - salvage

            # Generate depreciation schedule
            schedule = []
            book_value = cost

            for year in range(1, life + 1):
                depreciation = annual_depreciation
                accumulated_depreciation = annual_depreciation * year
                book_value = cost - accumulated_depreciation

                schedule.append(
                    {
                        "year": year,
                        "depreciation": round(depreciation, 2),
                        "accumulated_depreciation": round(accumulated_depreciation, 2),
                        "book_value": round(book_value, 2),
                    }
                )

            result = {
                "operation": "straight_line_depreciation",
                "result": round(annual_depreciation, 2),
                "inputs": {"cost": cost, "salvage": salvage, "life": life},
                "summary": {
                    "annual_depreciation": round(annual_depreciation, 2),
                    "total_depreciation": round(total_depreciation, 2),
                    "depreciation_rate": round((annual_depreciation / cost) * 100, 2),
                },
                "schedule": schedule,
                "metadata": {
                    "calculation_method": "straight_line",
                    "timestamp": datetime.now().isoformat(),
                },
            }

            log_info(f"Calculated straight-line depreciation: {annual_depreciation:.2f}")
            return self._format_json_response(result)

        except (FinancialValidationError, FinancialComputationError):
            raise
        except Exception as e:
            log_error(f"Unexpected error in straight-line depreciation calculation: {e}")
            raise FinancialComputationError(
                f"Failed to calculate straight-line depreciation: {e}"
            )

    def calculate_declining_balance_depreciation(
        self, cost: float, rate: float, life: int
    ) -> str:
        """
        Calculate depreciation using the declining balance method.

        Args:
            cost: Initial cost of the asset
            rate: Depreciation rate per period (as decimal)
            life: Useful life in years

        Returns:
            JSON string containing depreciation calculation
        """
        try:
            cost = self._validate_positive_amount(cost, "cost")
            rate = self._validate_rate(rate)
            life = self._validate_periods(life)

            # Generate depreciation schedule
            schedule = []
            book_value = cost
            total_depreciation = 0

            for year in range(1, life + 1):
                depreciation = book_value * rate
                book_value -= depreciation
                total_depreciation += depreciation

                schedule.append(
                    {
                        "year": year,
                        "depreciation": round(depreciation, 2),
                        "accumulated_depreciation": round(total_depreciation, 2),
                        "book_value": round(book_value, 2),
                    }
                )

            result = {
                "operation": "declining_balance_depreciation",
                "inputs": {"cost": cost, "rate": rate, "life": life},
                "summary": {
                    "total_depreciation": round(total_depreciation, 2),
                    "final_book_value": round(book_value, 2),
                    "depreciation_method": "declining_balance",
                },
                "schedule": schedule,
                "metadata": {
                    "calculation_method": "declining_balance",
                    "timestamp": datetime.now().isoformat(),
                },
            }

            log_info(f"Calculated declining balance depreciation schedule")
            return self._format_json_response(result)

        except (FinancialValidationError, FinancialComputationError):
            raise
        except Exception as e:
            log_error(
                f"Unexpected error in declining balance depreciation calculation: {e}"
            )
            raise FinancialComputationError(
                f"Failed to calculate declining balance depreciation: {e}"
            )

    @staticmethod
    def get_llm_usage_instructions() -> str:
        """
        Returns detailed instructions for LLMs on how to use depreciation calculations.
        """
        return """
<deprecation_calculators_tools_instructions>
**DEPRECIATION CALCULATIONS:**

- Use calculate_straight_line_depreciation for linear depreciation.
   Parameters:
      - cost (float): Initial cost of asset, e.g., 50000.0
      - salvage (float): Salvage value at end of life, e.g., 5000.0
      - life (int): Useful life in years, e.g., 10

- Use calculate_declining_balance_depreciation for accelerated depreciation.
   Parameters:
      - cost (float): Initial cost of asset, e.g., 30000.0
      - rate (float): Depreciation rate per period as decimal, e.g., 0.20
      - life (int): Useful life in years, e.g., 5

</deprecation_calculators_tools_instructions>
"""
