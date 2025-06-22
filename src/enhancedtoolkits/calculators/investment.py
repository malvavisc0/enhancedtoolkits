"""
Investment Analysis Calculator

Provides investment analysis calculations including NPV, IRR, CAGR, and ROI.
"""

from datetime import datetime
from typing import List

from agno.utils.log import log_error, log_info

from .base import (
    BaseCalculatorTools,
    FinancialComputationError,
    FinancialValidationError,
)


class InvestmentAnalysisCalculatorTools(BaseCalculatorTools):
    """Calculator for investment analysis calculations."""

    def __init__(self, **kwargs):
        """Initialize the investment analysis calculator and register all methods."""
        self.add_instructions = True
        self.instructions = InvestmentAnalysisCalculatorTools.get_llm_usage_instructions()

        super().__init__(name="investment_analysis_calculator", **kwargs)

        # Register all investment analysis methods
        self.register(self.calculate_net_present_value)
        self.register(self.calculate_internal_rate_of_return)
        self.register(self.calculate_compound_annual_growth_rate)
        self.register(self.calculate_return_on_investment)

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

    @staticmethod
    def get_llm_usage_instructions() -> str:
        """
        Returns detailed instructions for LLMs on how to use investment analysis calculations.
        """
        return """
<investment_calculators_tools_instructions>
**INVESTMENT ANALYSIS CALCULATOR TOOLS:**

CRITICAL: Cash flows must be provided as lists with square brackets: [value1, value2, ...]
CRITICAL: Cash flow lists must contain at least 2 values
CRITICAL: For IRR, first cash flow is typically negative (investment)
CRITICAL: Begin/end values must be positive for CAGR calculations
CRITICAL: Cost must be positive for ROI calculations (gain can be negative)

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

</investment_calculators_tools_instructions>
"""
