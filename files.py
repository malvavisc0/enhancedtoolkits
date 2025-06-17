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
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from agno.tools.toolkit import Toolkit
from agno.utils.log import log_error, log_info


class FileSecurityError(Exception):
    """Raised when file operation violates security constraints."""

    pass


class FileOperationError(Exception):
    """Raised when file operation fails."""

    pass


class EnhancedFilesTools(Toolkit):
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
        super().__init__(name="secure_files_toolkit", **kwargs)
        self.register(self.read_file_chunk)
        self.register(self.edit_file_chunk)
        self.register(self.insert_file_chunk)
        self.register(self.delete_file_chunk)
        self.register(self.save_file)
        self.register(self.get_file_metadata)
        self.register(self.list_files)

    def read_file_chunk(
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

    def edit_file_chunk(
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

    def insert_file_chunk(self, file_name: str, new_lines: List[str], offset: int) -> str:
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

    def delete_file_chunk(self, file_name: str, offset: int, length: int) -> str:
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

    def save_file(self, contents: str, file_name: str, overwrite: bool = True) -> str:
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

    def get_file_metadata(self, file_name: str) -> str:
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

    def list_files(self, pattern: str = "**/*") -> str:
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
        for line in src_file:
            if current_line < offset:
                tmp_file.write(line)
            elif current_line == offset:
                for new_line in new_lines:
                    tmp_file.write(new_line + "\n")
                # Skip 'length' lines
                for _ in range(length - 1):
                    next(src_file, None)
                    current_line += 1
            elif current_line >= offset + length:
                tmp_file.write(line)
            current_line += 1

    def _atomic_insert(self, src_file, tmp_file, new_lines: List[str], offset: int):
        """Atomic insert operation."""
        current_line = 0
        for line in src_file:
            if current_line == offset:
                for new_line in new_lines:
                    tmp_file.write(new_line + "\n")
            tmp_file.write(line)
            current_line += 1

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
        except:
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
        error_msg = "Operation failed" if isinstance(exc, FileSecurityError) else str(exc)
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

    @staticmethod
    def get_llm_usage_instructions() -> str:
        """
        Returns detailed instructions for LLMs on how to use each tool in EnhancedFilesTools.
        Each instruction includes the method name, description, parameters, types, example values, and security notes.
        """
        instructions = """
*** Secure Files Toolkit Instructions ***

This toolkit provides robust, secure file operations for LLMs. All operations are subject to strict security validation, resource limits, and atomicity guarantees. Use the following tools:

- read_file_chunk: Read a chunk of lines from a file.
   Parameters:
      - file_name (str): File path, e.g., "data/example.txt"
      - chunk_size (int, optional): Number of lines to read (default: 100, max: 10000)
      - offset (int, optional): Line offset to start reading from (default: 0)
   Notes: Only certain file types are allowed (.txt, .py, .js, .json, .md, .csv, .log, .yaml, .yml, .xml), max file size 100MB.

- edit_file_chunk: Replace lines in a file atomically.
   Parameters:
      - file_name (str): File path, e.g., "notes.md"
      - new_lines (List[str]): List of new lines to write, e.g., ["line1", "line2"]
      - offset (int): Line offset to start replacing, e.g., 10
      - length (int): Number of lines to replace, e.g., 2

- insert_file_chunk: Insert lines at a specific offset.
   Parameters:
      - file_name (str): File path, e.g., "script.py"
      - new_lines (List[str]): Lines to insert, e.g., ["import os"]
      - offset (int): Line offset to insert at, e.g., 5

- delete_file_chunk: Delete lines from a file.
   Parameters:
      - file_name (str): File path, e.g., "data.csv"
      - offset (int): Line offset to start deleting, e.g., 20
      - length (int): Number of lines to delete, e.g., 3

- save_file: Save contents to a file.
   Parameters:
      - contents (str): File contents, e.g., "# Title\nContent"
      - file_name (str): File path, e.g., "output.txt"
      - overwrite (bool, optional): Overwrite if file exists (default: True)

- get_file_metadata: Get metadata for a file.
   Parameters:
      - file_name (str): File path, e.g., "report.json"

- list_files: List files matching a pattern.
   Parameters:
      - pattern (str, optional): Glob pattern (default: "**/*"), e.g., "*.py"

**Security Notes:**
- Allowed extensions: .txt, .py, .js, .json, .md, .csv, .log, .yaml, .yml, .xml
- Max file size: 100MB
- Max chunk size: 10000 lines
- Max line length: 10000 characters
- Blocked patterns: "..", "~", "$", "`", ";", "|", "&", "<", ">"
- All operations are atomic and errors are returned in a secure, non-leaky format.
- All file operations are subject to comprehensive validation and security checks.
"""
        return instructions
