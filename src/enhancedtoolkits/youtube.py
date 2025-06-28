"""
Enhanced YouTube Tools v2.0

A production-ready YouTube toolkit that provides:
- Comprehensive video metadata retrieval
- Robust transcript fetching with language support
- Enhanced error handling and validation
- URL format validation and normalization
- Rate limiting and retry logic
- Multiple transcript language support
- Video duration and statistics parsing

Author: malvavisc0
License: MIT
Version: 2.0.0
"""

import json
import re
import time
from datetime import datetime
from typing import Any, Dict
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

from agno.utils.log import log_debug, log_error, log_info, log_warning

from .base import StrictToolkit

# Optional youtube-transcript-api import
try:
    from youtube_transcript_api import YouTubeTranscriptApi  # type: ignore
    from youtube_transcript_api._errors import (
        NoTranscriptFound,
        TranscriptsDisabled,
        VideoUnavailable,
    )

    TRANSCRIPT_API_AVAILABLE = True
except ImportError:
    TRANSCRIPT_API_AVAILABLE = False
    YouTubeTranscriptApi = None
    TranscriptsDisabled = Exception
    NoTranscriptFound = Exception
    VideoUnavailable = Exception
    log_warning(
        "youtube-transcript-api not available. Transcript functionality will be limited."
    )


class YouTubeError(Exception):
    """Custom exception for YouTube-related errors."""

    pass


class YouTubeValidationError(YouTubeError):
    """Exception for input validation errors."""

    pass


class YouTubeDataError(YouTubeError):
    """Exception for data retrieval errors."""

    pass


