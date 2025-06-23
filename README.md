# 🤖 Enhanced Tools Kits for Agno AI Agents

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Agno Framework](https://img.shields.io/badge/framework-Agno-green.svg)](https://github.com/agno-ai/agno)

**Production-ready AI agent tools for developers building intelligent chatbots and AI systems.**

This collection provides nine comprehensive toolkits designed for AI agents that need reliable, robust, and feature-rich capabilities. Each tool includes advanced error handling, input validation, caching, rate limiting, and comprehensive logging.

## 🚀 Features

- **🧠 Advanced Reasoning**: Multi-modal reasoning with cognitive bias detection
- **🔍 Intelligent Search**: Web search with content extraction and parsing
- **💭 Structured Thinking**: Cognitive frameworks with quality assessment
- **📁 Secure File Operations**: Enterprise-grade file handling with comprehensive security controls
- **📈 Financial Data**: Comprehensive stock market and financial information
- **🧮 Financial Calculator**: Advanced financial calculations and basic arithmetic operations
- **🎥 YouTube Integration**: Video metadata and transcript extraction
- **☁️ Weather Data**: Current conditions, forecasts, and temperature data in multiple languages
- **📥 Universal File Downloader**: Anti-bot bypass with smart content processing for any file type
- **⚡ Production Ready**: Robust error handling, caching, and rate limiting
- **🔧 Highly Configurable**: Extensive customization options for each tool
- **📊 Session Management**: Built-in state tracking and reasoning chains

🎉 ALL TOOLKITS are OpenAI compatible!

## 📦 Installation

Install directly from GitHub:

```bash
# Install with core dependencies
pip install git+https://github.com/malvavisc0/enhancedtoolkits.git

# Install with all optional dependencies
pip install "enhancedtoolkits[full] @ git+https://github.com/malvavisc0/enhancedtoolkits.git"

# Install with specific optional dependencies
pip install "enhancedtoolkits[youtube,content] @ git+https://github.com/malvavisc0/enhancedtoolkits.git"
```

## 📦 Quick Start

```python
from enhancedtoolkits import (
    ReasoningTools,
    SearxngTools,
    ThinkingTools,
    FilesTools,
    YFinanceTools,
    YouTubeTools,
    CalculatorTools,
    WeatherTools,
    DownloaderTools
)

# Initialize tools
reasoning_tool = ReasoningTools()
search_tool = SearxngTools(host="http://searxng:8080")
thinking_tool = ThinkingTools()
files_tool = FilesTools()
finance_tool = YFinanceTools()
youtube_tool = YouTubeTools()
calculator_tool = CalculatorTools()
weather_tool = WeatherTools()
downloader_tool = DownloaderTools()
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

## 💭 Enhanced Thinking Tools

**Structured thinking frameworks with cognitive awareness and quality assessment.**

### Key Features

- **8 Thinking Types**: Analysis, Synthesis, Evaluation, Reflection, Planning, Problem-solving, Creative, Critical
- **Cognitive Bias Detection**: Identify thinking biases and suggest improvements
- **Quality Assessment**: Depth, clarity, evidence integration analysis
- **Thinking Evolution**: Track thinking patterns and progression

## 📁 Secure Files Toolkit

**Enterprise-grade file operations with comprehensive security controls and atomic operations.**

### Key Features

- **Path Traversal Protection**: Robust validation against directory traversal attacks
- **File Type Validation**: Whitelist-based file extension filtering
- **Resource Limits**: Configurable file size, chunk size, and line length limits
- **Atomic Operations**: All write operations use temporary files with atomic replacement
- **File Locking**: Prevents race conditions with proper file locking mechanisms
- **Memory Optimization**: Stream-based reading for large files, efficient line counting
- **Security Controls**: Symlink blocking, input sanitization, and blocked pattern detection
- **Comprehensive Logging**: Secure audit trail without information disclosure

### Security Configuration

- **Max File Size**: 100MB (configurable)
- **Max Chunk Size**: 10,000 lines
- **Max Line Length**: 10,000 characters
- **Allowed Extensions**: `.txt`, `.py`, `.js`, `.json`, `.md`, `.csv`, `.log`, `.yaml`, `.yml`, `.xml`
- **Blocked Patterns**: `..`, `~`, `$`, `;`, `|`, `&`, `<`, `>`

### Available Methods

- `read_file_chunk()` - Read file chunks with security validation
- `edit_file_chunk()` - Replace lines with atomic operations
- `insert_file_chunk()` - Insert lines with security validation
- `delete_file_chunk()` - Delete lines with atomic operations
- `save_file()` - Save files with comprehensive security checks
- `get_file_metadata()` - Get secure file metadata
- `list_files()` - List files with safety filtering

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
- `get_quarterly_cashflow()` - Retrieve the quarterly cash
- `get_quarterly_balance_sheet()` - Retrieve the quarterly balance sheet

## 🧮 Calculator Tools

**Modular financial and mathematical calculation tools with comprehensive validation and error handling.**

### Available Calculator Classes

#### ArithmeticCalculatorTools

**Basic arithmetic operations with comprehensive validation.**

- `add()` - Add two numbers
- `subtract()` - Subtract second number from first
- `multiply()` - Multiply two numbers
- `divide()` - Divide first number by second
- `exponentiate()` - Raise first number to power of second
- `square_root()` - Calculate square root of a number
- `factorial()` - Calculate factorial of a non-negative integer
- `is_prime()` - Check if a number is prime

#### TimeValueCalculatorTools

**Time value of money calculations for financial planning.**

- `calculate_present_value()` - Calculate present value of a future sum
- `calculate_future_value()` - Calculate future value of a present sum
- `calculate_annuity_present_value()` - Calculate present value of an ordinary annuity
- `calculate_annuity_future_value()` - Calculate future value of an ordinary annuity
- `calculate_perpetuity_value()` - Calculate present value of a perpetuity

#### InvestmentAnalysisCalculatorTools

**Investment analysis tools for evaluating financial opportunities.**

- `calculate_net_present_value()` - Calculate NPV of a series of cash flows
- `calculate_internal_rate_of_return()` - Calculate IRR using Newton-Raphson method
- `calculate_compound_annual_growth_rate()` - Calculate CAGR between two values
- `calculate_return_on_investment()` - Calculate ROI percentage

#### LoanCalculatorTools

**Loan analysis tools for payment calculations and amortization.**

- `calculate_loan_payment()` - Calculate periodic payment for a loan
- `generate_amortization_schedule()` - Generate complete loan payment schedule

#### BondCalculatorTools

**Bond valuation tools for pricing and yield calculations.**

- `calculate_bond_price()` - Calculate price of a bond based on cash flows
- `calculate_yield_to_maturity()` - Calculate YTM using iterative approximation

#### RiskMetricsCalculatorTools

**Risk assessment tools for investment analysis.**

- `calculate_sharpe_ratio()` - Calculate risk-adjusted returns
- `calculate_volatility()` - Calculate standard deviation of returns

#### DepreciationCalculatorTools

**Asset depreciation calculation tools.**

- `calculate_straight_line_depreciation()` - Calculate linear depreciation
- `calculate_declining_balance_depreciation()` - Calculate accelerated depreciation

#### BusinessAnalysisCalculatorTools

**Business analysis tools for financial planning.**

- `calculate_break_even_point()` - Calculate break-even point in units or sales

#### UtilityCalculatorTools

**Utility calculations for financial adjustments.**

- `convert_currency()` - Convert between currencies using exchange rate
- `adjust_for_inflation()` - Adjust amounts for inflation over time

## ☁️ Enhanced Weather Tools

**Comprehensive weather data with multi-language support and robust error handling.**

### Key Features

- **Current Weather**: Temperature, humidity, wind speed, precipitation, and more
- **Weather Forecasts**: Multi-day forecasts with detailed conditions
- **Temperature Data**: Current, feels like, min/max temperatures in both Celsius and Fahrenheit
- **Weather Descriptions**: Textual descriptions of weather conditions
- **Multi-language Support**: Over 30 supported languages for global use
- **Location Flexibility**: City names, addresses, or latitude/longitude coordinates
- **Custom API URL**: Optional custom base URL for the weather API

### Available Methods

- `get_current_weather()` - Current weather conditions for a location
- `get_weather_forecast()` - Multi-day weather forecast
- `get_temperature()` - Detailed temperature data
- `get_weather_description()` - Textual weather description

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

## 📥 Enhanced URL Content Downloader

**Universal file downloading with anti-bot bypass and smart content processing.**

### Key Features

- **Universal File Support**: Download any file type (HTML, PDF, Word, Excel, images, videos, etc.)
- **Anti-Bot Bypass**: BYPARR integration with CloudFlare bypass capabilities
- **Smart Content Processing**: MarkItDown integration for automatic content extraction
- **Multiple Output Formats**: Auto-detection, markdown, text, html, binary
- **User-Agent Rotation**: Advanced header spoofing and rotation techniques
- **Robust Error Handling**: Retry logic with exponential backoff and comprehensive error recovery
- **Content Validation**: URL validation, format checking, and accessibility testing
- **Batch Processing**: Support for downloading multiple URLs simultaneously

### Available Methods

- `access_website_content()` - Download and parse content from a URL (legacy method)
- `get_file_from_url()` - Download any file with smart content processing
- `download_multiple_urls()` - Batch download content from multiple URLs
- `get_url_metadata()` - Extract metadata without downloading full content
- `check_url_accessibility()` - Test URL accessibility and response time

### Supported Formats

- **Auto**: Automatically detects best format based on content type
- **Markdown**: Converts HTML to markdown using MarkItDown
- **Text**: Plain text extraction with HTML tag removal
- **HTML**: Raw HTML content preservation
- **Binary**: File information for binary files with MarkItDown processing when possible

### Content Type Support

- **HTML/Web Pages**: Full content extraction and conversion
- **PDF Documents**: Text extraction via MarkItDown
- **Microsoft Office**: Word, Excel, PowerPoint document processing
- **Images**: Metadata extraction and file information
- **Videos/Audio**: File information and metadata
- **Archives**: ZIP, RAR, 7z file handling
- **Any File Type**: Universal download capability

## ⚙️ Configuration

### Environment Variables

```bash
# SearxNG Tools & URL Downloader
BYPARR_URL=http://byparr:8191/v1
BYPARR_TIMEOUT=60
BYPARR_ENABLED=false

# URL Downloader Tools
URL_DOWNLOADER_MAX_RETRIES=3
URL_DOWNLOADER_TIMEOUT=30

# General
LOG_LEVEL=INFO

# Weather Tools
WEATHER_API_URL=https://wttr.in
```

### Advanced Configuration

```python
from enhancedtoolkits import (
    ReasoningTools,
    SearxngTools,
    ThinkingTools,
    FilesTools,
    YFinanceTools,
    YouTubeTools,
    CalculatorTools,
    WeatherTools,
    DownloaderTools
)

# Reasoning Tools
reasoning = ReasoningTools(
    reasoning_depth=5,           # Max reasoning steps
    enable_bias_detection=True,  # Cognitive bias detection
    instructions="Custom instructions..."
)

# Search Tools
search = SearxngTools(
    host="https://searx.example.com",
    max_results=10,
    timeout=30,
    enable_content_fetching=True,
    byparr_enabled=False
)

# Thinking Tools
thinking = ThinkingTools(
    enable_bias_detection=True,
    enable_quality_assessment=True,
    thinking_depth=3
)

# Finance Tools
finance = YFinanceTools(
    enable_caching=True,
    cache_ttl=300,
    rate_limit_delay=0.1
)

# YouTube Tools
youtube = YouTubeTools(
    rate_limit_delay=0.5,
    timeout=30,
    max_retries=3
)

# Weather Tools
weather = WeatherTools(
    timeout=30,
    base_url="https://wttr.in"
)

# Files Tools
files = FilesTools(
    base_dir="/secure/workspace",     # Base directory for operations
)

# Calculator Tools
calculator = CalculatorTools()

# URL Downloader Tools
downloader = DownloaderTools(
    byparr_enabled=True,
    max_retries=3,
    timeout=30,
    user_agent_rotation=True,
    enable_caching=True
)
```

## 🛡️ Why We Use StrictToolkit

The EnhancedToolkits library uses StrictToolkit as its base class to ensure robust and predictable behavior when interacting with AI agents, particularly those using the OpenAI API. StrictToolkit extends the standard Agno Toolkit by enforcing that all parameters in registered functions are marked as required in the JSON schema, regardless of whether they have default values in the Python code. This strict parameter enforcement is crucial for AI agent compatibility as it prevents common issues where agents might omit parameters they incorrectly assume are optional, leading to runtime errors or unexpected behavior. By making all parameters explicitly required in the schema, we create a more consistent interface that guides AI agents to provide all necessary inputs, resulting in more reliable tool execution, clearer error messages, and improved debugging. This approach has proven especially valuable when working with complex financial calculations, data retrieval operations, and multi-step reasoning processes where parameter completeness is essential for accurate results.

## 🔧 Requirements

- **Python**: 3.8+
- **Agno Framework**: Latest version
- **Core Dependencies**: `httpx`, `yfinance`, `youtube-transcript-api`
- **Optional Dependencies**: `markitdown` (for content parsing), `pywttr` and `pywttr-models` (for weather data)

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
