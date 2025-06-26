# Downloader Tools for AI Agents

The Downloader Tools provide universal file downloading with anti-bot bypass capabilities for AI agents that need to access web content and files.

## 🤖 AI Agent Setup

```python
from enhancedtoolkits import DownloaderTools

# Initialize for your AI agent
downloader = DownloaderTools(
    byparr_enabled=True,           # Enable anti-bot bypass
    max_retries=3,                 # Maximum retry attempts
    timeout=30,                    # Request timeout in seconds
    user_agent_rotation=True,      # Rotate user agents
    enable_caching=True            # Cache downloaded content
)

# Register with your agent
agent.register_tools([downloader])
```

## ⚙️ Configuration Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `byparr_enabled` | bool | `False` | Enable BYPARR anti-bot bypass service |
| `max_retries` | int | `3` | Maximum retry attempts for failed downloads |
| `timeout` | int | `30` | Request timeout in seconds |
| `user_agent_rotation` | bool | `True` | Rotate user agents to avoid detection |
| `enable_caching` | bool | `True` | Cache downloaded content |

## 📥 Available Functions

Your AI agent will have access to these download functions:

### `get_file_from_url()`
Download any file with smart content processing.

**Parameters:**
- `url`: URL of the file to download
- `output`: Output format ("auto", "markdown", "text", "html", "binary")

**Returns:** Processed file content based on file type:
- **HTML/Web pages**: Converted to markdown or text
- **PDF documents**: Extracted text content
- **Office documents**: Extracted text from Word, Excel, PowerPoint
- **Images**: File metadata and information
- **Videos/Audio**: File information and metadata
- **Archives**: File listing and metadata

### `download_multiple_urls()`
Batch download content from multiple URLs.

**Parameters:**
- `urls`: List of URLs to download
- `format`: Output format for all downloads

**Returns:** Combined results from all downloads

### `get_url_metadata()`
Extract metadata without downloading full content.

**Parameters:**
- `url`: URL to analyze

**Returns:** URL metadata including:
- Content type and size
- Last modified date
- Server information
- Accessibility status

### `check_url_accessibility()`
Test URL accessibility and response time.

**Parameters:**
- `url`: URL to test

**Returns:** Accessibility report with:
- Response status
- Response time
- Content type
- Error information (if any)

## 🔧 Supported File Types

### Web Content
- **HTML pages**: Full content extraction and conversion
- **XML/RSS feeds**: Structured data extraction
- **JSON APIs**: Data parsing and formatting

### Documents
- **PDF files**: Text extraction via MarkItDown
- **Microsoft Office**: Word (.docx), Excel (.xlsx), PowerPoint (.pptx)
- **OpenDocument**: ODT, ODS, ODP formats
- **Text files**: Plain text, CSV, TSV

### Media Files
- **Images**: JPEG, PNG, GIF, WebP metadata
- **Videos**: MP4, AVI, MOV file information
- **Audio**: MP3, WAV, FLAC metadata

### Archives
- **ZIP files**: Content listing and extraction
- **RAR archives**: File information
- **7z files**: Archive metadata

## 🛡️ Anti-Bot Bypass

### BYPARR Integration
When `byparr_enabled=True`, the downloader uses BYPARR service to bypass:
- **CloudFlare protection**
- **Bot detection systems**
- **Rate limiting**
- **Geographic restrictions**

### User Agent Rotation
- Rotates between realistic browser user agents
- Mimics different browsers and operating systems
- Reduces detection probability

### Smart Headers
- Adds realistic HTTP headers
- Mimics browser behavior
- Includes referrer and accept headers

## 🎯 AI Agent Integration Examples

### OpenAI Function Calling
```python
import openai
from enhancedtoolkits import DownloaderTools

downloader = DownloaderTools(byparr_enabled=True)

# Get function schema for OpenAI
tools = [downloader.get_openai_schema()]

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{
        "role": "user", 
        "content": "Download and summarize this research paper: https://arxiv.org/pdf/2301.00001.pdf"
    }],
    tools=tools,
    tool_choice="auto"
)
```

