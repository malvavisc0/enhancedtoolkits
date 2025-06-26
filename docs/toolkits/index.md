# Core Toolkits for AI Agents

Enhanced Toolkits provides **8 core toolkits** designed specifically for AI agents. Each toolkit is optimized for OpenAI function calling and Agno framework integration.

## 🤖 AI Agent Integration

All toolkits follow the same pattern for AI agent integration:

```python
from agno.agent import Agent
from enhancedtoolkits import ToolkitName

# Create agent with toolkit (Agno handles registration automatically)
agent = Agent(
    name="Your Agent",
    model="gpt-4",
    tools=[ToolkitName(configuration_options)]
)

# Agent automatically has access to all toolkit functions
```

## 🛠️ Available Toolkits

### 🧠 Reasoning Tools
**Multi-modal reasoning with cognitive bias detection**

```python
from enhancedtoolkits import ReasoningTools

reasoning = ReasoningTools(
    reasoning_depth=5,              # Max reasoning steps
    enable_bias_detection=True,     # Detect cognitive biases
    instructions="Custom instructions..."
)
```

**Functions available to agents:**
- `reason()` - Apply specific reasoning type to problems
- `multi_modal_reason()` - Combine multiple reasoning approaches
- `analyze_reasoning()` - Evaluate reasoning quality
- `detect_biases()` - Identify cognitive biases
- `get_reasoning_history()` - Retrieve session history

[Setup Guide →](reasoning.md)

---

### 🔍 Search Tools (SearxNG)
**Web search with content extraction and parsing**

```python
from enhancedtoolkits import SearxngTools

search = SearxngTools(
    host="http://searxng:8080",     # SearxNG instance URL
    max_results=10,                 # Results per search
    timeout=30,                     # Request timeout
    enable_content_fetching=True,   # Extract page content
    byparr_enabled=False           # Anti-bot bypass
)
```

**Functions available to agents:**
- `search_web()` - General web search
- `search_news()` - News article search
- `search_images()` - Image search
- `search_videos()` - Video search
- `search_category()` - Category-specific search

[Setup Guide →](searxng.md)

---

### 💭 Thinking Tools
**Structured cognitive frameworks for systematic analysis**

```python
from enhancedtoolkits import ThinkingTools

thinking = ThinkingTools(
    enable_bias_detection=True,     # Detect thinking biases
    enable_quality_assessment=True, # Assess thinking quality
    thinking_depth=3               # Analysis depth
)
```

**Functions available to agents:**
- `think()` - Process thoughts with cognitive frameworks
- `analyze_thinking_quality()` - Assess thinking depth and clarity
- `detect_thinking_biases()` - Identify cognitive biases in thinking

[Setup Guide →](thinking.md)

---

### 📁 Files Tools
**Enterprise-grade file operations with security controls**

```python
from enhancedtoolkits import FilesTools

files = FilesTools(
    base_dir="/secure/workspace",   # Base directory for operations
    max_file_size=100*1024*1024,   # 100MB max file size
    allowed_extensions=[".txt", ".py", ".json", ".md", ".csv"]
)
```

**Functions available to agents:**
- `read_file_chunk()` - Read file chunks with security validation
- `edit_file_chunk()` - Replace lines with atomic operations
- `insert_file_chunk()` - Insert lines with security validation
- `delete_file_chunk()` - Delete lines with atomic operations
- `save_file()` - Save files with comprehensive security checks
- `get_file_metadata()` - Get secure file metadata
- `list_files()` - List files with safety filtering

[Setup Guide →](files.md)

---

### 📈 Finance Tools (YFinance)
**Real-time financial data and market information**

```python
from enhancedtoolkits import YFinanceTools

finance = YFinanceTools(
    enable_caching=True,           # Cache responses
    cache_ttl=300,                 # Cache for 5 minutes
    rate_limit_delay=0.1,          # Delay between requests
    timeout=30                     # Request timeout
)
```

**Functions available to agents:**
- `get_current_price()` - Current stock price with change data
- `get_company_information()` - Comprehensive company details
- `get_news_for_ticker()` - Latest news articles
- `get_earnings_history()` - Historical earnings data
- `get_income_statement()` - Annual income statement
- `get_balance_sheet()` - Balance sheet information
- `get_cashflow()` - Cash flow statements
- `get_recommendations()` - Analyst recommendations

