# MkDocstrings Integration Plan

## Overview

MkDocstrings will automatically generate comprehensive API documentation from the Enhanced Toolkits source code docstrings, eliminating the need to manually maintain API documentation.

## Benefits of MkDocstrings Integration

### 🚀 Automatic API Documentation
- **Source of Truth**: Documentation stays in sync with code
- **Comprehensive Coverage**: All classes, methods, and parameters documented
- **Type Annotations**: Automatic type information from Python type hints
- **Examples**: Include docstring examples in documentation
- **Cross-References**: Automatic linking between related components

### 📊 Enhanced Developer Experience
- **Interactive API Browser**: Navigate through classes and methods
- **Search Integration**: API methods searchable through MkDocs search
- **Code Examples**: Docstring examples rendered with syntax highlighting
- **Parameter Documentation**: Detailed parameter descriptions and types

## Implementation Strategy

### 1. Plugin Configuration

Add MkDocstrings to `mkdocs.yml`:

```yaml
plugins:
  - search
  - minify
  - mkdocstrings:
      handlers:
        python:
          options:
            docstring_style: google  # or numpy, sphinx
            show_source: true
            show_root_heading: true
            show_root_toc_entry: true
            show_object_full_path: false
            show_category_heading: true
            group_by_category: true
            heading_level: 2
            members_order: source
            filters:
              - "!^_"  # Hide private methods
            docstring_options:
              ignore_init_summary: true
            merge_init_into_class: true
```

### 2. Navigation Structure Enhancement

Update navigation to include auto-generated API docs:

```yaml
nav:
  - Home: index.md
  - Getting Started: ...
  - Core Toolkits: ...
  - Calculator Modules: ...
  - API Reference:
    - api/index.md
    - Core Toolkits:
      - Reasoning Tools: api/reasoning.md
      - Search Tools: api/searxng.md
      - Thinking Tools: api/thinking.md
      - Files Tools: api/files.md
      - Finance Tools: api/finance.md
      - YouTube Tools: api/youtube.md
      - Weather Tools: api/weather.md
      - Downloader Tools: api/downloader.md
    - Calculator Modules:
      - Arithmetic: api/calculators/arithmetic.md
      - Time Value: api/calculators/time-value.md
      - Investment: api/calculators/investment.md
      - Loan: api/calculators/loan.md
      - Bond: api/calculators/bond.md
      - Risk Metrics: api/calculators/risk.md
      - Depreciation: api/calculators/depreciation.md
      - Business: api/calculators/business.md
      - Utility: api/calculators/utility.md
    - Base Classes:
      - StrictToolkit: api/base.md
      - Calculator Base: api/calculators/base.md
    - Utilities: api/utils.md
```

### 3. API Documentation Pages

Create markdown files that use MkDocstrings directives:

#### Core Toolkit API Pages

**`docs/api/reasoning.md`**:
```markdown
# Reasoning Tools API

::: enhancedtoolkits.reasoning.EnhancedReasoningTools
    options:
      show_source: true
      heading_level: 2
      members:
        - reason
        - multi_modal_reason
        - analyze_reasoning
        - detect_biases
        - get_reasoning_history
```

**`docs/api/finance.md`**:
```markdown
# Finance Tools API

::: enhancedtoolkits.finance.EnhancedYFinanceTools
    options:
      show_source: true
      heading_level: 2
      members:
        - get_current_price
        - get_company_information
        - get_news_for_ticker
        - get_earnings_history
        - get_income_statement
        - get_balance_sheet
        - get_cashflow
```

#### Calculator API Pages

**`docs/api/calculators/arithmetic.md`**:
```markdown
# Arithmetic Calculator API

::: enhancedtoolkits.calculators.arithmetic.ArithmeticCalculatorTools
    options:
      show_source: true
      heading_level: 2
      members:
        - add
        - subtract
        - multiply
        - divide
        - exponentiate
        - square_root
        - factorial
        - is_prime
```

### 4. Enhanced Docstring Standards

Ensure all source code follows Google-style docstrings:

