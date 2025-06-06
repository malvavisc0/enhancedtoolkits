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
import tempfile
import urllib.parse
from typing import Dict, List, Optional
from urllib.parse import urlparse

import httpx
from agno.tools.toolkit import Toolkit
from agno.utils.log import log_debug, log_error, log_info, log_warning

# Optional Byparr configuration
BYPARR_URL = os.environ.get("BYPARR_URL", "http://byparr:8191/v1")
BYPARR_TIMEOUT = int(os.environ.get("BYPARR_TIMEOUT", "60"))
BYPARR_ENABLED = os.environ.get("BYPARR_ENABLED", "false").lower() == "true"

# Optional MarkItDown import
try:
    from markitdown import MarkItDown

    MARKITDOWN_AVAILABLE = True
    markitdown_converter = MarkItDown()
except ImportError:
    MARKITDOWN_AVAILABLE = False
    markitdown_converter = None
    log_warning("MarkItDown not available. Content parsing will be limited.")


class SearxngSearchError(Exception):
    """Custom exception for SearxNG search errors."""

    pass


class SearxngContentError(Exception):
    """Custom exception for content fetching errors."""

    pass


class EnhancedSearxngTools(Toolkit):
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
        enable_content_fetching: bool = False,
        byparr_enabled: Optional[bool] = False,
        **kwargs,
    ):
        """
        Initialize Enhanced SearxNG Tools.

        Args:
            host: SearxNG instance URL
            max_results: Maximum number of search results to return
            timeout: Request timeout in seconds
            enable_content_fetching: Whether to fetch full content from URLs
            byparr_enabled: Override for Byparr usage (None = auto-detect)
        """
        super().__init__(name="enhanced_searxng_tools", **kwargs)

        # Configuration
        self.host = self._validate_host(host)
        self.max_results = max(1, min(30, max_results or 10))  # Limit between 1-30
        self.timeout = max(5, min(120, timeout))  # Limit between 5-120 seconds
        self.enable_content_fetching = enable_content_fetching

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

        # Register search methods
        self.register(self.search_web)
        self.register(self.search_news)
        self.register(self.search_images)
        self.register(self.search_videos)
        self.register(self.search_category)

        # Register content fetching if enabled
        if self.enable_content_fetching:
            self.register(self.get_page_content)

        log_info(
            f"Enhanced SearxNG Tools initialized - Host: {self.host}, Max Results: {self.max_results}, Content Fetching: {self.enable_content_fetching}, Byparr: {self.byparr_enabled}"
        )

    def search_web(self, query: str, max_results: Optional[int] = None) -> str:
        """
        Search the web using SearxNG.

        Args:
            query: Search query string
            max_results: Maximum number of results (overrides default)

        Returns:
            JSON string containing search results

        Raises:
            SearxngSearchError: If search fails
        """
        return self._search(query, category="general", max_results=max_results)

    def search_news(self, query: str, max_results: Optional[int] = None) -> str:
        """
        Search for news articles using SearxNG.

        Args:
            query: Search query string
            max_results: Maximum number of results (overrides default)

        Returns:
            JSON string containing news search results

        Raises:
            SearxngSearchError: If search fails
        """
        return self._search(query, category="news", max_results=max_results)

    def search_images(self, query: str, max_results: Optional[int] = None) -> str:
        """
        Search for images using SearxNG.

        Args:
            query: Search query string
            max_results: Maximum number of results (overrides default)

        Returns:
            JSON string containing image search results

        Raises:
            SearxngSearchError: If search fails
        """
        return self._search(query, category="images", max_results=max_results)

    def search_videos(self, query: str, max_results: Optional[int] = None) -> str:
        """
        Search for videos using SearxNG.

        Args:
            query: Search query string
            max_results: Maximum number of results (overrides default)

        Returns:
            JSON string containing video search results

        Raises:
            SearxngSearchError: If search fails
        """
        return self._search(query, category="videos", max_results=max_results)

    def search_category(
        self, query: str, category: str, max_results: Optional[int] = None
    ) -> str:
        """
        Search in a specific category using SearxNG.

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

    def get_page_content(self, url: str) -> str:
        """
        Fetch and parse content from a webpage.

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

            # Try Byparr first if enabled
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

            # Fallback to direct HTTP request
            return self._fetch_content_direct(url)

        except Exception as e:
            log_error(f"Error fetching content from {url}: {e}")
            raise SearxngContentError(f"Failed to fetch content from {url}: {e}")

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

                # Add content if fetching is enabled and URL is valid
                if (
                    self.enable_content_fetching
                    and result["url"]
                    and category in ["general", "news"]
                    and len(results) < 3
                ):  # Limit content fetching to first 3 results
                    try:
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
        Parse HTML content to markdown or plain text.
        """
        if not html_content:
            return ""

        try:
            if MARKITDOWN_AVAILABLE and markitdown_converter is not None:
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_file_path = os.path.join(temp_dir, "content.html")
                    with open(temp_file_path, "w", encoding="utf-8") as temp_file:
                        temp_file.write(html_content)

                    markdown_content = markitdown_converter.convert(
                        temp_file_path
                    ).markdown
                    return self._clean_text(markdown_content)
            else:
                # Basic HTML stripping if MarkItDown is not available
                import re

                text = re.sub(r"<[^>]+>", "", html_content)
                return self._clean_text(text)

        except Exception as e:
            log_warning(f"HTML parsing failed: {e}")
            return "Content parsing failed"

    def _fetch_content_safe(self, url: str) -> str:
        """
        Safely fetch content with error handling.
        """
        try:
            return self.get_page_content(url)
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
*** SearxNG Search Tools Instructions ***

By leveraging the following set of tools, you can perform web, news, image, and video searches, as well as fetch content from URLs (if enabled). These tools empower you to deliver accurate, real-time search results and content extraction with ease. Here are the detailed instructions for using the set of tools:

- Use search_web to perform a general web search.
   Parameters:
      - query (str): The search query, e.g., "climate change".
      - max_results (int, optional): Maximum number of results (default: 10, range: 1-30).

- Use search_news to search for news articles.
   Parameters:
      - query (str): The search query, e.g., "AI regulation".
      - max_results (int, optional): Maximum number of results (default: 10, range: 1-30).

- Use search_images to search for images.
   Parameters:
      - query (str): The search query, e.g., "Eiffel Tower".
      - max_results (int, optional): Maximum number of results (default: 10, range: 1-30).

- Use search_videos to search for videos.
   Parameters:
      - query (str): The search query, e.g., "machine learning tutorial".
      - max_results (int, optional): Maximum number of results (default: 10, range: 1-30).

- Use search_category to search in a specific category.
   Parameters:
      - query (str): The search query, e.g., "quantum computing".
      - category (str): One of: general, news, images, videos, music, files, science, social.
      - max_results (int, optional): Maximum number of results (default: 10, range: 1-30).

- Use get_page_content to fetch and parse content from a webpage (only if content fetching is enabled).
   Parameters:
      - url (str): The URL to fetch, e.g., "https://example.com/article".

Notes:
- The get_page_content tool is only available if content fetching is enabled during initialization.
- The max_results parameter is always optional and defaults to the toolkit's configuration.
- The category parameter for search_category must be one of: general, news, images, videos, music, files, science, social.
"""
        return instructions

    def __del__(self):
        """
        Cleanup HTTP client on destruction.
        """
        try:
            if hasattr(self, "client"):
                self.client.close()
        except Exception:
            pass
