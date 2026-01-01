"""YouTube tools.

This toolkit uses:

- Metadata: YouTube oEmbed (title/author/thumbnail/embed html)
- Transcripts: `youtube-transcript-api`

All public tools return **JSON strings**.

Notes:
- oEmbed does **not** include view counts / likes / upload date / duration.
- Transcript tools require `youtube-transcript-api`.

Author: malvavisc0
License: MIT
"""

from __future__ import annotations

import json
import time
from datetime import datetime
from typing import Any, Dict, List, Optional
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlencode, urlparse
from urllib.request import urlopen

from agno.utils.log import log_error, log_info, log_warning
from youtube_transcript_api import YouTubeTranscriptApi  # type: ignore
from youtube_transcript_api._errors import (  # type: ignore
    NoTranscriptFound,
    TranscriptsDisabled,
    VideoUnavailable,
)

from .base import StrictToolkit


class YouTubeError(Exception):
    """Base exception for YouTube-related errors."""


class YouTubeValidationError(YouTubeError):
    """Exception for input validation errors."""


class YouTubeDataError(YouTubeError):
    """Exception for data retrieval errors."""


class EnhancedYouTubeTools(StrictToolkit):
    """YouTube metadata + transcript tools.

    - Metadata uses YouTube oEmbed.
    - Transcripts use `youtube-transcript-api`.

    All tools return JSON strings.
    """

    # Common transcript languages (used only for convenience filtering)
    COMMON_LANGUAGES: List[str] = [
        "en",
        "es",
        "fr",
        "de",
        "it",
        "pt",
        "ru",
        "ja",
        "ko",
        "zh",
        "ar",
        "hi",
    ]

    def __init__(
        self,
        rate_limit_delay: float = 0.5,
        timeout: int = 30,
        max_retries: int = 3,
        add_instructions: bool = True,
        **kwargs,
    ):
        """Initialize the toolkit.

        Args:
            rate_limit_delay: Delay between outbound requests (seconds).
            timeout: HTTP request timeout (seconds).
            max_retries: Retry attempts for transcript fetches.
            add_instructions: Whether to attach LLM usage instructions.
        """

        self.rate_limit_delay = float(max(0.1, min(5.0, rate_limit_delay)))
        self.timeout = int(max(5, min(120, timeout)))
        self.max_retries = int(max(1, min(10, max_retries)))
        self._last_request_time = 0.0

        instructions = (
            self.get_llm_usage_instructions() if add_instructions else ""
        )

        super().__init__(
            name="enhanced_youtube_tools",
            instructions=instructions,
            add_instructions=add_instructions,
            **kwargs,
        )

        # Register methods
        self.register(self.fetch_youtube_video_metadata)
        self.register(self.fetch_youtube_video_transcript)
        self.register(self.extract_youtube_video_id)
        self.register(self.fetch_comprehensive_youtube_video_info)

        self.register(self.fetch_available_youtube_transcripts)
        self.register(self.fetch_youtube_transcript_languages)

        log_info(
            "Enhanced YouTube Tools initialized - "
            f"Rate Limit: {self.rate_limit_delay}s, "
            f"Timeout: {self.timeout}s"
        )

    def fetch_youtube_video_metadata(self, video_url: str) -> str:
        """Fetch basic metadata for a YouTube video via oEmbed."""
        try:
            video_id = self._extract_video_id(video_url)
            self._apply_rate_limit()

            oembed = self._fetch_oembed_data(video_id)
            metadata = self._enhance_oembed_metadata(
                oembed, video_id, video_url
            )

            return self._format_json_response(metadata)
        except (YouTubeValidationError, YouTubeDataError):
            raise
        except Exception as e:  # pylint: disable=broad-exception-caught
            log_error(
                f"Unexpected error getting metadata for {video_url}: {e}"
            )
            raise YouTubeDataError(f"Failed to get video metadata: {e}") from e

    def fetch_youtube_video_transcript(
        self, video_url: str, language: str = "en", auto_generated: bool = True
    ) -> str:
        """Fetch a transcript (if available) with optional language preference."""
        try:
            video_id = self._extract_video_id(video_url)

            self._apply_rate_limit()
            transcript = self._fetch_transcript_with_retry(
                video_id=video_id,
                language=(language or "en").strip().lower(),
                auto_generated=bool(auto_generated),
            )

            return self._format_json_response(transcript)
        except (YouTubeValidationError, YouTubeDataError):
            raise
        except Exception as e:  # pylint: disable=broad-exception-caught
            log_error(
                f"Unexpected error getting transcript for {video_url}: {e}"
            )
            raise YouTubeDataError(
                f"Failed to get video transcript: {e}"
            ) from e

    def fetch_available_youtube_transcripts(self, video_url: str) -> str:
        """List available transcript tracks for a video."""
        try:
            video_id = self._extract_video_id(video_url)
            self._apply_rate_limit()

            ytt = YouTubeTranscriptApi()

            result: Dict[str, Any] = {
                "video_id": video_id,
                "manual_transcripts": [],
                "auto_generated_transcripts": [],
                "translatable_transcripts": [],
                "timestamp": datetime.now().isoformat(),
            }

            try:
                transcript_list = ytt.list(video_id)
            except (
                TranscriptsDisabled,
                NoTranscriptFound,
                VideoUnavailable,
            ) as e:
                result["message"] = f"No transcripts available: {e}"
                if isinstance(e, TranscriptsDisabled):
                    result["note"] = (
                        "TranscriptsDisabled can be a false-positive on some cloud "
                        "environments (IP-based blocking/challenges). If it works locally, "
                        "try a different egress IP or use the library's ProxyConfig."
                    )
                return self._format_json_response(result)

            for transcript in transcript_list:
                is_translatable = bool(
                    getattr(transcript, "is_translatable", False)
                )
                info = {
                    "language": transcript.language,
                    "language_code": transcript.language_code,
                    "is_generated": transcript.is_generated,
                    "is_translatable": is_translatable,
                }

                if transcript.is_generated:
                    result["auto_generated_transcripts"].append(info)
                else:
                    result["manual_transcripts"].append(info)

                if is_translatable:
                    result["translatable_transcripts"].append(info)

            return self._format_json_response(result)

        except (YouTubeValidationError, YouTubeDataError):
            raise
        except Exception as e:  # pylint: disable=broad-exception-caught
            log_error(
                f"Unexpected error getting available transcripts for {video_url}: {e}"
            )
            raise YouTubeDataError(
                f"Failed to get available transcripts: {e}"
            ) from e

    def fetch_youtube_transcript_languages(self, video_url: str) -> str:
        """Return a simplified list of available transcript language codes."""
        try:
            transcripts = json.loads(
                self.fetch_available_youtube_transcripts(video_url)
            )

            language_codes: set[str] = set()
            for key in ("manual_transcripts", "auto_generated_transcripts"):
                for item in transcripts.get(key, []) or []:
                    code = item.get("language_code")
                    if code:
                        language_codes.add(code)

            result: Dict[str, Any] = {
                "video_id": transcripts.get("video_id"),
                "available_languages": sorted(language_codes),
                "common_languages_available": [
                    lang
                    for lang in self.COMMON_LANGUAGES
                    if lang in language_codes
                ],
                "timestamp": datetime.now().isoformat(),
            }

            # Preserve capability errors (e.g., missing list_transcripts).
            if isinstance(transcripts, dict) and transcripts.get("error"):
                result["error"] = transcripts.get("error")

            return self._format_json_response(result)
        except (YouTubeValidationError, YouTubeDataError):
            raise
        except Exception as e:  # pylint: disable=broad-exception-caught
            log_error(
                f"Unexpected error getting transcript languages for {video_url}: {e}"
            )
            raise YouTubeDataError(
                f"Failed to get transcript languages: {e}"
            ) from e

    def extract_youtube_video_id(self, video_url: str) -> str:
        """Extract a YouTube video id from a URL (or accept a raw id)."""
        return self._extract_video_id(video_url)

    def fetch_comprehensive_youtube_video_info(
        self, video_url: str, include_transcript: bool = False
    ) -> str:
        """Combine oEmbed metadata and optional transcript info into one response."""
        try:
            video_id = self._extract_video_id(video_url)

            metadata = json.loads(self.fetch_youtube_video_metadata(video_url))

            result: Dict[str, Any] = {
                "video_id": video_id,
                "video_url": video_url,
                "metadata": metadata,
                "timestamp": datetime.now().isoformat(),
            }

            if include_transcript:
                # languages + best-effort transcript
                try:
                    languages = json.loads(
                        self.fetch_youtube_transcript_languages(video_url)
                    )
                    result["transcript_info"] = {
                        "available_languages": languages.get(
                            "available_languages", []
                        ),
                        "common_languages_available": languages.get(
                            "common_languages_available", []
                        ),
                    }

                    # Fetch English if available, else first available language.
                    preferred: Optional[str] = None
                    available = languages.get("available_languages", []) or []
                    if "en" in available:
                        preferred = "en"
                    elif available:
                        preferred = available[0]

                    if preferred:
                        result["transcript"] = json.loads(
                            self.fetch_youtube_video_transcript(
                                video_url, preferred
                            )
                        )
                except (
                    Exception
                ) as e:  # pylint: disable=broad-exception-caught
                    log_warning(f"Could not add transcript data: {e}")
                    result["transcript_info"] = {"error": str(e)}

            return self._format_json_response(result)

        except (YouTubeValidationError, YouTubeDataError):
            raise
        except Exception as e:  # pylint: disable=broad-exception-caught
            log_error(
                f"Unexpected error getting video info for {video_url}: {e}"
            )
            raise YouTubeDataError(
                f"Failed to get comprehensive video info: {e}"
            ) from e

    def _apply_rate_limit(self) -> None:
        """Apply an inter-request delay."""
        if self.rate_limit_delay <= 0:
            return

        now = time.time()
        elapsed = now - self._last_request_time
        if elapsed < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - elapsed)

        self._last_request_time = time.time()

    def _extract_video_id(self, video_url: str) -> str:
        """Extract a video id from common YouTube URL formats.

        Accepts either:
        - a full URL
        - a scheme-less URL (`youtu.be/<id>`, `youtube.com/watch?v=<id>`)
        - a raw 11-character video id
        """
        if not isinstance(video_url, str) or not video_url.strip():
            raise YouTubeValidationError("Video URL cannot be empty")

        raw = video_url.strip()

        # Accept a raw id.
        if self._looks_like_video_id(raw):
            return raw

        # Ensure urlparse sees netloc for schemeless URLs.
        candidate = raw if "://" in raw else f"https://{raw}"
        parsed = urlparse(candidate)

        host = (parsed.netloc or "").lower()
        path = parsed.path or ""

        # youtu.be/<id>
        if host.endswith("youtu.be"):
            video_id = path.strip("/").split("/")[0]
            if self._looks_like_video_id(video_id):
                return video_id

        # youtube.com/watch?v=<id>
        if "youtube.com" in host:
            if path == "/watch":
                qs = parse_qs(parsed.query or "")
                v = (qs.get("v") or [""])[0]
                if self._looks_like_video_id(v):
                    return v

            # /embed/<id>, /v/<id>, /shorts/<id>
            parts = [p for p in path.split("/") if p]
            if len(parts) >= 2 and parts[0] in {"embed", "v", "shorts"}:
                video_id = parts[1]
                if self._looks_like_video_id(video_id):
                    return video_id

            # Fallback: any query contains v
            qs = parse_qs(parsed.query or "")
            v = (qs.get("v") or [""])[0]
            if self._looks_like_video_id(v):
                return v

        raise YouTubeValidationError(
            f"Could not extract valid video ID from: {video_url}"
        )

    @staticmethod
    def _looks_like_video_id(value: str) -> bool:
        """Return True if value matches the YouTube 11-char id shape."""
        if not isinstance(value, str):
            return False
        if len(value) != 11:
            return False
        return all(c.isalnum() or c in "_-" for c in value)

    def _fetch_oembed_data(self, video_id: str) -> Dict[str, Any]:
        """Fetch metadata from YouTube oEmbed."""
        params = {
            "format": "json",
            "url": f"https://www.youtube.com/watch?v={video_id}",
        }
        url = "https://www.youtube.com/oembed?" + urlencode(params)

        try:
            with urlopen(url, timeout=self.timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as e:
            if e.code == 404:
                raise YouTubeDataError(
                    f"Video not found or unavailable: {video_id}"
                ) from e
            raise YouTubeDataError(
                f"HTTP error {e.code} getting video metadata"
            ) from e
        except URLError as e:
            raise YouTubeDataError(
                f"Network error getting video metadata: {e}"
            ) from e
        except json.JSONDecodeError as e:
            raise YouTubeDataError(
                f"Invalid response format from YouTube API: {e}"
            ) from e
        except Exception as e:  # pylint: disable=broad-exception-caught
            raise YouTubeDataError(
                f"Unexpected error getting video metadata: {e}"
            ) from e

    @staticmethod
    def _enhance_oembed_metadata(
        oembed: Dict[str, Any], video_id: str, video_url: str
    ) -> Dict[str, Any]:
        """Normalize oEmbed response into stable output."""
        return {
            "video_id": video_id,
            "video_url": video_url,
            "title": oembed.get("title", ""),
            "author_name": oembed.get("author_name", ""),
            "author_url": oembed.get("author_url", ""),
            "thumbnail_url": oembed.get("thumbnail_url", ""),
            "provider_name": oembed.get("provider_name", "YouTube"),
            "provider_url": oembed.get(
                "provider_url", "https://www.youtube.com/"
            ),
            "type": oembed.get("type", "video"),
            "width": oembed.get("width"),
            "height": oembed.get("height"),
            "html": oembed.get("html", ""),
            "timestamp": datetime.now().isoformat(),
            "api_source": "YouTube oEmbed",
        }

    def _fetch_transcript_with_retry(
        self, video_id: str, language: str, auto_generated: bool
    ) -> Dict[str, Any]:
        """Fetch transcript with retries.

        Current `youtube-transcript-api` uses an instance-based API:
        - `YouTubeTranscriptApi().list(video_id)`
        - `Transcript.fetch()` returning a `FetchedTranscript`

        This toolkit converts the fetched transcript to a list of dicts.
        """
        last_error: Optional[str] = None

        for attempt in range(1, self.max_retries + 1):
            try:
                ytt = YouTubeTranscriptApi()
                transcript_list = ytt.list(video_id)

                transcript = self._select_transcript(
                    transcript_list=transcript_list,
                    preferred_language=language,
                    allow_generated=auto_generated,
                )

                fetched = transcript.fetch()
                segments = self._normalize_transcript_segments(fetched)

                return {
                    "video_id": video_id,
                    "language": transcript.language,
                    "language_code": transcript.language_code,
                    "is_generated": transcript.is_generated,
                    "is_translatable": bool(
                        getattr(transcript, "is_translatable", False)
                    ),
                    "segments": segments,
                    "transcript_text": self._segments_to_text(segments),
                    "duration_seconds": self._segments_duration_seconds(
                        segments
                    ),
                    "segment_count": len(segments),
                    "timestamp": datetime.now().isoformat(),
                }

            except (TranscriptsDisabled, VideoUnavailable) as e:
                # `TranscriptsDisabled` can be a false-positive on some cloud
                # environments where YouTube blocks or alters responses by IP.
                raise YouTubeDataError(
                    "Transcript unavailable. If this works locally but fails on a "
                    "server/cloud VM, your egress IP may be blocked or challenged by "
                    "YouTube. Try a different egress IP, or use the library's ProxyConfig. "
                    f"Original error: {e}"
                ) from e
            except NoTranscriptFound as e:
                raise YouTubeDataError(
                    f"No transcript found for language '{language}': {e}"
                ) from e
            except Exception as e:  # pylint: disable=broad-exception-caught
                msg = str(e)
                last_error = msg

                is_rate_limited = (
                    "rate" in msg.lower() or "limit" in msg.lower()
                )
                if is_rate_limited and attempt < self.max_retries:
                    backoff = 2 ** (attempt - 1)
                    log_warning(
                        f"Rate limited fetching transcript (attempt {attempt}/{self.max_retries}), "
                        f"sleeping {backoff}s"
                    )
                    time.sleep(backoff)
                    continue

                log_error(
                    f"Transcript fetch failed (attempt {attempt}/{self.max_retries}): {e}"
                )
                if attempt < self.max_retries:
                    time.sleep(1)

        raise YouTubeDataError(
            f"Failed to get transcript after {self.max_retries} attempts: {last_error}"
        )

    @staticmethod
    def _select_transcript(
        transcript_list: Any,
        preferred_language: str,
        allow_generated: bool,
    ) -> Any:
        """Pick a transcript:

        1) Try preferred language.
        2) Fallback to the first allowed transcript.
        """
        try:
            if allow_generated:
                return transcript_list.find_transcript([preferred_language])
            return transcript_list.find_manually_created_transcript(
                [preferred_language]
            )
        except NoTranscriptFound:
            pass

        allowed: List[Any] = []
        for t in transcript_list:
            if allow_generated or not getattr(t, "is_generated", False):
                allowed.append(t)

        if not allowed:
            raise YouTubeDataError("No suitable transcript found")

        fallback = allowed[0]
        log_warning(
            f"Requested language '{preferred_language}' not found; "
            f"using '{fallback.language_code}'"
        )
        return fallback

    @staticmethod
    def _normalize_transcript_segments(segments: Any) -> List[Dict[str, Any]]:
        """Return transcript segments as a `list[dict]`.

        `youtube-transcript-api` v1+ returns a `FetchedTranscript` object; older
        variants often return a `list[dict]`.
        """
        to_raw_data = getattr(segments, "to_raw_data", None)
        if callable(to_raw_data):
            try:
                raw = to_raw_data()
                if isinstance(raw, list):
                    return [item for item in raw if isinstance(item, dict)]
            except Exception:  # pylint: disable=broad-exception-caught
                return []

        if not isinstance(segments, list):
            return []

        return [item for item in segments if isinstance(item, dict)]

    @staticmethod
    def _segments_to_text(segments: List[Dict[str, Any]]) -> str:
        """Join segment `text` fields into one string."""
        return " ".join(
            [(seg.get("text") or "").strip() for seg in segments]
        ).strip()

    @staticmethod
    def _segments_duration_seconds(segments: List[Dict[str, Any]]) -> float:
        """Compute max(start + duration) over segments."""
        end_times: List[float] = []
        for seg in segments:
            try:
                start = float(seg.get("start") or 0.0)
                dur = float(seg.get("duration") or 0.0)
                end_times.append(start + dur)
            except (TypeError, ValueError):
                continue

        return max(end_times) if end_times else 0.0

    @staticmethod
    def _format_json_response(data: Any) -> str:
        """Format response data as JSON."""
        try:
            return json.dumps(data, indent=2, ensure_ascii=False, default=str)
        except Exception as e:  # pylint: disable=broad-exception-caught
            log_error(f"Error formatting JSON response: {e}")
            return json.dumps({"error": f"Failed to format response: {e}"})

    @staticmethod
    def get_llm_usage_instructions() -> str:
        """Return short, text-first usage instructions for the YouTube tools."""
        return """
<youtube_tools>
YouTube metadata (oEmbed) + transcripts.
All tools return JSON strings.

Tools:
- fetch_youtube_video_metadata(video_url)
  - oEmbed fields only (title/author/thumbnail/embed_html); no view counts/likes/duration.
- extract_youtube_video_id(video_url)
- fetch_comprehensive_youtube_video_info(video_url, include_transcript=False)

Transcript tools:
- fetch_youtube_video_transcript(video_url, language='en', auto_generated=True)
- fetch_available_youtube_transcripts(video_url)
- fetch_youtube_transcript_languages(video_url)

Notes:
- If transcripts work locally but fail on a server/cloud VM with TranscriptsDisabled,
  YouTube may be blocking/challenging that egress IP.

Suggested workflow:
1) fetch_youtube_video_metadata(url)
2) fetch_youtube_transcript_languages(url)
3) fetch_youtube_video_transcript(url, language='en')
</youtube_tools>
"""
