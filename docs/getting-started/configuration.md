# Configuration

Configure Enhanced Toolkits for production use with caching, rate limiting, and security controls.

## Environment Variables

Set up environment variables for API keys and configuration:

```bash
# Required for specific tools
export OPENWEATHERMAP_API_KEY="your_api_key"
export YOUTUBE_API_KEY="your_api_key"

# Optional configuration
export SEARXNG_HOST="http://localhost:8080"
export CACHE_TTL="300"
export RATE_LIMIT_DELAY="0.1"
```

## Tool Configuration

### Reasoning Tools

```python
from enhancedtoolkits import ReasoningTools

reasoning = ReasoningTools(
    reasoning_depth=5,
    enable_bias_detection=True,
    max_iterations=10
)
```

### Search Tools

```python
from enhancedtoolkits import SearxngTools

search = SearxngTools(
    host="http://your-searxng:8080",
    max_results=10,
    enable_content_fetching=True,
    timeout=30
)
```

### Finance Tools

```python
from enhancedtoolkits import YFinanceTools

finance = YFinanceTools(
    enable_caching=True,
    cache_ttl=300,
    rate_limit_delay=0.1
)
```

### Files Tools

```python
from enhancedtoolkits import FilesTools

files = FilesTools(
    allowed_extensions=['.txt', '.json', '.csv'],
    max_file_size=10485760,  # 10MB
    enable_security_scan=True
)
```

## Production Settings

For production deployments, consider these settings:

```python
# Enable caching for all tools
tools_config = {
    'enable_caching': True,
    'cache_ttl': 300,
    'rate_limit_delay': 0.1,
    'timeout': 30,
    'max_retries': 3
}

# Apply to all tools
reasoning = ReasoningTools(**tools_config)
finance = YFinanceTools(**tools_config)
search = SearxngTools(host="http://searxng:8080", **tools_config)
```

## Security Configuration

```python
# Files Tools security settings
files = FilesTools(
    allowed_extensions=['.txt', '.json', '.csv', '.md'],
    blocked_extensions=['.exe', '.bat', '.sh'],
    max_file_size=10485760,  # 10MB
    enable_security_scan=True,
    scan_timeout=10
)

# Downloader Tools security settings
downloader = DownloaderTools(
    allowed_domains=['example.com', 'trusted-site.org'],
    blocked_domains=['malicious-site.com'],
    max_file_size=52428800,  # 50MB
    enable_virus_scan=True
)
```

## Next Steps

- [Quick Start Guide](quick-start.md)
- [Core Toolkits](../toolkits/index.md)
- [API Reference](../api/index.md)