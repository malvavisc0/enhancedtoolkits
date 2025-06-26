# YouTube Tools API Reference

API documentation for the YouTube Tools toolkit - video metadata and transcript extraction with multi-language support.

## Class: YouTubeTools

YouTube video analysis toolkit for extracting metadata, transcripts, and video information.

### YouTubeTools()

Initialize the YouTube Tools toolkit.

**Parameters:**
- `api_key` (str, optional): YouTube Data API key. Can be set via YOUTUBE_API_KEY environment variable
- `enable_caching` (bool, optional): Enable response caching. Default: True
- `cache_ttl` (int, optional): Cache time-to-live in seconds. Default: 300
- `timeout` (int, optional): Request timeout in seconds. Default: 30

### Methods

#### get_video_info()

Get comprehensive information about a YouTube video.

**Parameters:**
- `video_url` (str): YouTube video URL or video ID
- `include_transcript` (bool): Whether to include transcript. Default: False
- `language` (str): Preferred language for metadata. Default: 'en'

**Returns:**
- `dict`: Video metadata including title, description, duration, views, and optional transcript

#### get_video_transcript()

Extract transcript/captions from a YouTube video.

**Parameters:**
- `video_url` (str): YouTube video URL or video ID
- `language` (str): Preferred transcript language. Default: 'en'
- `auto_generated` (bool): Include auto-generated captions. Default: True

**Returns:**
- `dict`: Video transcript with timestamps and language information

#### get_channel_info()

Get information about a YouTube channel.

**Parameters:**
- `channel_url` (str): YouTube channel URL or channel ID
- `include_videos` (bool): Include recent videos list. Default: False
- `max_videos` (int): Maximum number of videos to include. Default: 10

**Returns:**
- `dict`: Channel metadata including subscriber count, video count, and optional video list

#### search_videos()

Search for YouTube videos based on query.

**Parameters:**
- `query` (str): Search query
- `max_results` (int): Maximum number of results. Default: 10
- `order` (str): Sort order (relevance, date, rating, viewCount). Default: 'relevance'
- `duration` (str): Video duration filter (short, medium, long). Default: 'any'

**Returns:**
- `dict`: Search results with video metadata and statistics

#### get_playlist_info()

Get information about a YouTube playlist.

**Parameters:**
- `playlist_url` (str): YouTube playlist URL or playlist ID
- `include_videos` (bool): Include videos in playlist. Default: True
- `max_videos` (int): Maximum number of videos to include. Default: 50

**Returns:**
- `dict`: Playlist metadata and video list with details

## Usage Examples

```python
from agno.agent import Agent
from enhancedtoolkits import YouTubeTools

# Initialize with API key
youtube = YouTubeTools(api_key="your_youtube_api_key")

# Add to agent
agent = Agent(
    name="Video Analyst",
    model="gpt-4",
    tools=[youtube]
)

# Agent can now analyze YouTube content
response = agent.run("Get the transcript of this YouTube video and summarize it")
```

## Features

- **Video Metadata**: Complete video information including statistics
- **Transcript Extraction**: Multi-language transcript support
- **Channel Analysis**: Channel statistics and video listings
- **Search Functionality**: Advanced video search with filters
- **Playlist Support**: Playlist metadata and video extraction
- **Multi-language**: Support for 30+ languages
- **Caching**: Intelligent caching to reduce API calls

## Related Documentation

- [YouTube Tools Guide](../toolkits/youtube.md)
- [StrictToolkit Base](base.md)
- [API Configuration](../getting-started/configuration.md)