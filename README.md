# 🤖 Enhanced Tools Kits for Agno AI Agents

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Agno Framework](https://img.shields.io/badge/framework-Agno-green.svg)](https://github.com/agno-ai/agno)

**Production-ready AI agent tools for developers building intelligent chatbots and AI systems.**

This collection provides six comprehensive toolkits designed for AI agents that need reliable, robust, and feature-rich capabilities. Each tool includes advanced error handling, input validation, caching, rate limiting, and comprehensive logging.

## 🚀 Features

- **🧠 Advanced Reasoning**: Multi-modal reasoning with cognitive bias detection
- **🔍 Intelligent Search**: Web search with content extraction and parsing
- **💭 Structured Thinking**: Cognitive frameworks with quality assessment
- **📈 Financial Data**: Comprehensive stock market and financial information
- **🧮 Financial Calculator**: Advanced financial calculations and basic arithmetic operations
- **🎥 YouTube Integration**: Video metadata and transcript extraction
- **⚡ Production Ready**: Robust error handling, caching, and rate limiting
- **🔧 Highly Configurable**: Extensive customization options for each tool
- **📊 Session Management**: Built-in state tracking and reasoning chains

## 📦 Quick Start

```python
from reasoning import EnhancedReasoningTools
from searxng import EnhancedSearxngTools
from thinking import EnhancedThinkingTools
from yfinance import EnhancedYFinanceTools
from youtube import EnhancedYouTubeTools
from calculator import EnhancedCalculatorTools

# Initialize tools
reasoning = EnhancedReasoningTools()
search = EnhancedSearxngTools(host="http://searxng:8080")
thinking = EnhancedThinkingTools()
finance = EnhancedYFinanceTools()
youtube = EnhancedYouTubeTools()
calculator = EnhancedCalculatorTools()
```

## 🧠 Enhanced Reasoning Tools

**Multi-modal reasoning with cognitive bias detection and session management.**

### Key Features
- **6 Reasoning Types**: Deductive, Inductive, Abductive, Causal, Probabilistic, Analogical
- **Bias Detection**: Automatic identification of cognitive biases
- **Session Tracking**: Reasoning step history and workflow management
- **Quality Assessment**: Confidence levels and evidence evaluation

### Available Methods
- `reason()` - Apply specific reasoning type to a problem
- `multi_modal_reason()` - Combine multiple reasoning approaches
- `analyze_reasoning()` - Evaluate reasoning results and determine next actions
- `detect_biases()` - Identify cognitive biases in reasoning content
- `get_reasoning_history()` - Retrieve session reasoning history

## 🔍 Enhanced SearxNG Tools

**Comprehensive web search with optional content fetching and parsing.**

### Key Features
- **Multiple Search Categories**: General, news, images, videos, files, science
- **Content Extraction**: Full webpage content parsing with MarkItDown
- **Byparr Integration**: Optional CloudFlare bypass for protected sites
- **Rate Limiting**: Built-in request throttling and retry logic
- **Input Validation**: URL validation and query sanitization

### Available Methods
- `search_web()` - General web search
- `search_news()` - News article search
- `search_images()` - Image search
- `search_videos()` - Video search
- `search_category()` - Search in specific categories
- `get_page_content()` - Extract full webpage content

## 💭 Enhanced Thinking Tools

**Structured thinking frameworks with cognitive awareness and quality assessment.**

### Key Features
- **8 Thinking Types**: Analysis, Synthesis, Evaluation, Reflection, Planning, Problem-solving, Creative, Critical
- **Cognitive Bias Detection**: Identify thinking biases and suggest improvements
- **Quality Assessment**: Depth, clarity, evidence integration analysis
- **Thinking Evolution**: Track thinking patterns and progression

### Available Methods
- `think()` - Process thoughts with structured cognitive frameworks

## 📈 Enhanced YFinance Tools

**Comprehensive financial data retrieval with robust error handling and caching.**

### Key Features
- **Complete Financial Data**: Prices, company info, financials, news, recommendations
- **Input Validation**: Ticker symbol validation and normalization
- **Caching System**: Configurable response caching with TTL
- **Rate Limiting**: Built-in request throttling
- **Error Recovery**: Comprehensive error handling and retry logic

### Available Methods
- `get_current_price()` - Current stock price with change data
- `get_company_information()` - Comprehensive company details
- `get_news_for_ticker()` - Latest news articles
- `get_earnings_history()` - Historical earnings data
- `get_income_statement()` - Annual income statement
- `get_quarterly_financials()` - Quarterly financial data
- `get_balance_sheet()` - Balance sheet information
- `get_cashflow()` - Cash flow statements
- `get_major_holders()` - Major shareholders
- `get_institutional_holders()` - Institutional ownership
- `get_recommendations()` - Analyst recommendations
- `get_sustainability_scores()` - ESG scores
- `get_price_history()` - Historical price data

## 🧮 Enhanced Calculator Tools

**Comprehensive financial calculations and basic arithmetic operations with advanced algorithms.**

### Key Features
- **Basic Arithmetic**: Addition, subtraction, multiplication, division, exponentiation, square root, factorial, prime checking
- **Time Value of Money**: Present value, future value, annuities, perpetuities
- **Investment Analysis**: NPV, IRR, CAGR, ROI, Sharpe ratio, volatility
- **Loan Calculations**: Payment calculations, complete amortization schedules
- **Bond Analysis**: Bond pricing and yield to maturity calculations
- **Risk Metrics**: Sharpe ratio, volatility (standard deviation)
- **Depreciation**: Straight-line and declining balance methods
- **Business Analysis**: Break-even point calculations
- **Utilities**: Currency conversion, inflation adjustments
- **Advanced Algorithms**: Newton-Raphson for IRR, iterative approximation for YTM

### Available Methods

#### Basic Arithmetic Operations
- `add()` - Add two numbers
- `subtract()` - Subtract two numbers
- `multiply()` - Multiply two numbers
- `divide()` - Divide two numbers
- `exponentiate()` - Raise to power
- `square_root()` - Calculate square root
- `factorial()` - Calculate factorial
- `is_prime()` - Check if number is prime

#### Financial Calculations
- `calculate_present_value()` - Present value of future sum
- `calculate_future_value()` - Future value of present sum
- `calculate_net_present_value()` - NPV of cash flow series
- `calculate_internal_rate_of_return()` - IRR using Newton-Raphson method
- `calculate_loan_payment()` - Periodic loan payment
- `generate_amortization_schedule()` - Complete loan payment schedule
- `calculate_compound_annual_growth_rate()` - CAGR calculation
- `calculate_return_on_investment()` - ROI percentage
- `calculate_bond_price()` - Bond pricing based on cash flows
- `calculate_yield_to_maturity()` - YTM using iterative approximation
- `calculate_annuity_present_value()` - PV of ordinary annuity
- `calculate_annuity_future_value()` - FV of ordinary annuity
- `calculate_perpetuity_value()` - Present value of perpetuity
- `calculate_straight_line_depreciation()` - Linear depreciation
- `calculate_declining_balance_depreciation()` - Accelerated depreciation
- `calculate_sharpe_ratio()` - Risk-adjusted returns
- `calculate_volatility()` - Standard deviation of returns
- `calculate_break_even_point()` - Business break-even analysis
- `convert_currency()` - Simple currency conversion
- `adjust_for_inflation()` - Inflation adjustment calculations

## 🎥 Enhanced YouTube Tools

**Video metadata and transcript extraction with multi-language support.**

### Key Features
- **Comprehensive Metadata**: Title, author, thumbnails, duration, statistics
- **Multi-language Transcripts**: Support for multiple languages and auto-generated content
- **URL Flexibility**: Support for various YouTube URL formats
- **Transcript Analysis**: Language detection and availability checking
- **Rate Limiting**: Built-in request throttling and retry logic

### Available Methods
- `get_video_metadata()` - Comprehensive video metadata
- `get_video_transcript()` - Video transcript with language support
- `get_available_transcripts()` - List available transcript languages
- `get_transcript_languages()` - Simplified language code list
- `extract_video_id()` - Extract video ID from various URL formats
- `get_video_info()` - Complete video information with optional transcript

## ⚙️ Configuration

### Environment Variables

```bash
# SearxNG Tools
BYPARR_URL=http://byparr:8191/v1
BYPARR_TIMEOUT=60
BYPARR_ENABLED=false

# General
LOG_LEVEL=INFO
```

### Advanced Configuration

```python
# Reasoning Tools
reasoning = EnhancedReasoningTools(
    reasoning_depth=5,           # Max reasoning steps
    enable_bias_detection=True,  # Cognitive bias detection
    instructions="Custom instructions..."
)

# Search Tools
search = EnhancedSearxngTools(
    host="https://searx.example.com",
    max_results=10,
    timeout=30,
    enable_content_fetching=True,
    byparr_enabled=False
)

# Thinking Tools
thinking = EnhancedThinkingTools(
    enable_bias_detection=True,
    enable_quality_assessment=True,
    thinking_depth=3
)

# Finance Tools
finance = EnhancedYFinanceTools(
    enable_caching=True,
    cache_ttl=300,
    rate_limit_delay=0.1
)

# YouTube Tools
youtube = EnhancedYouTubeTools(
    rate_limit_delay=0.5,
    timeout=30,
    max_retries=3
)

# Calculator Tools
calculator = EnhancedCalculatorTools()
```

## 🔧 Requirements

- **Python**: 3.8+
- **Agno Framework**: Latest version
- **Core Dependencies**: `httpx`, `yfinance`, `youtube-transcript-api`
- **Optional Dependencies**: `markitdown` (for content parsing)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Reporting Issues

Please use the [GitHub Issues](https://github.dev/malvavisc0/enhancedtoolkits) page to report bugs or request features.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built on the [Agno Framework](https://github.com/agno-agi/agno)
- Inspired by production AI agent requirements
- Community feedback and contributions

---

**Made with ❤️ for AI agent developers**
