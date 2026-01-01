# Configuration

Most toolkits are configured via Python constructor arguments.

Some toolkits also read a few environment variables (primarily for BYPARR and downloader defaults).

## Environment Variables

### BYPARR (optional)
Used by `DownloadingTools` and optionally by `SearxngTools` when content fetching is enabled.

```bash
# BYPARR service configuration
export BYPARR_URL="http://byparr:8191/v1"
export BYPARR_TIMEOUT="60"
export BYPARR_ENABLED="false"   # true/false
```

### URL downloader defaults
Used by `DownloadingTools`.

```bash
export URL_DOWNLOADER_MAX_RETRIES="3"
export URL_DOWNLOADER_TIMEOUT="30"
```

## Toolkit Configuration Examples

### Search (SearxNG)

```python
from enhancedtoolkits import SearxngTools

search = SearxngTools(
    host="http://searxng:8080",
    max_results=10,
    enable_content_fetching=False,
)
```

### Files (sandbox)

```python
from enhancedtoolkits import FilesTools

files = FilesTools(base_dir="/app/workspace")
```

### Finance

```python
from enhancedtoolkits import YFinanceTools

finance = YFinanceTools(enable_caching=True, cache_ttl=300, rate_limit_delay=0.1)
```

## Optional dependencies

Some toolkits require optional dependencies:

- Search + downloading require `markitdown` (install `enhancedtoolkits[content]`).
- YouTube requires `youtube-transcript-api` (install `enhancedtoolkits[youtube]`).
- Weather requires `pywttr` + models (install `enhancedtoolkits[weather]`).

## Next Steps

- [`docs/getting-started/quick-start.md`](quick-start.md)
- [`docs/toolkits/index.md`](../toolkits/index.md)
