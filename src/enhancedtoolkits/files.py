"""
Enhanced Files Tools v2.0

Provides robust, secure file operations with comprehensive security controls,
resource limits, and proper error handling for LLM interactions.

Author: malvavisc0
License: MIT
Version: 2.0.0
"""

import fcntl
import json
import mimetypes
import os
import re
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from agno.utils.log import log_error, log_info

from .base import StrictToolkit


class FileSecurityError(Exception):
    """Raised when file operation violates security constraints."""

    pass


class FileOperationError(Exception):
    """Raised when file operation fails."""

    pass


class EnhancedFilesTools(StrictToolkit):
    """
    Secure toolkit for file operations with comprehensive security controls.
    """

    # Security configuration
    MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
    MAX_CHUNK_SIZE = 10000  # lines
    MAX_LINE_LENGTH = 10000  # characters
    ALLOWED_EXTENSIONS = {
        ".txt",
        ".py",
        ".js",
        ".json",
        ".md",
        ".csv",
        ".log",
        ".yaml",
        ".yml",
        ".xml",
    }
    BLOCKED_PATTERNS = {"..", "~", "$", "`", ";", "|", "&", "<", ">"}

    def __init__(self, base_dir: Optional[Path] = None, **kwargs):
        self.base_dir = Path(base_dir).resolve() if base_dir else Path.cwd().resolve()
        self.add_instructions = True
        self.instructions = EnhancedFilesTools.get_llm_usage_instructions()

        super().__init__(name="secure_files_toolkit", **kwargs)
        self.register(self.read_file_lines_chunk)
        self.register(self.replace_file_lines_chunk)
        self.register(self.insert_lines_into_file_chunk)
        self.register(self.delete_lines_from_file_chunk)
        self.register(self.save_file_with_validation)
        self.register(self.retrieve_file_metadata)
        self.register(self.list_files_with_pattern)
        self.register(self.search_files_by_name_regex)
        self.register(self.search_file_contents_by_regex)

    def read_file_lines_chunk(
        self, file_name: str, chunk_size: int = 100, offset: int = 0
    ) -> str:
        """Read a chunk of lines from a file with security validation."""
        try:
            self._validate_inputs(file_name, chunk_size=chunk_size, offset=offset)
            file_path = self._secure_resolve_path(file_name)

            with self._secure_file_lock(file_path, "r") as f:
                lines = self._stream_read_lines(f, offset, chunk_size)
                total_lines = self._count_lines_efficiently(file_path)

            result = {
                "operation": "read_file_chunk",
                "result": lines,
                "metadata": {
                    "start_line": offset,
                    "lines_read": len(lines),
                    "total_lines": total_lines,
                    "eof": offset + len(lines) >= total_lines,
                    "timestamp": self._timestamp(),
                },
            }
            log_info(f"Read {len(lines)} lines from {file_name}")
            return self._safe_json(result)
        except Exception as e:
            return self._error_response("read_file_chunk", file_name, e)

    def replace_file_lines_chunk(
        self, file_name: str, new_lines: List[str], offset: int, length: int
    ) -> str:
        """Replace lines with security validation and atomic operations."""
        try:
            self._validate_inputs(
                file_name, new_lines=new_lines, offset=offset, length=length
            )
            file_path = self._secure_resolve_path(file_name)

            with tempfile.NamedTemporaryFile(
                mode="w", delete=False, suffix=".tmp"
            ) as tmp_file:
                with self._secure_file_lock(file_path, "r") as src:
                    self._atomic_edit(src, tmp_file, new_lines, offset, length)

                # Atomic replace
                os.replace(tmp_file.name, file_path)

            result = {
                "operation": "edit_file_chunk",
                "result": f"Replaced {length} lines at offset {offset}",
                "metadata": {"timestamp": self._timestamp()},
            }
            log_info(f"Edited {file_name}: replaced {length} lines at {offset}")
            return self._safe_json(result)
        except Exception as e:
            return self._error_response("edit_file_chunk", file_name, e)

    def insert_lines_into_file_chunk(self, file_name: str, new_lines: List[str], offset: int) -> str:
        """Insert lines with security validation."""
        try:
            self._validate_inputs(file_name, new_lines=new_lines, offset=offset)
            file_path = self._secure_resolve_path(file_name)

            with tempfile.NamedTemporaryFile(
                mode="w", delete=False, suffix=".tmp"
            ) as tmp_file:
                with self._secure_file_lock(file_path, "r") as src:
                    self._atomic_insert(src, tmp_file, new_lines, offset)

                os.replace(tmp_file.name, file_path)

            result = {
                "operation": "insert_file_chunk",
                "result": f"Inserted {len(new_lines)} lines at offset {offset}",
                "metadata": {"timestamp": self._timestamp()},
            }
            log_info(f"Inserted {len(new_lines)} lines in {file_name}")
            return self._safe_json(result)
        except Exception as e:
            return self._error_response("insert_file_chunk", file_name, e)

    def delete_lines_from_file_chunk(self, file_name: str, offset: int, length: int) -> str:
        """Delete lines with security validation."""
        try:
            self._validate_inputs(file_name, offset=offset, length=length)
            file_path = self._secure_resolve_path(file_name)

            with tempfile.NamedTemporaryFile(
                mode="w", delete=False, suffix=".tmp"
            ) as tmp_file:
                with self._secure_file_lock(file_path, "r") as src:
                    self._atomic_delete(src, tmp_file, offset, length)

                os.replace(tmp_file.name, file_path)

            result = {
                "operation": "delete_file_chunk",
                "result": f"Deleted {length} lines at offset {offset}",
                "metadata": {"timestamp": self._timestamp()},
            }
            log_info(f"Deleted {length} lines from {file_name}")
            return self._safe_json(result)
        except Exception as e:
            return self._error_response("delete_file_chunk", file_name, e)

    def save_file_with_validation(self, contents: str, file_name: str, overwrite: bool = True) -> str:
        """Save file with security validation."""
        try:
            self._validate_inputs(file_name, contents=contents)
            file_path = self._secure_resolve_path(file_name)

            if file_path.exists() and not overwrite:
                raise FileOperationError("File exists and overwrite is False")

            file_path.parent.mkdir(parents=True, exist_ok=True)

            with tempfile.NamedTemporaryFile(
                mode="w", delete=False, suffix=".tmp", dir=file_path.parent
            ) as tmp_file:
                tmp_file.write(contents)
                tmp_file.flush()
                os.fsync(tmp_file.fileno())

            os.replace(tmp_file.name, file_path)

            result = {
                "operation": "save_file",
                "result": f"Saved file {file_name}",
                "metadata": {
                    "file_size": file_path.stat().st_size,
                    "timestamp": self._timestamp(),
                },
            }
            log_info(f"Saved file {file_name}")
            return self._safe_json(result)
        except Exception as e:
            return self._error_response("save_file", file_name, e)

    def retrieve_file_metadata(self, file_name: str) -> str:
        """Get file metadata with security validation."""
        try:
            self._validate_inputs(file_name)
            file_path = self._secure_resolve_path(file_name)

            stat = file_path.stat()
            line_count = self._count_lines_efficiently(file_path)

            result = {
                "operation": "get_file_metadata",
                "result": {
                    "file_name": file_name,
                    "total_lines": line_count,
                    "file_size": stat.st_size,
                    "mime_type": mimetypes.guess_type(file_name)[0],
                },
                "metadata": {"timestamp": self._timestamp()},
            }
            return self._safe_json(result)
        except Exception as e:
            return self._error_response("get_file_metadata", file_name, e)

    def list_files_with_pattern(self, pattern: str = "**/*") -> str:
        """List files with security validation."""
        try:
            files = []
            for p in self.base_dir.glob(pattern):
                if p.is_file() and self._is_safe_file(p):
                    rel_path = str(p.relative_to(self.base_dir))
                    files.append(rel_path)
                    if len(files) > 1000:  # Limit results
                        break

            result = {
                "operation": "list_files",
                "result": sorted(files),
                "metadata": {"file_count": len(files), "timestamp": self._timestamp()},
            }
            return self._safe_json(result)
        except Exception as e:
            return self._error_response("list_files", str(self.base_dir), e)

    # Security and validation methods

    def _validate_inputs(self, file_name: str, **kwargs):
        """Comprehensive input validation."""
        if not file_name or not isinstance(file_name, str):
            raise FileSecurityError("Invalid file name")

        if any(pattern in file_name for pattern in self.BLOCKED_PATTERNS):
            raise FileSecurityError("File name contains blocked patterns")

        if kwargs.get("chunk_size", 0) > self.MAX_CHUNK_SIZE:
            raise FileSecurityError(f"Chunk size exceeds limit: {self.MAX_CHUNK_SIZE}")

        if kwargs.get("offset", 0) < 0 or kwargs.get("length", 0) < 0:
            raise FileSecurityError("Negative offset or length not allowed")

        if "contents" in kwargs and len(kwargs["contents"]) > self.MAX_FILE_SIZE:
            raise FileSecurityError(f"Content size exceeds limit: {self.MAX_FILE_SIZE}")

        if "new_lines" in kwargs:
            for line in kwargs["new_lines"]:
                if len(line) > self.MAX_LINE_LENGTH:
                    raise FileSecurityError(
                        f"Line length exceeds limit: {self.MAX_LINE_LENGTH}"
                    )

    def _secure_resolve_path(self, file_name: str) -> Path:
        """Secure path resolution with comprehensive validation."""
        try:
            # Normalize and resolve path
            file_path = (self.base_dir / file_name).resolve()

            # Check if path is within base directory
            if not str(file_path).startswith(str(self.base_dir)):
                raise FileSecurityError("Path traversal attempt detected")

            # Check for symlinks
            if file_path.is_symlink():
                raise FileSecurityError("Symlinks not allowed")

            # Validate file extension
            if file_path.suffix.lower() not in self.ALLOWED_EXTENSIONS:
                raise FileSecurityError(f"File type not allowed: {file_path.suffix}")

            return file_path
        except Exception as e:
            raise FileSecurityError(f"Path resolution failed: {e}")

    def _secure_file_lock(self, file_path: Path, mode: str):
        """Secure file locking context manager."""

        class FileLock:
            def __init__(self, path, mode):
                self.path = path
                self.mode = mode
                self.file = None

            def __enter__(self):
                self.file = open(self.path, self.mode, encoding="utf-8")
                fcntl.flock(self.file.fileno(), fcntl.LOCK_EX)
                return self.file

            def __exit__(self, exc_type, exc_val, exc_tb):
                if self.file:
                    fcntl.flock(self.file.fileno(), fcntl.LOCK_UN)
                    self.file.close()

        return FileLock(file_path, mode)

    def _stream_read_lines(self, file_obj, offset: int, chunk_size: int) -> List[str]:
        """Memory-efficient line reading."""
        lines = []
        current_line = 0

        for line in file_obj:
            if current_line >= offset:
                if len(lines) >= chunk_size:
                    break
                lines.append(line.rstrip("\n\r"))
            current_line += 1

        return lines

    def _count_lines_efficiently(self, file_path: Path) -> int:
        """Memory-efficient line counting."""
        count = 0
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                count += chunk.count(b"\n")
        return count

    def _atomic_edit(
        self, src_file, tmp_file, new_lines: List[str], offset: int, length: int
    ):
        """Atomic edit operation."""
        current_line = 0
        lines_skipped = 0

        for line in src_file:
            if current_line < offset:
                # Write lines before the edit point
                tmp_file.write(line)
            elif current_line == offset:
                # Write new lines at the edit point
                for new_line in new_lines:
                    tmp_file.write(new_line + "\n")
                # Skip this line (it's being replaced)
                lines_skipped = 1
            elif lines_skipped < length:
                # Skip lines that are being replaced
                lines_skipped += 1
            else:
                # Write lines after the edit range
                tmp_file.write(line)
            current_line += 1

    def _atomic_insert(self, src_file, tmp_file, new_lines: List[str], offset: int):
        """Atomic insert operation."""
        current_line = 0
        inserted = False

        for line in src_file:
            if current_line == offset and not inserted:
                # Insert new lines at the specified offset
                for new_line in new_lines:
                    tmp_file.write(new_line + "\n")
                inserted = True
            tmp_file.write(line)
            current_line += 1

        # Handle insertion at end of file
        if not inserted and current_line == offset:
            for new_line in new_lines:
                tmp_file.write(new_line + "\n")

    def _atomic_delete(self, src_file, tmp_file, offset: int, length: int):
        """Atomic delete operation."""
        current_line = 0
        for line in src_file:
            if not (offset <= current_line < offset + length):
                tmp_file.write(line)
            current_line += 1

    def _is_safe_file(self, file_path: Path) -> bool:
        """Check if file is safe to access."""
        try:
            return (
                file_path.suffix.lower() in self.ALLOWED_EXTENSIONS
                and not file_path.is_symlink()
                and file_path.stat().st_size <= self.MAX_FILE_SIZE
            )
        except (OSError, PermissionError, FileNotFoundError):
            return False

    def _safe_json(self, data: Dict[str, Any]) -> str:
        """Safe JSON serialization."""
        try:
            return json.dumps(data, ensure_ascii=False, indent=2)
        except Exception as e:
            log_error(f"JSON serialization error: {e}")
            return json.dumps({"error": "Serialization failed"})

    def _error_response(self, operation: str, file_name: str, exc: Exception) -> str:
        """Secure error response without information disclosure."""
        if isinstance(exc, FileSecurityError):
            error_msg = f"Security validation failed: {str(exc)}"
        elif isinstance(exc, FileOperationError):
            error_msg = f"File operation failed: {str(exc)}"
        elif isinstance(exc, (OSError, PermissionError)):
            error_msg = "File access denied or not found"
        else:
            error_msg = f"Unexpected error: {str(exc)}"

        log_error(f"{operation} failed for {file_name}: {exc}")
        return self._safe_json(
            {
                "operation": operation,
                "result": None,
                "metadata": {"error": error_msg, "timestamp": self._timestamp()},
            }
        )

    def _timestamp(self) -> str:
        """Generate ISO timestamp."""
        return datetime.now().isoformat()

    def _validate_regex(self, regex_pattern: str):
        """
        Validate regex pattern for security.

        Args:
            regex_pattern (str): The regex pattern to validate

        Raises:
            FileSecurityError: If the pattern is invalid or potentially dangerous
        """
        if not regex_pattern or not isinstance(regex_pattern, str):
            raise FileSecurityError("Invalid regex pattern")

        if len(regex_pattern) > 1000:
            raise FileSecurityError("Regex pattern too long")

        # Check for potentially dangerous patterns
        dangerous_patterns = [
            r"(?:){2,}",  # Nested quantifiers that can cause catastrophic backtracking
            r"(\w+)*\1",  # Backreferences with quantifiers that can cause exponential backtracking
        ]

        for dp in dangerous_patterns:
            if dp in regex_pattern:
                raise FileSecurityError(f"Potentially dangerous regex pattern detected")

        # Validate regex compilation
        try:
            re.compile(regex_pattern)
        except re.error as e:
            raise FileSecurityError(f"Invalid regex pattern: {e}")

    def search_files_by_name_regex(
        self, regex_pattern: str, recursive: bool = True, max_results: int = 1000
    ) -> str:
        """
        Search for files with names matching a regex pattern with security validation.

        Args:
            regex_pattern (str): Regular expression pattern to match against file names
            recursive (bool, optional): Whether to search recursively in subdirectories. Defaults to True.
            max_results (int, optional): Maximum number of results to return. Defaults to 1000.

        Returns:
            str: JSON string containing the search results and metadata
        """
        try:
            # Validate regex pattern
            self._validate_regex(regex_pattern)

            pattern = re.compile(regex_pattern)

            files = []
            search_path = self.base_dir

            # Use walk for recursive search or listdir for non-recursive
            if recursive:
                for root, _, filenames in os.walk(search_path):
                    for filename in filenames:
                        file_path = Path(root) / filename
                        if self._is_safe_file(file_path) and pattern.search(filename):
                            rel_path = str(file_path.relative_to(self.base_dir))
                            files.append(rel_path)
                            if len(files) >= max_results:  # Limit results
                                break
                    if len(files) >= max_results:
                        break
            else:
                for item in search_path.iterdir():
                    if (
                        item.is_file()
                        and self._is_safe_file(item)
                        and pattern.search(item.name)
                    ):
                        rel_path = str(item.relative_to(self.base_dir))
                        files.append(rel_path)
                        if len(files) >= max_results:  # Limit results
                            break

            result = {
                "operation": "search_files_by_name",
                "result": sorted(files),
                "metadata": {
                    "file_count": len(files),
                    "pattern": regex_pattern,
                    "recursive": recursive,
                    "timestamp": self._timestamp(),
                },
            }
            log_info(f"Found {len(files)} files matching pattern '{regex_pattern}'")
            return self._safe_json(result)
        except Exception as e:
            return self._error_response("search_files_by_name", str(self.base_dir), e)

    def search_file_contents_by_regex(
        self,
        regex_pattern: str,
        file_pattern: str = "**/*",
        recursive: bool = False,
        max_files: int = 100,
        max_matches: int = 1000,
        context_lines: int = 2,
    ) -> str:
        """
        Search for content inside files matching a regex pattern with security validation.

        Args:
            regex_pattern (str): Regular expression pattern to match against file content
            file_pattern (str, optional): Glob pattern to filter files. Defaults to "**/*".
            recursive (bool, optional): Whether to search recursively in subdirectories. Defaults to False.
            max_files (int, optional): Maximum number of files to search. Defaults to 100.
            max_matches (int, optional): Maximum number of matches to return. Defaults to 1000.
            context_lines (int, optional): Number of context lines to include before and after match. Defaults to 2.

        Returns:
            str: JSON string containing the search results and metadata
        """
        try:
            # Validate regex pattern
            self._validate_regex(regex_pattern)

            pattern = re.compile(regex_pattern)

            matches = []
            files_searched = 0
            total_matches = 0

            # Get files matching the file pattern
            if recursive:
                file_paths = self.base_dir.glob(file_pattern)
            else:
                # For non-recursive search, ensure the pattern doesn't contain directory traversal
                if "**" in file_pattern:
                    # Replace ** with * for non-recursive search
                    file_pattern = file_pattern.replace("**", "*")
                file_paths = self.base_dir.glob(file_pattern)

            for file_path in file_paths:
                if not (file_path.is_file() and self._is_safe_file(file_path)):
                    continue

                files_searched += 1
                if files_searched > max_files:
                    break

                rel_path = str(file_path.relative_to(self.base_dir))

                # Search inside the file
                try:
                    with self._secure_file_lock(file_path, "r") as f:
                        lines = f.readlines()

                    file_matches = []
                    for i, line in enumerate(lines):
                        if pattern.search(line):
                            # Get context lines
                            start = max(0, i - context_lines)
                            end = min(len(lines), i + context_lines + 1)

                            context = {
                                "line_number": i + 1,
                                "content": line.rstrip("\n\r"),
                                "context": [
                                    lines[j].rstrip("\n\r") for j in range(start, end)
                                ],
                            }

                            file_matches.append(context)
                            total_matches += 1

                            if total_matches >= max_matches:
                                break

                    if file_matches:
                        matches.append({"file": rel_path, "matches": file_matches})

                    if total_matches >= max_matches:
                        break

                except Exception as file_error:
                    # Skip files with errors
                    log_error(f"Error searching file {rel_path}: {file_error}")
                    continue

            result = {
                "operation": "search_inside_files",
                "result": matches,
                "metadata": {
                    "files_searched": files_searched,
                    "total_matches": total_matches,
                    "pattern": regex_pattern,
                    "recursive": recursive,
                    "timestamp": self._timestamp(),
                },
            }
            log_info(
                f"Found {total_matches} matches in {files_searched} files for pattern '{regex_pattern}'"
            )
            return self._safe_json(result)
        except Exception as e:
            return self._error_response("search_inside_files", str(self.base_dir), e)

    @staticmethod
    def get_llm_usage_instructions() -> str:
        """
        Returns detailed instructions for LLMs on how to use each tool in EnhancedFilesTools.
        Each instruction includes the method name, description, parameters, types, example values, and security notes.
        """
        instructions = """
<file_tools_instructions>
*** Secure Files Toolkit Instructions ***

This toolkit provides robust, secure file operations for LLMs. All operations are subject to strict security validation, resource limits, and atomicity guarantees. Use the following tools:

- read_file_lines_chunk: Read a chunk of lines from a file.
   Parameters:
      - file_name (str): File path, e.g., "data/example.txt"
      - chunk_size (int, optional): Number of lines to read (default: 100, max: 10000)
      - offset (int, optional): Line offset to start reading from (default: 0)
   Notes: Only certain file types are allowed (.txt, .py, .js, .json, .md, .csv, .log, .yaml, .yml, .xml), max file size 100MB.

- replace_file_lines_chunk: Replace lines in a file atomically.
   Parameters:
      - file_name (str): File path, e.g., "notes.md"
      - new_lines (List[str]): List of new lines to write, e.g., ["line1", "line2"]
      - offset (int): Line offset to start replacing, e.g., 10
      - length (int): Number of lines to replace, e.g., 2

- insert_lines_into_file_chunk: Insert lines at a specific offset.
   Parameters:
      - file_name (str): File path, e.g., "script.py"
      - new_lines (List[str]): Lines to insert, e.g., ["import os"]
      - offset (int): Line offset to insert at, e.g., 5

- delete_lines_from_file_chunk: Delete lines from a file.
   Parameters:
      - file_name (str): File path, e.g., "data.csv"
      - offset (int): Line offset to start deleting, e.g., 20
      - length (int): Number of lines to delete, e.g., 3

- save_file_with_validation: Save contents to a file with validation.
   Parameters:
      - contents (str): File contents, e.g., "# Title\nContent"
      - file_name (str): File path, e.g., "output.txt"
      - overwrite (bool, optional): Overwrite if file exists (default: True)

- retrieve_file_metadata: Get metadata for a file.
   Parameters:
      - file_name (str): File path, e.g., "report.json"

- list_files_with_pattern: List files matching a pattern.
   Parameters:
      - pattern (str, optional): Glob pattern (default: "**/*"), e.g., "*.py"

- search_files_by_name_regex: Search for files with names matching a regex pattern.
   Parameters:
      - regex_pattern (str): Regular expression pattern
      - recursive (bool, optional): Whether to search recursively (default: True)
      - max_results (int, optional): Maximum number of results to return (default: 1000)

- search_file_contents_by_regex: Search for content inside files matching a regex pattern.
   Parameters:
      - regex_pattern (str): Regular expression pattern
      - file_pattern (str, optional): Glob pattern to filter files (default: "**/*")
      - recursive (bool, optional): Whether to search recursively (default: False)
      - max_files (int, optional): Maximum number of files to search (default: 100)
      - max_matches (int, optional): Maximum number of matches to return (default: 1000)
      - context_lines (int, optional): Number of context lines to include (default: 2)

**Security Notes:**
- Allowed extensions: .txt, .py, .js, .json, .md, .csv, .log, .yaml, .yml, .xml
- Max file size: 100MB
- Max chunk size: 10000 lines
- Max line length: 10000 characters
- Blocked patterns: "..", "~", "$", "`", ";", "|", "&", "<", ">"
- All operations are atomic and errors are returned in a secure, non-leaky format.
- All file operations are subject to comprehensive validation and security checks.

</file_tools_instructions>
"""
        return instructions
