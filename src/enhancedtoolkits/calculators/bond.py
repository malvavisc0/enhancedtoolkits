"""
Bond Calculator

Provides bond calculations including bond pricing and yield to maturity calculations.
"""

from .base import (
    BaseCalculatorTools,
    FinancialComputationError,
    FinancialValidationError,
)


class BondCalculatorTools(BaseCalculatorTools):
    """Calculator for bond calculations."""

    def __init__(self, add_instructions: bool = True, **kwargs):
        """Initialize the bond calculator and register all methods."""
        instructions = (
            self.get_llm_usage_instructions() if add_instructions else ""
        )
        super().__init__(
            name="bond_calculator",
            add_instructions=add_instructions,
            instructions=instructions,
            **kwargs,
        )

        # Register all bond methods
        self.register(self.calculate_bond_price)
        self.register(self.calculate_yield_to_maturity)

    def calculate_bond_price(
        self,
        face_value: float,
        coupon_rate: float,
        periods: int,
        yield_rate: float,
    ) -> str:
        """
        Calculate the price of a bond.

        Args:
            face_value: Bond face value
            coupon_rate: Annual coupon rate (as decimal)
            periods: Number of periods until maturity
            yield_rate: Yield to maturity per period (as decimal)

        Returns:
            JSON string containing bond price calculation
        """
        try:
            face_value = self._validate_positive_amount(
                face_value, "face_value"
            )
            coupon_rate = self._validate_rate(coupon_rate)
            yield_rate = self._validate_rate(yield_rate)
            periods = self._validate_periods(periods)

            coupon_payment = face_value * coupon_rate

            if yield_rate == 0:
                bond_price = face_value + (coupon_payment * periods)
            else:
                # Present value of coupon payments
                pv_coupons = (
                    coupon_payment
                    * (1 - (1 + yield_rate) ** -periods)
                    / yield_rate
                )
                # Present value of face value
                pv_face_value = face_value / ((1 + yield_rate) ** periods)
                bond_price = pv_coupons + pv_face_value

            premium_discount = bond_price - face_value

            result = {
                "operation": "bond_price",
                "result": round(bond_price, 2),
                "inputs": {
                    "face_value": face_value,
                    "coupon_rate": coupon_rate,
                    "periods": periods,
                    "yield_rate": yield_rate,
                },
                "summary": {
                    "bond_price": round(bond_price, 2),
                    "face_value": face_value,
                    "coupon_payment": round(coupon_payment, 2),
                    "premium_discount": round(premium_discount, 2),
                    "price_type": (
                        "premium"
                        if premium_discount > 0
                        else "discount" if premium_discount < 0 else "par"
                    ),
                },
                "metadata": self._base_metadata("present_value_cash_flows"),
            }

            return self._format_json_response(result)

        except (FinancialValidationError, FinancialComputationError):
            raise
        except (TypeError, ValueError, OverflowError, ZeroDivisionError) as e:
            self._log_unexpected_error("Failed to calculate bond price", e)
            raise FinancialComputationError(
                f"Failed to calculate bond price: {e}"
            ) from e

    def calculate_yield_to_maturity(
        self, price: float, face_value: float, coupon_rate: float, periods: int
    ) -> str:
        """
        Calculate the yield to maturity for a bond.

        Args:
            price: Current bond price
            face_value: Bond face value
            coupon_rate: Annual coupon rate (as decimal)
            periods: Number of periods until maturity

        Returns:
            JSON string containing YTM calculation
        """
        try:
            price = self._validate_positive_amount(price, "price")
            face_value = self._validate_positive_amount(
                face_value, "face_value"
            )
            coupon_rate = self._validate_rate(coupon_rate)
            periods = self._validate_periods(periods)

            coupon_payment = face_value * coupon_rate

            # Use approximation method for YTM
            ytm = self._calculate_ytm_approximation(
                price, face_value, coupon_payment, periods
            )

            result = {
                "operation": "yield_to_maturity",
                "result": round(ytm, 6),
                "result_percentage": round(ytm * 100, 4),
                "inputs": {
                    "price": price,
                    "face_value": face_value,
                    "coupon_rate": coupon_rate,
                    "periods": periods,
                },
                "summary": {
                    "ytm_decimal": round(ytm, 6),
                    "ytm_percentage": round(ytm * 100, 4),
                    "coupon_payment": round(coupon_payment, 2),
                    "current_yield": round((coupon_payment / price) * 100, 4),
                },
                "metadata": self._base_metadata("iterative_approximation"),
            }

            return self._format_json_response(result)

        except (FinancialValidationError, FinancialComputationError):
            raise
        except (TypeError, ValueError, OverflowError, ZeroDivisionError) as e:
            self._log_unexpected_error("Failed to calculate YTM", e)
            raise FinancialComputationError(
                f"Failed to calculate YTM: {e}"
            ) from e

    @staticmethod
    def get_llm_usage_instructions() -> str:
        """Return short, text-first usage instructions for bond tools."""
        return """
<bond_calculator>
Bond pricing and yield. Tools return JSON strings.

Tools:
- calculate_bond_price(face_value, coupon_rate, periods, yield_rate)
- calculate_yield_to_maturity(price, face_value, coupon_rate, periods)

Notes:
- `coupon_rate` and `yield_rate` are per period as decimals.
</bond_calculator>
"""
