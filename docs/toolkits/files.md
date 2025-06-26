# Files Tools for AI Agents

The Files Tools provide enterprise-grade file operations with comprehensive security controls for AI agents that need to interact with files safely.

## 🤖 AI Agent Setup

```python
from enhancedtoolkits import FilesTools

# Initialize for your AI agent
files = FilesTools(
    base_dir="/secure/workspace",           # Base directory for operations
    max_file_size=100*1024*1024,           # 100MB max file size
    max_chunk_size=10000,                  # Max lines per chunk
    allowed_extensions=[".txt", ".py", ".json", ".md", ".csv", ".log", ".yaml", ".yml", ".xml"]
)

# Register with your agent
agent.register_tools([files])
```

## ⚙️ Configuration Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `base_dir` | str | `None` | Base directory for all file operations |
| `max_file_size` | int | `100MB` | Maximum file size allowed |
| `max_chunk_size` | int | `10000` | Maximum lines per chunk operation |
| `max_line_length` | int | `10000` | Maximum characters per line |
| `allowed_extensions` | list | See below | Allowed file extensions |

**Default allowed extensions:** `.txt`, `.py`, `.js`, `.json`, `.md`, `.csv`, `.log`, `.yaml`, `.yml`, `.xml`

## 🔒 Available Functions

Your AI agent will have access to these secure file operations:

### `read_file_chunk()`
Read a chunk of lines from a file with security validation.

**Parameters:**
- `file_name`: Name of the file to read
- `offset`: Starting line number (0-based)
- `chunk_size`: Number of lines to read

### `edit_file_chunk()`
Replace lines in a file with atomic operations.

**Parameters:**
- `file_name`: Name of the file to edit
- `new_lines`: List of new lines to replace with
- `offset`: Starting line number
- `length`: Number of lines to replace

### `insert_file_chunk()`
Insert lines into a file with security validation.

**Parameters:**
- `file_name`: Name of the file
- `new_lines`: List of lines to insert
- `offset`: Position to insert at

### `delete_file_chunk()`
Delete lines from a file with atomic operations.

**Parameters:**
- `file_name`: Name of the file
- `offset`: Starting line number
- `length`: Number of lines to delete

### `save_file()`
Save content to a file with comprehensive security checks.

**Parameters:**
- `contents`: File content as string
- `file_name`: Name of the file
- `overwrite`: Whether to overwrite existing file

### `get_file_metadata()`
Get file metadata with security validation.

**Parameters:**
- `file_name`: Name of the file

### `list_files()`
List files with safety filtering.

**Parameters:**
- `pattern`: Glob pattern for file matching

## 🛡️ Security Features

### Path Traversal Protection
- Blocks `..`, `~`, `$` and other dangerous patterns
- Validates all paths against base directory
- Prevents access outside allowed directories

### File Type Validation
- Whitelist-based file extension filtering
- Content type validation
- Blocks executable and binary files

### Resource Limits
- Configurable file size limits
- Chunk size limitations
- Line length restrictions

### Atomic Operations
- All write operations use temporary files
- Atomic replacement prevents corruption
- File locking prevents race conditions

## 🎯 AI Agent Integration Examples

### OpenAI Function Calling
```python
import openai
from enhancedtoolkits import FilesTools

files = FilesTools(base_dir="/workspace")

# Get function schema for OpenAI
tools = [files.get_openai_schema()]

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{
        "role": "user", 
        "content": "Read the first 10 lines of config.json"
    }],
    tools=tools,
    tool_choice="auto"
)
```

### Agno Framework
```python
from agno.agent import Agent
from enhancedtoolkits import FilesTools

agent = Agent(
    name="File Manager",
    model="gpt-4",
    tools=[FilesTools(base_dir="/secure/workspace")]
)

# Agent can now safely interact with files
response = agent.run("List all Python files and show me the first few lines of main.py")
```

## 🔧 Production Configuration

### Basic Setup
```python
files = FilesTools()
```

### Secure Production Setup
```python
files = FilesTools(
    base_dir="/app/workspace",
    max_file_size=50*1024*1024,  # 50MB limit
    allowed_extensions=[".txt", ".json", ".csv", ".md"],
    max_chunk_size=5000
)
```

### Docker Environment
```python
files = FilesTools(
    base_dir="/app/data",
    max_file_size=10*1024*1024,  # 10MB for containers
    allowed_extensions=[".json", ".txt", ".csv"]
)
```

## 📁 Example Agent Interactions

**Agent Query:** "Read the configuration file and update the database URL"

**Files Tool Operations:**
1. `read_file_chunk("config.json", 0, 100)` - Read config file
2. `edit_file_chunk("config.json", ["new_db_url"], 5, 1)` - Update specific line
3. `get_file_metadata("config.json")` - Verify changes

**Agent Query:** "Create a summary of all log files from today"

**Files Tool Operations:**
1. `list_files("*.log")` - Find all log files
2. `read_file_chunk("app.log", 0, 1000)` - Read recent entries
3. `save_file("summary.txt", "summary_content")` - Save summary

## 🚨 Error Handling

The Files Tools provide detailed error messages for:
- **Security violations**: Path traversal attempts, unauthorized extensions
- **Resource limits**: File too large, chunk too big
- **File system errors**: Permission denied, file not found
- **Validation errors**: Invalid parameters, malformed paths

## 📊 Monitoring

Enable detailed logging for file operations:
```python
import logging
logging.basicConfig(level=logging.DEBUG)

files = FilesTools(base_dir="/workspace", debug=True)
```

## 🔍 Security Best Practices

1. **Set restrictive base_dir**: Limit file access to specific directories
2. **Use allowed_extensions**: Only allow necessary file types
3. **Set reasonable limits**: Configure appropriate file and chunk sizes
4. **Monitor operations**: Enable logging for security auditing
5. **Regular validation**: Periodically review file access patterns

## 🚀 Next Steps

1. **Configure** FilesTools with appropriate security settings
2. **Set base directory** to limit file access scope
3. **Define allowed extensions** based on your use case
4. **Register** with your AI agent framework
5. **Test** with sample file operations
6. **Monitor** file access patterns and security events

The Files Tools enable your AI agent to safely interact with files while maintaining enterprise-grade security controls and preventing common file system vulnerabilities.