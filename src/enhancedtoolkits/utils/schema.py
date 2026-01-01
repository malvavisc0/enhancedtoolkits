"""
OpenAI schema utilities.

This module provides lightweight helpers to validate and normalize tool/function
schemas for OpenAI tool calling.

In this project, schemas are expected to be **strict** (OpenAI compatible): every
parameter defined in `properties` should appear in the `required` array.
"""

from __future__ import annotations

import inspect
from enum import Enum
from typing import Any, Callable, get_args, get_origin

JsonObject = dict[str, Any]


class OpenAISchemaValidator:
    """Validate and normalize function/tool JSON schemas for OpenAI compatibility."""

    @staticmethod
    def validate_schema(schema: JsonObject) -> list[str]:
        """Validate a function schema against OpenAI requirements.

        Args:
            schema: The function schema to validate.

        Returns:
            A list of validation errors (empty if valid).
        """

        errors: list[str] = []

        parameters = schema.get("parameters")
        if not isinstance(parameters, dict):
            return ["Missing or invalid 'parameters' field"]

        required = parameters.get("required")
        if required is None:
            errors.append("Missing 'required' field in parameters")
            required_list: list[str] = []
        elif not isinstance(required, list):
            errors.append("'required' field must be an array")
            required_list = []
        else:
            required_list = [x for x in required if isinstance(x, str)]

        properties = parameters.get("properties")
        if not isinstance(properties, dict):
            errors.append(
                "Missing or invalid 'properties' field in parameters"
            )
            return errors

        # Strict-mode requirement: every property should be required.
        for prop_name in properties.keys():
            if prop_name not in required_list:
                errors.append(
                    f"Property '{prop_name}' missing from required array"
                )

        # Common schema patterns that are frequently rejected by OpenAI validators.
        for prop_name, prop_schema in properties.items():
            if not isinstance(prop_schema, dict):
                continue

            if "anyOf" in prop_schema:
                errors.append(
                    f"Property '{prop_name}' uses 'anyOf' which may be rejected by OpenAI"
                )

            if isinstance(prop_schema.get("type"), list):
                errors.append(
                    f"Property '{prop_name}' uses an array of types which may be rejected by OpenAI"
                )

        return errors

    @staticmethod
    def fix_union_types(schema: JsonObject) -> JsonObject:
        """Normalize `anyOf` patterns in property schemas.

        This is a best-effort transformation intended to reduce schema rejection
        when `Union[...]` annotations produce `anyOf`.

        Rules:
        - If an `anyOf` option contains an `enum`, convert the property to a simple
          string enum.
        - Otherwise, downgrade to a plain string.

        Args:
            schema: The schema to fix (modified in-place).

        Returns:
            The updated schema.
        """

        parameters = schema.get("parameters")
        if not isinstance(parameters, dict):
            return schema

        properties = parameters.get("properties")
        if not isinstance(properties, dict):
            return schema

        for prop_name, prop_schema in list(properties.items()):
            if not isinstance(prop_schema, dict) or "anyOf" not in prop_schema:
                continue

            enum_values: list[str] | None = None
            anyof = prop_schema.get("anyOf")
            if isinstance(anyof, list):
                for option in anyof:
                    if isinstance(option, dict) and isinstance(
                        option.get("enum"), list
                    ):
                        enum_values = [
                            x for x in option["enum"] if isinstance(x, str)
                        ]
                        break

            if enum_values:
                properties[prop_name] = {
                    "type": "string",
                    "enum": enum_values,
                    "description": prop_schema.get("description", ""),
                }
            else:
                properties[prop_name] = {
                    "type": "string",
                    "description": prop_schema.get("description", ""),
                }

        return schema

    @staticmethod
    def analyze_function_signature(func: Callable[..., Any]) -> JsonObject:
        """Analyze a function signature for OpenAI schema compatibility risks.

        Args:
            func: Callable to analyze.

        Returns:
            Dict containing parameter info plus recommendations.
        """

        sig = inspect.signature(func)
        analysis: JsonObject = {
            "function_name": getattr(func, "__name__", "<anonymous>"),
            "parameters": {},
            "issues": [],
            "recommendations": [],
        }

        for name, param in sig.parameters.items():
            annotation = param.annotation
            origin = get_origin(annotation)
            args = get_args(annotation)

            param_info: JsonObject = {
                "name": name,
                "annotation": str(annotation),
                "has_default": param.default != inspect.Parameter.empty,
                "default_value": (
                    param.default
                    if param.default != inspect.Parameter.empty
                    else None
                ),
                "issues": [],
            }

            # Union types often become `anyOf`.
            if origin is None and str(annotation).startswith("typing.Union"):
                # Fallback for some typing representations.
                origin = getattr(annotation, "__origin__", None)

            if origin is not None and origin is getattr(
                __import__("typing"), "Union"
            ):
                param_info["issues"].append(
                    "Uses Union type which may produce an anyOf schema"
                )
                analysis["recommendations"].append(
                    f"Consider simplifying '{name}' from Union to a single type"
                )

            # Enums inside unions tend to create complex anyOf schemas.
            for arg in args:
                if inspect.isclass(arg) and issubclass(arg, Enum):
                    param_info["issues"].append(
                        "Uses Enum in Union which often produces complex anyOf"
                    )
                    analysis["recommendations"].append(
                        f"Consider changing '{name}' to str with runtime validation"
                    )

            analysis["parameters"][name] = param_info

        return analysis


def create_openai_compatible_docstring(
    func_name: str, description: str, parameters: dict[str, JsonObject]
) -> str:
    """Create a docstring that encourages OpenAI-compatible JSON schema generation.

    Args:
        func_name: Function name.
        description: Short description.
        parameters: Parameter specs. Each value may include `type`, `description`,
            and optional `enum`.

    Returns:
        A formatted docstring.
    """

    header = f"{func_name}: {description}".strip(": ")
    lines = [header, "", "Args:"]

    for param_name, param_info in parameters.items():
        param_type = str(param_info.get("type", "Any"))
        param_desc = str(param_info.get("description", ""))

        if "enum" in param_info and isinstance(param_info["enum"], list):
            enum_values = ", ".join(f'"{v}"' for v in param_info["enum"])
            param_desc = (param_desc + f" Valid values: {enum_values}").strip()

        lines.append(f"    {param_name} ({param_type}): {param_desc}".rstrip())

    lines.extend(["", "Returns:", "    str: Function result"])
    return "\n".join(lines)
