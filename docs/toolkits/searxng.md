# Search Tools (SearxNG)

The [`SearxngTools`](../api/searxng.md) toolkit provides web search via a SearxNG instance and returns results as **JSON strings**.

It supports:

- Multiple categories (`general`, `news`, `images`, `videos`, …)
- Optional **limited content fetching** (disabled by default)
- Optional file downloading/processing for a small allowlist (PDF/TXT/MD)

## 🤖 AI Agent Setup (Agno)

```python
from agno.agent import Agent
from enhancedtoolkits import SearxngTools

agent = Agent(
    name="Research Assistant",
    model="gpt-4",
    tools=[
        SearxngTools(
            host="http://searxng:8080",
            max_results=10,
            enable_content_fetching=False,  # default
        )
    ],
)
```

## ⚙️ Configuration

Constructor parameters for `SearxngTools`:

| Parameter | Type | Default | Notes |
|---|---:|---:|---|
| `host` | `str` | required | SearxNG base URL (e.g. `http://searxng:8080`) |
| `max_results` | `int \| None` | `20` | Clamped internally (1..30) |
| `timeout` | `int` | `30` | Clamped internally (5..120) |
| `enable_content_fetching` | `bool \| None` | `False` | If `True`, fetches *at most 3* result pages (general/news/files only) |
| `enable_file_downloads` | `bool \| None` | `True` | Enables file handling for supported types |
| `max_file_size_mb` | `int` | `10` | Clamped internally (1..500) |
| `file_download_timeout` | `int` | `60` | Clamped internally (10..300) |
| `byparr_enabled` | `bool \| None` | `True` | Used only for content fetching; can be auto-detected if set to `None` |

### Supported categories
See `SearxngTools.SUPPORTED_CATEGORIES`.

## 🔍 Available Functions

All functions return a **JSON string** encoding a list of result objects.

- `perform_web_search(query, max_results=None)`
- `perform_news_search(query, max_results=None)`
- `perform_image_search(query, max_results=None)`
- `perform_video_search(query, max_results=None)`
- `perform_category_search(query, category, max_results=None)`

## ✅ Examples

### Web search

```python
from enhancedtoolkits import SearxngTools

search = SearxngTools(host="http://searxng:8080", max_results=5)
results_json = search.perform_web_search("agno ai agents")
```

### Category search

```python
results_json = search.perform_category_search(
    query="latest LLM safety papers",
    category="science",
    max_results=5,
)
```

### Enable limited content fetching (first 3 results only)

```python
search = SearxngTools(
    host="http://searxng:8080",
    max_results=10,
    enable_content_fetching=True,
)

results_json = search.perform_news_search("EU AI Act updates", max_results=5)
```

## 📝 Notes / Best Practices

- Keep `max_results` small (5–10) unless you really need more.
- Content fetching can produce large outputs; it is disabled by default and limited to the first 3 results.

## API Reference

- [`docs/api/searxng.md`](../api/searxng.md)
