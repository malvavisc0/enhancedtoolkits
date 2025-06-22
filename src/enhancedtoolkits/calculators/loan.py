"""
Loan Calculator

Provides loan calculations including payment calculations and amortization schedules.
"""

from datetime import datetime

from agno.utils.log import log_error, log_info

from .base import (
    BaseCalculatorTools,
    FinancialComputationError,
    FinancialValidationError,
)


class LoanCalculatorTools(BaseCalculatorTools):
    """Calculator for loan calculations."""

    def __init__(self, **kwargs):
        """Initialize the loan calculator and register all methods."""
        self.add_instructions = True
        self.instructions = LoanCalculatorTools.get_llm_usage_instructions()

        super().__init__(name="loan_calculator", **kwargs)

        # Register all loan methods
        self.register(self.calculate_loan_payment)
        self.register(self.generate_amortization_schedule)

    def calculate_loan_payment(self, principal: float, rate: float, periods: int) -> str:
        """
        Calculate the periodic payment for a loan.

        Args:
            principal: Loan amount
            rate: Interest rate per period (as decimal)
            periods: Total number of payment periods

        Returns:
            JSON string containing loan payment calculation
        """
        try:
            principal = self._validate_positive_amount(principal, "principal")
            rate = self._validate_rate(rate)
            periods = self._validate_periods(periods)

            if rate == 0:
                payment = principal / periods
            else:
                payment = (
                    principal
                    * (rate * (1 + rate) ** periods)
                    / ((1 + rate) ** periods - 1)
                )

            total_payments = payment * periods
            total_interest = total_payments - principal

            result = {
                "operation": "loan_payment",
                "result": round(payment, 2),
                "inputs": {"principal": principal, "rate": rate, "periods": periods},
                "summary": {
                    "monthly_payment": round(payment, 2),
                    "total_payments": round(total_payments, 2),
                    "total_interest": round(total_interest, 2),
                    "interest_percentage": round((total_interest / principal) * 100, 2),
                },
                "metadata": {
                    "calculation_method": "annuity_payment_formula",
                    "timestamp": datetime.now().isoformat(),
                },
            }

            log_info(f"Calculated loan payment: {payment:.2f}")
            return self._format_json_response(result)

        except (FinancialValidationError, FinancialComputationError):
            raise
        except Exception as e:
            log_error(f"Unexpected error in loan payment calculation: {e}")
            raise FinancialComputationError(f"Failed to calculate loan payment: {e}")

    def generate_amortization_schedule(
        self, principal: float, rate: float, periods: int
    ) -> str:
        """
        Generate a complete amortization schedule for a loan.

        Args:
            principal: Loan amount
            rate: Interest rate per period (as decimal)
            periods: Total number of payment periods

        Returns:
            JSON string containing complete amortization schedule
        """
        try:
            principal = self._validate_positive_amount(principal, "principal")
            rate = self._validate_rate(rate)
            periods = self._validate_periods(periods)

            # Calculate payment amount
            if rate == 0:
                payment = principal / periods
            else:
                payment = (
                    principal
                    * (rate * (1 + rate) ** periods)
                    / ((1 + rate) ** periods - 1)
                )

            schedule = []
            remaining_balance = principal
            total_interest = 0

            for period in range(1, periods + 1):
                interest_payment = remaining_balance * rate
                principal_payment = payment - interest_payment
                remaining_balance -= principal_payment
                total_interest += interest_payment

                # Ensure remaining balance doesn't go negative due to rounding
                if remaining_balance < 0.01:
                    principal_payment += remaining_balance
                    remaining_balance = 0

                schedule.append(
                    {
                        "period": period,
                        "payment": round(payment, 2),
                        "principal": round(principal_payment, 2),
                        "interest": round(interest_payment, 2),
                        "balance": round(remaining_balance, 2),
                    }
                )

            result = {
                "operation": "amortization_schedule",
                "inputs": {"principal": principal, "rate": rate, "periods": periods},
                "summary": {
                    "payment_amount": round(payment, 2),
                    "total_payments": round(payment * periods, 2),
                    "total_interest": round(total_interest, 2),
                    "total_principal": principal,
                },
                "schedule": schedule,
                "metadata": {
                    "calculation_method": "amortization_formula",
                    "schedule_length": len(schedule),
                    "timestamp": datetime.now().isoformat(),
                },
            }

            log_info(f"Generated amortization schedule with {periods} payments")
            return self._format_json_response(result)

        except (FinancialValidationError, FinancialComputationError):
            raise
        except Exception as e:
            log_error(f"Unexpected error in amortization schedule generation: {e}")
            raise FinancialComputationError(
                f"Failed to generate amortization schedule: {e}"
            )

    @staticmethod
    def get_llm_usage_instructions() -> str:
        """
        Returns detailed instructions for LLMs on how to use loan calculations.
        """
        return """
<loan_calculations_tools_instructions>
**LOAN CALCULATIONS TOOLS:**

- Use calculate_loan_payment to calculate periodic payment for a loan.
   Parameters:
      - principal (float): Loan amount, e.g., 200000.0
      - rate (float): Interest rate per period as decimal, e.g., 0.005 for 0.5% monthly
      - periods (int): Total number of payment periods, e.g., 360

- Use generate_amortization_schedule to create complete loan payment schedule.
   Parameters:
      - principal (float): Loan amount, e.g., 100000.0
      - rate (float): Interest rate per period as decimal, e.g., 0.004167 for monthly
      - periods (int): Total number of payment periods, e.g., 240

</loan_calculations_tools_instructions>
"""
