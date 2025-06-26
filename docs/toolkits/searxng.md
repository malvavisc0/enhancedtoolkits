# Search Tools (SearxNG) for AI Agents

The Search Tools provide comprehensive web search capabilities using SearxNG integration with content extraction and anti-bot bypass for AI agents.

## 🤖 AI Agent Setup

```python
from enhancedtoolkits import SearxngTools

# Initialize for your AI agent
search = SearxngTools(
    host="http://searxng:8080",     # SearxNG instance URL
    max_results=10,                 # Results per search
    timeout=30,                     # Request timeout
    enable_content_fetching=True,   # Extract page content
    byparr_enabled=False           # Anti-bot bypass (optional)
)

# Register with your agent
agent.register_tools([search])
```

## ⚙️ Configuration Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `host` | str | Required | SearxNG instance URL |
| `max_results` | int | `10` | Maximum results per search |
| `timeout` | int | `30` | Request timeout in seconds |
| `enable_content_fetching` | bool | `True` | Extract full page content |
| `byparr_enabled` | bool | `False` | Enable anti-bot bypass for content |

## 🔍 Available Functions

Your AI agent will have access to these search functions:

### `search_web()`
General web search across all categories.

**Parameters:**
- `query`: Search query string
- `max_results`: Number of results to return (optional)

**Returns:** JSON with search results including:
- Title, URL, description
- Content snippet
- Full page content (if enabled)

### `search_news()`
Search specifically for news articles.

**Parameters:**
- `query`: News search query
- `max_results`: Number of results to return (optional)

**Returns:** News articles with publication dates and sources

### `search_images()`
Search for images related to the query.

**Parameters:**
- `query`: Image search query
- `max_results`: Number of results to return (optional)

**Returns:** Image results with URLs, titles, and metadata

### `search_videos()`
Search for videos across platforms.

**Parameters:**
- `query`: Video search query
- `max_results`: Number of results to return (optional)

**Returns:** Video results with titles, URLs, and descriptions

### `search_category()`
Search within specific categories.

**Parameters:**
- `query`: Search query
- `category`: Search category (see supported categories below)
- `max_results`: Number of results to return (optional)

**Returns:** Category-specific search results

## 📂 Supported Categories

### General Categories
- `"general"` - General web search
- `"news"` - News articles and current events
- `"images"` - Image search
- `"videos"` - Video content
- `"music"` - Music and audio content

### Specialized Categories
- `"science"` - Scientific papers and research
- `"files"` - File downloads and documents
- `"it"` - Technology and programming
- `"map"` - Maps and location data
- `"social media"` - Social media content

## 🌐 Content Extraction

When `enable_content_fetching=True`, the search tools will:
- **Extract full page content** from search results
- **Convert HTML to markdown** for better readability
- **Handle protected sites** with anti-bot bypass (if enabled)
- **Parse structured data** from web pages

### Content Processing
- **MarkItDown integration**: Converts HTML to clean markdown
- **Text extraction**: Removes ads and navigation elements
- **Smart parsing**: Identifies main content areas
- **Format preservation**: Maintains important formatting

## 🎯 AI Agent Integration Examples

### OpenAI Function Calling
```python
import openai
from enhancedtoolkits import SearxngTools

search = SearxngTools(host="http://searxng:8080")

# Get function schema for OpenAI
tools = [search.get_openai_schema()]

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{
        "role": "user", 
        "content": "Search for recent news about artificial intelligence"
    }],
    tools=tools,
    tool_choice="auto"
)
```

### Agno Framework
```python
from agno.agent import Agent
from enhancedtoolkits import SearxngTools

agent = Agent(
    name="Research Assistant",
    model="gpt-4",
    tools=[SearxngTools(
        host="http://searxng:8080",
        enable_content_fetching=True,
        max_results=15
    )]
)

# Agent can now search and analyze web content
response = agent.run("Find recent research papers about quantum computing and summarize the key findings")
```

## 🔧 Production Configuration

### Basic Setup
```python
search = SearxngTools(host="http://searxng:8080")
```

