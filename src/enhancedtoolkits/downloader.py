"""
URL Content Downloader Tool v1.1

A production-ready URL content downloading toolkit that provides:
- Universal file downloading with BYPARR integration
- Anti-bot bypass mechanisms
- Smart content processing (MarkItDown for HTML, binary handling for files)
- Robust error handling and logging
- Input validation and sanitization
- Configurable timeouts and retry logic
- Multiple output formats support

Author: Assistant
License: MIT
Version: 1.1.0
"""

import json
import mimetypes
import os
import random
import tempfile
import time
from typing import Dict, List, Optional, Union
from urllib.parse import urlparse

import httpx
from agno.utils.log import log_debug, log_error, log_info, log_warning

from .base import StrictToolkit

# BYPARR configuration
BYPARR_URL = os.environ.get("BYPARR_URL", "http://byparr:8191/v1")
BYPARR_TIMEOUT = int(os.environ.get("BYPARR_TIMEOUT", "60"))
BYPARR_ENABLED = os.environ.get("BYPARR_ENABLED", "false").lower() == "true"

# URL Downloader configuration
URL_DOWNLOADER_MAX_RETRIES = int(os.environ.get("URL_DOWNLOADER_MAX_RETRIES", "3"))
URL_DOWNLOADER_TIMEOUT = int(os.environ.get("URL_DOWNLOADER_TIMEOUT", "30"))

# Optional MarkItDown import
try:
    from markitdown import MarkItDown

    MARKITDOWN_AVAILABLE = True
    markitdown_converter = MarkItDown()
except ImportError:
    MARKITDOWN_AVAILABLE = False
    markitdown_converter = None
    log_warning("MarkItDown not available. Content parsing will be limited.")


class URLDownloadError(Exception):
    """Custom exception for URL download errors."""

    pass


class AntiBotDetectedError(Exception):
    """Custom exception for anti-bot detection."""

    pass


class ContentParsingError(Exception):
    """Custom exception for content parsing errors."""

    pass


