# YouTube Tools for AI Agents

The YouTube Tools provide video metadata and transcript extraction capabilities for AI agents that need to analyze YouTube content.

## 🤖 AI Agent Setup

```python
from enhancedtoolkits import YouTubeTools

# Initialize for your AI agent
youtube = YouTubeTools(
    rate_limit_delay=0.5,          # Delay between requests (seconds)
    timeout=30,                    # Request timeout
    max_retries=3                  # Maximum retry attempts
)

# Register with your agent
agent.register_tools([youtube])
```

## ⚙️ Configuration Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `rate_limit_delay` | float | `0.5` | Delay between requests in seconds |
| `timeout` | int | `30` | Request timeout in seconds |
| `max_retries` | int | `3` | Maximum retry attempts for failed requests |

## 🎥 Available Functions

Your AI agent will have access to these YouTube functions:

### `get_video_metadata()`
Get comprehensive video metadata including title, description, duration, and statistics.

**Parameters:**
- `video_url`: YouTube video URL (supports various formats)

**Returns:** JSON with video metadata including:
- Title, description, author
- Duration, view count, like count
- Upload date, thumbnails
- Channel information

### `get_video_transcript()`
Extract video transcript with language support.

**Parameters:**
- `video_url`: YouTube video URL
- `language_code`: Language code (e.g., 'en', 'es', 'fr') - optional

**Returns:** JSON with transcript text and timing information

### `get_available_transcripts()`
List all available transcript languages for a video.

**Parameters:**
- `video_url`: YouTube video URL

**Returns:** JSON with available transcript languages and types

### `get_video_info()`
Get complete video information including metadata and optional transcript.

**Parameters:**
- `video_url`: YouTube video URL
- `include_transcript`: Whether to include transcript (default: false)

**Returns:** Combined metadata and transcript information

## 🌍 Supported URL Formats

The YouTube Tools support various YouTube URL formats:
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://youtube.com/watch?v=VIDEO_ID`
- `https://m.youtube.com/watch?v=VIDEO_ID`

## 🗣️ Language Support

### Transcript Languages
Supports 50+ languages including:
- **English** (`en`) - Most common
- **Spanish** (`es`) - Spanish content
- **French** (`fr`) - French content
- **German** (`de`) - German content
- **Chinese** (`zh`) - Chinese content
- **Japanese** (`ja`) - Japanese content
- **Korean** (`ko`) - Korean content
- **Portuguese** (`pt`) - Portuguese content
- **Russian** (`ru`) - Russian content
- **Arabic** (`ar`) - Arabic content

### Auto-Generated vs Manual
- **Manual transcripts**: Human-created, higher accuracy
- **Auto-generated**: AI-generated, available for most videos
- **Translated**: Auto-translated from original language

## 🎯 AI Agent Integration Examples

### OpenAI Function Calling
```python
import openai
from enhancedtoolkits import YouTubeTools

youtube = YouTubeTools()

# Get function schema for OpenAI
tools = [youtube.get_openai_schema()]

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{
        "role": "user", 
        "content": "Analyze this YouTube video: https://youtu.be/dQw4w9WgXcQ"
    }],
    tools=tools,
    tool_choice="auto"
)
```

### Agno Framework
```python
from agno.agent import Agent
from enhancedtoolkits import YouTubeTools

agent = Agent(
    name="Video Analyst",
    model="gpt-4",
    tools=[YouTubeTools(rate_limit_delay=1.0)]
)

# Agent can now analyze YouTube videos
response = agent.run("Get the transcript of this video and summarize the key points: https://youtu.be/VIDEO_ID")
```

## 🔧 Production Configuration

### Basic Setup
```python
youtube = YouTubeTools()
```

### High-Volume Setup
```python
youtube = YouTubeTools(
    rate_limit_delay=1.0,          # Slower for high volume
    timeout=60,                    # Longer timeout
    max_retries=5                  # More retries
)
```

### Fast Response Setup
```python
youtube = YouTubeTools(
    rate_limit_delay=0.1,          # Faster requests
    timeout=15,                    # Quick timeout
    max_retries=1                  # Fewer retries
)
```

## 📊 Example Agent Interactions

**Agent Query:** "What is this video about? https://youtu.be/dQw4w9WgXcQ"

**YouTube Tool Response:**
```json
{
  "title": "Rick Astley - Never Gonna Give You Up",
  "description": "The official video for Rick Astley's 'Never Gonna Give You Up'...",
  "duration": "3:33",
  "view_count": "1.4B",
  "upload_date": "2009-10-25",
  "channel": "Rick Astley",
  "summary": "Classic 1980s pop song and internet meme"
}
```

**Agent Query:** "Get the transcript of this educational video and extract the main topics"

**YouTube Tool Operations:**
1. `get_video_metadata()` - Get video information
2. `get_available_transcripts()` - Check transcript availability
3. `get_video_transcript()` - Extract transcript text
4. Agent analyzes transcript for main topics

## 🚨 Error Handling

The YouTube Tools handle various error scenarios:
- **Video not found**: Invalid or deleted videos
- **Private videos**: Access restricted content
- **No transcripts**: Videos without available transcripts
- **Rate limiting**: YouTube API rate limits
- **Network errors**: Connection timeouts and failures

## 📈 Rate Limiting

YouTube has rate limits to prevent abuse:
- **Default delay**: 0.5 seconds between requests
- **Recommended**: 1.0 second for production use
- **Burst protection**: Automatic retry with exponential backoff
- **Respect limits**: Avoid overwhelming YouTube's servers

## 🔍 Use Cases for AI Agents

### Content Analysis
- Extract video summaries and key points
- Analyze educational content structure
- Identify main topics and themes

### Research Assistance
- Gather information from video lectures
- Extract quotes and references
- Compile research from multiple videos

### Content Moderation
- Analyze video content for compliance
- Extract metadata for categorization
- Monitor channel activity

### Educational Support
- Create study notes from lectures
- Extract learning objectives
- Generate quiz questions from content

## 📊 Monitoring

Enable detailed logging for YouTube operations:
```python
import logging
logging.basicConfig(level=logging.DEBUG)

youtube = YouTubeTools(debug=True)
```

## 🚀 Next Steps

1. **Initialize** YouTubeTools with appropriate rate limiting
2. **Register** with your AI agent framework
3. **Test** with sample YouTube URLs
4. **Configure** rate limits for your use case
5. **Monitor** API usage and respect YouTube's terms

The YouTube Tools enable your AI agent to extract valuable information from YouTube videos while respecting platform limits and providing robust error handling.