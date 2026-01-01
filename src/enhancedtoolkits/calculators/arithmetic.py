"""
Basic Arithmetic Calculator

Provides basic arithmetic operations including addition, subtraction,
multiplication, division, exponentiation, square root, factorial, prime checking,
modulo, absolute value, rounding, logarithms, GCD/LCM, and basic statistics.
"""

import math
import statistics
from datetime import datetime
from math import gcd as math_gcd
from typing import List

from agno.utils.log import log_info

from .base import (
    BaseCalculatorTools,
    FinancialComputationError,
    FinancialValidationError,
)


class ArithmeticCalculatorTools(BaseCalculatorTools):
    """Calculator for basic arithmetic operations."""

    def __init__(self, add_instructions: bool = True, **kwargs):
        """Initialize the arithmetic calculator and register all methods."""
        instructions = (
            self.get_llm_usage_instructions() if add_instructions else ""
        )
        super().__init__(
            name="basic_arithmetic_calculator",
            add_instructions=add_instructions,
            instructions=instructions,
            **kwargs,
        )

        # Register core arithmetic methods
        for fn in (
            self.add,
            self.subtract,
            self.multiply,
            self.divide,
            self.exponentiate,
            self.square_root,
            self.factorial,
            self.is_prime,
            self.modulo,
            self.absolute,
            self.round_number,
            self.log,
            self.ln,
            self.gcd,
            self.lcm,
            self.mean,
            self.median,
            self.standard_deviation,
        ):
            self.register(fn)

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

        except (TypeError, ValueError, OverflowError, ZeroDivisionError) as e:
            self._log_unexpected_error("Failed to add numbers", e)
            raise FinancialComputationError(
                f"Failed to add numbers: {e}"
            ) from e

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

        except (TypeError, ValueError, OverflowError, ZeroDivisionError) as e:
            self._log_unexpected_error("Failed to subtract numbers", e)
            raise FinancialComputationError(
                f"Failed to subtract numbers: {e}"
            ) from e

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

        except (TypeError, ValueError, OverflowError, ZeroDivisionError) as e:
            self._log_unexpected_error("Failed to multiply numbers", e)
            raise FinancialComputationError(
                f"Failed to multiply numbers: {e}"
            ) from e

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
                raise FinancialComputationError(
                    "Division by zero is undefined"
                )

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
        except (TypeError, ValueError, OverflowError, ZeroDivisionError) as e:
            self._log_unexpected_error("Failed to divide numbers", e)
            raise FinancialComputationError(
                f"Failed to divide numbers: {e}"
            ) from e

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

        except (TypeError, ValueError, OverflowError, ZeroDivisionError) as e:
            self._log_unexpected_error("Failed to calculate power", e)
            raise FinancialComputationError(
                f"Failed to calculate power: {e}"
            ) from e

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
        except (TypeError, ValueError, OverflowError, ZeroDivisionError) as e:
            self._log_unexpected_error("Failed to calculate square root", e)
            raise FinancialComputationError(
                f"Failed to calculate square root: {e}"
            ) from e

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
        except (TypeError, ValueError, OverflowError, ZeroDivisionError) as e:
            self._log_unexpected_error("Failed to calculate factorial", e)
            raise FinancialComputationError(
                f"Failed to calculate factorial: {e}"
            ) from e

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
                raise FinancialValidationError(
                    "Prime check requires an integer"
                )

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
        except (TypeError, ValueError, OverflowError, ZeroDivisionError) as e:
            self._log_unexpected_error(
                "Failed to check if number is prime",
                e,
            )
            raise FinancialComputationError(
                f"Failed to check if number is prime: {e}"
            ) from e

    def modulo(self, a: float, b: float) -> str:
        """
        Calculate the remainder when a is divided by b.

        Args:
            a: Dividend
            b: Divisor

        Returns:
            JSON string containing modulo result
        """
        try:
            if b == 0:
                raise FinancialComputationError("Modulo by zero is undefined")

            result = a % b

            response = {
                "operation": "modulo",
                "result": result,
                "inputs": {"a": a, "b": b},
                "metadata": {
                    "calculation_method": "modulo_operation",
                    "timestamp": datetime.now().isoformat(),
                },
            }

            log_info(f"Calculating {a} modulo {b} to get {result}")
            return self._format_json_response(response)

        except FinancialComputationError:
            raise
        except (TypeError, ValueError, OverflowError, ZeroDivisionError) as e:
            self._log_unexpected_error("Failed to calculate modulo", e)
            raise FinancialComputationError(
                f"Failed to calculate modulo: {e}"
            ) from e

    def absolute(self, n: float) -> str:
        """
        Calculate the absolute value of a number.

        Args:
            n: Number to find absolute value of

        Returns:
            JSON string containing absolute value result
        """
        try:
            result = abs(n)

            response = {
                "operation": "absolute_value",
                "result": result,
                "inputs": {"number": n},
                "metadata": {
                    "calculation_method": "abs_function",
                    "timestamp": datetime.now().isoformat(),
                },
            }

            log_info(f"Calculating absolute value of {n} to get {result}")
            return self._format_json_response(response)

        except (TypeError, ValueError, OverflowError, ZeroDivisionError) as e:
            self._log_unexpected_error("Failed to calculate absolute value", e)
            raise FinancialComputationError(
                f"Failed to calculate absolute value: {e}"
            ) from e

    def round_number(self, n: float, decimals: int = 0) -> str:
        """
        Round a number to specified decimal places.

        Args:
            n: Number to round
            decimals: Number of decimal places (default: 0)

        Returns:
            JSON string containing rounded number result
        """
        try:
            if not isinstance(decimals, int):
                raise FinancialValidationError("Decimals must be an integer")

            result = round(n, decimals)

            response = {
                "operation": "round",
                "result": result,
                "inputs": {"number": n, "decimals": decimals},
                "metadata": {
                    "calculation_method": "round_function",
                    "timestamp": datetime.now().isoformat(),
                },
            }

            log_info(
                f"Rounding {n} to {decimals} decimal places to get {result}"
            )
            return self._format_json_response(response)

        except (FinancialValidationError, FinancialComputationError):
            raise
        except (TypeError, ValueError, OverflowError, ZeroDivisionError) as e:
            self._log_unexpected_error("Failed to round number", e)
            raise FinancialComputationError(
                f"Failed to round number: {e}"
            ) from e

    def log(self, n: float, base: float = 10.0) -> str:
        """
        Calculate logarithm with specified base.

        Args:
            n: Number to calculate logarithm of
            base: Logarithm base (default: 10.0)

        Returns:
            JSON string containing logarithm result
        """
        try:
            if n <= 0:
                raise FinancialValidationError(
                    "Logarithm is only defined for positive numbers"
                )
            if base <= 0 or base == 1:
                raise FinancialValidationError(
                    "Logarithm base must be positive and not equal to 1"
                )

            result = math.log(n, base)

            response = {
                "operation": "logarithm",
                "result": result,
                "inputs": {"number": n, "base": base},
                "metadata": {
                    "calculation_method": "logarithm_function",
                    "timestamp": datetime.now().isoformat(),
                },
            }

            log_info(f"Calculating log base {base} of {n} to get {result}")
            return self._format_json_response(response)

        except (FinancialValidationError, FinancialComputationError):
            raise
        except (TypeError, ValueError, OverflowError, ZeroDivisionError) as e:
            self._log_unexpected_error("Failed to calculate logarithm", e)
            raise FinancialComputationError(
                f"Failed to calculate logarithm: {e}"
            ) from e

    def ln(self, n: float) -> str:
        """
        Calculate natural logarithm (base e).

        Args:
            n: Number to calculate natural logarithm of

        Returns:
            JSON string containing natural logarithm result
        """
        try:
            if n <= 0:
                raise FinancialValidationError(
                    "Natural logarithm is only defined for positive numbers"
                )

            result = math.log(n)  # math.log defaults to natural logarithm

            response = {
                "operation": "natural_logarithm",
                "result": result,
                "inputs": {"number": n},
                "metadata": {
                    "calculation_method": "natural_logarithm_function",
                    "timestamp": datetime.now().isoformat(),
                },
            }

            log_info(f"Calculating natural logarithm of {n} to get {result}")
            return self._format_json_response(response)

        except (FinancialValidationError, FinancialComputationError):
            raise
        except (TypeError, ValueError, OverflowError, ZeroDivisionError) as e:
            self._log_unexpected_error(
                "Failed to calculate natural logarithm",
                e,
            )
            raise FinancialComputationError(
                f"Failed to calculate natural logarithm: {e}"
            ) from e

    def gcd(self, a: int, b: int) -> str:
        """
        Calculate greatest common divisor of two integers.

        Args:
            a: First integer
            b: Second integer

        Returns:
            JSON string containing GCD result
        """
        try:
            if not isinstance(a, int) or not isinstance(b, int):
                raise FinancialValidationError("GCD requires integer inputs")

            result = math_gcd(abs(a), abs(b))

            response = {
                "operation": "greatest_common_divisor",
                "result": result,
                "inputs": {"a": a, "b": b},
                "metadata": {
                    "calculation_method": "euclidean_algorithm",
                    "timestamp": datetime.now().isoformat(),
                },
            }

            log_info(f"Calculating GCD of {a} and {b} to get {result}")
            return self._format_json_response(response)

        except (FinancialValidationError, FinancialComputationError):
            raise
        except (TypeError, ValueError, OverflowError, ZeroDivisionError) as e:
            self._log_unexpected_error("Failed to calculate GCD", e)
            raise FinancialComputationError(
                f"Failed to calculate GCD: {e}"
            ) from e

    def lcm(self, a: int, b: int) -> str:
        """
        Calculate least common multiple of two integers.

        Args:
            a: First integer
            b: Second integer

        Returns:
            JSON string containing LCM result
        """
        try:
            if not isinstance(a, int) or not isinstance(b, int):
                raise FinancialValidationError("LCM requires integer inputs")
            if a == 0 or b == 0:
                raise FinancialValidationError(
                    "LCM is undefined when any input is zero"
                )

            # LCM(a, b) = |a * b| / GCD(a, b)
            result = abs(a * b) // math_gcd(abs(a), abs(b))

            response = {
                "operation": "least_common_multiple",
                "result": result,
                "inputs": {"a": a, "b": b},
                "metadata": {
                    "calculation_method": "gcd_based_lcm",
                    "timestamp": datetime.now().isoformat(),
                },
            }

            log_info(f"Calculating LCM of {a} and {b} to get {result}")
            return self._format_json_response(response)

        except (FinancialValidationError, FinancialComputationError):
            raise
        except (TypeError, ValueError, OverflowError, ZeroDivisionError) as e:
            self._log_unexpected_error("Failed to calculate LCM", e)
            raise FinancialComputationError(
                f"Failed to calculate LCM: {e}"
            ) from e

    def mean(self, numbers: List[float]) -> str:
        """
        Calculate arithmetic mean of a list of numbers.

        Args:
            numbers: List of numbers

        Returns:
            JSON string containing mean result
        """
        try:
            if not numbers:
                raise FinancialValidationError(
                    "Cannot calculate mean of empty list"
                )

            # Validate all elements are numbers
            for num in numbers:
                if not isinstance(num, (int, float)):
                    raise FinancialValidationError(
                        "All elements must be numbers"
                    )

            result = statistics.mean(numbers)

            response = {
                "operation": "arithmetic_mean",
                "result": result,
                "inputs": {"numbers": numbers},
                "metadata": {
                    "calculation_method": "statistical_mean",
                    "count": len(numbers),
                    "timestamp": datetime.now().isoformat(),
                },
            }

            log_info(
                f"Calculating mean of {len(numbers)} numbers to get {result}"
            )
            return self._format_json_response(response)

        except (FinancialValidationError, FinancialComputationError):
            raise
        except (TypeError, ValueError, OverflowError, ZeroDivisionError) as e:
            self._log_unexpected_error("Failed to calculate mean", e)
            raise FinancialComputationError(
                f"Failed to calculate mean: {e}"
            ) from e

    def median(self, numbers: List[float]) -> str:
        """
        Calculate median of a list of numbers.

        Args:
            numbers: List of numbers

        Returns:
            JSON string containing median result
        """
        try:
            if not numbers:
                raise FinancialValidationError(
                    "Cannot calculate median of empty list"
                )

            # Validate all elements are numbers
            for num in numbers:
                if not isinstance(num, (int, float)):
                    raise FinancialValidationError(
                        "All elements must be numbers"
                    )

            result = statistics.median(numbers)

            response = {
                "operation": "median",
                "result": result,
                "inputs": {"numbers": numbers},
                "metadata": {
                    "calculation_method": "statistical_median",
                    "count": len(numbers),
                    "timestamp": datetime.now().isoformat(),
                },
            }

            log_info(
                f"Calculating median of {len(numbers)} numbers to get {result}"
            )
            return self._format_json_response(response)

        except (FinancialValidationError, FinancialComputationError):
            raise
        except (TypeError, ValueError, OverflowError, ZeroDivisionError) as e:
            self._log_unexpected_error("Failed to calculate median", e)
            raise FinancialComputationError(
                f"Failed to calculate median: {e}"
            ) from e

    def standard_deviation(self, numbers: List[float]) -> str:
        """
        Calculate standard deviation of a list of numbers.

        Args:
            numbers: List of numbers

        Returns:
            JSON string containing standard deviation result
        """
        try:
            if len(numbers) < 2:
                raise FinancialValidationError(
                    "Standard deviation requires at least two values"
                )

            # Validate all elements are numbers
            for num in numbers:
                if not isinstance(num, (int, float)):
                    raise FinancialValidationError(
                        "All elements must be numbers"
                    )

            # Calculate population standard deviation
            population_std_dev = statistics.pstdev(numbers)

            # Calculate sample standard deviation
            sample_std_dev = statistics.stdev(numbers)

            response = {
                "operation": "standard_deviation",
                "result": sample_std_dev,  # Default to sample standard deviation
                "inputs": {"numbers": numbers},
                "summary": {
                    "sample_standard_deviation": sample_std_dev,
                    "population_standard_deviation": population_std_dev,
                    "variance": statistics.variance(numbers),
                    "mean": statistics.mean(numbers),
                },
                "metadata": {
                    "calculation_method": "statistical_standard_deviation",
                    "count": len(numbers),
                    "timestamp": datetime.now().isoformat(),
                },
            }

            log_info(
                f"Calculating standard deviation of {len(numbers)} numbers to get {sample_std_dev}"
            )
            return self._format_json_response(response)

        except (FinancialValidationError, FinancialComputationError):
            raise
        except (TypeError, ValueError, OverflowError, ZeroDivisionError) as e:
            self._log_unexpected_error(
                "Failed to calculate standard deviation",
                e,
            )
            raise FinancialComputationError(
                f"Failed to calculate standard deviation: {e}"
            ) from e

    @staticmethod
    def get_llm_usage_instructions() -> str:
        """Return short, text-first usage instructions for arithmetic tools."""
        return """
<arithmetic_calculator>
Arithmetic utilities. Tools return JSON strings.

Core tools:
- add(a, b)
- subtract(a, b)
- multiply(a, b)
- divide(a, b)
- exponentiate(a, b)
- square_root(n)
- factorial(n)
- is_prime(n)

Extras:
- modulo(a, b)
- absolute(n)
- round_number(n, decimals=0)
- log(n, base=10.0)  # n>0, base>0, base!=1
- ln(n)  # n>0
- gcd(a, b)
- lcm(a, b)
- mean(numbers)
- median(numbers)
- standard_deviation(numbers)  # requires at least 2 values
</arithmetic_calculator>
"""
