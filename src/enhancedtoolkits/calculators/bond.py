"""
Bond Calculator

Provides bond calculations including bond pricing and yield to maturity calculations.
"""

from datetime import datetime

from agno.utils.log import log_error, log_info

from .base import (
    BaseCalculatorTools,
    FinancialComputationError,
    FinancialValidationError,
)


class BondCalculatorTools(BaseCalculatorTools):
    """Calculator for bond calculations."""

    def __init__(self, **kwargs):
        """Initialize the bond calculator and register all methods."""
        self.add_instructions = True
        self.instructions = BondCalculatorTools.get_llm_usage_instructions()

        super().__init__(name="bond_calculator", **kwargs)

        # Register all bond methods
        self.register(self.calculate_bond_price)
        self.register(self.calculate_yield_to_maturity)

    def calculate_bond_price(
        self, face_value: float, coupon_rate: float, periods: int, yield_rate: float
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
            face_value = self._validate_positive_amount(face_value, "face_value")
            coupon_rate = self._validate_rate(coupon_rate)
            yield_rate = self._validate_rate(yield_rate)
            periods = self._validate_periods(periods)

            coupon_payment = face_value * coupon_rate

            if yield_rate == 0:
                bond_price = face_value + (coupon_payment * periods)
            else:
                # Present value of coupon payments
                pv_coupons = (
                    coupon_payment * (1 - (1 + yield_rate) ** -periods) / yield_rate
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
                "metadata": {
                    "calculation_method": "present_value_cash_flows",
                    "timestamp": datetime.now().isoformat(),
                },
            }

            log_info(f"Calculated bond price: {bond_price:.2f}")
            return self._format_json_response(result)

        except (FinancialValidationError, FinancialComputationError):
            raise
        except Exception as e:
            log_error(f"Unexpected error in bond price calculation: {e}")
            raise FinancialComputationError(f"Failed to calculate bond price: {e}")

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
            face_value = self._validate_positive_amount(face_value, "face_value")
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
                "metadata": {
                    "calculation_method": "iterative_approximation",
                    "timestamp": datetime.now().isoformat(),
                },
            }

            log_info(f"Calculated YTM: {ytm:.4%}")
            return self._format_json_response(result)

        except (FinancialValidationError, FinancialComputationError):
            raise
        except Exception as e:
            log_error(f"Unexpected error in YTM calculation: {e}")
            raise FinancialComputationError(f"Failed to calculate YTM: {e}")

    @staticmethod
    def get_llm_usage_instructions() -> str:
        """
        Returns detailed instructions for LLMs on how to use bond calculations.
        """
        return """
<bond_calculations_tools_instructions>
**BOND CALCULATIONS TOOLS:**

- Use calculate_bond_price to calculate the price of a bond.
   Parameters:
      - face_value (float): Bond face value, e.g., 1000.0
      - coupon_rate (float): Annual coupon rate as decimal, e.g., 0.06
      - periods (int): Number of periods until maturity, e.g., 10
      - yield_rate (float): Yield to maturity per period as decimal, e.g., 0.07

- Use calculate_yield_to_maturity to estimate YTM for a bond.
   Parameters:
      - price (float): Current bond price, e.g., 950.0
      - face_value (float): Bond face value, e.g., 1000.0
      - coupon_rate (float): Annual coupon rate as decimal, e.g., 0.05
      - periods (int): Number of periods until maturity, e.g., 8

</bond_calculations_tools_instructions>
"""
