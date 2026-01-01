"""
Shared base utilities for toolkit implementations.

This module defines [`StrictToolkit`](src/enhancedtoolkits/base.py:10), a thin wrapper
around agno's `Toolkit` that enforces strict JSON schemas for OpenAI tool calling.
"""

from typing import Any, Callable, Optional, Union

from agno.tools.function import Function
from agno.tools.toolkit import Toolkit
from agno.utils.log import log_debug, logger

from .utils.schema import OpenAISchemaValidator


class StrictToolkit(Toolkit):
    """Toolkit wrapper that enforces OpenAI-compatible strict schemas.

    Key behavior:
    - When registering a *callable*, we create an agno `Function` with `strict=True`.
    - When registering an agno `Function` (from `@tool` decorator), we delegate to
      the base [`Toolkit.register()`](.venv/lib/python3.13/site-packages/agno/tools/toolkit.py:132).

    This keeps the override signature compatible with agno (fixing the “red” method
    warning) while preserving strict behavior for normal callables.
    """

    def register(
        self,
        function: Union[Callable[..., Any], Function],
        name: Optional[str] = None,
    ) -> None:
        """Register a callable or agno `Function` with OpenAI-compatible strictness."""
        try:
            # agno supports registering already-decorated Function objects. Keep that behavior.
            if isinstance(function, Function):
                tool_name = name or function.name
                super().register(function, name=name)

                # Validate OpenAI compatibility only if the function was actually registered.
                registered = self.functions.get(tool_name)
                if (
                    registered is not None
                    and registered.entrypoint is not None
                ):
                    self._validate_openai_compatibility(
                        registered, registered.entrypoint
                    )
                return

            tool_name = name or function.__name__
            if (
                self.include_tools is not None
                and tool_name not in self.include_tools
            ):
                return
            if (
                self.exclude_tools is not None
                and tool_name in self.exclude_tools
            ):
                return

            # Create Function directly with strict=True
            f = Function.from_callable(function, name=tool_name, strict=True)

            # Validate OpenAI compatibility
            self._validate_openai_compatibility(f, function)

            # Set all the necessary properties
            f.cache_results = self.cache_results
            f.cache_dir = self.cache_dir
            f.cache_ttl = self.cache_ttl
            f.requires_confirmation = (
                tool_name in self.requires_confirmation_tools
            )
            f.external_execution = (
                tool_name in self.external_execution_required_tools
            )
            f.stop_after_tool_call = (
                tool_name in self.stop_after_tool_call_tools
            )
            f.show_result = tool_name in self.show_result_tools

            # Add to functions dictionary
            self.functions[f.name] = f
            log_debug(
                f"Function: {f.name} registered with {self.name} (strict=True, OpenAI compatible)"
            )
        except Exception:
            func_name = (
                function.name
                if isinstance(function, Function)
                else function.__name__
            )
            logger.warning("Failed to create Function for: %s", func_name)
            raise

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
                    "OpenAI compatibility issues found in %s:",
                    function_obj.name,
                )
                for error in errors:
                    logger.warning("  - %s", error)

                # Analyze the function signature for recommendations
                analysis = validator.analyze_function_signature(original_func)
                if analysis["recommendations"]:
                    logger.warning(
                        "Recommendations for %s:", function_obj.name
                    )
                    for rec in analysis["recommendations"]:
                        logger.warning("  - %s", rec)
            else:
                log_debug(f"Function {function_obj.name} is OpenAI compatible")

        except (ValueError, TypeError, KeyError, AttributeError) as e:
            logger.warning(
                "Failed to validate OpenAI compatibility for %s: %s",
                function_obj.name,
                e,
            )
