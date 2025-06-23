"""
OpenAI Schema Utilities

Utilities for generating and validating OpenAI-compatible function schemas.
This module ensures that all function schemas meet OpenAI's strict requirements.
"""

import inspect
import json
from enum import Enum
from typing import Any, Dict, List, Optional, Union, get_args, get_origin


class OpenAISchemaValidator:
    """Validates and fixes function schemas for OpenAI compatibility."""

    @staticmethod
    def validate_schema(schema: Dict[str, Any]) -> List[str]:
        """
        Validate a function schema against OpenAI requirements.

        Args:
            schema: The function schema to validate

        Returns:
            List of validation errors (empty if valid)
        """
        errors = []

        # Check basic structure
        if "parameters" not in schema:
            errors.append("Missing 'parameters' field")
            return errors

        parameters = schema["parameters"]

        # Check required field exists and is array
        if "required" not in parameters:
            errors.append("Missing 'required' field in parameters")
        elif not isinstance(parameters["required"], list):
            errors.append("'required' field must be an array")

        # Check properties exist
        if "properties" not in parameters:
            errors.append("Missing 'properties' field in parameters")
            return errors

        properties = parameters["properties"]
        required = parameters.get("required", [])

        # OpenAI requirement: every key in properties should be in required array for strict mode
        for prop_name in properties.keys():
            if prop_name not in required:
                errors.append(f"Property '{prop_name}' missing from required array")

        # Check for problematic schema patterns
        for prop_name, prop_schema in properties.items():
            # Check for anyOf patterns (problematic for OpenAI)
            if "anyOf" in prop_schema:
                errors.append(
                    f"Property '{prop_name}' uses 'anyOf' pattern which may be rejected by OpenAI"
                )

            # Check for complex Union types
            if isinstance(prop_schema.get("type"), list):
                errors.append(
                    f"Property '{prop_name}' uses array of types which may be rejected by OpenAI"
                )

        return errors

    @staticmethod
    def fix_union_types(schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fix Union types in schema to be OpenAI compatible.

        Args:
            schema: The function schema to fix

        Returns:
            Fixed schema
        """
        if "parameters" not in schema or "properties" not in schema["parameters"]:
            return schema

        properties = schema["parameters"]["properties"]

        for prop_name, prop_schema in properties.items():
            # Fix anyOf patterns with enums
            if "anyOf" in prop_schema:
                # Look for enum in anyOf
                enum_values = None
                for option in prop_schema["anyOf"]:
                    if "enum" in option:
                        enum_values = option["enum"]
                        break

                if enum_values:
                    # Replace anyOf with simple enum
                    properties[prop_name] = {
                        "type": "string",
                        "enum": enum_values,
                        "description": prop_schema.get("description", ""),
                    }
                else:
                    # Replace anyOf with simple string type
                    properties[prop_name] = {
                        "type": "string",
                        "description": prop_schema.get("description", ""),
                    }

        return schema

    @staticmethod
    def analyze_function_signature(func) -> Dict[str, Any]:
        """
        Analyze a function signature for potential OpenAI compatibility issues.

        Args:
            func: The function to analyze

        Returns:
            Analysis results with recommendations
        """
        sig = inspect.signature(func)
        analysis = {
            "function_name": func.__name__,
            "parameters": {},
            "issues": [],
            "recommendations": [],
        }

        for name, param in sig.parameters.items():
            param_info = {
                "name": name,
                "annotation": str(param.annotation),
                "has_default": param.default != inspect.Parameter.empty,
                "default_value": (
                    param.default if param.default != inspect.Parameter.empty else None
                ),
                "issues": [],
            }

            # Check for Union types
            if (
                hasattr(param.annotation, "__origin__")
                and param.annotation.__origin__ is Union
            ):
                param_info["issues"].append(
                    "Uses Union type which may cause anyOf schema"
                )
                analysis["recommendations"].append(
                    f"Consider simplifying {name} from Union to single type"
                )

            # Check for Enum types in Union
            if hasattr(param.annotation, "__args__"):
                for arg in param.annotation.__args__:
                    if inspect.isclass(arg) and issubclass(arg, Enum):
                        param_info["issues"].append(
                            "Uses Enum in Union which causes complex anyOf schema"
                        )
                        analysis["recommendations"].append(
                            f"Consider changing {name} to str with validation"
                        )

            analysis["parameters"][name] = param_info

        return analysis


class OpenAISchemaGenerator:
    """Generates OpenAI-compatible schemas from function signatures."""

    @staticmethod
    def generate_compatible_schema(func) -> Dict[str, Any]:
        """
        Generate an OpenAI-compatible schema from a function.

        Args:
            func: The function to generate schema for

        Returns:
            OpenAI-compatible function schema
        """
        # This would integrate with the existing Function.from_callable
        # but apply fixes to ensure OpenAI compatibility

        # For now, this is a placeholder that would need integration
        # with the agno.tools.function module
        return {
            "name": func.__name__,
            "description": func.__doc__ or "No description available",
            "parameters": {"type": "object", "properties": {}, "required": []},
        }


def create_openai_compatible_docstring(
    func_name: str, description: str, parameters: Dict[str, Dict[str, Any]]
) -> str:
    """
    Create a docstring that helps generate OpenAI-compatible schemas.

    Args:
        func_name: Name of the function
        description: Function description
        parameters: Parameter definitions with types and descriptions

    Returns:
        Formatted docstring
    """
    lines = [description, "", "Args:"]

    for param_name, param_info in parameters.items():
        param_type = param_info.get("type", "Any")
        param_desc = param_info.get("description", "")

        # Add enum values if present
        if "enum" in param_info:
            enum_values = ", ".join(f'"{v}"' for v in param_info["enum"])
            param_desc += f" Valid values: {enum_values}"

        lines.append(f"    {param_name} ({param_type}): {param_desc}")

    lines.extend(["", "Returns:", "    str: Function result"])

    return "\n".join(lines)


# Example usage and testing functions
def test_schema_validation():
    """Test the schema validation functionality."""

    # Example problematic schema (with anyOf)
    problematic_schema = {
        "name": "test_function",
        "parameters": {
            "type": "object",
            "properties": {
                "param1": {
                    "anyOf": [
                        {"type": "string", "enum": ["a", "b", "c"]},
                        {"type": "string"},
                    ]
                }
            },
            "required": ["param1"],
        },
    }

    # Validate
    validator = OpenAISchemaValidator()
    errors = validator.validate_schema(problematic_schema)
    print(f"Validation errors: {errors}")

    # Fix
    fixed_schema = validator.fix_union_types(problematic_schema)
    print(f"Fixed schema: {json.dumps(fixed_schema, indent=2)}")

    # Validate fixed schema
    fixed_errors = validator.validate_schema(fixed_schema)
    print(f"Fixed schema errors: {fixed_errors}")


if __name__ == "__main__":
    test_schema_validation()
