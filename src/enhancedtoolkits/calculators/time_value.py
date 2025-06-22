"""
Time Value of Money Calculator

Provides time value of money calculations including present value,
future value, annuities, and perpetuities.
"""

from datetime import datetime

from agno.utils.log import log_error, log_info

from .base import (
    BaseCalculatorTools,
    FinancialComputationError,
    FinancialValidationError,
)


class TimeValueCalculatorTools(BaseCalculatorTools):
    """Calculator for time value of money calculations."""

    def __init__(self, **kwargs):
        """Initialize the time value calculator and register all methods."""
        self.add_instructions = True
        self.instructions = TimeValueCalculatorTools.get_llm_usage_instructions()

        super().__init__(name="time_value_calculator", **kwargs)

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
            future_value = self._validate_positive_amount(future_value, "future_value")
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
                "metadata": {
                    "calculation_method": "compound_discounting",
                    "timestamp": datetime.now().isoformat(),
                },
            }

            log_info(f"Calculated present value: {present_value:.2f}")
            return self._format_json_response(result)

        except (FinancialValidationError, FinancialComputationError):
            raise
        except Exception as e:
            log_error(f"Unexpected error in present value calculation: {e}")
            raise FinancialComputationError(f"Failed to calculate present value: {e}")

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
            present_value = self._validate_positive_amount(present_value, "present_value")
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
                "metadata": {
                    "calculation_method": "compound_interest",
                    "timestamp": datetime.now().isoformat(),
                },
            }

            log_info(f"Calculated future value: {future_value:.2f}")
            return self._format_json_response(result)

        except (FinancialValidationError, FinancialComputationError):
            raise
        except Exception as e:
            log_error(f"Unexpected error in future value calculation: {e}")
            raise FinancialComputationError(f"Failed to calculate future value: {e}")

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
                "inputs": {"payment": payment, "rate": rate, "periods": periods},
                "summary": {
                    "present_value": round(pv_annuity, 2),
                    "total_payments": round(total_payments, 2),
                    "discount_amount": round(total_payments - pv_annuity, 2),
                },
                "metadata": {
                    "calculation_method": "ordinary_annuity_pv",
                    "timestamp": datetime.now().isoformat(),
                },
            }

            log_info(f"Calculated annuity present value: {pv_annuity:.2f}")
            return self._format_json_response(result)

        except (FinancialValidationError, FinancialComputationError):
            raise
        except Exception as e:
            log_error(f"Unexpected error in annuity PV calculation: {e}")
            raise FinancialComputationError(
                f"Failed to calculate annuity present value: {e}"
            )

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
                "inputs": {"payment": payment, "rate": rate, "periods": periods},
                "summary": {
                    "future_value": round(fv_annuity, 2),
                    "total_payments": round(total_payments, 2),
                    "interest_earned": round(interest_earned, 2),
                },
                "metadata": {
                    "calculation_method": "ordinary_annuity_fv",
                    "timestamp": datetime.now().isoformat(),
                },
            }

            log_info(f"Calculated annuity future value: {fv_annuity:.2f}")
            return self._format_json_response(result)

        except (FinancialValidationError, FinancialComputationError):
            raise
        except Exception as e:
            log_error(f"Unexpected error in annuity FV calculation: {e}")
            raise FinancialComputationError(
                f"Failed to calculate annuity future value: {e}"
            )

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
                "metadata": {
                    "calculation_method": "perpetuity_formula",
                    "timestamp": datetime.now().isoformat(),
                },
            }

            log_info(f"Calculated perpetuity value: {perpetuity_value:.2f}")
            return self._format_json_response(result)

        except (FinancialValidationError, FinancialComputationError):
            raise
        except Exception as e:
            log_error(f"Unexpected error in perpetuity calculation: {e}")
            raise FinancialComputationError(f"Failed to calculate perpetuity value: {e}")

    @staticmethod
    def get_llm_usage_instructions() -> str:
        """
        Returns detailed instructions for LLMs on how to use time value of money calculations.
        """
        return """
<time_value_money_calculator_tools_instructions>
**TIME VALUE OF MONEY CALCULATIONS TOOLS:**

- Use calculate_present_value to calculate the present value of a future sum of money.
   Parameters:
      - future_value (float): The amount of money in the future, e.g., 10000.0
      - rate (float): Discount rate per period as decimal, e.g., 0.05 for 5%
      - periods (int): Number of periods, e.g., 4

- Use calculate_future_value to calculate the future value of a present sum of money.
   Parameters:
      - present_value (float): The current amount of money, e.g., 8000.0
      - rate (float): Interest rate per period as decimal, e.g., 0.06 for 6%
      - periods (int): Number of periods, e.g., 5

**ANNUITY CALCULATIONS:**

- Use calculate_annuity_present_value to calculate PV of ordinary annuity.
   Parameters:
      - payment (float): Payment per period, e.g., 1000.0
      - rate (float): Interest rate per period as decimal, e.g., 0.08
      - periods (int): Number of periods, e.g., 10

- Use calculate_annuity_future_value to calculate FV of ordinary annuity.
   Parameters:
      - payment (float): Payment per period, e.g., 500.0
      - rate (float): Interest rate per period as decimal, e.g., 0.06
      - periods (int): Number of periods, e.g., 20

- Use calculate_perpetuity_value to calculate present value of perpetuity.
   Parameters:
      - payment (float): Payment per period, e.g., 100.0
      - rate (float): Interest rate per period as decimal, e.g., 0.05
</time_value_money_calculator_tools_instructions>
"""
