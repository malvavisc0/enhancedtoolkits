# MkDocstrings Troubleshooting Guide

## Common Issues and Solutions

### Issue: "ModuleNotFoundError: No module named 'enhancedtoolkits'"

This is the most common issue when setting up MkDocstrings. Here are several solutions:

#### Solution 1: Install the Package in Development Mode
```bash
# From the project root directory
pip install -e .

# Or with all dependencies
pip install -e ".[full]"

# Then serve docs
mkdocs serve
```

#### Solution 2: Use Manual API Reference
If you can't install the package, use the manual reference:
- Navigate to **API Reference > Manual Reference** in the documentation
- This provides complete API documentation without requiring module imports

#### Solution 3: Update Python Path
Add this to your `mkdocs.yml`:
```yaml
plugins:
  - mkdocstrings:
      handlers:
        python:
          paths: [src]  # This tells MkDocstrings where to find the code
```

#### Solution 4: Set PYTHONPATH Environment Variable
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
mkdocs serve
```

### Issue: "Could not collect 'enhancedtoolkits.module.Class'"

This happens when MkDocstrings can find the module but can't import specific classes.

#### Solution: Check Import Path
Verify the import path in your API documentation:
```markdown
# Correct format
::: enhancedtoolkits.reasoning.EnhancedReasoningTools

# Not this
::: src.enhancedtoolkits.reasoning.EnhancedReasoningTools
```

#### Solution: Check Class Names
Ensure class names match exactly:
```python
# In source code
class EnhancedReasoningTools(StrictToolkit):
    pass

# In API docs
::: enhancedtoolkits.reasoning.EnhancedReasoningTools
```

### Issue: "No module named 'agno'"

The enhancedtoolkits package depends on the Agno framework.

#### Solution: Install Dependencies
```bash
# Install Agno framework
pip install agno

# Or install enhancedtoolkits with all dependencies
pip install -e ".[full]"
```

### Issue: Documentation Builds But Shows No Content

#### Solution: Check MkDocstrings Configuration
Ensure your `mkdocs.yml` has proper configuration:
```yaml
plugins:
  - mkdocstrings:
      handlers:
        python:
          paths: [src]
          options:
            docstring_style: google
            show_source: false
            show_root_heading: true
```

#### Solution: Verify Docstrings Exist
Check that your source code has docstrings:
```python
class MyClass:
    """This class needs a docstring to appear in docs."""
    
    def my_method(self):
        """This method needs a docstring too."""
        pass
```

### Issue: "TypeError: 'NoneType' object is not iterable"

This can happen with complex inheritance or missing imports.

#### Solution: Simplify API Pages
Start with basic API pages:
```markdown
::: enhancedtoolkits.reasoning.EnhancedReasoningTools
    options:
      show_source: false
      members:
        - __init__
        - reason
```

Add more members gradually to identify problematic methods.

## Development Workflow

### Recommended Setup for Documentation Development

1. **Install in Development Mode**:
   ```bash
   cd /path/to/enhancedtoolkits
   pip install -e ".[full]"
   ```

2. **Install Documentation Dependencies**:
   ```bash
   pip install -r docs/requirements.txt
   ```

3. **Test MkDocstrings**:
   ```bash
   # Test if module can be imported
   python -c "import enhancedtoolkits; print('Success!')"
   
   # Test specific classes
   python -c "from enhancedtoolkits.reasoning import EnhancedReasoningTools; print('Success!')"
   ```

4. **Serve Documentation**:
   ```bash
   mkdocs serve
   ```

### Alternative: Use Manual Reference

If automatic generation doesn't work, the manual reference provides complete API documentation:

1. **Navigate to Manual Reference**: Go to API Reference > Manual Reference
2. **Complete Coverage**: All classes and methods documented manually
3. **Always Works**: No dependency on module imports
4. **Easy to Maintain**: Update as you add new features

## Configuration Options

### Basic Configuration (Recommended)
```yaml
plugins:
  - mkdocstrings:
      handlers:
        python:
          paths: [src]
          options:
            docstring_style: google
            show_source: false
            show_root_heading: true
```

### Advanced Configuration
```yaml
plugins:
  - mkdocstrings:
      handlers:
        python:
          paths: [src]
          options:
            docstring_style: google
            show_source: true
            show_root_heading: true
            show_root_toc_entry: true
            show_object_full_path: false
            show_category_heading: true
            group_by_category: true
            heading_level: 2
            members_order: source
            filters:
              - "!^_"
            show_signature_annotations: true
```

### Minimal Configuration (Fallback)
```yaml
plugins:
  - mkdocstrings
```

## Testing MkDocstrings

### Test Individual Components
```bash
# Test if specific modules can be documented
python -c "
import sys
sys.path.insert(0, 'src')
from enhancedtoolkits.reasoning import EnhancedReasoningTools
print('Module import successful')
print('Class:', EnhancedReasoningTools.__name__)
print('Docstring:', bool(EnhancedReasoningTools.__doc__))
"
```

### Test MkDocs Build
```bash
# Build without serving (faster for testing)
mkdocs build

# Check for errors in build output
mkdocs build --verbose
```

## Best Practices

### 1. Start Simple
Begin with basic API pages and add complexity gradually:
```markdown
# Start with this
::: enhancedtoolkits.reasoning.EnhancedReasoningTools

# Then add options
::: enhancedtoolkits.reasoning.EnhancedReasoningTools
    options:
      show_source: false
```

### 2. Use Manual Reference as Backup
Always maintain the manual reference as a fallback for when automatic generation fails.

### 3. Test Locally First
Always test documentation builds locally before deploying:
```bash
mkdocs serve --dev-addr=127.0.0.1:8000
```

### 4. Check Dependencies
Ensure all required packages are installed:
```bash
pip list | grep -E "(mkdocs|mkdocstrings|enhancedtoolkits|agno)"
```

## Getting Help

If you continue to have issues:

1. **Check the Manual Reference**: Complete API documentation without imports
2. **Review Error Messages**: Look for specific import or path issues
3. **Test Module Imports**: Verify the package can be imported in Python
4. **Use Minimal Configuration**: Start with basic MkDocstrings setup
5. **Check GitHub Issues**: Look for similar issues in the MkDocstrings repository

The manual reference ensures you always have complete API documentation, regardless of MkDocstrings configuration issues.