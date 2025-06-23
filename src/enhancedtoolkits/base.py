from typing import Any, Callable, Optional

from agno.tools.function import Function
from agno.tools.toolkit import Toolkit
from agno.utils.log import log_debug, logger

from .utils.schema import OpenAISchemaValidator


class StrictToolkit(Toolkit):
    """
    A base toolkit class that ensures all registered functions have strict=True.

    This forces all parameters to be included in the 'required' array of the JSON schema,
    regardless of whether they have default values, which is necessary for OpenAI API compatibility.
    """

    def register(self, function: Callable[..., Any], name: Optional[str] = None) -> None:
        """
        Register a function with the toolkit, always using strict=True and validating OpenAI compatibility.

        Args:
            function: The callable to register
            name: Optional custom name for the function
        """
        try:
            tool_name = name or function.__name__
            if self.include_tools is not None and tool_name not in self.include_tools:
                return
            if self.exclude_tools is not None and tool_name in self.exclude_tools:
                return

            # Create Function directly with strict=True
            f = Function.from_callable(function, name=tool_name, strict=True)

            # Validate OpenAI compatibility
            self._validate_openai_compatibility(f, function)

            # Set all the necessary properties
            f.cache_results = self.cache_results
            f.cache_dir = self.cache_dir
            f.cache_ttl = self.cache_ttl
            f.requires_confirmation = tool_name in self.requires_confirmation_tools
            f.external_execution = tool_name in self.external_execution_required_tools
            if hasattr(self, "stop_after_tool_call_tools"):
                f.stop_after_tool_call = tool_name in self.stop_after_tool_call_tools
            if hasattr(self, "show_result_tools"):
                f.show_result = tool_name in self.show_result_tools

            # Add to functions dictionary
            self.functions[f.name] = f
            log_debug(
                f"Function: {f.name} registered with {self.name} (strict=True, OpenAI compatible)"
            )
        except Exception as e:
            logger.warning(f"Failed to create Function for: {function.__name__}")
            raise e

    def _validate_openai_compatibility(
        self, function_obj: Function, original_func: Callable
    ) -> None:
        """
        Validate that the function schema is OpenAI compatible.

        Args:
            function_obj: The Function object with generated schema
            original_func: The original callable for analysis
        """
        try:
            # Get the schema
            schema = function_obj.to_dict()

            # Validate with our validator
            validator = OpenAISchemaValidator()
            errors = validator.validate_schema(schema)

            if errors:
                logger.warning(
                    f"OpenAI compatibility issues found in {function_obj.name}:"
                )
                for error in errors:
                    logger.warning(f"  - {error}")

                # Analyze the function signature for recommendations
                analysis = validator.analyze_function_signature(original_func)
                if analysis["recommendations"]:
                    logger.warning(f"Recommendations for {function_obj.name}:")
                    for rec in analysis["recommendations"]:
                        logger.warning(f"  - {rec}")
            else:
                log_debug(f"Function {function_obj.name} is OpenAI compatible")

        except Exception as e:
            logger.warning(
                f"Failed to validate OpenAI compatibility for {function_obj.name}: {e}"
            )
