# StrictToolkit Base API Reference

API documentation for the StrictToolkit base class - foundation for all Enhanced Toolkits.

## Class: StrictToolkit

Base class that provides the foundation for all Enhanced Toolkits, ensuring consistent behavior, OpenAI compatibility, and strict parameter validation.

### StrictToolkit()

Initialize the base toolkit with common configuration options.

**Parameters:**
- `enable_caching` (bool, optional): Enable response caching. Default: True
- `cache_ttl` (int, optional): Cache time-to-live in seconds. Default: 300
- `timeout` (int, optional): Request timeout in seconds. Default: 30
- `rate_limit_delay` (float, optional): Delay between requests in seconds. Default: 0.0
- `max_retries` (int, optional): Maximum number of retries for failed requests. Default: 3

### Core Methods

#### get_openai_schema()

Get OpenAI-compatible function schema for the toolkit.

**Returns:**
- `dict`: OpenAI function calling schema with all toolkit methods

#### validate_parameters()

Validate input parameters against the toolkit's schema.

**Parameters:**
- `method_name` (str): Name of the method to validate parameters for
- `parameters` (dict): Parameters to validate

**Returns:**
- `dict`: Validated parameters with type conversion and defaults applied

**Raises:**
- `ValidationError`: If parameters don't match the required schema

#### execute_with_retry()

Execute a method with automatic retry logic and error handling.

**Parameters:**
- `method` (callable): Method to execute
- `args` (tuple): Positional arguments for the method
- `kwargs` (dict): Keyword arguments for the method

**Returns:**
- `Any`: Method result with retry logic applied

#### cache_result()

Cache a method result for future use.

**Parameters:**
- `cache_key` (str): Unique key for the cached result
- `result` (Any): Result to cache
- `ttl` (int, optional): Time-to-live override for this cache entry

**Returns:**
- `None`

#### get_cached_result()

Retrieve a cached result if available and not expired.

**Parameters:**
- `cache_key` (str): Cache key to look up

**Returns:**
- `Any`: Cached result if available, None otherwise

### Error Handling

#### handle_error()

Standardized error handling for all toolkit methods.

**Parameters:**
- `error` (Exception): The exception that occurred
- `method_name` (str): Name of the method where the error occurred
- `context` (dict, optional): Additional context about the error

**Returns:**
- `dict`: Standardized error response with details and suggestions

### Validation Methods

#### validate_required_params()

Ensure all required parameters are present and valid.

**Parameters:**
- `params` (dict): Parameters to validate
- `required_fields` (List[str]): List of required parameter names

**Raises:**
- `ValidationError`: If required parameters are missing or invalid

#### validate_param_types()

Validate parameter types against expected types.

**Parameters:**
- `params` (dict): Parameters to validate
- `type_schema` (dict): Expected types for each parameter

**Raises:**
- `ValidationError`: If parameter types don't match expectations

#### sanitize_input()

Sanitize input parameters to prevent security issues.

**Parameters:**
- `value` (Any): Value to sanitize
- `param_type` (type): Expected parameter type

**Returns:**
- `Any`: Sanitized value safe for processing

## Key Features

### Strict Parameter Validation
- **All parameters are required** in function schemas (no optional parameters)
- **Type validation** ensures parameters match expected types
- **Input sanitization** prevents security vulnerabilities
- **Comprehensive error messages** help developers debug issues

### OpenAI Compatibility
- **Function schemas** automatically generated for OpenAI function calling
- **Consistent response format** across all toolkit methods
- **Error handling** compatible with OpenAI's expectations
- **Parameter validation** ensures reliable agent execution

### Caching and Performance
- **Intelligent caching** reduces redundant API calls
- **Configurable TTL** for different types of data
- **Memory-efficient** cache management
- **Cache invalidation** when needed

### Error Handling
- **Standardized error responses** across all toolkits
- **Detailed error context** for debugging
- **Graceful degradation** when services are unavailable
- **Retry logic** for transient failures

## Usage Examples

### Creating a Custom Toolkit

```python
from enhancedtoolkits.base import StrictToolkit

class MyCustomTools(StrictToolkit):
    def __init__(self, api_key: str = None):
        super().__init__(
            enable_caching=True,
            cache_ttl=300,
            timeout=30
        )
        self.api_key = api_key
    
    def my_method(self, param1: str, param2: int) -> dict:
        """Custom method with strict parameter validation."""
        # Validation is automatically handled by the base class
        result = self._perform_operation(param1, param2)
        return {"result": result, "status": "success"}
```

### Using with OpenAI

```python
from enhancedtoolkits import ReasoningTools
import openai

# Initialize toolkit
toolkit = ReasoningTools()

# Get OpenAI schema
schema = toolkit.get_openai_schema()

# Use with OpenAI function calling
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Analyze this problem"}],
    functions=[schema],
    function_call="auto"
)
```

## Related Documentation

- [Creating Custom Toolkits](../developer/contributing.md)
- [All Toolkit APIs](index.md)
- [Error Handling Guide](../developer/contributing.md)