"""
Financial Calculator Tools v1.0

A comprehensive financial calculator toolkit providing essential financial calculations
including time value of money, investment analysis, loan calculations, bond pricing,
risk metrics, depreciation, and utility functions.

Author: Financial Calculator Tool
License: MIT
Version: 1.0.0
"""

import json
import math
import statistics
from datetime import datetime
from typing import List

from agno.tools.toolkit import Toolkit
from agno.utils.log import log_error, log_info


class FinancialCalculationError(Exception):
    """Base exception for financial calculation errors."""

    pass


class FinancialValidationError(FinancialCalculationError):
    """Exception for input validation errors."""

    pass


class FinancialComputationError(FinancialCalculationError):
    """Exception for computation errors (convergence, etc.)."""

    pass


class FinancialCalculatorTools(Toolkit):
    """
    Financial Calculator Tools v1.0

    A comprehensive toolkit for financial calculations including:
    - Time value of money calculations
    - Investment analysis metrics
    - Loan and amortization calculations
    - Bond pricing and yield calculations
    - Risk and performance metrics
    - Depreciation calculations
    - Currency and inflation utilities
    """

    def __init__(self, **kwargs):
        """Initialize Financial Calculator Tools."""
        super().__init__(name="financial_calculator_tools", **kwargs)

        # Register basic arithmetic operations
        self.register(self.add)
        self.register(self.subtract)
        self.register(self.multiply)
        self.register(self.divide)
        self.register(self.exponentiate)
        self.register(self.square_root)
        self.register(self.factorial)
        self.register(self.is_prime)

        # Register all financial calculation methods
        self.register(self.calculate_present_value)
        self.register(self.calculate_future_value)
        self.register(self.calculate_net_present_value)
        self.register(self.calculate_internal_rate_of_return)
        self.register(self.calculate_loan_payment)
        self.register(self.generate_amortization_schedule)
        self.register(self.calculate_compound_annual_growth_rate)
        self.register(self.calculate_return_on_investment)
        self.register(self.calculate_bond_price)
        self.register(self.calculate_yield_to_maturity)
        self.register(self.calculate_annuity_present_value)
        self.register(self.calculate_annuity_future_value)
        self.register(self.calculate_perpetuity_value)
        self.register(self.calculate_straight_line_depreciation)
        self.register(self.calculate_declining_balance_depreciation)
        self.register(self.convert_currency)
        self.register(self.adjust_for_inflation)
        self.register(self.calculate_sharpe_ratio)
        self.register(self.calculate_volatility)
        self.register(self.calculate_break_even_point)

        log_info(
            "Financial Calculator Tools initialized with basic arithmetic and 20 financial methods"
        )

    # Basic Arithmetic Operations
    def add(self, a: float, b: float) -> str:
        """
        Add two numbers and return the result.

        Args:
            a: First number
            b: Second number

        Returns:
            JSON string containing addition result
        """
        try:
            result = a + b

            response = {
                "operation": "addition",
                "result": result,
                "inputs": {"a": a, "b": b},
                "metadata": {
                    "calculation_method": "basic_arithmetic",
                    "timestamp": datetime.now().isoformat(),
                },
            }

            log_info(f"Adding {a} and {b} to get {result}")
            return self._format_json_response(response)

        except Exception as e:
            log_error(f"Error in addition: {e}")
            raise FinancialComputationError(f"Failed to add numbers: {e}")

    def subtract(self, a: float, b: float) -> str:
        """
        Subtract second number from first and return the result.

        Args:
            a: First number
            b: Second number

        Returns:
            JSON string containing subtraction result
        """
        try:
            result = a - b

            response = {
                "operation": "subtraction",
                "result": result,
                "inputs": {"a": a, "b": b},
                "metadata": {
                    "calculation_method": "basic_arithmetic",
                    "timestamp": datetime.now().isoformat(),
                },
            }

            log_info(f"Subtracting {b} from {a} to get {result}")
            return self._format_json_response(response)

        except Exception as e:
            log_error(f"Error in subtraction: {e}")
            raise FinancialComputationError(f"Failed to subtract numbers: {e}")

    def multiply(self, a: float, b: float) -> str:
        """
        Multiply two numbers and return the result.

        Args:
            a: First number
            b: Second number

        Returns:
            JSON string containing multiplication result
        """
        try:
            result = a * b

            response = {
                "operation": "multiplication",
                "result": result,
                "inputs": {"a": a, "b": b},
                "metadata": {
                    "calculation_method": "basic_arithmetic",
                    "timestamp": datetime.now().isoformat(),
                },
            }

            log_info(f"Multiplying {a} and {b} to get {result}")
            return self._format_json_response(response)

        except Exception as e:
            log_error(f"Error in multiplication: {e}")
            raise FinancialComputationError(f"Failed to multiply numbers: {e}")

    def divide(self, a: float, b: float) -> str:
        """
        Divide first number by second and return the result.

        Args:
            a: Numerator
            b: Denominator

        Returns:
            JSON string containing division result
        """
        try:
            if b == 0:
                raise FinancialComputationError("Division by zero is undefined")

            result = a / b

            response = {
                "operation": "division",
                "result": result,
                "inputs": {"a": a, "b": b},
                "metadata": {
                    "calculation_method": "basic_arithmetic",
                    "timestamp": datetime.now().isoformat(),
                },
            }

            log_info(f"Dividing {a} by {b} to get {result}")
            return self._format_json_response(response)

        except FinancialComputationError:
            raise
        except Exception as e:
            log_error(f"Error in division: {e}")
            raise FinancialComputationError(f"Failed to divide numbers: {e}")

    def exponentiate(self, a: float, b: float) -> str:
        """
        Raise first number to the power of the second number.

        Args:
            a: Base
            b: Exponent

        Returns:
            JSON string containing exponentiation result
        """
        try:
            result = math.pow(a, b)

            response = {
                "operation": "exponentiation",
                "result": result,
                "inputs": {"base": a, "exponent": b},
                "metadata": {
                    "calculation_method": "power_function",
                    "timestamp": datetime.now().isoformat(),
                },
            }

            log_info(f"Raising {a} to the power of {b} to get {result}")
            return self._format_json_response(response)

        except Exception as e:
            log_error(f"Error in exponentiation: {e}")
            raise FinancialComputationError(f"Failed to calculate power: {e}")

    def square_root(self, n: float) -> str:
        """
        Calculate the square root of a number.

        Args:
            n: Number to calculate square root of

        Returns:
            JSON string containing square root result
        """
        try:
            if n < 0:
                raise FinancialValidationError(
                    "Square root of negative number is undefined"
                )

            result = math.sqrt(n)

            response = {
                "operation": "square_root",
                "result": result,
                "inputs": {"number": n},
                "metadata": {
                    "calculation_method": "square_root_function",
                    "timestamp": datetime.now().isoformat(),
                },
            }

            log_info(f"Calculating square root of {n} to get {result}")
            return self._format_json_response(response)

        except (FinancialValidationError, FinancialComputationError):
            raise
        except Exception as e:
            log_error(f"Error in square root calculation: {e}")
            raise FinancialComputationError(f"Failed to calculate square root: {e}")

    def factorial(self, n: int) -> str:
        """
        Calculate the factorial of a number.

        Args:
            n: Number to calculate factorial of (must be non-negative integer)

        Returns:
            JSON string containing factorial result
        """
        try:
            if not isinstance(n, int) or n < 0:
                raise FinancialValidationError(
                    "Factorial requires a non-negative integer"
                )

            result = math.factorial(n)

            response = {
                "operation": "factorial",
                "result": result,
                "inputs": {"number": n},
                "metadata": {
                    "calculation_method": "factorial_function",
                    "timestamp": datetime.now().isoformat(),
                },
            }

            log_info(f"Calculating factorial of {n} to get {result}")
            return self._format_json_response(response)

        except (FinancialValidationError, FinancialComputationError):
            raise
        except Exception as e:
            log_error(f"Error in factorial calculation: {e}")
            raise FinancialComputationError(f"Failed to calculate factorial: {e}")

    def is_prime(self, n: int) -> str:
        """
        Check if a number is prime.

        Args:
            n: Number to check for primality

        Returns:
            JSON string containing prime check result
        """
        try:
            if not isinstance(n, int):
                raise FinancialValidationError("Prime check requires an integer")

            if n <= 1:
                is_prime_result = False
            elif n <= 3:
                is_prime_result = True
            elif n % 2 == 0 or n % 3 == 0:
                is_prime_result = False
            else:
                is_prime_result = True
                i = 5
                while i * i <= n:
                    if n % i == 0 or n % (i + 2) == 0:
                        is_prime_result = False
                        break
                    i += 6

            response = {
                "operation": "prime_check",
                "result": is_prime_result,
                "inputs": {"number": n},
                "metadata": {
                    "calculation_method": "prime_algorithm",
                    "timestamp": datetime.now().isoformat(),
                },
            }

            log_info(f"Checking if {n} is prime: {is_prime_result}")
            return self._format_json_response(response)

        except (FinancialValidationError, FinancialComputationError):
            raise
        except Exception as e:
            log_error(f"Error in prime check: {e}")
            raise FinancialComputationError(f"Failed to check if number is prime: {e}")

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

    def calculate_net_present_value(self, rate: float, cash_flows: List[float]) -> str:
        """
        Calculate the net present value of a series of cash flows.

        Args:
            rate: Discount rate per period (as decimal)
            cash_flows: List of cash flows (first is usually initial investment, negative)

        Returns:
            JSON string containing NPV calculation
        """
        try:
            rate = self._validate_rate(rate)
            cash_flows = self._validate_cash_flows(cash_flows)

            npv = 0
            for i, cash_flow in enumerate(cash_flows):
                if rate == 0:
                    npv += cash_flow
                else:
                    npv += cash_flow / ((1 + rate) ** i)

            result = {
                "operation": "net_present_value",
                "result": round(npv, 2),
                "inputs": {
                    "rate": rate,
                    "cash_flows": cash_flows,
                    "periods": len(cash_flows),
                },
                "metadata": {
                    "calculation_method": "discounted_cash_flow",
                    "interpretation": (
                        "positive_npv_profitable"
                        if npv > 0
                        else "negative_npv_unprofitable"
                    ),
                    "timestamp": datetime.now().isoformat(),
                },
            }

            log_info(f"Calculated NPV: {npv:.2f}")
            return self._format_json_response(result)

        except (FinancialValidationError, FinancialComputationError):
            raise
        except Exception as e:
            log_error(f"Unexpected error in NPV calculation: {e}")
            raise FinancialComputationError(f"Failed to calculate NPV: {e}")

    def calculate_internal_rate_of_return(
        self, cash_flows: List[float], guess: float = 0.1
    ) -> str:
        """
        Calculate the internal rate of return for a series of cash flows.

        Args:
            cash_flows: List of cash flows (first is usually initial investment, negative)
            guess: Initial guess for IRR (default: 0.1 or 10%)

        Returns:
            JSON string containing IRR calculation
        """
        try:
            cash_flows = self._validate_cash_flows(cash_flows)

            # Use Newton-Raphson method to find IRR
            irr = self._calculate_irr_newton_raphson(cash_flows, guess)

            result = {
                "operation": "internal_rate_of_return",
                "result": round(irr, 6),
                "result_percentage": round(irr * 100, 4),
                "inputs": {
                    "cash_flows": cash_flows,
                    "periods": len(cash_flows),
                    "initial_guess": guess,
                },
                "metadata": {
                    "calculation_method": "newton_raphson",
                    "interpretation": "rate_of_return_percentage",
                    "timestamp": datetime.now().isoformat(),
                },
            }

            log_info(f"Calculated IRR: {irr:.4%}")
            return self._format_json_response(result)

        except (FinancialValidationError, FinancialComputationError):
            raise
        except Exception as e:
            log_error(f"Unexpected error in IRR calculation: {e}")
            raise FinancialComputationError(f"Failed to calculate IRR: {e}")

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

    def calculate_compound_annual_growth_rate(
        self, begin_value: float, end_value: float, years: int
    ) -> str:
        """
        Calculate the compound annual growth rate (CAGR).

        Args:
            begin_value: Initial investment value
            end_value: Final investment value
            years: Number of years

        Returns:
            JSON string containing CAGR calculation
        """
        try:
            begin_value = self._validate_positive_amount(begin_value, "begin_value")
            end_value = self._validate_positive_amount(end_value, "end_value")
            years = self._validate_periods(years)

            cagr = (end_value / begin_value) ** (1 / years) - 1
            total_return = (end_value - begin_value) / begin_value

            result = {
                "operation": "compound_annual_growth_rate",
                "result": round(cagr, 6),
                "result_percentage": round(cagr * 100, 4),
                "inputs": {
                    "begin_value": begin_value,
                    "end_value": end_value,
                    "years": years,
                },
                "summary": {
                    "cagr_decimal": round(cagr, 6),
                    "cagr_percentage": round(cagr * 100, 4),
                    "total_return_percentage": round(total_return * 100, 2),
                    "total_growth": round(end_value - begin_value, 2),
                },
                "metadata": {
                    "calculation_method": "geometric_mean",
                    "timestamp": datetime.now().isoformat(),
                },
            }

            log_info(f"Calculated CAGR: {cagr:.4%}")
            return self._format_json_response(result)

        except (FinancialValidationError, FinancialComputationError):
            raise
        except Exception as e:
            log_error(f"Unexpected error in CAGR calculation: {e}")
            raise FinancialComputationError(f"Failed to calculate CAGR: {e}")

    def calculate_return_on_investment(self, gain: float, cost: float) -> str:
        """
        Calculate the return on investment (ROI).

        Args:
            gain: Total gain from investment
            cost: Initial cost of investment

        Returns:
            JSON string containing ROI calculation
        """
        try:
            cost = self._validate_positive_amount(cost, "cost")
            # Gain can be negative (loss)

            roi = gain / cost
            roi_percentage = roi * 100

            result = {
                "operation": "return_on_investment",
                "result": round(roi, 6),
                "result_percentage": round(roi_percentage, 4),
                "inputs": {"gain": gain, "cost": cost},
                "summary": {
                    "roi_decimal": round(roi, 6),
                    "roi_percentage": round(roi_percentage, 4),
                    "total_value": cost + gain,
                    "profit_loss": gain,
                },
                "metadata": {
                    "calculation_method": "simple_roi",
                    "interpretation": "profit" if gain > 0 else "loss",
                    "timestamp": datetime.now().isoformat(),
                },
            }

            log_info(f"Calculated ROI: {roi:.4%}")
            return self._format_json_response(result)

        except (FinancialValidationError, FinancialComputationError):
            raise
        except Exception as e:
            log_error(f"Unexpected error in ROI calculation: {e}")
            raise FinancialComputationError(f"Failed to calculate ROI: {e}")

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

    def convert_currency(self, amount: float, rate: float) -> str:
        """
        Convert an amount from one currency to another using a given exchange rate.

        Args:
            amount: Amount to convert
            rate: Exchange rate (target per source)

        Returns:
            JSON string containing currency conversion
        """
        try:
            amount = self._validate_positive_amount(amount, "amount")
            rate = self._validate_positive_amount(rate, "rate")

            converted_amount = amount * rate

            result = {
                "operation": "currency_conversion",
                "result": round(converted_amount, 2),
                "inputs": {"amount": amount, "exchange_rate": rate},
                "summary": {
                    "original_amount": amount,
                    "converted_amount": round(converted_amount, 2),
                    "exchange_rate": rate,
                },
                "metadata": {
                    "calculation_method": "simple_multiplication",
                    "timestamp": datetime.now().isoformat(),
                },
            }

            log_info(f"Converted currency: {amount} -> {converted_amount:.2f}")
            return self._format_json_response(result)

        except (FinancialValidationError, FinancialComputationError):
            raise
        except Exception as e:
            log_error(f"Unexpected error in currency conversion: {e}")
            raise FinancialComputationError(f"Failed to convert currency: {e}")

    def adjust_for_inflation(self, amount: float, rate: float, periods: int) -> str:
        """
        Adjust an amount for inflation over a number of periods.

        Args:
            amount: Initial amount
            rate: Inflation rate per period (as decimal)
            periods: Number of periods

        Returns:
            JSON string containing inflation adjustment
        """
        try:
            amount = self._validate_positive_amount(amount, "amount")
            rate = self._validate_rate(rate)
            periods = self._validate_periods(periods)

            adjusted_amount = amount * ((1 + rate) ** periods)
            inflation_impact = adjusted_amount - amount

            result = {
                "operation": "inflation_adjustment",
                "result": round(adjusted_amount, 2),
                "inputs": {
                    "original_amount": amount,
                    "inflation_rate": rate,
                    "periods": periods,
                },
                "summary": {
                    "original_amount": amount,
                    "adjusted_amount": round(adjusted_amount, 2),
                    "inflation_impact": round(inflation_impact, 2),
                    "purchasing_power_loss": round((inflation_impact / amount) * 100, 2),
                },
                "metadata": {
                    "calculation_method": "compound_inflation",
                    "timestamp": datetime.now().isoformat(),
                },
            }

            log_info(f"Adjusted for inflation: {amount} -> {adjusted_amount:.2f}")
            return self._format_json_response(result)

        except (FinancialValidationError, FinancialComputationError):
            raise
        except Exception as e:
            log_error(f"Unexpected error in inflation adjustment: {e}")
            raise FinancialComputationError(f"Failed to adjust for inflation: {e}")

    def calculate_sharpe_ratio(self, returns: List[float], risk_free_rate: float) -> str:
        """
        Calculate the Sharpe ratio for an investment.

        Args:
            returns: List of periodic returns (as decimals)
            risk_free_rate: Risk-free rate per period (as decimal)

        Returns:
            JSON string containing Sharpe ratio calculation
        """
        try:
            returns = self._validate_returns_list(returns)
            risk_free_rate = self._validate_rate(risk_free_rate)

            if len(returns) < 2:
                raise FinancialValidationError("At least 2 return observations required")

            mean_return = statistics.mean(returns)
            std_deviation = statistics.stdev(returns)

            if std_deviation == 0:
                raise FinancialComputationError(
                    "Cannot calculate Sharpe ratio with zero volatility"
                )

            excess_return = mean_return - risk_free_rate
            sharpe_ratio = excess_return / std_deviation

            result = {
                "operation": "sharpe_ratio",
                "result": round(sharpe_ratio, 4),
                "inputs": {
                    "returns": returns,
                    "risk_free_rate": risk_free_rate,
                    "observations": len(returns),
                },
                "summary": {
                    "sharpe_ratio": round(sharpe_ratio, 4),
                    "mean_return": round(mean_return, 4),
                    "volatility": round(std_deviation, 4),
                    "excess_return": round(excess_return, 4),
                },
                "metadata": {
                    "calculation_method": "sharpe_ratio_formula",
                    "timestamp": datetime.now().isoformat(),
                },
            }

            log_info(f"Calculated Sharpe ratio: {sharpe_ratio:.4f}")
            return self._format_json_response(result)

        except (FinancialValidationError, FinancialComputationError):
            raise
        except Exception as e:
            log_error(f"Unexpected error in Sharpe ratio calculation: {e}")
            raise FinancialComputationError(f"Failed to calculate Sharpe ratio: {e}")

    def calculate_volatility(self, returns: List[float]) -> str:
        """
        Calculate the volatility (standard deviation) of returns.

        Args:
            returns: List of periodic returns (as decimals)

        Returns:
            JSON string containing volatility calculation
        """
        try:
            returns = self._validate_returns_list(returns)

            if len(returns) < 2:
                raise FinancialValidationError("At least 2 return observations required")

            mean_return = statistics.mean(returns)
            volatility = statistics.stdev(returns)
            variance = statistics.variance(returns)

            result = {
                "operation": "volatility",
                "result": round(volatility, 6),
                "result_percentage": round(volatility * 100, 4),
                "inputs": {"returns": returns, "observations": len(returns)},
                "summary": {
                    "volatility_decimal": round(volatility, 6),
                    "volatility_percentage": round(volatility * 100, 4),
                    "variance": round(variance, 6),
                    "mean_return": round(mean_return, 4),
                },
                "metadata": {
                    "calculation_method": "standard_deviation",
                    "timestamp": datetime.now().isoformat(),
                },
            }

            log_info(f"Calculated volatility: {volatility:.4%}")
            return self._format_json_response(result)

        except (FinancialValidationError, FinancialComputationError):
            raise
        except Exception as e:
            log_error(f"Unexpected error in volatility calculation: {e}")
            raise FinancialComputationError(f"Failed to calculate volatility: {e}")

    def calculate_break_even_point(
        self, fixed_costs: float, price_per_unit: float, variable_cost_per_unit: float
    ) -> str:
        """
        Calculate the break-even point in units or sales.

        Args:
            fixed_costs: Total fixed costs
            price_per_unit: Selling price per unit
            variable_cost_per_unit: Variable cost per unit

        Returns:
            JSON string containing break-even analysis
        """
        try:
            fixed_costs = self._validate_positive_amount(fixed_costs, "fixed_costs")
            price_per_unit = self._validate_positive_amount(
                price_per_unit, "price_per_unit"
            )
            variable_cost_per_unit = max(0, variable_cost_per_unit)  # Can be zero

            if price_per_unit <= variable_cost_per_unit:
                raise FinancialValidationError(
                    "Price per unit must be greater than variable cost per unit"
                )

            contribution_margin = price_per_unit - variable_cost_per_unit
            break_even_units = fixed_costs / contribution_margin
            break_even_sales = break_even_units * price_per_unit

            result = {
                "operation": "break_even_point",
                "result": round(break_even_units, 2),
                "inputs": {
                    "fixed_costs": fixed_costs,
                    "price_per_unit": price_per_unit,
                    "variable_cost_per_unit": variable_cost_per_unit,
                },
                "summary": {
                    "break_even_units": round(break_even_units, 2),
                    "break_even_sales": round(break_even_sales, 2),
                    "contribution_margin": round(contribution_margin, 2),
                    "contribution_margin_ratio": round(
                        (contribution_margin / price_per_unit) * 100, 2
                    ),
                },
                "metadata": {
                    "calculation_method": "contribution_margin_analysis",
                    "timestamp": datetime.now().isoformat(),
                },
            }

            log_info(f"Calculated break-even point: {break_even_units:.2f} units")
            return self._format_json_response(result)

        except (FinancialValidationError, FinancialComputationError):
            raise
        except Exception as e:
            log_error(f"Unexpected error in break-even calculation: {e}")
            raise FinancialComputationError(f"Failed to calculate break-even point: {e}")

    # Helper methods for validation and calculations
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
        """Validate cash flows list."""
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
        """Validate returns list."""
        if not isinstance(returns, list) or len(returns) < 1:
            raise FinancialValidationError("Returns must be a list with at least 1 value")

        validated_returns = []
        for i, ret in enumerate(returns):
            if not isinstance(ret, (int, float)):
                raise FinancialValidationError(f"Return at index {i} must be a number")
            validated_returns.append(float(ret))

        return validated_returns

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

    def _format_json_response(self, data: dict) -> str:
        """Format response as JSON string."""
        try:
            return json.dumps(data, indent=2, ensure_ascii=False)
        except Exception as e:
            log_error(f"Error formatting JSON response: {e}")
            return json.dumps({"error": "Failed to format response", "data": str(data)})

    @staticmethod
    def get_llm_usage_instructions() -> str:
        """
        Returns detailed instructions for LLMs on how to use each tool in FinancialCalculatorTools.
        Each instruction includes the method name, description, parameters, types, and example values.
        """
        instructions = """
*** Financial Calculator Tools Instructions ***

By leveraging the following comprehensive set of calculation tools, you can perform both basic arithmetic operations and advanced financial computations including time value of money calculations, investment analysis, loan calculations, bond pricing, risk metrics, depreciation, and utility functions. These tools provide accurate calculations with detailed results and metadata. Here are the detailed instructions for using each tool:

**BASIC ARITHMETIC OPERATIONS:**

- Use add to add two numbers together.
   Parameters:
      - a (float): First number, e.g., 15.5
      - b (float): Second number, e.g., 23.7

- Use subtract to subtract the second number from the first.
   Parameters:
      - a (float): First number (minuend), e.g., 100.0
      - b (float): Second number (subtrahend), e.g., 25.0

- Use multiply to multiply two numbers together.
   Parameters:
      - a (float): First number, e.g., 12.5
      - b (float): Second number, e.g., 8.0

- Use divide to divide the first number by the second.
   Parameters:
      - a (float): Numerator, e.g., 144.0
      - b (float): Denominator, e.g., 12.0

- Use exponentiate to raise the first number to the power of the second.
   Parameters:
      - a (float): Base number, e.g., 2.0
      - b (float): Exponent, e.g., 8.0

- Use square_root to calculate the square root of a number.
   Parameters:
      - n (float): Number to find square root of, e.g., 64.0

- Use factorial to calculate the factorial of a non-negative integer.
   Parameters:
      - n (int): Non-negative integer, e.g., 5

- Use is_prime to check if a number is prime.
   Parameters:
      - n (int): Integer to check for primality, e.g., 17

**TIME VALUE OF MONEY CALCULATIONS:**

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

**INVESTMENT ANALYSIS:**

- Use calculate_net_present_value to calculate NPV of a series of cash flows.
   Parameters:
      - rate (float): Discount rate per period as decimal, e.g., 0.10 for 10%
      - cash_flows (List[float]): List of cash flows, e.g., [-1000, 300, 400, 500, 600]

- Use calculate_internal_rate_of_return to calculate IRR for a series of cash flows.
   Parameters:
      - cash_flows (List[float]): List of cash flows, e.g., [-1000, 300, 400, 500, 600]
      - guess (float, optional): Initial guess for IRR, default 0.1

- Use calculate_compound_annual_growth_rate to calculate CAGR.
   Parameters:
      - begin_value (float): Initial investment value, e.g., 1000.0
      - end_value (float): Final investment value, e.g., 1500.0
      - years (int): Number of years, e.g., 3

- Use calculate_return_on_investment to calculate ROI percentage.
   Parameters:
      - gain (float): Total gain from investment, e.g., 500.0
      - cost (float): Initial cost of investment, e.g., 1000.0

**LOAN CALCULATIONS:**

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

**BOND CALCULATIONS:**

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

**RISK AND PERFORMANCE METRICS:**

- Use calculate_sharpe_ratio to calculate risk-adjusted returns.
   Parameters:
      - returns (List[float]): List of periodic returns as decimals, e.g., [0.10, 0.15, -0.05, 0.20]
      - risk_free_rate (float): Risk-free rate per period as decimal, e.g., 0.02

- Use calculate_volatility to calculate standard deviation of returns.
   Parameters:
      - returns (List[float]): List of periodic returns as decimals, e.g., [0.08, 0.12, -0.03, 0.18]

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

**BUSINESS ANALYSIS:**

- Use calculate_break_even_point to find break-even in units or sales.
   Parameters:
      - fixed_costs (float): Total fixed costs, e.g., 10000.0
      - price_per_unit (float): Selling price per unit, e.g., 25.0
      - variable_cost_per_unit (float): Variable cost per unit, e.g., 15.0

**UTILITY FUNCTIONS:**

- Use convert_currency for simple currency conversion.
   Parameters:
      - amount (float): Amount to convert, e.g., 1000.0
      - rate (float): Exchange rate (target per source), e.g., 1.25

- Use adjust_for_inflation to adjust amounts for inflation.
   Parameters:
      - amount (float): Initial amount, e.g., 1000.0
      - rate (float): Inflation rate per period as decimal, e.g., 0.03
      - periods (int): Number of periods, e.g., 5

**NOTES:**
- All rates should be provided as decimals (e.g., 0.05 for 5%)
- Cash flows lists should have the initial investment as the first (usually negative) value
- All monetary amounts should be positive unless specifically noted
- Results include detailed metadata and calculation summaries
- Error handling provides clear validation messages for invalid inputs
"""
        return instructions
