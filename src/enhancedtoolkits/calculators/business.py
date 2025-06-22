"""
Business Analysis Calculator

Provides business analysis calculations including break-even point analysis.
"""

from datetime import datetime

from agno.utils.log import log_error, log_info

from .base import (
    BaseCalculatorTools,
    FinancialComputationError,
    FinancialValidationError,
)


class BusinessAnalysisCalculatorTools(BaseCalculatorTools):
    """Calculator for business analysis calculations."""

    def __init__(self, **kwargs):
        """Initialize the business analysis calculator and register all methods."""
        self.add_instructions = True
        self.instructions = BusinessAnalysisCalculatorTools.get_llm_usage_instructions()

        super().__init__(name="business_analysis_calculator", **kwargs)

        # Register all business analysis methods
        self.register(self.calculate_break_even_point)

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

    @staticmethod
    def get_llm_usage_instructions() -> str:
        """
        Returns detailed instructions for LLMs on how to use business analysis calculations.
        """
        return """
<business_anaylis_calculations_tools_instructions>
**BUSINESS ANALYSIS CALCULATIONS TOOLS:**

- Use calculate_break_even_point to find break-even in units or sales.
   Parameters:
      - fixed_costs (float): Total fixed costs, e.g., 10000.0
      - price_per_unit (float): Selling price per unit, e.g., 25.0
      - variable_cost_per_unit (float): Variable cost per unit, e.g., 15.0

</business_anaylis_calculations_tools_instructions>
"""
