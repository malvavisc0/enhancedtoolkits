# Core Toolkits

Enhanced Toolkits provides 8 comprehensive toolkits designed for AI agents that need reliable, robust, and feature-rich capabilities.

## Available Toolkits

<div class="toolkit-grid">
  <div class="toolkit-card">
    <h3>🧠 Reasoning Tools</h3>
    <p>Multi-modal reasoning with cognitive bias detection and session management.</p>
    <ul>
      <li>6 reasoning types (Deductive, Inductive, Abductive, etc.)</li>
      <li>Bias detection and mitigation</li>
      <li>Session tracking and history</li>
      <li>Quality assessment metrics</li>
    </ul>
    <a href="reasoning/">Learn More →</a>
  </div>
  
  <div class="toolkit-card">
    <h3>🔍 Search Tools (SearxNG)</h3>
    <p>Comprehensive web search with content extraction and parsing.</p>
    <ul>
      <li>Multiple search categories</li>
      <li>Content extraction with MarkItDown</li>
      <li>Anti-bot bypass capabilities</li>
      <li>Rate limiting and retry logic</li>
    </ul>
    <a href="searxng/">Learn More →</a>
  </div>
  
  <div class="toolkit-card">
    <h3>💭 Thinking Tools</h3>
    <p>Structured thinking frameworks with cognitive awareness.</p>
    <ul>
      <li>8 thinking types (Analysis, Synthesis, etc.)</li>
      <li>Cognitive bias detection</li>
      <li>Quality assessment</li>
      <li>Thinking pattern evolution</li>
    </ul>
    <a href="thinking/">Learn More →</a>
  </div>
  
  <div class="toolkit-card">
    <h3>📁 Files Tools</h3>
    <p>Enterprise-grade file operations with comprehensive security.</p>
    <ul>
      <li>Path traversal protection</li>
      <li>File type validation</li>
      <li>Atomic operations</li>
      <li>Memory optimization</li>
    </ul>
    <a href="files/">Learn More →</a>
  </div>
  
  <div class="toolkit-card">
    <h3>📈 Finance Tools (YFinance)</h3>
    <p>Comprehensive financial data retrieval with caching.</p>
    <ul>
      <li>Real-time stock prices</li>
      <li>Company information</li>
      <li>Financial statements</li>
      <li>News and recommendations</li>
    </ul>
    <a href="finance/">Learn More →</a>
  </div>
  
  <div class="toolkit-card">
    <h3>🎥 YouTube Tools</h3>
    <p>Video metadata and transcript extraction.</p>
    <ul>
      <li>Comprehensive metadata</li>
      <li>Multi-language transcripts</li>
      <li>URL format flexibility</li>
      <li>Error handling and retry logic</li>
    </ul>
    <a href="youtube/">Learn More →</a>
  </div>
  
  <div class="toolkit-card">
    <h3>☁️ Weather Tools</h3>
    <p>Weather data and forecasts with multi-language support.</p>
    <ul>
      <li>Current weather conditions</li>
      <li>Multi-day forecasts</li>
      <li>30+ supported languages</li>
      <li>Flexible location input</li>
    </ul>
    <a href="weather/">Learn More →</a>
  </div>
  
  <div class="toolkit-card">
    <h3>📥 Downloader Tools</h3>
    <p>Universal file downloading with anti-bot bypass.</p>
    <ul>
      <li>Universal file support</li>
      <li>Anti-bot bypass with BYPARR</li>
      <li>Smart content processing</li>
      <li>Multiple output formats</li>
    </ul>
    <a href="downloader/">Learn More →</a>
  </div>
</div>

## Common Features

All toolkits share these production-ready features:

### 🛡️ Security & Validation
- Input validation and sanitization
- Error handling with detailed logging
- Rate limiting and request throttling
- Secure configuration management

### ⚡ Performance
- Built-in caching mechanisms
- Memory optimization
- Efficient data processing
- Configurable timeouts

### 🔧 Integration
- OpenAI function calling compatibility
- Agno framework integration
- Consistent API patterns
- Comprehensive documentation

### 📊 Monitoring
- Detailed logging and debugging
- Performance metrics
- Error tracking and reporting
- Session state management

## Getting Started

### Basic Usage Pattern

All toolkits follow a consistent pattern:

```python
from enhancedtoolkits import ToolkitName

# Initialize with optional configuration
toolkit = ToolkitName(
    # Configuration options
    enable_caching=True,
    timeout=30
)

# Use toolkit methods
result = toolkit.method_name(
    required_param="value",
    optional_param="value"
)
```

### Configuration Options

Most toolkits support these common configuration options:

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `enable_caching` | bool | `True` | Enable response caching |
| `cache_ttl` | int | `300` | Cache time-to-live in seconds |
| `timeout` | int | `30` | Request timeout in seconds |
| `max_retries` | int | `3` | Maximum retry attempts |
| `rate_limit_delay` | float | `0.1` | Delay between requests |

### Error Handling

All toolkits use consistent error handling:

```python
try:
    result = toolkit.method_name(param="value")
    print(result)
except ToolkitSpecificError as e:
    print(f"Toolkit error: {e}")
except Exception as e:
    print(f"General error: {e}")
```

## Next Steps

1. **Choose a toolkit** that fits your needs
2. **Read the specific documentation** for detailed usage
3. **Try the examples** provided in each toolkit guide
4. **Explore advanced features** like caching and rate limiting

## Need Help?

- 📖 Check individual toolkit documentation
- 🧮 Explore [Calculator Modules](../calculators/)
- 🔧 Learn about [Advanced Features](../advanced/)
- 💬 Join our [community discussions](https://github.com/malvavisc0/enhancedtoolkits/discussions)