```python
class EnhancedReasoningTools(StrictToolkit):
    """Multi-modal reasoning tools with cognitive bias detection.
    
    This class provides sophisticated reasoning capabilities that help AI agents
    think through complex problems using various reasoning methodologies while
    detecting and mitigating cognitive biases.
    
    Attributes:
        reasoning_depth (int): Maximum number of reasoning steps.
        enable_bias_detection (bool): Whether to detect cognitive biases.
        session_state (dict): Current reasoning session state.
    
    Example:
        ```python
        from enhancedtoolkits import ReasoningTools
        
        reasoning = ReasoningTools(
            reasoning_depth=5,
            enable_bias_detection=True
        )
        
        result = reasoning.reason(
            agent_or_team=agent,
            problem="Should we invest in renewable energy?",
            reasoning_type="analytical",
            evidence=["Government incentives", "Market growth"]
        )
        ```
    """
    
    def reason(
        self,
        agent_or_team: Any,
        problem: str,
        reasoning_type: str,
        evidence: List[str],
        context: Optional[str] = None
    ) -> str:
        """Apply specific reasoning type to a problem.
        
        Args:
            agent_or_team: Agent instance for session tracking.
            problem: The problem to reason about.
            reasoning_type: Type of reasoning to apply. Options:
                - "analytical": Systematic breakdown
                - "probabilistic": Uncertainty reasoning
                - "causal": Cause-effect analysis
                - "deductive": Logical deduction
                - "inductive": Pattern-based reasoning
                - "abductive": Best explanation reasoning
            evidence: List of supporting evidence.
            context: Additional context for reasoning.
        
        Returns:
            JSON string containing reasoning results with confidence scores,
            identified biases, and recommended next actions.
        
        Raises:
            ValueError: If reasoning_type is not supported.
            ReasoningError: If reasoning process fails.
        
        Example:
            ```python
            result = reasoning.reason(
                agent_or_team=agent,
                problem="Market entry strategy",
                reasoning_type="analytical",
                evidence=[
                    "Market size: $50B",
                    "Competition: 5 players",
                    "Our advantage: AI tech"
                ]
            )
            ```
        """
```

### 5. Cross-Reference Integration

Enable automatic cross-references between components:

```python
def calculate_loan_payment(self, principal: float, annual_rate: float, years: int) -> str:
    """Calculate monthly loan payment.
    
    This method uses the standard loan payment formula and leverages
    [arithmetic operations][enhancedtoolkits.calculators.arithmetic.ArithmeticCalculatorTools.divide]
    for precise calculations.
    
    See Also:
        [generate_amortization_schedule][enhancedtoolkits.calculators.loan.LoanCalculatorTools.generate_amortization_schedule]:
            Generate complete payment schedule.
        [calculate_present_value][enhancedtoolkits.calculators.time_value.TimeValueCalculatorTools.calculate_present_value]:
            Related time value calculation.
    """
```

### 6. Code Example Integration

Include runnable examples in docstrings:

```python
def get_current_price(self, ticker: str) -> str:
    """Get current stock price with change data.
    
    Examples:
        Basic usage:
        ```python
        finance = YFinanceTools()
        price_info = finance.get_current_price("AAPL")
        print(price_info)
        ```
        
        With error handling:
        ```python
        try:
            price_info = finance.get_current_price("INVALID")
        except YFinanceValidationError as e:
            print(f"Invalid ticker: {e}")
        ```
        
        Batch processing:
        ```python
        tickers = ["AAPL", "GOOGL", "MSFT"]
        for ticker in tickers:
            price = finance.get_current_price(ticker)
            print(f"{ticker}: {price}")
        ```
    """
```

## Implementation Benefits

### 🔄 Automatic Synchronization
- **Always Current**: API docs update automatically with code changes
- **No Maintenance**: Eliminates manual API documentation maintenance
- **Consistency**: Ensures documentation matches actual implementation

### 📚 Comprehensive Coverage
- **All Methods**: Every public method automatically documented
- **Type Information**: Parameter and return types from annotations
- **Examples**: Docstring examples rendered with syntax highlighting
- **Error Information**: Exception documentation included

### 🔍 Enhanced Discoverability
- **Search Integration**: All API methods searchable
- **Cross-References**: Automatic linking between related methods
- **Inheritance**: Shows class hierarchies and inherited methods
- **Source Code**: Optional source code viewing

### 👨‍💻 Developer Experience
- **IDE Integration**: Docstrings visible in IDEs
- **Interactive Browsing**: Navigate through API structure
- **Copy-Paste Examples**: Ready-to-use code examples
- **Type Safety**: Clear parameter and return type information

## Migration Strategy

### Phase 1: Setup and Configuration
1. Add MkDocstrings to dependencies
2. Configure plugin in mkdocs.yml
3. Create basic API page structure

### Phase 2: Core Toolkit Documentation
1. Create API pages for main toolkits
2. Enhance docstrings in core modules
3. Add cross-references between related methods

### Phase 3: Calculator Documentation
1. Create API pages for all calculator modules
2. Add comprehensive examples to calculator docstrings
3. Document mathematical formulas and assumptions

### Phase 4: Enhancement and Polish
1. Add advanced MkDocstrings features
2. Optimize navigation and search
3. Add custom CSS for API documentation styling

## Technical Requirements

### Dependencies
```txt
mkdocs>=1.5.0
mkdocs-material>=9.0.0
mkdocstrings[python]>=0.24.0
mkdocstrings-python>=1.7.0
```

### Source Code Requirements
- **Google-style docstrings** throughout codebase
- **Type annotations** for all public methods
- **Comprehensive examples** in docstrings
- **Clear parameter descriptions**

### Configuration Options
- **Docstring Style**: Google (recommended for Enhanced Toolkits)
- **Source Code Display**: Optional source viewing
- **Member Filtering**: Hide private methods
- **Cross-References**: Automatic linking
- **Example Rendering**: Syntax-highlighted code blocks

This integration will transform the Enhanced Toolkits documentation into a comprehensive, automatically-maintained API reference that stays perfectly synchronized with the codebase.