class EnhancedYouTubeTools(StrictToolkit):
    """
    Enhanced YouTube Tools v2.0

    A production-ready YouTube toolkit with comprehensive error handling,
    input validation, transcript support, and enhanced metadata extraction.
    """

    # YouTube URL patterns for validation
    YOUTUBE_URL_PATTERNS = [
        r"(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})",
        r"(?:https?://)?(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]{11})",
        r"(?:https?://)?(?:www\.)?youtube\.com/v/([a-zA-Z0-9_-]{11})",
        r"(?:https?://)?youtu\.be/([a-zA-Z0-9_-]{11})",
        r"(?:https?://)?(?:www\.)?youtube\.com/watch\?.*v=([a-zA-Z0-9_-]{11})",
    ]

    # Common transcript languages
    COMMON_LANGUAGES = [
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
        rate_limit_delay: float = 0.5,  # 500ms between requests
        timeout: int = 30,
        max_retries: int = 3,
        **kwargs,
    ):
        """
        Initialize Enhanced YouTube Tools.

        Args:
            rate_limit_delay: Delay between API requests in seconds
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
        """
        self.add_instructions = True
        self.instructions = EnhancedYouTubeTools.get_llm_usage_instructions()

        super().__init__(name="enhanced_youtube_tools", **kwargs)

        # Configuration
        self.rate_limit_delay = max(0.1, min(5.0, rate_limit_delay))
        self.timeout = max(5, min(120, timeout))
        self.max_retries = max(1, min(10, max_retries))
        self.last_request_time = 0.0

        # Register methods
        self.register(self.fetch_youtube_video_metadata)
        self.register(self.fetch_youtube_video_transcript)
        self.register(self.extract_youtube_video_id)
        self.register(self.fetch_comprehensive_youtube_video_info)

        # Register backward compatibility methods
        self.register(self.legacy_fetch_youtube_video_metadata)
        self.register(self.legacy_fetch_youtube_video_transcript)

        if TRANSCRIPT_API_AVAILABLE:
            self.register(self.fetch_available_youtube_transcripts)
            self.register(self.fetch_youtube_transcript_languages)

        log_info(
            f"Enhanced YouTube Tools initialized - Rate Limit: {rate_limit_delay}s, Timeout: {timeout}s, Transcript API: {TRANSCRIPT_API_AVAILABLE}"
        )

    def fetch_youtube_video_metadata(self, video_url: str) -> str:
        """
        Retrieve comprehensive metadata for a YouTube video.

        Args:
            video_url: The URL of the YouTube video

        Returns:
            JSON string containing video metadata

        Raises:
            YouTubeValidationError: If URL is invalid
            YouTubeDataError: If metadata cannot be retrieved
        """
        try:
            video_id = self._extract_video_id(video_url)
            log_debug(f"Getting metadata for video: {video_id}")

            # Apply rate limiting
            self._apply_rate_limit()

            # Get metadata from YouTube oEmbed API
            metadata = self._fetch_oembed_data(video_id)

            # Enhance metadata with additional information
            enhanced_metadata = self._enhance_metadata(metadata, video_id, video_url)

            return self._format_json_response(enhanced_metadata)

        except (YouTubeValidationError, YouTubeDataError):
            raise
        except Exception as e:
            log_error(f"Unexpected error getting metadata for {video_url}: {e}")
            raise YouTubeDataError(f"Failed to get video metadata: {e}")

    def fetch_youtube_video_transcript(
        self, video_url: str, language: str = "en", auto_generated: bool = True
    ) -> str:
        """
        Retrieve transcript for a YouTube video with language support.

        Args:
            video_url: The URL of the YouTube video
            language: Preferred language code (e.g., 'en', 'es', 'fr')
            auto_generated: Whether to include auto-generated transcripts

        Returns:
            JSON string containing transcript data

        Raises:
            YouTubeValidationError: If URL is invalid
            YouTubeDataError: If transcript cannot be retrieved
        """
        try:
            if not TRANSCRIPT_API_AVAILABLE:
                raise YouTubeDataError(
                    "Transcript API not available. Install youtube-transcript-api package."
                )

            video_id = self._extract_video_id(video_url)
            log_debug(f"Getting transcript for video: {video_id} (language: {language})")

            # Apply rate limiting
            self._apply_rate_limit()

            # Get transcript with retry logic
            transcript_data = self._fetch_transcript_with_retry(
                video_id, language, auto_generated
            )

            return self._format_json_response(transcript_data)

        except (YouTubeValidationError, YouTubeDataError):
            raise
        except Exception as e:
            log_error(f"Unexpected error getting transcript for {video_url}: {e}")
            raise YouTubeDataError(f"Failed to get video transcript: {e}")

    def fetch_available_youtube_transcripts(self, video_url: str) -> str:
        """
        Get list of available transcript languages for a video.

        Args:
            video_url: The URL of the YouTube video

        Returns:
            JSON string containing available transcript languages

        Raises:
            YouTubeValidationError: If URL is invalid
            YouTubeDataError: If transcript info cannot be retrieved
        """
        try:
            if not TRANSCRIPT_API_AVAILABLE:
                raise YouTubeDataError(
                    "Transcript API not available. Install youtube-transcript-api package."
                )

            video_id = self._extract_video_id(video_url)
            log_debug(f"Getting available transcripts for video: {video_id}")

            # Apply rate limiting
            self._apply_rate_limit()

            try:
                if not TRANSCRIPT_API_AVAILABLE or YouTubeTranscriptApi is None:
                    raise YouTubeDataError("Transcript API not available")
                transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

                available_transcripts = {
                    "video_id": video_id,
                    "manual_transcripts": [],
                    "auto_generated_transcripts": [],
                    "translatable_transcripts": [],
                }

                for transcript in transcript_list:
                    transcript_info = {
                        "language": transcript.language,
                        "language_code": transcript.language_code,
                        "is_generated": transcript.is_generated,
                        "is_translatable": transcript.is_translatable,
                    }

                    if transcript.is_generated:
                        available_transcripts["auto_generated_transcripts"].append(
                            transcript_info
                        )
                    else:
                        available_transcripts["manual_transcripts"].append(
                            transcript_info
                        )

                    if transcript.is_translatable:
                        available_transcripts["translatable_transcripts"].append(
                            transcript_info
                        )

                available_transcripts["timestamp"] = datetime.now().isoformat()
                return self._format_json_response(available_transcripts)

            except (TranscriptsDisabled, NoTranscriptFound) as e:
                return self._format_json_response(
                    {
                        "video_id": video_id,
                        "available_transcripts": [],
                        "message": f"No transcripts available: {e}",
                        "timestamp": datetime.now().isoformat(),
                    }
                )

        except (YouTubeValidationError, YouTubeDataError):
            raise
        except Exception as e:
            log_error(
                f"Unexpected error getting available transcripts for {video_url}: {e}"
            )
            raise YouTubeDataError(f"Failed to get available transcripts: {e}")

    def fetch_youtube_transcript_languages(self, video_url: str) -> str:
        """
        Get simplified list of available transcript language codes.

        Args:
            video_url: The URL of the YouTube video

        Returns:
            JSON string containing language codes

        Raises:
            YouTubeValidationError: If URL is invalid
            YouTubeDataError: If language info cannot be retrieved
        """
        try:
            transcripts_data = self.fetch_available_youtube_transcripts(video_url)
            transcripts = json.loads(transcripts_data)

            language_codes = set()

            # Collect all language codes
            for transcript_type in ["manual_transcripts", "auto_generated_transcripts"]:
                for transcript in transcripts.get(transcript_type, []):
                    language_codes.add(transcript["language_code"])

            result = {
                "video_id": transcripts.get("video_id"),
                "available_languages": sorted(list(language_codes)),
                "common_languages_available": [
                    lang for lang in self.COMMON_LANGUAGES if lang in language_codes
                ],
                "timestamp": datetime.now().isoformat(),
            }

            return self._format_json_response(result)

        except (YouTubeValidationError, YouTubeDataError):
            raise
        except Exception as e:
            log_error(
                f"Unexpected error getting transcript languages for {video_url}: {e}"
            )
            raise YouTubeDataError(f"Failed to get transcript languages: {e}")

    def extract_youtube_video_id(self, video_url: str) -> str:
        """
        Extract video ID from YouTube URL (public method).

        Args:
            video_url: The URL of the YouTube video

        Returns:
            Video ID string

        Raises:
            YouTubeValidationError: If URL is invalid or video ID cannot be extracted
        """
        return self._extract_video_id(video_url)

    def fetch_comprehensive_youtube_video_info(self, video_url: str, include_transcript: bool = False) -> str:
        """
        Get comprehensive video information including metadata and optionally transcript.

        Args:
            video_url: The URL of the YouTube video
            include_transcript: Whether to include transcript data

        Returns:
            JSON string containing comprehensive video information

        Raises:
            YouTubeValidationError: If URL is invalid
            YouTubeDataError: If video info cannot be retrieved
        """
        try:
            video_id = self._extract_video_id(video_url)
            log_debug(f"Getting comprehensive info for video: {video_id}")

            # Get metadata
            metadata_str = self.fetch_youtube_video_metadata(video_url)
            metadata = json.loads(metadata_str)

            comprehensive_info = {
                "video_id": video_id,
                "video_url": video_url,
                "metadata": metadata,
                "timestamp": datetime.now().isoformat(),
            }

            # Add transcript info if requested and available
            if include_transcript and TRANSCRIPT_API_AVAILABLE:
                try:
                    # Get available languages first
                    languages_str = self.fetch_youtube_transcript_languages(video_url)
                    languages_data = json.loads(languages_str)

                    comprehensive_info["transcript_info"] = {
                        "available_languages": languages_data.get(
                            "available_languages", []
                        ),
                        "common_languages_available": languages_data.get(
                            "common_languages_available", []
                        ),
                    }

                    # Try to get English transcript if available
                    if "en" in languages_data.get("available_languages", []):
                        try:
                            transcript_str = self.fetch_youtube_video_transcript(video_url, "en")
                            transcript_data = json.loads(transcript_str)
                            comprehensive_info["transcript"] = transcript_data
                        except Exception as e:
                            log_warning(f"Could not get English transcript: {e}")
                            comprehensive_info["transcript_error"] = str(e)

                except Exception as e:
                    log_warning(f"Could not get transcript info: {e}")
                    comprehensive_info["transcript_info"] = {"error": str(e)}

            return self._format_json_response(comprehensive_info)

        except (YouTubeValidationError, YouTubeDataError):
            raise
        except Exception as e:
            log_error(f"Unexpected error getting video info for {video_url}: {e}")
            raise YouTubeDataError(f"Failed to get comprehensive video info: {e}")

    # Backward compatibility methods

    def legacy_fetch_youtube_video_metadata(self, video_url: str) -> str:
        """
        Legacy method for backward compatibility.
        Use fetch_youtube_video_metadata() instead.
        """
        return self.fetch_youtube_video_metadata(video_url)

    def legacy_fetch_youtube_video_transcript(self, video_url: str) -> str:
        """
        Legacy method for backward compatibility.
        Use fetch_youtube_video_transcript() instead.
        """
        try:
            transcript_data_str = self.fetch_youtube_video_transcript(video_url)
            transcript_data = json.loads(transcript_data_str)

            # Return just the text for backward compatibility
            if "transcript_text" in transcript_data:
                return transcript_data["transcript_text"]
            elif "segments" in transcript_data:
                return " ".join(
                    [segment.get("text", "") for segment in transcript_data["segments"]]
                )
            else:
                return "No transcript text available"

        except Exception as e:
            raise Exception(f"Error getting video transcript: {e}")

    def legacy_extract_youtube_video_id(self, youtube_url: str) -> str:
        """
        Legacy method for backward compatibility.
        Use extract_youtube_video_id() instead.
        """
        return self._extract_video_id(youtube_url)

    # Private helper methods

    def _extract_video_id(self, video_url: str) -> str:
        """
        Extract video ID from various YouTube URL formats.

        Args:
            video_url: YouTube video URL

        Returns:
            Video ID string

        Raises:
            YouTubeValidationError: If URL is invalid or video ID cannot be extracted
        """
        if not video_url or not isinstance(video_url, str):
            raise YouTubeValidationError("Video URL cannot be empty")

        video_url = video_url.strip()

        # Try each pattern
        for pattern in self.YOUTUBE_URL_PATTERNS:
            match = re.search(pattern, video_url)
            if match:
                video_id = match.group(1)
                # Validate video ID format
                if re.match(r"^[a-zA-Z0-9_-]{11}$", video_id):
                    return video_id

        raise YouTubeValidationError(
            f"Could not extract valid video ID from URL: {video_url}"
        )

    def _apply_rate_limit(self) -> None:
        """Apply rate limiting between API requests."""
        if self.rate_limit_delay > 0:
            current_time = time.time()
            time_since_last = current_time - self.last_request_time
            if time_since_last < self.rate_limit_delay:
                sleep_time = self.rate_limit_delay - time_since_last
                time.sleep(sleep_time)
            self.last_request_time = time.time()

    def _fetch_oembed_data(self, video_id: str) -> Dict[str, Any]:
        """
        Fetch metadata from YouTube oEmbed API.

        Args:
            video_id: YouTube video ID

        Returns:
            Metadata dictionary

        Raises:
            YouTubeDataError: If metadata cannot be retrieved
        """
        try:
            params = {
                "format": "json",
                "url": f"https://www.youtube.com/watch?v={video_id}",
            }
            url = "https://www.youtube.com/oembed?" + urlencode(params)

            with urlopen(url, timeout=self.timeout) as response:
                response_text = response.read()
                return json.loads(response_text.decode())

        except HTTPError as e:
            if e.code == 404:
                raise YouTubeDataError(f"Video not found or unavailable: {video_id}")
            else:
                raise YouTubeDataError(f"HTTP error {e.code} getting video metadata")
        except URLError as e:
            raise YouTubeDataError(f"Network error getting video metadata: {e}")
        except json.JSONDecodeError as e:
            raise YouTubeDataError(f"Invalid response format from YouTube API: {e}")
        except Exception as e:
            raise YouTubeDataError(f"Unexpected error getting video metadata: {e}")

    def _enhance_metadata(
        self, metadata: Dict[str, Any], video_id: str, video_url: str
    ) -> Dict[str, Any]:
        """
        Enhance basic metadata with additional information.

        Args:
            metadata: Basic metadata from oEmbed
            video_id: Video ID
            video_url: Original video URL

        Returns:
            Enhanced metadata dictionary
        """
        enhanced = {
            "video_id": video_id,
            "video_url": video_url,
            "title": metadata.get("title", "Unknown Title"),
            "author_name": metadata.get("author_name", "Unknown Author"),
            "author_url": metadata.get("author_url", ""),
            "thumbnail_url": metadata.get("thumbnail_url", ""),
            "provider_name": metadata.get("provider_name", "YouTube"),
            "provider_url": metadata.get("provider_url", "https://www.youtube.com/"),
            "type": metadata.get("type", "video"),
            "width": metadata.get("width"),
            "height": metadata.get("height"),
            "html": metadata.get("html", ""),
            "timestamp": datetime.now().isoformat(),
            "api_source": "YouTube oEmbed",
        }

        return enhanced

    def _fetch_transcript_with_retry(
        self, video_id: str, language: str, auto_generated: bool
    ) -> Dict[str, Any]:
        """
        Fetch transcript with retry logic and error handling.

        Args:
            video_id: YouTube video ID
            language: Language code
            auto_generated: Include auto-generated transcripts

        Returns:
            Transcript data dictionary

        Raises:
            YouTubeDataError: If transcript cannot be retrieved
        """
        last_error = None

        for attempt in range(self.max_retries):
            try:
                # Get transcript list
                if not TRANSCRIPT_API_AVAILABLE or YouTubeTranscriptApi is None:
                    raise YouTubeDataError("Transcript API not available")
                transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

                # Try to find requested language
                transcript = None
                try:
                    transcript = transcript_list.find_transcript([language])
                except NoTranscriptFound:
                    # Try to find any available transcript
                    available_transcripts = []
                    for t in transcript_list:
                        if auto_generated or not t.is_generated:
                            available_transcripts.append(t)

                    if available_transcripts:
                        transcript = available_transcripts[0]
                        log_warning(
                            f"Requested language '{language}' not found, using '{transcript.language_code}'"
                        )

                if not transcript:
                    raise YouTubeDataError(
                        f"No suitable transcript found for video {video_id}"
                    )

                # Fetch transcript data
                transcript_data = transcript.fetch()

                # Process transcript
                processed_transcript = {
                    "video_id": video_id,
                    "language": transcript.language,
                    "language_code": transcript.language_code,
                    "is_generated": transcript.is_generated,
                    "is_translatable": transcript.is_translatable,
                    "segments": transcript_data,
                    "transcript_text": " ".join(
                        [getattr(entry, "text", "") for entry in transcript_data]
                    ),
                    "duration_seconds": (
                        max(
                            [
                                getattr(entry, "start", 0) + getattr(entry, "duration", 0)
                                for entry in transcript_data
                            ]
                        )
                        if transcript_data
                        else 0
                    ),
                    "segment_count": len(transcript_data),
                    "timestamp": datetime.now().isoformat(),
                }

                return processed_transcript

            except (TranscriptsDisabled, VideoUnavailable) as e:
                raise YouTubeDataError(f"Transcript unavailable: {e}")
            except NoTranscriptFound as e:
                raise YouTubeDataError(
                    f"No transcript found for language '{language}': {e}"
                )
            except Exception as e:
                # Handle rate limiting or other API errors
                if "rate" in str(e).lower() or "limit" in str(e).lower():
                    last_error = (
                        f"Rate limited (attempt {attempt + 1}/{self.max_retries})"
                    )
                    log_warning(last_error)
                    if attempt < self.max_retries - 1:
                        time.sleep(2**attempt)  # Exponential backoff
                        continue
                # Handle other exceptions
                last_error = f"Transcript fetch failed: {e}"
                log_error(last_error)
                if attempt < self.max_retries - 1:
                    time.sleep(1)

        raise YouTubeDataError(
            f"Failed to get transcript after {self.max_retries} attempts: {last_error}"
        )

    def _format_json_response(self, data: Any) -> str:
        """
        Format response data as clean JSON string.

        Args:
            data: Data to format

        Returns:
            Clean JSON string
        """
        try:
            return json.dumps(data, indent=2, ensure_ascii=False, default=str)
        except Exception as e:
            log_error(f"Error formatting JSON response: {e}")
            return json.dumps({"error": f"Failed to format response: {e}"})

    @staticmethod
    def get_llm_usage_instructions() -> str:
        """
        Returns a set of detailed instructions for LLMs on how to use each tool in EnhancedYouTubeTools.
        Each instruction includes the method name, description, parameters, types, and example values.
        """
        instructions = """
<youtube_tools_instructions>
*** YouTube Tools Instructions ***

By leveraging the following set of tools, you can retrieve comprehensive metadata, transcripts, and video information from YouTube. These tools empower you to deliver accurate, real-time video intelligence and content extraction with ease. Here are the detailed instructions for using the set of tools:

- Use fetch_youtube_video_metadata to retrieve metadata for a YouTube video.
   Parameters:
      - video_url (str): The URL of the YouTube video, e.g., "https://www.youtube.com/watch?v=dQw4w9WgXcQ".

- Use fetch_youtube_video_transcript to retrieve the transcript for a YouTube video (requires youtube-transcript-api).
   Parameters:
      - video_url (str): The URL of the YouTube video, e.g., "https://youtu.be/dQw4w9WgXcQ".
      - language (str, optional): Preferred language code, e.g., "en", "es", "fr" (default: "en").
      - auto_generated (bool, optional): Whether to include auto-generated transcripts (default: True).

- Use fetch_available_youtube_transcripts to list available transcript languages for a video (requires youtube-transcript-api).
   Parameters:
      - video_url (str): The URL of the YouTube video.

- Use fetch_youtube_transcript_languages to get a simplified list of available transcript language codes (requires youtube-transcript-api).
   Parameters:
      - video_url (str): The URL of the YouTube video.

- Use extract_youtube_video_id to extract the video ID from a YouTube URL.
   Parameters:
      - video_url (str): The URL of the YouTube video.

- Use fetch_comprehensive_youtube_video_info to get comprehensive video information, including metadata and optionally transcript.
   Parameters:
      - video_url (str): The URL of the YouTube video.
      - include_transcript (bool, optional): Whether to include transcript data (default: False).

- Use legacy_fetch_youtube_video_metadata for backward compatibility (same as fetch_youtube_video_metadata).
   Parameters:
      - video_url (str): The URL of the YouTube video.

- Use legacy_fetch_youtube_video_transcript for backward compatibility (same as fetch_youtube_video_transcript).
   Parameters:
      - video_url (str): The URL of the YouTube video.

Notes:
- Transcript-related tools (fetch_youtube_video_transcript, fetch_available_youtube_transcripts, fetch_youtube_transcript_languages) require the youtube-transcript-api package to be installed.
- The language parameter for transcripts should be a valid language code, e.g., "en" for English, "es" for Spanish.
- The auto_generated parameter controls whether to include auto-generated transcripts.
</youtube_tools_instructions>
"""
        return instructions
