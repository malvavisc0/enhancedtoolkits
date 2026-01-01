# Core Toolkits for AI Agents

Enhanced Toolkits provides **8 core toolkits** designed for AI agents. These toolkits are built on top of [`StrictToolkit`](../api/base.md) and are intended to be used via agent tool/function calling (Agno or OpenAI-compatible schemas).

> Important: tool schemas are **strict**. In practice, agents should pass **all parameters** shown in function signatures, even when Python has defaults.

## 🤖 AI Agent Integration (Agno)

```python
from agno.agent import Agent
from enhancedtoolkits import (
    ReasoningTools,
    SearxngTools,
    ThinkingTools,
    FilesTools,
    YFinanceTools,
    YouTubeTools,
    WeatherTools,
    DownloadingTools,
)

agent = Agent(
    name="Your Agent",
    model="gpt-4",
    tools=[
        ReasoningTools(),
        SearxngTools(host="http://searxng:8080"),
        ThinkingTools(),
        FilesTools(),
        YFinanceTools(),
        YouTubeTools(),
        WeatherTools(),
        DownloadingTools(),
    ],
)
```

## 🛠️ Available Toolkits

### 🧠 Reasoning Tools
Class: [`ReasoningTools`](../api/reasoning.md)

**Functions available to agents:**
- `add_structured_reasoning_step()`
- `add_meta_cognitive_reflection()`
- `manage_working_memory_scratchpad()`
- `assess_reasoning_quality_and_suggest_improvements()`
- `synthesize_reasoning_chain_into_conclusion_or_insight()`
- `retrieve_current_reasoning_session_state()`
- `reset_reasoning_session_state()`

[Setup Guide →](reasoning.md)

---

### 🔍 Search Tools (SearxNG)
Class: [`SearxngTools`](../api/searxng.md)

**Functions available to agents:**
- `perform_web_search()`
- `perform_news_search()`
- `perform_image_search()`
- `perform_video_search()`
- `perform_category_search()`

[Setup Guide →](searxng.md)

---

### 💭 Thinking Tools
Class: [`ThinkingTools`](../api/thinking.md)

**Functions available to agents:**
- `build_step_by_step_reasoning_chain()`
- `add_meta_cognitive_reflection()`
- `manage_working_memory_scratchpad()`
- `assess_reasoning_chain_quality_and_suggest_improvements()`
- `synthesize_reasoning_chain_into_output()`
- `retrieve_current_thinking_chain_state()`
- `reset_current_thinking_chain()`

[Setup Guide →](thinking.md)

---

### 📁 Files Tools
Class: [`FilesTools`](../api/files.md)

**Functions available to agents:**
- `read_file_lines_chunk()`
- `replace_file_lines_chunk()`
- `insert_lines_into_file_chunk()`
- `delete_lines_from_file_chunk()`
- `save_file_with_validation()`
- `retrieve_file_metadata()`
- `list_files_with_pattern()`
- `search_files_by_name_regex()`
- `search_file_contents_by_regex()`

[Setup Guide →](files.md)

---

### 📈 Finance Tools (Yahoo Finance)
Class: [`YFinanceTools`](../api/finance.md)

**Functions available to agents:**
- `fetch_current_stock_price()`
- `fetch_company_information()`
- `fetch_ticker_news()`
- `fetch_earnings_history()`
- `fetch_income_statement()`
- `fetch_quarterly_financials()`
- `fetch_balance_sheet()`
- `fetch_quarterly_balance_sheet()`
- `fetch_cashflow_statement()`
- `fetch_quarterly_cashflow_statement()`
- `fetch_major_shareholders()`
- `fetch_institutional_shareholders()`
- `fetch_analyst_recommendations()`
- `fetch_sustainability_scores()`
- `fetch_price_history()`

[Setup Guide →](finance.md)

---

### 🎥 YouTube Tools
Class: [`YouTubeTools`](../api/youtube.md)

**Functions available to agents:**
- `fetch_youtube_video_metadata()`
- `extract_youtube_video_id()`
- `fetch_comprehensive_youtube_video_info()`
- `fetch_youtube_video_transcript()`
- `fetch_available_youtube_transcripts()`
- `fetch_youtube_transcript_languages()`

[Setup Guide →](youtube.md)

---

### ☁️ Weather Tools
Class: [`WeatherTools`](../api/weather.md)

**Functions available to agents:**
- `fetch_current_weather_conditions()`
- `fetch_weather_forecast()`
- `fetch_temperature_data()`
- `fetch_weather_text_description()`

[Setup Guide →](weather.md)

---

### 📥 Downloading Tools (URL Content Downloader)
Class: [`DownloadingTools`](../api/downloader.md)

**Functions available to agents:**
- `get_file_from_url()`
- `access_website_content()` (alias)
- `download_multiple_urls()`
- `get_url_metadata()`
- `check_url_accessibility()`

[Setup Guide →](downloader.md)

---

## 🧮 Calculator Modules (separate from core toolkits)

Calculator tools live under `enhancedtoolkits.calculators` and are documented in the Calculator section.

- [Calculator Modules →](../calculators/index.md)
