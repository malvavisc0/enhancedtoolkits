"""
Enhanced SearxNG Tools v2.0

A production-ready search toolkit that provides:
- Web search with SearxNG integration
- Optional content fetching with Byparr
- Robust error handling and logging
- Input validation and sanitization
- Configurable timeouts and retry logic
- Multiple search categories support

Author: malvavisc0
License: MIT
Version: 2.0.0
"""

import json
import os
import random
import tempfile
import time
import urllib.parse
from typing import Dict, List, Optional
from urllib.parse import urlparse

import httpx
from agno.utils.log import log_debug, log_error, log_info, log_warning

from .base import StrictToolkit

# Optional Byparr configuration
BYPARR_URL = os.environ.get("BYPARR_URL", "http://byparr:8191/v1")
BYPARR_TIMEOUT = int(os.environ.get("BYPARR_TIMEOUT", "60"))
BYPARR_ENABLED = os.environ.get("BYPARR_ENABLED", "false").lower() == "true"

# Required MarkItDown import
try:
    from markitdown import MarkItDown

    markitdown_converter = MarkItDown()
except ImportError:
    raise ImportError(
        "MarkItDown is required for EnhancedSearxngTools. "
        "Please install it with: pip install markitdown"
    )


class SearxngSearchError(Exception):
    """Custom exception for SearxNG search errors."""

    pass


class SearxngContentError(Exception):
    """Custom exception for content fetching errors."""

    pass


class FileDownloadError(SearxngContentError):
    """Custom exception for file download errors."""

    pass


class UnsupportedFileTypeError(SearxngContentError):
    """Custom exception for unsupported file types."""

    pass


