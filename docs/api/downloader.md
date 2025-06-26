# Downloader Tools API Reference

API documentation for the Downloader Tools toolkit - universal file downloading with anti-bot bypass capabilities.

## Class: DownloaderTools

Universal file downloading toolkit with anti-bot bypass, security validation, and comprehensive error handling.

### DownloaderTools()

Initialize the Downloader Tools toolkit.

**Parameters:**
- `allowed_domains` (List[str], optional): Allowed domains for downloads. Default: None (all domains)
- `blocked_domains` (List[str], optional): Blocked domains. Default: []
- `max_file_size` (int, optional): Maximum file size in bytes. Default: 52428800 (50MB)
- `enable_virus_scan` (bool, optional): Enable virus scanning. Default: False
- `user_agent` (str, optional): Custom user agent string
- `timeout` (int, optional): Download timeout in seconds. Default: 30

### Methods

#### download_file()

Download a file from a URL with security validation and anti-bot bypass.

**Parameters:**
- `url` (str): URL of the file to download
- `destination` (str, optional): Local destination path. If not provided, uses filename from URL
- `overwrite` (bool): Whether to overwrite existing files. Default: False
- `verify_ssl` (bool): Whether to verify SSL certificates. Default: True

**Returns:**
- `dict`: Download result with file metadata, size, and validation status

#### download_with_headers()

Download a file with custom headers for bypassing restrictions.

**Parameters:**
- `url` (str): URL of the file to download
- `headers` (dict): Custom HTTP headers
- `destination` (str, optional): Local destination path
- `cookies` (dict, optional): Custom cookies for the request

**Returns:**
- `dict`: Download result with response headers and file information

#### batch_download()

Download multiple files in batch with progress tracking.

**Parameters:**
- `urls` (List[str]): List of URLs to download
- `destination_dir` (str): Directory to save downloaded files
- `max_concurrent` (int): Maximum concurrent downloads. Default: 3
- `retry_failed` (bool): Whether to retry failed downloads. Default: True

**Returns:**
- `dict`: Batch download results with success/failure status for each file

#### get_file_info()

Get information about a remote file without downloading it.

**Parameters:**
- `url` (str): URL of the file to inspect
- `follow_redirects` (bool): Whether to follow redirects. Default: True

**Returns:**
- `dict`: File information including size, content type, and last modified date

#### download_with_progress()

Download a file with real-time progress tracking.

**Parameters:**
- `url` (str): URL of the file to download
- `destination` (str): Local destination path
- `progress_callback` (callable, optional): Callback function for progress updates

**Returns:**
- `dict`: Download result with progress information and final status

#### validate_download()

Validate a downloaded file's integrity and security.

**Parameters:**
- `file_path` (str): Path to the downloaded file
- `expected_hash` (str, optional): Expected file hash for verification
- `hash_algorithm` (str): Hash algorithm to use. Default: 'sha256'

**Returns:**
- `dict`: Validation results including hash verification and security scan

## Usage Examples

```python
from agno.agent import Agent
from enhancedtoolkits import DownloaderTools

# Initialize with security settings
downloader = DownloaderTools(
    allowed_domains=['example.com', 'trusted-site.org'],
    max_file_size=52428800,  # 50MB
    enable_virus_scan=True
)

# Add to agent
agent = Agent(
    name="File Downloader",
    model="gpt-4",
    tools=[downloader]
)

# Agent can now download files safely
response = agent.run("Download the file from this URL and validate it")
```

## Security Features

- **Domain Validation**: Configurable allowed/blocked domains
- **Size Limits**: Configurable maximum file size limits
- **Virus Scanning**: Optional virus scanning of downloaded files
- **SSL Verification**: Configurable SSL certificate validation
- **Content Type Validation**: Verification of file types
- **Hash Verification**: File integrity checking with multiple algorithms

## Anti-Bot Features

- **Custom User Agents**: Configurable user agent strings
- **Header Spoofing**: Custom HTTP headers for bypassing restrictions
- **Cookie Support**: Session cookie handling
- **Retry Logic**: Intelligent retry mechanisms for failed downloads
- **Rate Limiting**: Built-in rate limiting to avoid detection

## Related Documentation

- [Downloader Tools Guide](../toolkits/downloader.md)
- [Files Tools API](files.md)
- [StrictToolkit Base](base.md)