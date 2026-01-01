"""
Loan Calculator

Provides loan calculations including payment calculations and amortization schedules.
"""

from .base import (
    BaseCalculatorTools,
    FinancialComputationError,
    FinancialValidationError,
)


class LoanCalculatorTools(BaseCalculatorTools):
    """Calculator for loan calculations."""

    def __init__(self, add_instructions: bool = True, **kwargs):
        """Initialize the loan calculator and register all methods."""
        instructions = (
            self.get_llm_usage_instructions() if add_instructions else ""
        )
        super().__init__(
            name="loan_calculator",
            add_instructions=add_instructions,
            instructions=instructions,
            **kwargs,
        )

        self.register(self.calculate_loan_payment)
        self.register(self.generate_amortization_schedule)
        self.register(self.calculate_total_interest)
        self.register(self.calculate_remaining_balance)

    @staticmethod
    def _payment_amount(principal: float, rate: float, periods: int) -> float:
        """Compute the fixed periodic payment for an amortizing loan."""
        if rate == 0:
            return principal / periods
        return (
            principal
            * (rate * (1 + rate) ** periods)
            / ((1 + rate) ** periods - 1)
        )

    def calculate_loan_payment(
        self, principal: float, rate: float, periods: int
    ) -> str:
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

            payment = self._payment_amount(principal, rate, periods)

            total_payments = payment * periods
            total_interest = total_payments - principal

            result = {
                "operation": "loan_payment",
                "result": round(payment, 2),
                "inputs": {
                    "principal": principal,
                    "rate": rate,
                    "periods": periods,
                },
                "summary": {
                    "monthly_payment": round(payment, 2),
                    "total_payments": round(total_payments, 2),
                    "total_interest": round(total_interest, 2),
                    "interest_percentage": round(
                        (total_interest / principal) * 100, 2
                    ),
                },
                "metadata": self._base_metadata("annuity_payment_formula"),
            }

            return self._format_json_response(result)

        except (TypeError, ValueError, OverflowError, ZeroDivisionError) as e:
            self._log_unexpected_error("Failed to calculate loan payment", e)
            raise FinancialComputationError(
                f"Failed to calculate loan payment: {e}"
            ) from e

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

            payment = self._payment_amount(principal, rate, periods)

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
                "inputs": {
                    "principal": principal,
                    "rate": rate,
                    "periods": periods,
                },
                "summary": {
                    "payment_amount": round(payment, 2),
                    "total_payments": round(payment * periods, 2),
                    "total_interest": round(total_interest, 2),
                    "total_principal": principal,
                },
                "schedule": schedule,
                "metadata": self._base_metadata(
                    "amortization_formula", schedule_length=len(schedule)
                ),
            }

            return self._format_json_response(result)

        except (TypeError, ValueError, OverflowError, ZeroDivisionError) as e:
            self._log_unexpected_error(
                "Failed to generate amortization schedule",
                e,
            )
            raise FinancialComputationError(
                f"Failed to generate amortization schedule: {e}"
            ) from e

    def calculate_total_interest(
        self, principal: float, rate: float, periods: int
    ) -> str:
        """Calculate total interest paid over the full loan term."""
        principal = self._validate_positive_amount(principal, "principal")
        rate = self._validate_rate(rate)
        periods = self._validate_periods(periods)

        payment = self._payment_amount(principal, rate, periods)
        total_payments = payment * periods
        total_interest = total_payments - principal

        return self._format_json_response(
            {
                "operation": "total_interest",
                "result": round(total_interest, 2),
                "inputs": {
                    "principal": principal,
                    "rate": rate,
                    "periods": periods,
                },
                "summary": {
                    "payment": round(payment, 2),
                    "total_payments": round(total_payments, 2),
                    "total_interest": round(total_interest, 2),
                },
                "metadata": self._base_metadata("annuity_payment_formula"),
            }
        )

    def calculate_remaining_balance(
        self, principal: float, rate: float, periods: int, payments_made: int
    ) -> str:
        """Calculate remaining balance after `payments_made` payments."""
        principal = self._validate_positive_amount(principal, "principal")
        rate = self._validate_rate(rate)
        periods = self._validate_periods(periods)

        if not isinstance(payments_made, int) or payments_made < 0:
            raise FinancialValidationError(
                "payments_made must be a non-negative integer"
            )
        if payments_made > periods:
            raise FinancialValidationError(
                "payments_made cannot exceed periods"
            )

        payment = self._payment_amount(principal, rate, periods)

        if rate == 0:
            remaining = max(0.0, principal - payment * payments_made)
        else:
            growth = (1 + rate) ** payments_made
            remaining = principal * growth - payment * (growth - 1) / rate
            remaining = max(0.0, remaining)

        return self._format_json_response(
            {
                "operation": "remaining_balance",
                "result": round(remaining, 2),
                "inputs": {
                    "principal": principal,
                    "rate": rate,
                    "periods": periods,
                    "payments_made": payments_made,
                },
                "summary": {
                    "payment": round(payment, 2),
                    "remaining_balance": round(remaining, 2),
                    "payments_remaining": periods - payments_made,
                },
                "metadata": self._base_metadata(
                    "amortization_balance_formula"
                ),
            }
        )

    @staticmethod
    def get_llm_usage_instructions() -> str:
        """Return short, text-first usage instructions for loan tools."""
        return """
<loan_calculator>
Loan payments and amortization

GOAL
- Compute payments/interest/amortization for an amortizing loan and return JSON.

Loan calculations. Tools return JSON strings.

Tools:
- calculate_loan_payment(principal, rate, periods)
- generate_amortization_schedule(principal, rate, periods)
- calculate_total_interest(principal, rate, periods)
- calculate_remaining_balance(principal, rate, periods, payments_made)

Notes:
- `rate` is the interest rate per payment period as a decimal (e.g. monthly rate).
- For an annual APR `apr`, monthly rate is `apr / 12`.

CONTEXT-SIZE RULES (IMPORTANT)
- Amortization schedules can be large; summarize totals + a few representative rows.
</loan_calculator>
"""