[Setup Guide →](finance.md)

---

### 🎥 YouTube Tools
**Video metadata and transcript extraction**

```python
from enhancedtoolkits import YouTubeTools

youtube = YouTubeTools(
    rate_limit_delay=0.5,          # Delay between requests
    timeout=30,                    # Request timeout
    max_retries=3                  # Retry attempts
)
```

**Functions available to agents:**
- `get_video_metadata()` - Comprehensive video metadata
- `get_video_transcript()` - Video transcript with language support
- `get_available_transcripts()` - List available transcript languages
- `get_video_info()` - Complete video information with optional transcript

[Setup Guide →](youtube.md)

---

### ☁️ Weather Tools
**Weather data and forecasts with multi-language support**

```python
from enhancedtoolkits import WeatherTools

weather = WeatherTools(
    timeout=30,                    # Request timeout
    base_url="https://wttr.in"     # Weather API URL
)
```

**Functions available to agents:**
- `get_current_weather()` - Current weather conditions for a location
- `get_weather_forecast()` - Multi-day weather forecast
- `get_temperature()` - Detailed temperature data
- `get_weather_description()` - Textual weather description

**Supported languages:** 30+ languages including English, Spanish, French, German, Chinese, Japanese, etc.

[Setup Guide →](weather.md)

---

### 📥 Downloader Tools
**Universal file downloading with anti-bot bypass**

```python
from enhancedtoolkits import DownloaderTools

downloader = DownloaderTools(
    byparr_enabled=True,           # Enable anti-bot bypass
    max_retries=3,                 # Retry attempts
    timeout=30,                    # Request timeout
    user_agent_rotation=True,      # Rotate user agents
    enable_caching=True            # Cache downloads
)
```

**Functions available to agents:**
- `get_file_from_url()` - Download any file with smart content processing
- `download_multiple_urls()` - Batch download content from multiple URLs
- `get_url_metadata()` - Extract metadata without downloading full content
- `check_url_accessibility()` - Test URL accessibility and response time

**Supported formats:** HTML, PDF, Word, Excel, images, videos, archives, and any file type.

[Setup Guide →](downloader.md)

---

## 🔧 Common Configuration Patterns

### Production Configuration
```python
from agno.agent import Agent
from enhancedtoolkits import *

# Create production agent with configured tools
agent = Agent(
    name="Production Assistant",
    model="gpt-4",
    tools=[
        ReasoningTools(reasoning_depth=5, enable_bias_detection=True),
        SearxngTools(host="http://searxng:8080", enable_content_fetching=True),
        YFinanceTools(enable_caching=True, cache_ttl=300),
        WeatherTools(timeout=30),
        YouTubeTools(rate_limit_delay=0.5),
        DownloaderTools(byparr_enabled=True, max_retries=3),
        FilesTools(base_dir="/secure/workspace"),
        ThinkingTools(enable_bias_detection=True)
    ]
)
```

### Environment Variables
```bash
# SearxNG and Downloader Tools
BYPARR_URL=http://byparr:8191/v1
BYPARR_TIMEOUT=60
BYPARR_ENABLED=false

# Weather Tools
WEATHER_API_URL=https://wttr.in

# General
LOG_LEVEL=INFO
```

## 🛡️ Security and Validation

All toolkits include:
- **Input validation** and sanitization
- **Rate limiting** and request throttling
- **Error handling** with detailed logging
- **Security controls** for file operations
- **Timeout management** for external APIs

## 📊 Monitoring and Debugging

Enable detailed logging for debugging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# All toolkit operations will be logged
toolkit = ToolkitName(debug=True)
```

## 🚀 Next Steps

1. **Choose the toolkits** your AI agent needs
2. **Follow the setup guides** for each toolkit
3. **Configure for your environment** (production vs development)
4. **Register with your AI agent** using OpenAI or Agno
5. **Test the integration** with sample agent queries

Each toolkit setup guide provides detailed configuration options and AI agent integration examples.