# Files Tools API Reference

API documentation for the Files Tools toolkit - enterprise-grade file operations with comprehensive security controls.

## Class: FilesTools

Enterprise-grade file operations toolkit with security controls, validation, and comprehensive error handling.

### FilesTools()

Initialize the Files Tools toolkit.

**Parameters:**
- `allowed_extensions` (List[str], optional): Allowed file extensions. Default: ['.txt', '.json', '.csv', '.md']
- `blocked_extensions` (List[str], optional): Blocked file extensions. Default: ['.exe', '.bat', '.sh']
- `max_file_size` (int, optional): Maximum file size in bytes. Default: 10485760 (10MB)
- `enable_security_scan` (bool, optional): Enable security scanning. Default: True
- `scan_timeout` (int, optional): Security scan timeout in seconds. Default: 10

### Methods

#### read_file()

Read and return the contents of a file with security validation.

**Parameters:**
- `file_path` (str): Path to the file to read
- `encoding` (str): File encoding. Default: 'utf-8'
- `validate_content` (bool): Whether to validate file content. Default: True

**Returns:**
- `dict`: File contents and metadata including size, encoding, and validation status

#### write_file()

Write content to a file with security checks and validation.

**Parameters:**
- `file_path` (str): Path where to write the file
- `content` (str): Content to write to the file
- `encoding` (str): File encoding. Default: 'utf-8'
- `create_dirs` (bool): Create directories if they don't exist. Default: True

**Returns:**
- `dict`: Write operation result with file metadata

#### list_directory()

List contents of a directory with filtering and metadata.

**Parameters:**
- `directory_path` (str): Path to the directory to list
- `recursive` (bool): Whether to list recursively. Default: False
- `include_hidden` (bool): Whether to include hidden files. Default: False
- `filter_extensions` (List[str], optional): Filter by file extensions

**Returns:**
- `dict`: Directory contents with file metadata and statistics

#### copy_file()

Copy a file from source to destination with validation.

**Parameters:**
- `source_path` (str): Source file path
- `destination_path` (str): Destination file path
- `overwrite` (bool): Whether to overwrite existing files. Default: False
- `preserve_metadata` (bool): Whether to preserve file metadata. Default: True

**Returns:**
- `dict`: Copy operation result with source and destination metadata

#### move_file()

Move a file from source to destination with validation.

**Parameters:**
- `source_path` (str): Source file path
- `destination_path` (str): Destination file path
- `overwrite` (bool): Whether to overwrite existing files. Default: False

**Returns:**
- `dict`: Move operation result with operation details

#### delete_file()

Delete a file with safety checks and confirmation.

**Parameters:**
- `file_path` (str): Path to the file to delete
- `confirm_deletion` (bool): Require confirmation for deletion. Default: True
- `secure_delete` (bool): Use secure deletion method. Default: False

**Returns:**
- `dict`: Deletion operation result with confirmation details

#### get_file_info()

Get comprehensive information about a file.

**Parameters:**
- `file_path` (str): Path to the file
- `include_hash` (bool): Whether to calculate file hash. Default: False
- `hash_algorithm` (str): Hash algorithm to use. Default: 'sha256'

**Returns:**
- `dict`: Comprehensive file information including size, dates, permissions, and optional hash

## Usage Examples

```python
from agno.agent import Agent
from enhancedtoolkits import FilesTools

# Initialize with security settings
files = FilesTools(
    allowed_extensions=['.txt', '.json', '.csv', '.md'],
    max_file_size=10485760,  # 10MB
    enable_security_scan=True
)

# Add to agent
agent = Agent(
    name="File Manager",
    model="gpt-4",
    tools=[files]
)

# Agent can now perform file operations
response = agent.run("Read the contents of data.txt and analyze it")
```

## Security Features

- **Extension Validation**: Configurable allowed/blocked file extensions
- **Size Limits**: Configurable maximum file size limits
- **Content Scanning**: Optional security scanning of file contents
- **Path Validation**: Protection against directory traversal attacks
- **Permission Checks**: Validation of file system permissions
- **Secure Deletion**: Optional secure file deletion methods

## Related Documentation

- [Files Tools Guide](../toolkits/files.md)
- [StrictToolkit Base](base.md)
- [Security Best Practices](../developer/contributing.md)