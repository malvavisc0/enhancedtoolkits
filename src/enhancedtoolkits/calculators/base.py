"""
Base Calculator Class

Provides shared utilities, validation methods, and common functionality
for all specialized calculator classes.
"""

import json
import math
from datetime import datetime
from typing import List

from agno.utils.log import log_error, log_info

from ..base import StrictToolkit


class FinancialCalculationError(Exception):
    """Base exception for financial calculation errors."""

    pass


class FinancialValidationError(FinancialCalculationError):
    """Exception for input validation errors."""

    pass


class FinancialComputationError(FinancialCalculationError):
    """Exception for computation errors (convergence, etc.)."""

    pass


class BaseCalculatorTools(StrictToolkit):
    """
    Base calculator class providing shared utilities and validation methods.

    All specialized calculator classes inherit from this base to ensure
    consistent validation, error handling, and response formatting.
    Each calculator can be used independently as a StrictToolkit.
    """

    def __init__(self, name: str = "base_calculator", **kwargs):
        """Initialize the base calculator with StrictToolkit functionality."""
        super().__init__(name=name, **kwargs)

    def _validate_positive_amount(self, amount: float, field_name: str) -> float:
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
        if rate < -1 or rate > 10:  # Allow negative rates but within reasonable bounds
            raise FinancialValidationError("Rate must be between -100% and 1000%")
        return float(rate)

    def _validate_periods(self, periods: int) -> int:
        """Validate that periods is a positive integer."""
        if not isinstance(periods, int) or periods <= 0:
            raise FinancialValidationError("Periods must be a positive integer")
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
                raise FinancialValidationError(f"Cash flow at index {i} must be a number")
            validated_flows.append(float(flow))

        return validated_flows

    def _validate_returns_list(self, returns: List[float]) -> List[float]:
        """Validate returns list with strict typing."""
        if not isinstance(returns, list) or len(returns) < 1:
            raise FinancialValidationError("Returns must be a list with at least 1 value")

        validated_returns = []
        for i, ret in enumerate(returns):
            if not isinstance(ret, (int, float)):
                raise FinancialValidationError(f"Return at index {i} must be a number")
            validated_returns.append(float(ret))

        return validated_returns

    def _format_json_response(self, data: dict) -> str:
        """Format response as JSON string."""
        try:
            return json.dumps(data, indent=2, ensure_ascii=False)
        except Exception as e:
            log_error(f"Error formatting JSON response: {e}")
            return json.dumps({"error": "Failed to format response", "data": str(data)})

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
                raise FinancialComputationError("IRR calculation failed to converge")

            rate = rate - npv / npv_derivative

        raise FinancialComputationError("IRR calculation did not converge")

    def _calculate_ytm_approximation(
        self, price: float, face_value: float, coupon_payment: float, periods: int
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
        self, face_value: float, coupon_payment: float, periods: int, yield_rate: float
    ) -> float:
        """Helper method to calculate bond price for YTM iteration."""
        if yield_rate == 0:
            return face_value + (coupon_payment * periods)

        pv_coupons = coupon_payment * (1 - (1 + yield_rate) ** -periods) / yield_rate
        pv_face_value = face_value / ((1 + yield_rate) ** periods)
        return pv_coupons + pv_face_value