class EnhancedSearxngTools(StrictToolkit):
    """
    Enhanced SearxNG Tools v2.0

    A production-ready search toolkit with optional content fetching,
    robust error handling, and comprehensive search capabilities.
    """

    # Supported search categories
    SUPPORTED_CATEGORIES = {
        "general": "General web search",
        "news": "News articles",
        "images": "Image search",
        "videos": "Video search",
        "music": "Music search",
        "files": "File search",
        "science": "Scientific articles",
        "social": "Social media content",
    }

    def __init__(
        self,
        host: str,
        max_results: Optional[int] = 10,
        timeout: int = 30,
        enable_content_fetching: Optional[bool] = False,
        enable_file_downloads: Optional[bool] = True,
        max_file_size_mb: int = 10,
        file_download_timeout: int = 60,
        byparr_enabled: Optional[bool] = True,
        add_instructions: bool = True,
        **kwargs,
    ):
        """
        Initialize Enhanced SearxNG Tools.

        Args:
            host: SearxNG instance URL
            max_results: Maximum number of search results to return
            timeout: Request timeout in seconds
            enable_content_fetching: Whether to fetch full content from URLs
            enable_file_downloads: Whether to download and process files (PDF, TXT, MD)
            max_file_size_mb: Maximum file size to download in MB
            file_download_timeout: Timeout for file downloads in seconds
            byparr_enabled: Override for Byparr usage (None = auto-detect)
        """
        if not host:
            raise ValueError("Invalid SearxNG host URL")

        # Configuration
        self.host = self._validate_host(host)
        self.max_results = max(1, min(30, max_results or 10))  # Limit between 1-30
        self.timeout = max(5, min(120, timeout))  # Limit between 5-120 seconds
        self.enable_content_fetching = enable_content_fetching
        self.enable_file_downloads = enable_file_downloads
        self.supported_file_types = ["pdf", "txt", "md"]
        self.max_file_size_mb = max(
            1, min(500, max_file_size_mb)
        )  # Limit between 1-500 MB
        self.file_download_timeout = max(
            10, min(300, file_download_timeout)
        )  # 10-300 seconds
        self.add_instructions = add_instructions
        self.instructions = EnhancedSearxngTools.get_llm_usage_instructions()

        super().__init__(name="enhanced_searxng_tools", **kwargs)

        # Byparr configuration (optional)
        if byparr_enabled is not None:
            self.byparr_enabled = byparr_enabled
        else:
            self.byparr_enabled = BYPARR_ENABLED and self.enable_content_fetching

        # HTTP client configuration
        self.client = httpx.Client(
            timeout=httpx.Timeout(self.timeout),
            follow_redirects=True,
            headers={"User-Agent": "Enhanced-SearxNG-Tools/2.0 (Python/httpx)"},
        )

        # File download client configuration (separate timeout)
        if self.enable_file_downloads:
            self.file_client = httpx.Client(
                timeout=httpx.Timeout(self.file_download_timeout),
                follow_redirects=True,
                headers=self._get_file_download_headers(),
            )
        else:
            self.file_client = None

        # Register search methods
        self.register(self.perform_web_search)
        self.register(self.perform_news_search)
        self.register(self.perform_image_search)
        self.register(self.perform_video_search)
        self.register(self.perform_category_search)

        log_info(
            f"Enhanced SearxNG Tools initialized - Host: {self.host}, Max Results: {self.max_results}, "
            f"Content Fetching: {self.enable_content_fetching}, File Downloads: {self.enable_file_downloads}, "
            f"Supported Files: {self.supported_file_types}, Byparr: {self.byparr_enabled}"
        )

    def perform_web_search(self, query: str, max_results: Optional[int] = None) -> str:
        """
        Perform a web search using SearxNG.

        Args:
            query: Search query string
            max_results: Maximum number of results (overrides default)

        Returns:
            JSON string containing search results

        Raises:
            SearxngSearchError: If search fails
        """
        return self._search(query, category="general", max_results=max_results)

    def perform_news_search(self, query: str, max_results: Optional[int] = None) -> str:
        """
        Perform a news search using SearxNG.

        Args:
            query: Search query string
            max_results: Maximum number of results (overrides default)

        Returns:
            JSON string containing news search results

        Raises:
            SearxngSearchError: If search fails
        """
        return self._search(query, category="news", max_results=max_results)

    def perform_image_search(self, query: str, max_results: Optional[int] = None) -> str:
        """
        Perform an image search using SearxNG.

        Args:
            query: Search query string
            max_results: Maximum number of results (overrides default)

        Returns:
            JSON string containing image search results

        Raises:
            SearxngSearchError: If search fails
        """
        return self._search(query, category="images", max_results=max_results)

    def perform_video_search(self, query: str, max_results: Optional[int] = None) -> str:
        """
        Perform a video search using SearxNG.

        Args:
            query: Search query string
            max_results: Maximum number of results (overrides default)

        Returns:
            JSON string containing video search results

        Raises:
            SearxngSearchError: If search fails
        """
        return self._search(query, category="videos", max_results=max_results)

    def perform_category_search(
        self, query: str, category: str, max_results: Optional[int] = None
    ) -> str:
        """
        Perform a search in a specific category using SearxNG.

        Args:
            query: Search query string
            category: Search category (general, news, images, videos, etc.)
            max_results: Maximum number of results (overrides default)

        Returns:
            JSON string containing search results

        Raises:
            SearxngSearchError: If search fails or category is invalid
        """
        if category not in self.SUPPORTED_CATEGORIES:
            available_categories = ", ".join(self.SUPPORTED_CATEGORIES.keys())
            raise SearxngSearchError(
                f"Unsupported category '{category}'. Available categories: {available_categories}"
            )

        return self._search(query, category=category, max_results=max_results)

    def _get_page_content(self, url: str) -> str:
        """
        Fetch and parse content from a webpage or file.

        Args:
            url: URL to fetch content from

        Returns:
            Parsed content as markdown or plain text

        Raises:
            SearxngContentError: If content fetching fails
        """
        if not self.enable_content_fetching:
            raise SearxngContentError(
                "Content fetching is disabled. Enable it during initialization."
            )

        try:
            # Validate URL
            parsed_url = self._validate_url(url)
            log_debug(f"Fetching content from: {parsed_url}")

            # Get content-type for better file detection
            content_type = (
                self._get_content_type(parsed_url) if self.enable_file_downloads else None
            )

            # Check if this is a supported file type
            if self._is_supported_file_type(parsed_url, content_type):
                file_type = self._detect_file_type(parsed_url, content_type)
                log_info(
                    f"Detected {file_type} file (content-type: {content_type}), processing with file downloader"
                )
                return self._download_and_process_file(parsed_url, file_type)

            # Try Byparr first if enabled for HTML content
            if self.byparr_enabled:
                try:
                    content = self._fetch_content_with_byparr(parsed_url)
                    if content:
                        return content
                    log_warning(f"Byparr failed for {url}, falling back to direct fetch")
                except Exception as e:
                    log_warning(
                        f"Byparr error for {url}: {e}, falling back to direct fetch"
                    )

            # Fallback to direct HTTP request for HTML content
            return self._fetch_content_direct(url)

        except Exception as e:
            log_error(f"Error fetching content from {url}: {e}")
            raise SearxngContentError(f"Failed to fetch content from {url}: {e}")

    def _detect_file_type(self, url: str, content_type: Optional[str] = None) -> str:
        """
        Detect file type from URL extension and content-type header.

        Args:
            url: URL to analyze
            content_type: HTTP content-type header (optional)

        Returns:
            File type ('pdf', 'txt', 'md', 'html', or 'unknown')
        """
        try:
            # First check content-type if available (more reliable)
            if content_type:
                content_type_lower = content_type.lower()
                if "application/pdf" in content_type_lower:
                    return "pdf"
                elif any(ct in content_type_lower for ct in ["text/plain", "text/txt"]):
                    return "txt"
                elif any(
                    ct in content_type_lower
                    for ct in ["text/markdown", "text/x-markdown"]
                ):
                    return "md"
                elif any(
                    ct in content_type_lower
                    for ct in ["text/html", "application/xhtml+xml"]
                ):
                    return "html"

            # Fallback to URL extension
            parsed_url = urlparse(url)
            path = parsed_url.path.lower()

            if path.endswith(".pdf"):
                return "pdf"
            elif path.endswith((".txt", ".text")):
                return "txt"
            elif path.endswith((".md", ".markdown")):
                return "md"
            elif path.endswith((".html", ".htm")):
                return "html"
            else:
                return "unknown"
        except Exception:
            return "unknown"

    def _is_supported_file_type(
        self, url: str, content_type: Optional[str] = None
    ) -> bool:
        """
        Check if URL points to a supported file type.

        Args:
            url: URL to check
            content_type: HTTP content-type header (optional)

        Returns:
            True if file type is supported
        """
        if not self.enable_file_downloads:
            return False

        file_type = self._detect_file_type(url, content_type)
        return file_type in self.supported_file_types

    def _get_content_type(self, url: str) -> Optional[str]:
        """
        Get content-type header from URL using HEAD request.

        Args:
            url: URL to check

        Returns:
            Content-type string or None if unavailable
        """
        try:
            if self.file_client:
                response = self.file_client.head(url, timeout=10)
                return response.headers.get("content-type")
        except Exception as e:
            log_debug(f"Failed to get content-type for {url}: {e}")
        return None

    def _download_and_process_file(self, url: str, file_type: str) -> str:
        """
        Download and process files based on type.

        Args:
            url: URL to download from
            file_type: Type of file ('pdf', 'txt', 'md')

        Returns:
            Processed file content

        Raises:
            FileDownloadError: If download or processing fails
        """
        try:
            log_debug(f"Downloading {file_type} file from: {url}")

            if file_type == "pdf":
                return self._process_pdf_content(url)
            elif file_type == "txt":
                return self._process_text_file(url)
            elif file_type == "md":
                return self._process_markdown_file(url)
            else:
                raise UnsupportedFileTypeError(f"Unsupported file type: {file_type}")

        except (FileDownloadError, UnsupportedFileTypeError):
            raise
        except Exception as e:
            log_error(f"Error processing {file_type} file from {url}: {e}")
            raise FileDownloadError(f"Failed to process {file_type} file: {e}")

    def _process_pdf_content(self, url: str) -> str:
        """
        Download PDF and extract content using MarkItDown.

        Args:
            url: URL of PDF file

        Returns:
            Extracted content as markdown

        Raises:
            FileDownloadError: If download or processing fails
        """
        try:
            # Download PDF content
            response = self._fetch_file_with_antibot(url)
            content_type = response.headers.get("content-type", "").lower()

            # Validate content-type matches expectation
            if "application/pdf" not in content_type:
                log_warning(f"Expected PDF content type, got: {content_type}")
                # Still proceed but log the mismatch

            # Check file size
            content_length = response.headers.get("content-length")
            if (
                content_length
                and int(content_length) > self.max_file_size_mb * 1024 * 1024
            ):
                raise FileDownloadError(f"PDF file too large: {content_length} bytes")

            # Process with MarkItDown
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_file_path = os.path.join(temp_dir, "document.pdf")
                with open(temp_file_path, "wb") as temp_file:
                    temp_file.write(response.content)

                markdown_content = markitdown_converter.convert(temp_file_path).markdown
                return self._clean_text(markdown_content)

        except Exception as e:
            log_error(f"PDF processing failed for {url}: {e}")
            raise FileDownloadError(f"Failed to process PDF: {e}")

    def _process_text_file(self, url: str) -> str:
        """
        Download and return text file content.

        Args:
            url: URL of text file

        Returns:
            Text file content

        Raises:
            FileDownloadError: If download fails
        """
        try:
            # Download text content
            response = self._fetch_file_with_antibot(url)
            content_type = response.headers.get("content-type", "").lower()

            # Validate content-type for text files
            if content_type and not any(
                ct in content_type
                for ct in ["text/plain", "text/txt", "text/", "application/octet-stream"]
            ):
                log_warning(f"Expected text content type, got: {content_type}")

            # Check file size
            content_length = response.headers.get("content-length")
            if (
                content_length
                and int(content_length) > self.max_file_size_mb * 1024 * 1024
            ):
                raise FileDownloadError(f"Text file too large: {content_length} bytes")

            # Try to decode as text
            try:
                content = response.content.decode("utf-8")
            except UnicodeDecodeError:
                try:
                    content = response.content.decode("latin-1")
                except UnicodeDecodeError:
                    content = response.content.decode("utf-8", errors="replace")

            return self._clean_text(content)

        except Exception as e:
            log_error(f"Text file processing failed for {url}: {e}")
            raise FileDownloadError(f"Failed to process text file: {e}")

    def _process_markdown_file(self, url: str) -> str:
        """
        Download and return markdown file content.

        Args:
            url: URL of markdown file

        Returns:
            Markdown file content

        Raises:
            FileDownloadError: If download fails
        """
        try:
            # Download markdown content
            response = self._fetch_file_with_antibot(url)
            content_type = response.headers.get("content-type", "").lower()

            # Validate content-type for markdown files
            if content_type and not any(
                ct in content_type
                for ct in [
                    "text/markdown",
                    "text/x-markdown",
                    "text/plain",
                    "text/",
                    "application/octet-stream",
                ]
            ):
                log_warning(f"Expected markdown content type, got: {content_type}")

            # Check file size
            content_length = response.headers.get("content-length")
            if (
                content_length
                and int(content_length) > self.max_file_size_mb * 1024 * 1024
            ):
                raise FileDownloadError(
                    f"Markdown file too large: {content_length} bytes"
                )

            # Try to decode as text
            try:
                content = response.content.decode("utf-8")
            except UnicodeDecodeError:
                try:
                    content = response.content.decode("latin-1")
                except UnicodeDecodeError:
                    content = response.content.decode("utf-8", errors="replace")

            return self._clean_text(content)

        except Exception as e:
            log_error(f"Markdown file processing failed for {url}: {e}")
            raise FileDownloadError(f"Failed to process markdown file: {e}")

    def _fetch_file_with_antibot(self, url: str) -> httpx.Response:
        """
        Fetch file with anti-bot bypass techniques.

        Args:
            url: URL to fetch

        Returns:
            HTTP response object

        Raises:
            FileDownloadError: If fetch fails
        """
        if not self.file_client:
            raise FileDownloadError("File download client not initialized")

        max_retries = 3
        last_error = None

        for attempt in range(max_retries):
            try:
                # Apply anti-bot techniques
                headers = self._get_file_download_headers()

                # Add random delay between attempts
                if attempt > 0:
                    delay = min(2**attempt, 10) + random.uniform(0, 1)
                    log_debug(f"Waiting {delay:.1f}s before retry {attempt + 1}")
                    time.sleep(delay)

                response = self.file_client.get(url, headers=headers)
                response.raise_for_status()

                return response

            except httpx.TimeoutException as e:
                last_error = f"Request timeout (attempt {attempt + 1}/{max_retries})"
                log_warning(last_error)
            except httpx.HTTPStatusError as e:
                last_error = f"HTTP error {e.response.status_code}"
                log_warning(last_error)
                if e.response.status_code in [403, 429]:  # Likely anti-bot
                    continue
                else:
                    break  # Don't retry other HTTP errors
            except Exception as e:
                last_error = f"Request failed: {e}"
                log_error(last_error)
                break

        raise FileDownloadError(
            f"Failed to fetch file after {max_retries} attempts: {last_error}"
        )

    def _get_file_download_headers(self) -> Dict[str, str]:
        """
        Get headers for file downloads with anti-bot techniques.

        Returns:
            Dictionary of HTTP headers
        """
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        ]

        headers = {
            "User-Agent": random.choice(user_agents),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }

        # Add random referer
        referers = [
            "https://www.google.com/",
            "https://www.bing.com/",
            "https://duckduckgo.com/",
        ]
        headers["Referer"] = random.choice(referers)

        return headers

    def _search(
        self,
        query: str,
        category: Optional[str] = None,
        max_results: Optional[int] = None,
    ) -> str:
        """
        Internal search method with comprehensive error handling.
        """
        try:
            # Input validation
            if not query or not query.strip():
                raise SearxngSearchError("Search query cannot be empty")

            query = query.strip()
            if len(query) > 500:  # Reasonable query length limit
                query = query[:500]
                log_warning(f"Query truncated to 500 characters: {query}")

            # Build search URL
            encoded_query = urllib.parse.quote(query)
            url = f"{self.host}/search?format=json&q={encoded_query}"

            if category and category != "general":
                url += f"&categories={category}"

            # Determine result count
            count = max_results or self.max_results
            count = max(1, min(50, count))  # Ensure reasonable limits

            log_debug(f"Searching SearxNG: {url} (max_results: {count})")

            # Perform search with retry logic
            response_data = self._make_search_request(url)

            # Process results
            results = self._process_search_results(response_data, count, category)

            log_info(
                f"Search completed: {len(results)} results for query '{query}' in category '{category or 'general'}'"
            )
            return json.dumps(results, indent=2, ensure_ascii=False)

        except SearxngSearchError:
            raise
        except Exception as e:
            log_error(f"Unexpected error during search: {e}")
            raise SearxngSearchError(f"Search failed: {e}")

    def _make_search_request(self, url: str, max_retries: int = 3) -> Dict:
        """
        Make search request with retry logic.
        """
        last_error = None

        for attempt in range(max_retries):
            try:
                response = self.client.get(url)
                response.raise_for_status()

                data = response.json()
                if "results" not in data:
                    raise SearxngSearchError("Invalid response format from SearxNG")

                return data

            except httpx.TimeoutException as e:
                last_error = f"Request timeout (attempt {attempt + 1}/{max_retries})"
                log_warning(last_error)
                log_warning(e)
            except httpx.HTTPStatusError as e:
                last_error = f"HTTP error {e.response.status_code}: {e.response.text}"
                log_error(last_error)
                log_warning(e)
                break  # Don't retry HTTP errors
            except json.JSONDecodeError as e:
                last_error = (
                    f"Invalid JSON response (attempt {attempt + 1}/{max_retries})"
                )
                log_warning(last_error)
                log_warning(e)
            except Exception as e:
                last_error = f"Request failed: {e}"
                log_error(last_error)
                break  # Don't retry unexpected errors

        raise SearxngSearchError(
            f"Search request failed after {max_retries} attempts: {last_error}"
        )

    def _process_search_results(
        self, response_data: Dict, count: int, category: Optional[str]
    ) -> List[Dict]:
        """
        Process and format search results.
        """
        raw_results = response_data.get("results", [])
        if not raw_results:
            log_info("No search results found")
            return []

        results = []
        for i, row in enumerate(raw_results[:count]):
            try:
                # Basic result structure
                result = {
                    "title": self._clean_text(row.get("title", "No title")),
                    "url": row.get("url", ""),
                    "summary": self._clean_text(row.get("content", "")),
                    "category": category or "general",
                }

                # Add category-specific fields
                if category == "images":
                    result.update(
                        {
                            "thumbnail": row.get("thumbnail_src", ""),
                            "img_src": row.get("img_src", ""),
                            "width": row.get("img_width"),
                            "height": row.get("img_height"),
                        }
                    )
                elif category == "videos":
                    result.update(
                        {
                            "thumbnail": row.get("thumbnail", ""),
                            "duration": row.get("duration", ""),
                            "publishedDate": row.get("publishedDate", ""),
                        }
                    )
                elif category == "news":
                    result.update(
                        {
                            "publishedDate": row.get("publishedDate", ""),
                            "source": row.get("engine", ""),
                        }
                    )

                # Check if this is a supported file type
                content_type = None
                file_type = (
                    self._detect_file_type(result["url"]) if result["url"] else "unknown"
                )

                # Get content-type for better detection if file downloads are enabled
                if (
                    self.enable_file_downloads
                    and result["url"]
                    and file_type != "unknown"
                ):
                    content_type = self._get_content_type(result["url"])
                    # Re-detect with content-type for accuracy
                    file_type = self._detect_file_type(result["url"], content_type)

                if file_type != "unknown":
                    result["file_type"] = file_type
                    if content_type:
                        result["content_type"] = content_type

                # Add content if fetching is enabled and URL is valid
                if (
                    self.enable_content_fetching
                    and result["url"]
                    and category in ["general", "news", "files"]
                    and len(results) < 3
                ):  # Limit content fetching to first 3 results
                    try:
                        # Check if this is a supported file type for download
                        if self._is_supported_file_type(result["url"], content_type):
                            log_info(
                                f"Processing {file_type} file: {result['url']} (content-type: {content_type})"
                            )
                            result["content"] = self._download_and_process_file(
                                result["url"], file_type
                            )
                        else:
                            # Regular HTML content fetching
                            result["content"] = self._fetch_content_safe(result["url"])
                    except Exception as e:
                        log_debug(f"Content fetching failed for {result['url']}: {e}")
                        result["content"] = ""

                results.append(result)

            except Exception as e:
                log_warning(f"Error processing search result {i}: {e}")
                continue

        return results

    def _fetch_content_with_byparr(self, url: str) -> Optional[str]:
        """
        Fetch content using Byparr service.
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
            return self._parse_html_content(raw_html)

        except Exception as e:
            log_debug(f"Byparr request failed: {e}")
            return None

    def _fetch_content_direct(self, url: str) -> str:
        """
        Fetch content directly via HTTP.
        """
        try:
            response = self.client.get(url)
            response.raise_for_status()

            content_type = response.headers.get("content-type", "").lower()
            if "text/html" not in content_type:
                return f"Content type not supported: {content_type}"

            return self._parse_html_content(response.text)

        except Exception as e:
            raise SearxngContentError(f"Direct fetch failed: {e}")

    def _parse_html_content(self, html_content: str) -> str:
        """
        Parse HTML content to markdown using MarkItDown.

        Args:
            html_content: HTML content to parse

        Returns:
            Processed markdown content

        Raises:
            SearxngContentError: If content parsing fails
        """
        if not html_content:
            return ""

        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_file_path = os.path.join(temp_dir, "content.html")
                with open(temp_file_path, "w", encoding="utf-8") as temp_file:
                    temp_file.write(html_content)

                markdown_content = markitdown_converter.convert(temp_file_path).markdown
                return self._clean_text(markdown_content)
        except Exception as e:
            log_error(f"HTML parsing failed: {e}")
            raise SearxngContentError(f"Failed to parse HTML content: {e}")

    def _fetch_content_safe(self, url: str) -> str:
        """
        Safely fetch content with error handling.
        """
        try:
            return self._get_page_content(url)
        except Exception:
            return ""

    def _validate_host(self, host: str) -> str:
        """
        Validate and normalize SearxNG host URL.
        """
        if not host:
            raise ValueError("SearxNG host cannot be empty")

        if not host.startswith(("http://", "https://")):
            host = f"http://{host}"

        try:
            parsed = urlparse(host)
            if not parsed.netloc:
                raise ValueError("Invalid host URL")
        except Exception:
            raise ValueError(f"Invalid host URL: {host}")

        return host.rstrip("/")

    def _validate_url(self, url: str) -> str:
        """
        Validate URL format.
        """
        if not url:
            raise SearxngContentError("URL cannot be empty")

        try:
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                raise SearxngContentError("Invalid URL format")
            if parsed.scheme not in ["http", "https"]:
                raise SearxngContentError("Only HTTP and HTTPS URLs are supported")
        except Exception as e:
            raise SearxngContentError(f"URL validation failed: {e}")

        return url

    def _clean_text(self, text: str) -> str:
        """
        Clean and normalize text content.
        """
        if not text:
            return ""

        # Remove excessive whitespace and normalize
        import re

        text = re.sub(r"\s+", " ", text.strip())

        # Remove control characters
        text = "".join(char for char in text if ord(char) >= 32 or char in "\n\t")

        return text

    @staticmethod
    def get_llm_usage_instructions() -> str:
        """
        Returns a set of detailed instructions for LLMs on how to use each tool in EnhancedSearxngTools.
        Each instruction includes the method name, description, parameters, types, and example values.
        """
        instructions = """
