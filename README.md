# Enhanced Toolkits for Agno AI Agents

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Agno Framework](https://img.shields.io/badge/framework-Agno-green.svg)](https://github.com/agno-ai/agno)

Production-ready AI agent tools for developers building agents with **Agno** and/or **OpenAI-compatible tool calling**.

This repository contains:

- **8 core toolkits** (search, reasoning, thinking, files, finance, weather, youtube, url downloading)
- **9 calculator modules** under `enhancedtoolkits.calculators`

## Installation

Install from GitHub:

```bash
# Recommended: install all optional dependencies used by the exported toolkits
pip install "enhancedtoolkits[full] @ git+https://github.com/malvavisc0/enhancedtoolkits.git"

# Minimal install (only core dependencies)
pip install git+https://github.com/malvavisc0/enhancedtoolkits.git

# Focused extras
pip install "enhancedtoolkits[content] @ git+https://github.com/malvavisc0/enhancedtoolkits.git"   # markitdown (search + downloading)
pip install "enhancedtoolkits[youtube] @ git+https://github.com/malvavisc0/enhancedtoolkits.git"   # youtube-transcript-api
pip install "enhancedtoolkits[weather] @ git+https://github.com/malvavisc0/enhancedtoolkits.git"   # pywttr + models
```

Extras are defined in [`pyproject.toml`](pyproject.toml).

## Quick Start (Agno)

### Core toolkits

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
    name="AI Assistant",
    model="gpt-4",
    tools=[
        ReasoningTools(),
        SearxngTools(host="http://searxng:8080"),
        ThinkingTools(),
        FilesTools(base_dir="/app/workspace"),
        YFinanceTools(),
        YouTubeTools(),
        WeatherTools(),
        DownloadingTools(),
    ],
)
```

### Calculator modules

```python
from agno.agent import Agent
from enhancedtoolkits.calculators import (
    ArithmeticCalculatorTools,
    TimeValueCalculatorTools,
    InvestmentAnalysisCalculatorTools,
    LoanCalculatorTools,
)

agent = Agent(
    name="Finance Calculator",
    model="gpt-4",
    tools=[
        ArithmeticCalculatorTools(),
        TimeValueCalculatorTools(),
        InvestmentAnalysisCalculatorTools(),
        LoanCalculatorTools(),
    ],
)
```

## Toolkit Overview (public tool/function names)

### Reasoning
Class: [`ReasoningTools`](src/enhancedtoolkits/reasoning.py)

- `add_structured_reasoning_step()`
- `add_meta_cognitive_reflection()`
- `manage_working_memory_scratchpad()`
- `assess_reasoning_quality_and_suggest_improvements()`
- `synthesize_reasoning_chain_into_conclusion_or_insight()`

### Search (SearxNG)
Class: [`SearxngTools`](src/enhancedtoolkits/searxng.py)

- `perform_web_search()` / `perform_news_search()` / `perform_image_search()` / `perform_video_search()`
- `perform_category_search()`

### Thinking
Class: [`ThinkingTools`](src/enhancedtoolkits/thinking.py)

- `build_step_by_step_reasoning_chain()`
- `add_meta_cognitive_reflection()`
- `manage_working_memory_scratchpad()`
- `synthesize_reasoning_chain_into_output()`

### Files
Class: [`FilesTools`](src/enhancedtoolkits/files.py)

- `read_file_lines_chunk()` / `replace_file_lines_chunk()` / `insert_lines_into_file_chunk()` / `delete_lines_from_file_chunk()`
- `save_file_with_validation()`
- `retrieve_file_metadata()` / `list_files_with_pattern()` / `search_files_by_name_regex()` / `search_file_contents_by_regex()`

### Finance (Yahoo Finance)
Class: [`YFinanceTools`](src/enhancedtoolkits/finance.py)

- `fetch_current_stock_price()` / `fetch_price_history()`
- `fetch_company_information()`
- `fetch_ticker_news()`

### YouTube
Class: [`YouTubeTools`](src/enhancedtoolkits/youtube.py)

- `fetch_youtube_video_metadata()`
- `extract_youtube_video_id()`
- `fetch_comprehensive_youtube_video_info()`
- `fetch_youtube_video_transcript()`

### Weather
Class: [`WeatherTools`](src/enhancedtoolkits/weather.py)

- `fetch_current_weather_conditions()`
- `fetch_weather_forecast()`
- `fetch_temperature_data()`
- `fetch_weather_text_description()`

### URL Downloading
Class: [`DownloadingTools`](src/enhancedtoolkits/downloading.py)

- `get_file_from_url()` / `access_website_content()`
- `download_multiple_urls()`
- `get_url_metadata()` / `check_url_accessibility()`

## Why `StrictToolkit`

Enhanced Toolkits uses [`StrictToolkit`](src/enhancedtoolkits/base.py) as a base class to keep tool schemas predictable for agents.

In particular, it enforces strict parameter requirements in the generated JSON schema (OpenAI-compatible), which reduces failures from agents omitting parameters.

## Documentation

- MkDocs site sources: [`docs/`](docs/index.md)
- Toolkit guides: [`docs/toolkits/index.md`](docs/toolkits/index.md)
- Calculator modules: [`docs/calculators/index.md`](docs/calculators/index.md)
- API reference: [`docs/api/index.md`](docs/api/index.md)

## License

MIT. See [`LICENSE`](./LICENSE).