class URLContentDownloader(StrictToolkit):
    """
    URL Content Downloader Tool v1.1

    A production-ready universal file downloading toolkit with BYPARR integration,
    anti-bot bypass capabilities, and smart content processing for any file type.
    """

    # Common user agents for rotation
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    ]

    # Supported output formats
    SUPPORTED_FORMATS = ["markdown", "text", "html", "binary", "auto"]

    # File types that should be processed with MarkItDown
    HTML_CONTENT_TYPES = [
        "text/html",
        "application/xhtml+xml",
        "text/xml",
        "application/xml",
    ]

    # Binary file types that should be saved as-is
    BINARY_CONTENT_TYPES = [
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/vnd.ms-powerpoint",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        "image/",
        "video/",
        "audio/",
        "application/zip",
        "application/x-rar-compressed",
        "application/x-7z-compressed",
        "application/octet-stream",
    ]

    def __init__(
        self,
        byparr_enabled: Optional[bool] = None,
        max_retries: int = URL_DOWNLOADER_MAX_RETRIES,
        timeout: int = URL_DOWNLOADER_TIMEOUT,
        user_agent_rotation: bool = True,
        enable_caching: bool = False,
        add_instructions: bool = True,
        **kwargs,
    ):
        """
        Initialize URL Content Downloader.

        Args:
            byparr_enabled: Whether to use BYPARR service (None = auto-detect)
            max_retries: Maximum number of retry attempts
            timeout: Request timeout in seconds
            user_agent_rotation: Whether to rotate user agents
            enable_caching: Whether to cache downloaded content
            add_instructions: Whether to add LLM usage instructions
        """
        # Configuration
        self.max_retries = max(1, min(10, max_retries))
        self.timeout = max(5, min(300, timeout))
        self.user_agent_rotation = user_agent_rotation
        self.enable_caching = enable_caching
        self.add_instructions = add_instructions
        self.instructions = URLContentDownloader.get_llm_usage_instructions()

        super().__init__(name="url_content_downloader", **kwargs)

        # BYPARR configuration
        if byparr_enabled is not None:
            self.byparr_enabled = byparr_enabled
        else:
            self.byparr_enabled = BYPARR_ENABLED

        # HTTP client configuration
        self.client = httpx.Client(
            timeout=httpx.Timeout(self.timeout),
            follow_redirects=True,
            headers=self._get_default_headers(),
        )

        # Simple cache for downloaded content
        self.content_cache = {} if enable_caching else None

        # Register methods
        self.register(self.access_website_content)
        self.register(self.get_file_from_url)
        self.register(self.download_multiple_urls)
        self.register(self.get_url_metadata)
        self.register(self.check_url_accessibility)

        log_info(
            f"URL Content Downloader initialized - BYPARR: {self.byparr_enabled}, "
            f"Max Retries: {self.max_retries}, Timeout: {self.timeout}s"
        )

    def access_website_content(self, url: str, output: str = "auto") -> str:
        """
        Access, download and parse Website content using URL with anti-bot bypass.
        Automatically detects content type and applies appropriate processing.

        Args:
            url: URL to download content from
            output: Output format ("auto", "markdown", "text", "html", or "binary")

        Returns:
            Parsed content in the specified format

        Raises:
            URLDownloadError: If download fails
            ContentParsingError: If content parsing fails
        """
        return self.get_file_from_url(url, output)

    def get_file_from_url(self, url: str, output: str = "auto") -> str:
        """
        Download any file from a URL with smart content processing.
        Uses MarkItDown for HTML content, handles binary files appropriately.

        Args:
            url: URL to download file from
            output: Output format ("auto", "markdown", "text", "html", or "binary")

        Returns:
            Processed content or file information

        Raises:
            URLDownloadError: If download fails
            ContentParsingError: If content parsing fails
        """
        try:
            # Validate inputs
            validated_url = self._validate_url(url)
            validated_format = self._validate_format(output)

            log_debug(f"Downloading file from: {validated_url}")

            # Check cache first
            cache_key = f"{validated_url}:{validated_format}"
            if self.content_cache and cache_key in self.content_cache:
                log_debug(f"Using cached content for: {validated_url}")
                return self.content_cache[cache_key]

            # Try BYPARR first if enabled
            response_data = None
            content_type = None

            if self.byparr_enabled:
                try:
                    byparr_result = self._fetch_content_with_byparr(validated_url)
                    if byparr_result:
                        response_data = byparr_result
                        content_type = "text/html"  # BYPARR typically returns HTML
                        log_info(
                            f"Successfully fetched content via BYPARR: {validated_url}"
                        )
                except Exception as e:
                    log_warning(
                        f"BYPARR failed for {url}: {e}, falling back to direct fetch"
                    )

            # Fallback to direct fetch with anti-bot bypass
            if not response_data:
                response_data, content_type = self._fetch_file_with_antibot(validated_url)
                log_info(f"Successfully fetched file via direct fetch: {validated_url}")

            # Process content based on type and format
            processed_content = self._process_file_content(
                response_data,
                content_type or "application/octet-stream",
                validated_format,
                validated_url,
            )

            # Cache the processed content
            if self.content_cache:
                self.content_cache[cache_key] = processed_content

            log_info(
                f"File download completed: {len(str(processed_content))} characters/bytes"
            )
            return processed_content

        except (URLDownloadError, ContentParsingError):
            raise
        except Exception as e:
            log_error(f"Unexpected error downloading {url}: {e}")
            raise URLDownloadError(f"Failed to download file from {url}: {e}")

    def download_multiple_urls(self, urls: List[str], format: str = "markdown") -> str:
        """
        Download content from multiple URLs.

        Args:
            urls: List of URLs to download
            format: Output format for all URLs

        Returns:
            JSON string containing results for all URLs
        """
        if not urls:
            raise URLDownloadError("URL list cannot be empty")

        if len(urls) > 10:
            log_warning(f"Large URL list ({len(urls)} URLs), limiting to first 10")
            urls = urls[:10]

        results = []
        for i, url in enumerate(urls):
            try:
                content = self.access_website_content(url, format)
                results.append(
                    {"url": url, "success": True, "content": content, "error": None}
                )
                log_debug(f"Successfully downloaded {i+1}/{len(urls)}: {url}")
            except Exception as e:
                results.append(
                    {"url": url, "success": False, "content": None, "error": str(e)}
                )
                log_warning(f"Failed to download {i+1}/{len(urls)}: {url} - {e}")

        return json.dumps(results, indent=2, ensure_ascii=False)

    def get_url_metadata(self, url: str) -> str:
        """
        Extract metadata from a URL without downloading full content.

        Args:
            url: URL to extract metadata from

        Returns:
            JSON string containing URL metadata
        """
        try:
            validated_url = self._validate_url(url)

            # Make HEAD request to get metadata
            response = self.client.head(validated_url)
            response.raise_for_status()

            metadata = {
                "url": validated_url,
                "status_code": response.status_code,
                "content_type": response.headers.get("content-type", ""),
                "content_length": response.headers.get("content-length"),
                "last_modified": response.headers.get("last-modified"),
                "server": response.headers.get("server", ""),
                "accessible": True,
            }

            return json.dumps(metadata, indent=2)

        except Exception as e:
            log_error(f"Error getting metadata for {url}: {e}")
            return json.dumps(
                {"url": url, "accessible": False, "error": str(e)}, indent=2
            )

    def check_url_accessibility(self, url: str) -> str:
        """
        Check if a URL is accessible without downloading content.

        Args:
            url: URL to check

        Returns:
            JSON string with accessibility status
        """
        try:
            validated_url = self._validate_url(url)

            response = self.client.head(validated_url)
            response.raise_for_status()

            result = {
                "url": validated_url,
                "accessible": True,
                "status_code": response.status_code,
                "response_time_ms": int(response.elapsed.total_seconds() * 1000),
            }

        except Exception as e:
            result = {
                "url": url,
                "accessible": False,
                "error": str(e),
                "response_time_ms": None,
            }

        return json.dumps(result, indent=2)

    def _fetch_content_with_byparr(self, url: str) -> Optional[str]:
        """
        Fetch content using BYPARR service (anti-bot bypass).
        """
        if not self.byparr_enabled:
            return None

        try:
            response = self.client.post(
                url=BYPARR_URL,
                headers={"Content-Type": "application/json"},
                json={
                    "cmd": "request.get",
                    "url": url,
                    "maxTimeout": BYPARR_TIMEOUT,
                },
                timeout=httpx.Timeout(BYPARR_TIMEOUT + 10),
            )
            response.raise_for_status()

            solution = response.json()
            if "solution" not in solution:
                return None

            raw_html = solution["solution"]["response"]
            return raw_html

        except Exception as e:
            log_debug(f"BYPARR request failed: {e}")
            return None

    def _fetch_content_with_antibot(self, url: str) -> str:
        """
        Fetch content with anti-bot bypass techniques.
        """
        last_error = None

        for attempt in range(self.max_retries):
            try:
                # Apply anti-bot techniques
                headers = self._get_antibot_headers()

                # Add random delay between attempts
                if attempt > 0:
                    delay = min(2**attempt, 10) + random.uniform(0, 1)
                    log_debug(f"Waiting {delay:.1f}s before retry {attempt + 1}")
                    time.sleep(delay)

                response = self.client.get(url, headers=headers)
                response.raise_for_status()

                # Check for anti-bot indicators
                if self._detect_antibot_response(response):
                    raise AntiBotDetectedError("Anti-bot system detected")

                content_type = response.headers.get("content-type", "").lower()
                if "text/html" not in content_type and "text/plain" not in content_type:
                    log_warning(f"Unexpected content type: {content_type}")

                return response.text

            except httpx.TimeoutException as e:
                last_error = f"Request timeout (attempt {attempt + 1}/{self.max_retries})"
                log_warning(last_error)
            except httpx.HTTPStatusError as e:
                last_error = f"HTTP error {e.response.status_code}"
                log_warning(last_error)
                if e.response.status_code in [403, 429]:  # Likely anti-bot
                    continue
                else:
                    break  # Don't retry other HTTP errors
            except AntiBotDetectedError as e:
                last_error = (
                    f"Anti-bot detected (attempt {attempt + 1}/{self.max_retries})"
                )
                log_warning(last_error)
            except Exception as e:
                last_error = f"Request failed: {e}"
                log_error(last_error)
                break

        raise URLDownloadError(
            f"Failed to fetch content after {self.max_retries} attempts: {last_error}"
        )

    def _fetch_file_with_antibot(self, url: str) -> tuple[Union[str, bytes], str]:
        """
        Fetch any file with anti-bot bypass techniques.
        Returns tuple of (content, content_type).
        """
        last_error = None

        for attempt in range(self.max_retries):
            try:
                # Apply anti-bot techniques
                headers = self._get_antibot_headers()

                # Add random delay between attempts
                if attempt > 0:
                    delay = min(2**attempt, 10) + random.uniform(0, 1)
                    log_debug(f"Waiting {delay:.1f}s before retry {attempt + 1}")
                    time.sleep(delay)

                response = self.client.get(url, headers=headers)
                response.raise_for_status()

                content_type = response.headers.get("content-type", "").lower()
                log_debug(f"Content type: {content_type}")

                # Check for anti-bot indicators only for HTML content
                if self._is_html_content(content_type):
                    if self._detect_antibot_response(response):
                        raise AntiBotDetectedError("Anti-bot system detected")
                    return response.text, content_type
                else:
                    # For binary content, return bytes
                    return response.content, content_type

            except httpx.TimeoutException as e:
                last_error = f"Request timeout (attempt {attempt + 1}/{self.max_retries})"
                log_warning(last_error)
            except httpx.HTTPStatusError as e:
                last_error = f"HTTP error {e.response.status_code}"
                log_warning(last_error)
                if e.response.status_code in [403, 429]:  # Likely anti-bot
                    continue
                else:
                    break  # Don't retry other HTTP errors
            except AntiBotDetectedError as e:
                last_error = (
                    f"Anti-bot detected (attempt {attempt + 1}/{self.max_retries})"
                )
                log_warning(last_error)
            except Exception as e:
                last_error = f"Request failed: {e}"
                log_error(last_error)
                break

        raise URLDownloadError(
            f"Failed to fetch file after {self.max_retries} attempts: {last_error}"
        )

    def _process_file_content(
        self, content: Union[str, bytes], content_type: str, format: str, url: str
    ) -> str:
        """
        Process file content based on type and requested format.
        """
        try:
            # Auto-detect format based on content type
            if format == "auto":
                if self._is_html_content(content_type):
                    format = "markdown"
                elif self._is_markitdown_supported(content_type):
                    format = (
                        "markdown"  # Use MarkItDown for PDFs and other supported formats
                    )
                elif self._is_binary_content(content_type):
                    format = "binary"
                else:
                    format = "text"

            # Handle binary content
            if isinstance(content, bytes):
                if format == "binary":
                    # For binary files, save to temp file and return file info
                    return self._handle_binary_file(content, content_type, url)
                else:
                    # Try to decode as text
                    try:
                        content = content.decode("utf-8")
                    except UnicodeDecodeError:
                        try:
                            content = content.decode("latin-1")
                        except UnicodeDecodeError:
                            return self._handle_binary_file(content, content_type, url)

            # Ensure content is string at this point
            if not isinstance(content, str):
                content = str(content)

            # Process text content
            if format == "markdown":
                if self._is_html_content(content_type):
                    return self._html_to_markdown(content)
                elif self._is_markitdown_supported(content_type):
                    # For PDFs and other MarkItDown-supported formats, process as binary with MarkItDown
                    if isinstance(content, str):
                        content = content.encode("utf-8")
                    return self._handle_binary_file(content, content_type, url)
                else:
                    return self._clean_text(content)
            elif format == "text":
                if self._is_html_content(content_type):
                    return self._html_to_text(content)
                elif self._is_markitdown_supported(content_type):
                    # For PDFs and other MarkItDown-supported formats, process as binary with MarkItDown
                    if isinstance(content, str):
                        content = content.encode("utf-8")
                    return self._handle_binary_file(content, content_type, url)
                else:
                    return self._clean_text(content)
            elif format == "html":
                return content
            else:
                return content

        except Exception as e:
            log_error(f"Content processing failed: {e}")
            raise ContentParsingError(f"Failed to process content: {e}")

    def _handle_binary_file(self, content: bytes, content_type: str, url: str) -> str:
        """
        Handle binary files - try MarkItDown if available, otherwise return file info.
        """
        try:
            # Try MarkItDown for supported binary formats
            if MARKITDOWN_AVAILABLE and markitdown_converter is not None:
                # Get file extension from URL or content type
                file_ext = self._get_file_extension(url, content_type)

                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_file_path = os.path.join(temp_dir, f"content{file_ext}")
                    with open(temp_file_path, "wb") as temp_file:
                        temp_file.write(content)

                    try:
                        markdown_content = markitdown_converter.convert(
                            temp_file_path
                        ).markdown
                        if markdown_content and len(markdown_content.strip()) > 0:
                            return self._clean_text(markdown_content)
                    except Exception as e:
                        log_debug(f"MarkItDown failed for binary file: {e}")

            # Fallback: return file information
            return json.dumps(
                {
                    "file_type": "binary",
                    "content_type": content_type,
                    "size_bytes": len(content),
                    "url": url,
                    "message": "Binary file downloaded successfully. Use MarkItDown-compatible formats for content extraction.",
                },
                indent=2,
            )

        except Exception as e:
            log_error(f"Binary file handling failed: {e}")
            return f"Binary file downloaded ({len(content)} bytes) but processing failed: {e}"

    def _is_html_content(self, content_type: str) -> bool:
        """Check if content type is HTML."""
        return any(html_type in content_type for html_type in self.HTML_CONTENT_TYPES)

    def _is_binary_content(self, content_type: str) -> bool:
        """Check if content type is binary."""
        return any(
            binary_type in content_type for binary_type in self.BINARY_CONTENT_TYPES
        )

    def _is_markitdown_supported(self, content_type: str) -> bool:
        """Check if content type is supported by MarkItDown for direct processing."""
        markitdown_supported_types = [
            "application/pdf",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/vnd.ms-excel",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "application/vnd.ms-powerpoint",
            "application/vnd.openxmlformats-officedocument.presentationml.presentation",
            "text/csv",
            "application/json",
            "text/xml",
            "application/xml",
        ]
        return any(
            supported_type in content_type
            for supported_type in markitdown_supported_types
        )

    def _get_file_extension(self, url: str, content_type: str) -> str:
        """Get file extension from URL or content type."""
        # Try to get extension from URL
        parsed_url = urlparse(url)
        if parsed_url.path:
            _, ext = os.path.splitext(parsed_url.path)
            if ext:
                return ext

        # Fallback to content type mapping
        ext = mimetypes.guess_extension(content_type)
        return ext or ".bin"

    def _get_default_headers(self) -> Dict[str, str]:
        """Get default HTTP headers."""
        return {
            "User-Agent": (
                random.choice(self.USER_AGENTS)
                if self.user_agent_rotation
                else self.USER_AGENTS[0]
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }

    def _get_antibot_headers(self) -> Dict[str, str]:
        """Get headers with anti-bot bypass techniques."""
        headers = self._get_default_headers()

        if self.user_agent_rotation:
            headers["User-Agent"] = random.choice(self.USER_AGENTS)

        # Add random referer
        referers = [
            "https://www.google.com/",
            "https://www.bing.com/",
            "https://duckduckgo.com/",
            "https://www.reddit.com/",
            "https://news.ycombinator.com/",
        ]
        headers["Referer"] = random.choice(referers)

        return headers

    def _detect_antibot_response(self, response: httpx.Response) -> bool:
        """Detect if response indicates anti-bot protection."""
        # Check for common anti-bot indicators
        content = response.text.lower()
        antibot_indicators = [
            "cloudflare",
            "captcha",
            "bot detection",
            "access denied",
            "blocked",
            "security check",
            "ddos protection",
        ]

        return any(indicator in content for indicator in antibot_indicators)

    def _format_content(self, content: str, format: str) -> str:
        """Format content to the specified output format."""
        if not content:
            return ""

        try:
            if format == "html":
                return content
            elif format == "text":
                return self._html_to_text(content)
            elif format == "markdown":
                return self._html_to_markdown(content)
            else:
                raise ContentParsingError(f"Unsupported format: {format}")

        except Exception as e:
            log_error(f"Content formatting failed: {e}")
            raise ContentParsingError(f"Failed to format content: {e}")

    def _html_to_markdown(self, html_content: str) -> str:
        """Convert HTML content to markdown."""
        if MARKITDOWN_AVAILABLE and markitdown_converter is not None:
            try:
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_file_path = os.path.join(temp_dir, "content.html")
                    with open(temp_file_path, "w", encoding="utf-8") as temp_file:
                        temp_file.write(html_content)

                    markdown_content = markitdown_converter.convert(
                        temp_file_path
                    ).markdown
                    return self._clean_text(markdown_content)
            except Exception as e:
                log_warning(
                    f"MarkItDown conversion failed: {e}, falling back to basic conversion"
                )

        # Fallback to basic HTML stripping
        return self._html_to_text(html_content)

    def _html_to_text(self, html_content: str) -> str:
        """Convert HTML content to plain text."""
        import re

        # Remove script and style elements
        text = re.sub(
            r"<(script|style)[^>]*>.*?</\1>",
            "",
            html_content,
            flags=re.DOTALL | re.IGNORECASE,
        )

        # Remove HTML tags
        text = re.sub(r"<[^>]+>", "", text)

        # Clean up whitespace
        text = re.sub(r"\s+", " ", text)

        return self._clean_text(text)

    def _clean_text(self, text: str) -> str:
        """Clean and normalize text content."""
        if not text:
            return ""

        import re

        # Remove excessive whitespace and normalize
        text = re.sub(r"\s+", " ", text.strip())

        # Remove control characters
        text = "".join(char for char in text if ord(char) >= 32 or char in "\n\t")

        return text

    def _validate_url(self, url: str) -> str:
        """Validate URL format."""
        if not url:
            raise URLDownloadError("URL cannot be empty")

        try:
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                raise URLDownloadError("Invalid URL format")
            if parsed.scheme not in ["http", "https"]:
                raise URLDownloadError("Only HTTP and HTTPS URLs are supported")
        except Exception as e:
            raise URLDownloadError(f"URL validation failed: {e}")

        return url

    def _validate_format(self, format: str) -> str:
        """Validate output format."""
        if format not in self.SUPPORTED_FORMATS:
            raise ContentParsingError(
                f"Unsupported format '{format}'. Supported formats: {', '.join(self.SUPPORTED_FORMATS)}"
            )
        return format

    @staticmethod
    def get_llm_usage_instructions() -> str:
        """
        Returns detailed instructions for LLMs on how to use the URL Content Downloader.
        """
        instructions = """
<content_downloader_tools_instructions>
*** URL Content Downloader Tool Instructions ***

Use this tool to download and parse content from any URL with advanced anti-bot bypass capabilities. By using these tools you can automatically fetch and process web content via URLs without manual intervention.

### Functions Tools

1. **access_website_content**: Fetch content from a single URL.
     - Parameters:
       - `url` (str): The URL to download, e.g., "https://example.com/article"
       - `output` (str, optional): Output format - "auto" (default), "markdown", "text", "html", or "binary"

2. **get_file_from_url**: Fetch any file from a URL with smart content processing.
     - Parameters:
       - `url` (str): The URL to download, e.g., "https://example.com/document.pdf"
       - `output` (str, optional): Output format - "auto" (default), "markdown", "text", "html", or "binary"

3. **download_multiple_urls**: Fetch content from multiple URLs in batch.
     - Parameters:
       - `urls` (list): List of URLs to download, e.g., ["https://site1.com", "https://site2.com"]
       - `output` (str, optional): Output format for all URLs - "auto" (default), "markdown", "text", "html", or "binary"

4. **get_url_metadata**: Extract metadata without downloading full content.
     - Parameters:
       - `url` (str): The URL to analyze, e.g., "https://example.com"

5. **check_url_accessibility**: Test if a URL is accessible.
     - Parameters:
       - `url` (str): The URL to check, e.g., "https://example.com"

### Features

- Universal file downloading support for various formats including HTML, PDF, Word documents, images, etc.
- Smart content processing: Uses MarkItDown for HTML and binary handling for files.
- Automatic BYPARR integration for anti-bot bypass capabilities.
- User-agent rotation and header spoofing to avoid detection.
- Robust retry logic with exponential backoff to handle transient errors.
- Multiple output format support with automatic detection based on content type.
- Comprehensive error handling mechanisms.

### Output Options

- `auto`: Automatically detects the best format (markdown for HTML, binary info for files).
- `markdown`: Converts HTML to markdown using MarkItDown.
- `text`: Extracts plain text from content.
- `html`: Returns raw HTML content.
- `binary`: Provides file information and processes binary data using MarkItDown when possible.

### Automatic Handling

The tool automatically manages:
- Any type of file including HTML, PDF, Word documents, Excel spreadsheets, images, etc.
- Anti-bot detection and bypass mechanisms.
- Content parsing and formatting based on the detected file type.
- Error recovery strategies and retries.
- Timeout management for long-running requests.
- Integration with MarkItDown for enhanced binary processing.

</content_downloader_tools_instructions>
"""
        return instructions

    def __del__(self):
        """Cleanup HTTP client on destruction."""
        try:
            if hasattr(self, "client"):
                self.client.close()
        except Exception:
            pass