### Agno Framework
```python
from agno.agent import Agent
from enhancedtoolkits import DownloaderTools

agent = Agent(
    name="Content Researcher",
    model="gpt-4",
    tools=[DownloaderTools(byparr_enabled=True, max_retries=5)]
)

# Agent can now download and analyze web content
response = agent.run("Download this webpage and extract the main points: https://example.com/article")
```

## 🔧 Production Configuration

### Basic Setup
```python
downloader = DownloaderTools()
```

### High-Security Setup
```python
downloader = DownloaderTools(
    byparr_enabled=True,           # Enable anti-bot bypass
    max_retries=5,                 # More retries for reliability
    timeout=60,                    # Longer timeout
    user_agent_rotation=True,      # Rotate user agents
    enable_caching=True            # Cache for performance
)
```

### Fast Download Setup
```python
downloader = DownloaderTools(
    byparr_enabled=False,          # Direct downloads only
    max_retries=1,                 # Quick failure
    timeout=15,                    # Fast timeout
    enable_caching=True            # Cache for speed
)
```

### Environment Variables
```bash
# BYPARR service configuration
BYPARR_URL=http://byparr:8191/v1
BYPARR_TIMEOUT=60
BYPARR_ENABLED=true

# Download configuration
URL_DOWNLOADER_MAX_RETRIES=3
URL_DOWNLOADER_TIMEOUT=30
```

## 📊 Example Agent Interactions

**Agent Query:** "Download this PDF and summarize the key findings: https://example.com/research.pdf"

**Downloader Tool Response:**
```json
{
  "url": "https://example.com/research.pdf",
  "content_type": "application/pdf",
  "size": "2.3 MB",
  "extracted_text": "Research findings show that...",
  "summary": "Key findings include improved efficiency and reduced costs..."
}
```

**Agent Query:** "Check if this website is accessible and download the main content"

**Downloader Tool Operations:**
1. `check_url_accessibility()` - Test URL accessibility
2. `get_url_metadata()` - Get content information
3. `get_file_from_url()` - Download and process content

**Agent Query:** "Download content from these 5 URLs and compare them"

**Downloader Tool Operations:**
1. `download_multiple_urls()` - Batch download all URLs
2. Agent analyzes and compares content

## 🚨 Error Handling

The Downloader Tools handle various scenarios:
- **Network errors**: Connection timeouts, DNS failures
- **HTTP errors**: 404 Not Found, 403 Forbidden, 500 Server Error
- **Bot detection**: CloudFlare challenges, rate limiting
- **File format errors**: Corrupted files, unsupported formats
- **Size limits**: Files too large for processing

## 📈 Performance Features

### Caching
- Downloaded content cached for 1 hour
- Reduces redundant downloads
- Improves response times for repeated requests

### Retry Logic
- Exponential backoff for failed requests
- Different strategies for different error types
- Automatic fallback from BYPARR to direct download

### Content Processing
- Streaming downloads for large files
- Memory-efficient processing
- Automatic format detection

## 🔍 Use Cases for AI Agents

### Research Assistance
- Download academic papers and extract text
- Gather information from multiple sources
- Access research databases and repositories

### Content Analysis
- Download web articles for analysis
- Extract data from online reports
- Process multimedia content metadata

### Data Collection
- Batch download datasets
- Access API endpoints and process responses
- Collect information from multiple websites

### Document Processing
- Download and process office documents
- Extract text from PDFs for analysis
- Handle various file formats automatically

## 📊 Monitoring

Enable detailed logging for download operations:
```python
import logging
logging.basicConfig(level=logging.DEBUG)

downloader = DownloaderTools(debug=True)
```

## 🚀 Next Steps

1. **Configure** DownloaderTools with appropriate anti-bot settings
2. **Set up BYPARR** service if needed for protected sites
3. **Register** with your AI agent framework
4. **Test** with various file types and URLs
5. **Monitor** download success rates and performance
6. **Adjust** retry and timeout settings based on usage

The Downloader Tools enable your AI agent to access virtually any web content while bypassing common restrictions and providing robust error handling for reliable content acquisition.