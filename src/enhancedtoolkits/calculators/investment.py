"""
Investment Analysis Calculator

Provides investment analysis calculations including NPV, IRR, CAGR, and ROI.
"""

from typing import List

from .base import BaseCalculatorTools, FinancialComputationError


class InvestmentAnalysisCalculatorTools(BaseCalculatorTools):
    """Calculator for investment analysis calculations."""

    def __init__(self, add_instructions: bool = True, **kwargs):
        """Initialize the investment analysis calculator and register all methods."""
        instructions = (
            self.get_llm_usage_instructions() if add_instructions else ""
        )
        super().__init__(
            name="investment_analysis_calculator",
            add_instructions=add_instructions,
            instructions=instructions,
            **kwargs,
        )

        # Register all investment analysis methods
        self.register(self.calculate_net_present_value)
        self.register(self.calculate_internal_rate_of_return)
        self.register(self.calculate_compound_annual_growth_rate)
        self.register(self.calculate_return_on_investment)

    def calculate_net_present_value(
        self, rate: float, cash_flows: List[float]
    ) -> str:
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
                "metadata": self._base_metadata(
                    "discounted_cash_flow",
                    interpretation=(
                        "positive_npv_profitable"
                        if npv > 0
                        else "negative_npv_unprofitable"
                    ),
                ),
            }

            return self._format_json_response(result)

        except (TypeError, ValueError, OverflowError, ZeroDivisionError) as e:
            self._log_unexpected_error("Failed to calculate NPV", e)
            raise FinancialComputationError(
                f"Failed to calculate NPV: {e}"
            ) from e

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
                "metadata": self._base_metadata(
                    "newton_raphson",
                    interpretation="rate_of_return_percentage",
                ),
            }

            return self._format_json_response(result)

        except (TypeError, ValueError, OverflowError, ZeroDivisionError) as e:
            self._log_unexpected_error("Failed to calculate IRR", e)
            raise FinancialComputationError(
                f"Failed to calculate IRR: {e}"
            ) from e

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
            begin_value = self._validate_positive_amount(
                begin_value, "begin_value"
            )
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
                "metadata": self._base_metadata("geometric_mean"),
            }

            return self._format_json_response(result)

        except (TypeError, ValueError, OverflowError, ZeroDivisionError) as e:
            self._log_unexpected_error("Failed to calculate CAGR", e)
            raise FinancialComputationError(
                f"Failed to calculate CAGR: {e}"
            ) from e

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
                "metadata": self._base_metadata(
                    "simple_roi",
                    interpretation="profit" if gain > 0 else "loss",
                ),
            }

            return self._format_json_response(result)

        except (TypeError, ValueError, OverflowError, ZeroDivisionError) as e:
            self._log_unexpected_error("Failed to calculate ROI", e)
            raise FinancialComputationError(
                f"Failed to calculate ROI: {e}"
            ) from e

    @staticmethod
    def get_llm_usage_instructions() -> str:
        """Return short, text-first usage instructions for investment tools."""
        return """
<investment_analysis_calculator>
Investment analysis (NPV/IRR/CAGR/ROI)

GOAL
- Compute common investment metrics from small cash-flow series and return JSON.

Investment analysis. Tools return JSON strings.

Tools:
- calculate_net_present_value(rate, cash_flows)
- calculate_internal_rate_of_return(cash_flows, guess=0.1)
- calculate_compound_annual_growth_rate(begin_value, end_value, years)
- calculate_return_on_investment(gain, cost)

Notes:
- `cash_flows` is a list like [-1000, 300, 400, 500].
- `rate` is per period as a decimal (0.10 = 10%).

CONTEXT-SIZE RULES (IMPORTANT)
- Keep cash flow lists small; do not pass huge arrays.
- In final user responses, summarize NPV/IRR/ROI rather than pasting full JSON.
</investment_analysis_calculator>
"""
