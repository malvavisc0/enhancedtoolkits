from typing import Any, Callable, Optional

from agno.tools.function import Function
from agno.tools.toolkit import Toolkit
from agno.utils.log import log_debug, logger


class StrictToolkit(Toolkit):
    """
    A base toolkit class that ensures all registered functions have strict=True.

    This forces all parameters to be included in the 'required' array of the JSON schema,
    regardless of whether they have default values, which is necessary for OpenAI API compatibility.
    """

    def register(self, function: Callable[..., Any], name: Optional[str] = None) -> None:
        """
        Register a function with the toolkit, always using strict=True.

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
            log_debug(f"Function: {f.name} registered with {self.name} (strict=True)")
        except Exception as e:
            logger.warning(f"Failed to create Function for: {function.__name__}")
            raise e