<internet_search_tools_instructions>
*** Web Search Tools Instructions using SearxNG ***

These tools enable you to perform various web searches and manage the results. They provide accurate, real-time information with improved file handling capabilities.

**Content Fetching Capabilities:**
- The tools can automatically fetch and process content from URLs in search results when content fetching is enabled
- Supported file types (PDF, TXT, MD) are detected and their contents extracted
- HTML content can be fetched and converted to markdown
- File processing includes anti-bot measures for reliable access

**General Instructions:**
- All methods return a dictionary with 'results' (list) and 'status' (str) keys.
- Each result is a dictionary containing relevant data based on the search type.
- The 'file_type' field will be present if supported file types are detected in URLs.
- If errors occur, an error message will be returned under the 'error' key.

### Functions Tools

1. **perform_web_search**: Perform a web search.
   - Parameters:
     - `query` (str): Search term or phrase, e.g., "climate change impacts".
     - `max_results` (int, optional): Maximum results to return (default: 5, range: 1-30).
   - *Example:* `perform_web_search("python best practices", max_results=7)`

2. **perform_news_search**: Perform a news search.
   - Parameters:
     - `query` (str): Search term or phrase, e.g., "AI in healthcare".
     - `max_results` (int, optional): Maximum results to return (default: 5, range: 1-30).
   - *Example:* `perform_news_search("space exploration", max_results=5)`

