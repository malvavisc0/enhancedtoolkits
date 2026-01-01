"""
Business Analysis Calculator

Provides business analysis calculations including break-even point analysis.
"""

from .base import BaseCalculatorTools, FinancialValidationError


class BusinessAnalysisCalculatorTools(BaseCalculatorTools):
    """Calculator for business analysis calculations."""

    def __init__(self, add_instructions: bool = True, **kwargs):
        """Initialize the business analysis calculator and register all methods."""
        instructions = (
            self.get_llm_usage_instructions() if add_instructions else ""
        )
        super().__init__(
            name="business_analysis_calculator",
            add_instructions=add_instructions,
            instructions=instructions,
            **kwargs,
        )

        # Register all business analysis methods
        self.register(self.calculate_break_even_point)

    def calculate_break_even_point(
        self,
        fixed_costs: float,
        price_per_unit: float,
        variable_cost_per_unit: float,
    ) -> str:
        """Calculate the break-even point in units and sales."""
        fixed_costs = self._validate_positive_amount(
            fixed_costs, "fixed_costs"
        )
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
            "metadata": self._base_metadata("contribution_margin_analysis"),
        }

        return self._format_json_response(result)

    @staticmethod
    def get_llm_usage_instructions() -> str:
        """Return short, text-first usage instructions for business analysis tools."""
        return """
<business_analysis_calculator>
Break-even analysis

GOAL
- Compute break-even units and sales and return JSON.

Break-even analysis. Tools return JSON strings.

Tools:
- calculate_break_even_point(fixed_costs, price_per_unit, variable_cost_per_unit)

CONTEXT-SIZE RULES (IMPORTANT)
- In final user responses, report break-even units + sales and key assumptions; avoid dumping full JSON.
</business_analysis_calculator>
"""
