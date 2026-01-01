# Downloading Tools (URL Content Downloader)

The [`DownloadingTools`](../api/downloader.md) toolkit downloads content from URLs and returns either:

- extracted **text/markdown/html**, or
- **minimal metadata** for binary content (or when extraction is not possible)

It supports optional BYPARR integration for anti-bot bypass.

All public functions return **strings**.

## 📦 Installation

This toolkit requires `markitdown` (imported at module load time):

```bash
pip install markitdown
```

## 🤖 AI Agent Setup (Agno)

```python
from agno.agent import Agent
from enhancedtoolkits import DownloadingTools

agent = Agent(
    name="Content Researcher",
    model="gpt-4",
    tools=[
        DownloadingTools(
            byparr_enabled=None,      # None = auto-detect via env
            max_retries=3,
            timeout=30,
            user_agent_rotation=True,
            enable_caching=False,
        )
    ],
)
```

## ⚙️ Configuration

Constructor parameters for `DownloadingTools`:

| Parameter | Type | Default | Notes |
|---|---:|---:|---|
| `byparr_enabled` | `bool \| None` | `None` | If `None`, uses env `BYPARR_ENABLED` |
| `max_retries` | `int` | `URL_DOWNLOADER_MAX_RETRIES` | Clamped internally (1..10) |
| `timeout` | `int` | `URL_DOWNLOADER_TIMEOUT` | Clamped internally (5..300) |
| `user_agent_rotation` | `bool` | `True` | Rotates headers/user agents |
| `enable_caching` | `bool` | `False` | In-memory per-instance cache (no TTL) |

### Environment variables

- `BYPARR_URL` (default `http://byparr:8191/v1`)
- `BYPARR_TIMEOUT` (default `60`)
- `BYPARR_ENABLED` (`true`/`false`)
- `URL_DOWNLOADER_MAX_RETRIES` (default `3`)
- `URL_DOWNLOADER_TIMEOUT` (default `30`)

## 📥 Available Functions

### `get_file_from_url(url, output='auto')`
Downloads and processes the URL.

`output` options (see `DownloadingTools.SUPPORTED_FORMATS`):

- `auto`
- `markdown`
- `text`
- `html`
- `binary`

### `access_website_content(url, output='auto')`
Alias for `get_file_from_url()`.

### `download_multiple_urls(urls, output='auto')`
Downloads up to 10 URLs and returns a JSON string of results.

### `get_url_metadata(url)`
Makes a HEAD request and returns a JSON string with basic metadata.

### `check_url_accessibility(url)`
Makes a HEAD request and returns a JSON string with accessibility + timing.

## ✅ Examples

```python
from enhancedtoolkits import DownloadingTools

downloader = DownloadingTools(byparr_enabled=False)

md = downloader.get_file_from_url("https://example.com", output="markdown")
meta = downloader.get_url_metadata("https://example.com")

batch = downloader.download_multiple_urls(
    urls=["https://example.com", "https://example.org"],
    output="text",
)
```

## API Reference

- [`docs/api/downloader.md`](../api/downloader.md)
