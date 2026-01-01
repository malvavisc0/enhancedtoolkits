"""
Time Value of Money Calculator

Provides time value of money calculations including present value,
future value, annuities, and perpetuities.
"""

from .base import (
    BaseCalculatorTools,
    FinancialComputationError,
    FinancialValidationError,
)


class TimeValueCalculatorTools(BaseCalculatorTools):
    """Calculator for time value of money calculations."""

    def __init__(self, add_instructions: bool = True, **kwargs):
        """Initialize the time value calculator and register all methods."""
        instructions = (
            self.get_llm_usage_instructions() if add_instructions else ""
        )
        super().__init__(
            name="time_value_calculator",
            add_instructions=add_instructions,
            instructions=instructions,
            **kwargs,
        )

        # Register all time value methods
        self.register(self.calculate_present_value)
        self.register(self.calculate_future_value)
        self.register(self.calculate_annuity_present_value)
        self.register(self.calculate_annuity_future_value)
        self.register(self.calculate_perpetuity_value)

    def calculate_present_value(
        self, future_value: float, rate: float, periods: int
    ) -> str:
        """
        Calculate the present value of a future sum of money.

        Args:
            future_value: The amount of money in the future
            rate: Discount rate per period (as decimal, e.g., 0.05 for 5%)
            periods: Number of periods

        Returns:
            JSON string containing present value calculation
        """
        try:
            future_value = self._validate_positive_amount(
                future_value, "future_value"
            )
            rate = self._validate_rate(rate)
            periods = self._validate_periods(periods)

            if rate == 0:
                present_value = future_value
            else:
                present_value = future_value / ((1 + rate) ** periods)

            result = {
                "operation": "present_value",
                "result": round(present_value, 2),
                "inputs": {
                    "future_value": future_value,
                    "rate": rate,
                    "periods": periods,
                },
                "metadata": self._base_metadata("compound_discounting"),
            }

            return self._format_json_response(result)

        except (FinancialValidationError, FinancialComputationError):
            raise
        except (TypeError, ValueError, OverflowError, ZeroDivisionError) as e:
            self._log_unexpected_error("Failed to calculate present value", e)
            raise FinancialComputationError(
                f"Failed to calculate present value: {e}"
            ) from e

    def calculate_future_value(
        self, present_value: float, rate: float, periods: int
    ) -> str:
        """
        Calculate the future value of a present sum of money.

        Args:
            present_value: The current amount of money
            rate: Interest rate per period (as decimal)
            periods: Number of periods

        Returns:
            JSON string containing future value calculation
        """
        try:
            present_value = self._validate_positive_amount(
                present_value, "present_value"
            )
            rate = self._validate_rate(rate)
            periods = self._validate_periods(periods)

            future_value = present_value * ((1 + rate) ** periods)

            result = {
                "operation": "future_value",
                "result": round(future_value, 2),
                "inputs": {
                    "present_value": present_value,
                    "rate": rate,
                    "periods": periods,
                },
                "metadata": self._base_metadata("compound_interest"),
            }

            return self._format_json_response(result)

        except (FinancialValidationError, FinancialComputationError):
            raise
        except (TypeError, ValueError, OverflowError, ZeroDivisionError) as e:
            self._log_unexpected_error("Failed to calculate future value", e)
            raise FinancialComputationError(
                f"Failed to calculate future value: {e}"
            ) from e

    def calculate_annuity_present_value(
        self, payment: float, rate: float, periods: int
    ) -> str:
        """
        Calculate the present value of an ordinary annuity.

        Args:
            payment: Payment per period
            rate: Interest rate per period (as decimal)
            periods: Number of periods

        Returns:
            JSON string containing annuity present value calculation
        """
        try:
            payment = self._validate_positive_amount(payment, "payment")
            rate = self._validate_rate(rate)
            periods = self._validate_periods(periods)

            if rate == 0:
                pv_annuity = payment * periods
            else:
                pv_annuity = payment * (1 - (1 + rate) ** -periods) / rate

            total_payments = payment * periods

            result = {
                "operation": "annuity_present_value",
                "result": round(pv_annuity, 2),
                "inputs": {
                    "payment": payment,
                    "rate": rate,
                    "periods": periods,
                },
                "summary": {
                    "present_value": round(pv_annuity, 2),
                    "total_payments": round(total_payments, 2),
                    "discount_amount": round(total_payments - pv_annuity, 2),
                },
                "metadata": self._base_metadata("ordinary_annuity_pv"),
            }

            return self._format_json_response(result)

        except (FinancialValidationError, FinancialComputationError):
            raise
        except (TypeError, ValueError, OverflowError, ZeroDivisionError) as e:
            self._log_unexpected_error(
                "Failed to calculate annuity present value",
                e,
            )
            raise FinancialComputationError(
                f"Failed to calculate annuity present value: {e}"
            ) from e

    def calculate_annuity_future_value(
        self, payment: float, rate: float, periods: int
    ) -> str:
        """
        Calculate the future value of an ordinary annuity.

        Args:
            payment: Payment per period
            rate: Interest rate per period (as decimal)
            periods: Number of periods

        Returns:
            JSON string containing annuity future value calculation
        """
        try:
            payment = self._validate_positive_amount(payment, "payment")
            rate = self._validate_rate(rate)
            periods = self._validate_periods(periods)

            if rate == 0:
                fv_annuity = payment * periods
            else:
                fv_annuity = payment * (((1 + rate) ** periods - 1) / rate)

            total_payments = payment * periods
            interest_earned = fv_annuity - total_payments

            result = {
                "operation": "annuity_future_value",
                "result": round(fv_annuity, 2),
                "inputs": {
                    "payment": payment,
                    "rate": rate,
                    "periods": periods,
                },
                "summary": {
                    "future_value": round(fv_annuity, 2),
                    "total_payments": round(total_payments, 2),
                    "interest_earned": round(interest_earned, 2),
                },
                "metadata": self._base_metadata("ordinary_annuity_fv"),
            }

            return self._format_json_response(result)

        except (FinancialValidationError, FinancialComputationError):
            raise
        except (TypeError, ValueError, OverflowError, ZeroDivisionError) as e:
            self._log_unexpected_error(
                "Failed to calculate annuity future value",
                e,
            )
            raise FinancialComputationError(
                f"Failed to calculate annuity future value: {e}"
            ) from e

    def calculate_perpetuity_value(self, payment: float, rate: float) -> str:
        """
        Calculate the present value of a perpetuity.

        Args:
            payment: Payment per period
            rate: Interest rate per period (as decimal)

        Returns:
            JSON string containing perpetuity value calculation
        """
        try:
            payment = self._validate_positive_amount(payment, "payment")
            rate = self._validate_rate(rate)

            if rate <= 0:
                raise FinancialValidationError(
                    "Rate must be positive for perpetuity calculation"
                )

            perpetuity_value = payment / rate

            result = {
                "operation": "perpetuity_value",
                "result": round(perpetuity_value, 2),
                "inputs": {"payment": payment, "rate": rate},
                "summary": {
                    "perpetuity_value": round(perpetuity_value, 2),
                    "annual_payment": payment,
                    "required_rate": rate,
                },
                "metadata": self._base_metadata("perpetuity_formula"),
            }

            return self._format_json_response(result)

        except (FinancialValidationError, FinancialComputationError):
            raise
        except (TypeError, ValueError, OverflowError, ZeroDivisionError) as e:
            self._log_unexpected_error(
                "Failed to calculate perpetuity value",
                e,
            )
            raise FinancialComputationError(
                f"Failed to calculate perpetuity value: {e}"
            ) from e

    @staticmethod
    def get_llm_usage_instructions() -> str:
        """Return short, text-first usage instructions for time-value tools."""
        return """
<time_value_calculator>
Time value of money. Tools return JSON strings.

Tools:
- calculate_present_value(future_value, rate, periods)
- calculate_future_value(present_value, rate, periods)
- calculate_annuity_present_value(payment, rate, periods)
- calculate_annuity_future_value(payment, rate, periods)
- calculate_perpetuity_value(payment, rate)

Notes:
- `rate` is per period as a decimal (e.g. 0.05 for 5%).
</time_value_calculator>
"""
