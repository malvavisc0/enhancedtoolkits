# Files Tools

The [`FilesTools`](../api/files.md) toolkit provides **sandboxed file operations** intended for AI agents.

Key properties:

- Enforces a base directory (`base_dir`) and blocks path traversal
- Blocks symlinks
- Enforces an extension allowlist and size limits
- Uses atomic writes for edits

All public functions return **JSON strings** with:

- `operation`: string
- `result`: payload or `null`
- `metadata`: includes timestamps; on failures includes a sanitized `metadata.error`

## 🤖 AI Agent Setup (Agno)

```python
from agno.agent import Agent
from enhancedtoolkits import FilesTools

agent = Agent(
    name="File Manager",
    model="gpt-4",
    tools=[FilesTools(base_dir="/app/workspace")],
)
```

## ⚙️ Configuration

Constructor parameters for `FilesTools`:

| Parameter | Type | Default | Notes |
|---|---:|---:|---|
| `base_dir` | `pathlib.Path \| None` | `Path.cwd()` | All file operations resolve under this directory |

### Built-in safety limits

These are currently defined as class constants in `FilesTools`:

- Max file size: `100MB`
- Max chunk size: `10000` lines
- Max line length: `10000` characters
- Allowed extensions: `.txt`, `.py`, `.js`, `.json`, `.md`, `.csv`, `.log`, `.yaml`, `.yml`, `.xml`

## 🔒 Available Functions

### Read / write / edit (chunked)

- `read_file_lines_chunk(file_name, chunk_size=100, offset=0)`
- `replace_file_lines_chunk(file_name, new_lines, offset, length)`
- `insert_lines_into_file_chunk(file_name, new_lines, offset)`
- `delete_lines_from_file_chunk(file_name, offset, length)`
- `save_file_with_validation(contents, file_name, overwrite=True)`

### Metadata / discovery

- `retrieve_file_metadata(file_name)`
- `list_files_with_pattern(pattern='**/*')`
- `search_files_by_name_regex(regex_pattern, recursive=True, max_results=1000)`
- `search_file_contents_by_regex(regex_pattern, file_pattern='**/*', recursive=False, max_files=100, max_matches=1000, context_lines=2)`

## ✅ Examples

### Read a chunk

```python
from enhancedtoolkits import FilesTools

files = FilesTools(base_dir="/app/workspace")
chunk_json = files.read_file_lines_chunk(
    file_name="notes.md",
    offset=0,
    chunk_size=50,
)
```

### Edit a specific region

```python
files.replace_file_lines_chunk(
    file_name="notes.md",
    new_lines=["# Updated title"],
    offset=0,
    length=1,
)
```

## API Reference

- [`docs/api/files.md`](../api/files.md)
