# YouTube Tools for AI Agents

The YouTube tools provide **basic video metadata** (via YouTube oEmbed) and **transcript extraction** (via `youtube-transcript-api`).

All tool functions return **JSON strings**.

Note: tool schemas are **strict** (OpenAI compatibility), so agents should pass all parameters even when defaults are shown.

This toolkit requires `youtube-transcript-api`.

## AI Agent Setup

```python
from enhancedtoolkits import YouTubeTools

youtube = YouTubeTools(
    rate_limit_delay=0.5,  # seconds between requests
    timeout=30,            # request timeout
    max_retries=3          # retries for transcript fetches
)

agent.register_tools([youtube])
```

## Configuration

| Parameter | Type | Default | Description |
|---|---:|---:|---|
| `rate_limit_delay` | float | `0.5` | Delay between outbound requests (seconds) |
| `timeout` | int | `30` | HTTP request timeout (seconds) |
| `max_retries` | int | `3` | Retry attempts for transcript fetches |

## Available Functions

### `fetch_youtube_video_metadata(video_url)`
Fetch **basic metadata** via YouTube oEmbed.

**Important limitation:** oEmbed does **not** include view counts, likes, upload date, or duration.

**Returns** JSON with fields like:
- `title`, `author_name`, `thumbnail_url`
- `html` (embed HTML)

### `extract_youtube_video_id(video_url)`
Extract the 11-character YouTube video id.

**Returns** JSON like:
- `{"video_id": "dQw4w9WgXcQ", "timestamp": "..."}`

Accepts common formats:
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `youtube.com/watch?v=VIDEO_ID` (schemeless)
- Raw `VIDEO_ID` (11 chars)

### `fetch_comprehensive_youtube_video_info(video_url, include_transcript=False)`
Combine metadata and (optionally) transcript info into one response.

If `include_transcript=True` and transcripts are available, the tool will:
- list available transcript languages
- fetch a best-effort transcript (prefers `en` if available)

## Transcript Functions

Transcript functionality requires:

```bash
pip install youtube-transcript-api
```

### `fetch_youtube_video_transcript(video_url, language='en', auto_generated=True)`
Fetch the transcript in the preferred language (best-effort fallback if unavailable).

**Returns** JSON with:
- `segments`: list of `{text, start, duration, ...}` objects
- `transcript_text`: concatenated text
- `duration_seconds`: computed from segment timings

### `fetch_available_youtube_transcripts(video_url)`
List manual, auto-generated, and translatable transcript options.

### `fetch_youtube_transcript_languages(video_url)`
Return a simplified list of available transcript language codes.

## Example workflow

1) Fetch metadata
```python
youtube.fetch_youtube_video_metadata("https://youtu.be/dQw4w9WgXcQ")
```

2) Check transcript languages
```python
youtube.fetch_youtube_transcript_languages("https://youtu.be/dQw4w9WgXcQ")
```

3) Fetch transcript
```python
youtube.fetch_youtube_video_transcript("https://youtu.be/dQw4w9WgXcQ", language="en")
```

## Error handling

Common error scenarios:
- invalid URL / video id extraction failure
- video unavailable
- transcripts disabled or missing
- network errors / timeouts

## API Reference

- [`docs/api/youtube.md`](../api/youtube.md)
