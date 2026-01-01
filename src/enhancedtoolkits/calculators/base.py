"""Calculator base utilities.

Shared validation + helpers for all calculator toolkits.

All calculator tools return JSON strings.
"""

import json
from datetime import datetime
from typing import Any, Dict, List

from agno.utils.log import log_error

from ..base import StrictToolkit


class FinancialCalculationError(Exception):
    """Base exception for financial calculation errors."""


class FinancialValidationError(FinancialCalculationError):
    """Exception for input validation errors."""


class FinancialComputationError(FinancialCalculationError):
    """Exception for computation errors (convergence, etc.)."""


class BaseCalculatorTools(StrictToolkit):
    """Base calculator class providing shared utilities and validation."""

    def __init__(
        self,
        name: str = "base_calculator",
        add_instructions: bool = True,
        instructions: str = "",
        **kwargs,
    ):
        """Initialize a calculator toolkit.

        Args:
            name: Toolkit name.
            add_instructions: Whether to attach LLM usage instructions.
            instructions: Instructions text.
        """
        super().__init__(
            name=name,
            instructions=instructions if add_instructions else "",
            add_instructions=add_instructions,
            **kwargs,
        )

    def _validate_positive_amount(
        self, amount: float, field_name: str
    ) -> float:
        """Validate that an amount is positive."""
        if not isinstance(amount, (int, float)):
            raise FinancialValidationError(f"{field_name} must be a number")
        if amount <= 0:
            raise FinancialValidationError(f"{field_name} must be positive")
        return float(amount)

    def _validate_rate(self, rate: float) -> float:
        """Validate that a rate is reasonable."""
        if not isinstance(rate, (int, float)):
            raise FinancialValidationError("Rate must be a number")
        if (
            rate < -1 or rate > 10
        ):  # Allow negative rates but within reasonable bounds
            raise FinancialValidationError(
                "Rate must be between -100% and 1000%"
            )
        return float(rate)

    def _validate_periods(self, periods: int) -> int:
        """Validate that periods is a positive integer."""
        if not isinstance(periods, int) or periods <= 0:
            raise FinancialValidationError(
                "Periods must be a positive integer"
            )
        if periods > 1000:  # Reasonable upper limit
            raise FinancialValidationError("Periods cannot exceed 1000")
        return periods

    def _validate_cash_flows(self, cash_flows: List[float]) -> List[float]:
        """Validate cash flows list with strict typing."""
        if not isinstance(cash_flows, list) or len(cash_flows) < 2:
            raise FinancialValidationError(
                "Cash flows must be a list with at least 2 values"
            )

        validated_flows = []
        for i, flow in enumerate(cash_flows):
            if not isinstance(flow, (int, float)):
                raise FinancialValidationError(
                    f"Cash flow at index {i} must be a number"
                )
            validated_flows.append(float(flow))

        return validated_flows

    def _validate_returns_list(self, returns: List[float]) -> List[float]:
        """Validate returns list with strict typing."""
        if not isinstance(returns, list) or len(returns) < 1:
            raise FinancialValidationError(
                "Returns must be a list with at least 1 value"
            )

        validated_returns = []
        for i, ret in enumerate(returns):
            if not isinstance(ret, (int, float)):
                raise FinancialValidationError(
                    f"Return at index {i} must be a number"
                )
            validated_returns.append(float(ret))

        return validated_returns

    def _format_json_response(self, data: Any) -> str:
        """Format response as a JSON string."""
        try:
            return json.dumps(data, indent=2, ensure_ascii=False, default=str)
        except Exception as e:  # pylint: disable=broad-exception-caught
            log_error(f"Error formatting JSON response: {e}")
            return json.dumps({"error": "Failed to format response"}, indent=2)

    def _base_metadata(
        self, calculation_method: str, **extra: Any
    ) -> Dict[str, Any]:
        """Return a consistent metadata object for calculator responses."""
        return {
            "calculation_method": calculation_method,
            "timestamp": datetime.now().isoformat(),
            **extra,
        }

    def _log_unexpected_error(self, message: str, exc: Exception) -> None:
        """Log unexpected exceptions with a consistent message."""
        log_error(f"{message}: {exc}")

    def _error_json_response(
        self, operation: str, message: str, exc: Exception
    ) -> str:
        """Return a JSON error payload (tool-friendly: always returns a string)."""
        self._log_unexpected_error(message, exc)
        return self._format_json_response(
            {
                "operation": operation,
                "error": message,
                "details": str(exc),
                "metadata": self._base_metadata("error"),
            }
        )

    def _calculate_irr_newton_raphson(
        self,
        cash_flows: List[float],
        guess: float,
        max_iterations: int = 100,
        tolerance: float = 1e-6,
    ) -> float:
        """Calculate IRR using Newton-Raphson method."""
        rate = guess

        for _ in range(max_iterations):
            # Calculate NPV and its derivative
            npv = 0
            npv_derivative = 0

            for i, cash_flow in enumerate(cash_flows):
                if rate == -1:  # Avoid division by zero
                    rate += tolerance

                npv += cash_flow / ((1 + rate) ** i)
                if i > 0:
                    npv_derivative -= i * cash_flow / ((1 + rate) ** (i + 1))

            if abs(npv) < tolerance:
                return rate

            if abs(npv_derivative) < tolerance:
                raise FinancialComputationError(
                    "IRR calculation failed to converge"
                )

            rate = rate - npv / npv_derivative

        raise FinancialComputationError("IRR calculation did not converge")

    def _calculate_ytm_approximation(
        self,
        price: float,
        face_value: float,
        coupon_payment: float,
        periods: int,
    ) -> float:
        """Calculate YTM using approximation method."""
        # Initial approximation
        ytm = (coupon_payment + (face_value - price) / periods) / (
            (face_value + price) / 2
        )

        # Refine using iterative method
        for _ in range(50):  # Maximum iterations
            bond_price_calc = self._calculate_bond_price_for_ytm(
                face_value, coupon_payment, periods, ytm
            )

            if abs(bond_price_calc - price) < 0.01:  # Close enough
                break

            # Adjust YTM based on price difference
            if bond_price_calc > price:
                ytm += 0.001  # Increase YTM if calculated price is too high
            else:
                ytm -= 0.001  # Decrease YTM if calculated price is too low

        return ytm

    def _calculate_bond_price_for_ytm(
        self,
        face_value: float,
        coupon_payment: float,
        periods: int,
        yield_rate: float,
    ) -> float:
        """Helper method to calculate bond price for YTM iteration."""
        if yield_rate == 0:
            return face_value + (coupon_payment * periods)

        pv_coupons = (
            coupon_payment * (1 - (1 + yield_rate) ** -periods) / yield_rate
        )
        pv_face_value = face_value / ((1 + yield_rate) ** periods)
        return pv_coupons + pv_face_value