3. **perform_image_search**: Perform an image search.
   - Parameters:
     - `query` (str): Search term or phrase, e.g., "coffee shop interior".
     - `max_results` (int, optional): Maximum results to return (default: 5, range: 1-30).
   - *Example:* `perform_image_search("dog breeds")`

4. **perform_video_search**: Perform a video search.
   - Parameters:
     - `query` (str): Search term or phrase, e.g., "language learning".
     - `max_results` (int, optional): Maximum results to return (default: 5, range: 1-30).
   - *Example:* `perform_video_search("language learning", max_results=8)`

5. **perform_category_search**: Search within a specific category.
   - Parameters:
     - `query` (str): Search term or phrase, e.g., "quantum computing advancements".
     - `category` (str): One of: general, news, images, videos, music, files, science, social, or it.
     - `max_results` (int, optional): Maximum results to return (default: 5, range: 1-30).
   - *Example:* `perform_category_search("cybersecurity trends", category="it")`

**File Processing Features:**
- Automatically detects PDF, TXT, and Markdown files in search results, including from URLs in the search results.

**Configuration Options:**
- Max file download size (default: 50MB)
- Download timeout protection
- Enable/disable URL content fetching and file downloads

**Additional Notes:**
- Ensure the category parameter in `perform_category_search` matches one of the accepted values.
- File processing is automatically applied when supported file types are detected in URLs.

**Error Handling:**
If any errors occur during execution (e.g., invalid parameters, connectivity issues), appropriate error messages will be returned under the 'error' key to guide troubleshooting.

</internet_search_tools_instructions>
"""
        return instructions

    def __del__(self):
        """
        Cleanup HTTP clients on destruction.
        """
        try:
            if hasattr(self, "client"):
                self.client.close()
            if hasattr(self, "file_client") and self.file_client:
                self.file_client.close()
        except Exception:
            pass