### Advanced Setup with Content Extraction
```python
search = SearxngTools(
    host="http://searxng:8080",
    max_results=20,                 # More results
    timeout=60,                     # Longer timeout
    enable_content_fetching=True,   # Extract full content
    byparr_enabled=True            # Bypass protection
)
```

### High-Performance Setup
```python
search = SearxngTools(
    host="http://searxng:8080",
    max_results=5,                  # Fewer results for speed
    timeout=15,                     # Quick timeout
    enable_content_fetching=False,  # No content extraction
    byparr_enabled=False           # Direct requests only
)
```

### Environment Variables
```bash
# SearxNG configuration
SEARXNG_HOST=http://searxng:8080
SEARXNG_TIMEOUT=30

# BYPARR service (for anti-bot bypass)
BYPARR_URL=http://byparr:8191/v1
BYPARR_TIMEOUT=60
BYPARR_ENABLED=false
```

## 📊 Example Agent Interactions

**Agent Query:** "Search for information about renewable energy trends"

**Search Tool Response:**
```json
{
  "query": "renewable energy trends",
  "results": [
    {
      "title": "Global Renewable Energy Trends 2024",
      "url": "https://example.com/renewable-trends",
      "description": "Latest trends in renewable energy adoption...",
      "content": "Full article content extracted and converted to markdown..."
    }
  ],
  "total_results": 10
}
```

**Agent Query:** "Find recent news about AI developments"

**Search Tool Operations:**
1. `search_news("AI developments")` - Search news category
2. Extract content from top articles
3. Agent analyzes and summarizes findings

**Agent Query:** "Search for scientific papers about climate change"

**Search Tool Operations:**
1. `search_category("climate change", "science")` - Scientific search
2. Extract abstracts and key information
3. Agent compiles research summary

## 🛡️ Anti-Bot Bypass

### BYPARR Integration
When `byparr_enabled=True`, the search tools can:
- **Bypass CloudFlare** protection on search results
- **Handle JavaScript** rendering for dynamic content
- **Overcome rate limiting** on protected sites
- **Access geo-restricted** content

### Smart Content Extraction
- **Retry logic** for failed content extraction
- **Fallback methods** when bypass fails
- **User agent rotation** to avoid detection
- **Request throttling** to respect site limits

## 🚨 Error Handling

The Search Tools handle various scenarios:
- **SearxNG unavailable**: Service downtime or misconfiguration
- **Network errors**: Connection timeouts and failures
- **Content extraction failures**: Protected or dynamic content
- **Rate limiting**: Search engine rate limits
- **Invalid queries**: Malformed or empty search terms

## 📈 Performance Features

### Caching
- Search results cached for 5 minutes
- Content extraction cached for 1 hour
- Reduces redundant requests to SearxNG

### Parallel Processing
- Concurrent content extraction from multiple URLs
- Batch processing for multiple search results
- Optimized for high-volume searches

### Smart Filtering
- Removes duplicate results
- Filters out low-quality content
- Prioritizes authoritative sources

## 🔍 Use Cases for AI Agents

### Research Assistance
- Academic research and paper discovery
- Market research and trend analysis
- Competitive intelligence gathering

### News Monitoring
- Current events tracking
- Industry news aggregation
- Real-time information updates

### Content Discovery
- Finding relevant articles and resources
- Image and video content search
- Specialized content in specific domains

### Fact Checking
- Verifying information across sources
- Finding authoritative references
- Cross-referencing claims and data

## 📊 Monitoring

Enable detailed logging for search operations:
```python
import logging
logging.basicConfig(level=logging.DEBUG)

search = SearxngTools(host="http://searxng:8080", debug=True)
```

## 🚀 Next Steps

1. **Set up SearxNG instance** or use existing one
2. **Configure** SearxngTools with your instance URL
3. **Enable content fetching** for full article extraction
4. **Set up BYPARR** if you need anti-bot bypass
5. **Register** with your AI agent framework
6. **Test** with various search queries and categories
7. **Monitor** search performance and adjust settings

The Search Tools enable your AI agent to access comprehensive web search capabilities while extracting full content from results, making it perfect for research, monitoring, and information gathering tasks.