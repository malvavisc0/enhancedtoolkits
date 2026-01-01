"""
Depreciation Calculator

Provides depreciation calculations including straight-line and declining balance methods.
"""

from .base import (
    BaseCalculatorTools,
    FinancialComputationError,
    FinancialValidationError,
)


class DepreciationCalculatorTools(BaseCalculatorTools):
    """Calculator for depreciation calculations."""

    def __init__(self, add_instructions: bool = True, **kwargs):
        """Initialize the depreciation calculator and register all methods."""
        instructions = (
            self.get_llm_usage_instructions() if add_instructions else ""
        )
        super().__init__(
            name="depreciation_calculator",
            add_instructions=add_instructions,
            instructions=instructions,
            **kwargs,
        )

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
                        "accumulated_depreciation": round(
                            accumulated_depreciation, 2
                        ),
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
                    "depreciation_rate": round(
                        (annual_depreciation / cost) * 100, 2
                    ),
                },
                "schedule": schedule,
                "metadata": self._base_metadata("straight_line"),
            }

            return self._format_json_response(result)

        except (FinancialValidationError, FinancialComputationError):
            raise
        except (TypeError, ValueError, OverflowError, ZeroDivisionError) as e:
            self._log_unexpected_error(
                "Failed to calculate straight-line depreciation",
                e,
            )
            raise FinancialComputationError(
                f"Failed to calculate straight-line depreciation: {e}"
            ) from e

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
                        "accumulated_depreciation": round(
                            total_depreciation, 2
                        ),
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
                "metadata": self._base_metadata("declining_balance"),
            }

            return self._format_json_response(result)

        except (FinancialValidationError, FinancialComputationError):
            raise
        except (TypeError, ValueError, OverflowError, ZeroDivisionError) as e:
            self._log_unexpected_error(
                "Failed to calculate declining balance depreciation",
                e,
            )
            raise FinancialComputationError(
                f"Failed to calculate declining balance depreciation: {e}"
            ) from e

    @staticmethod
    def get_llm_usage_instructions() -> str:
        """Return short, text-first usage instructions for depreciation tools."""
        return """
<depreciation_calculator>
Depreciation schedules. Tools return JSON strings.

Tools:
- calculate_straight_line_depreciation(cost, salvage, life)
- calculate_declining_balance_depreciation(cost, rate, life)

Notes:
- `rate` is per period as a decimal (e.g., 0.2 for 20%).
</depreciation_calculator>
"""
