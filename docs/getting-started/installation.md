# Installation

Enhanced Toolkits supports Python 3.8+ and can be installed directly from GitHub with optional dependencies for specific features.

## Requirements

- **Python**: 3.8 or higher
- **Agno Framework**: Latest version
- **Operating System**: Windows, macOS, Linux

## Installation Methods

### Basic Installation

Install with core dependencies only:

```bash
pip install git+https://github.com/malvavisc0/enhancedtoolkits.git
```

This includes:
- Core toolkit functionality
- Basic HTTP client (`httpx`)
- Financial data access (`yfinance`)

### Full Installation (Recommended)

Install with all optional dependencies:

```bash
pip install "enhancedtoolkits[full] @ git+https://github.com/malvavisc0/enhancedtoolkits.git"
```

This includes everything from basic installation plus:
- YouTube transcript support (`youtube-transcript-api`)
- Content parsing (`markitdown`)
- Weather data (`pywttr`, `pywttr-models`)
- Enhanced validation (`pydantic`)

### Selective Installation

Install with specific optional dependencies:

=== "YouTube Support"
    ```bash
    pip install "enhancedtoolkits[youtube] @ git+https://github.com/malvavisc0/enhancedtoolkits.git"
    ```

=== "Content Processing"
    ```bash
    pip install "enhancedtoolkits[content] @ git+https://github.com/malvavisc0/enhancedtoolkits.git"
    ```

=== "Weather Data"
    ```bash
    pip install "enhancedtoolkits[weather] @ git+https://github.com/malvavisc0/enhancedtoolkits.git"
    ```

=== "Development Tools"
    ```bash
    pip install "enhancedtoolkits[dev] @ git+https://github.com/malvavisc0/enhancedtoolkits.git"
    ```

## Dependency Groups

| Group | Dependencies | Purpose |
|-------|-------------|---------|
| `full` | All optional dependencies | Complete functionality |
| `youtube` | `youtube-transcript-api` | YouTube video transcripts |
| `content` | `markitdown` | Content parsing and conversion |
| `weather` | `pywttr`, `pywttr-models`, `pydantic` | Weather data access |
| `dev` | Testing and development tools | Development workflow |

## Verification

Verify your installation:

```python
import enhancedtoolkits

# Check version
print(enhancedtoolkits.__version__)

# Test basic import
from enhancedtoolkits import (
    ReasoningTools,
    SearxngTools,
    CalculatorTools
)

print("✅ Enhanced Toolkits installed successfully!")
```

## Virtual Environment (Recommended)

We recommend using a virtual environment:

=== "venv"
    ```bash
    # Create virtual environment
    python -m venv enhanced-toolkits-env
    
    # Activate (Linux/macOS)
    source enhanced-toolkits-env/bin/activate
    
    # Activate (Windows)
    enhanced-toolkits-env\Scripts\activate
    
    # Install Enhanced Toolkits
    pip install "enhancedtoolkits[full] @ git+https://github.com/malvavisc0/enhancedtoolkits.git"
    ```

=== "conda"
    ```bash
    # Create conda environment
    conda create -n enhanced-toolkits python=3.11
    
    # Activate environment
    conda activate enhanced-toolkits
    
    # Install Enhanced Toolkits
    pip install "enhancedtoolkits[full] @ git+https://github.com/malvavisc0/enhancedtoolkits.git"
    ```

=== "poetry"
    ```bash
    # Initialize poetry project
    poetry init
    
    # Add Enhanced Toolkits
    poetry add "git+https://github.com/malvavisc0/enhancedtoolkits.git#egg=enhancedtoolkits[full]"
    
    # Install dependencies
    poetry install
    ```

## Docker Installation

Use Enhanced Toolkits in a Docker container:

```dockerfile
FROM python:3.11-slim

# Install Enhanced Toolkits
RUN pip install "enhancedtoolkits[full] @ git+https://github.com/malvavisc0/enhancedtoolkits.git"

# Your application code
COPY . /app
WORKDIR /app

CMD ["python", "your_app.py"]
```

## Troubleshooting

### Common Issues

**Import Error**: `ModuleNotFoundError: No module named 'enhancedtoolkits'`
```bash
# Ensure you're in the correct environment
pip list | grep enhancedtoolkits

# Reinstall if necessary
pip uninstall enhancedtoolkits
pip install "enhancedtoolkits[full] @ git+https://github.com/malvavisc0/enhancedtoolkits.git"
```

**YouTube Transcript Error**: `ModuleNotFoundError: No module named 'youtube_transcript_api'`
```bash
# Install YouTube support
pip install "enhancedtoolkits[youtube] @ git+https://github.com/malvavisc0/enhancedtoolkits.git"
```

**Weather Data Error**: `ModuleNotFoundError: No module named 'pywttr'`
```bash
# Install weather support
pip install "enhancedtoolkits[weather] @ git+https://github.com/malvavisc0/enhancedtoolkits.git"
```

### System Requirements

**Minimum System Requirements**:
- RAM: 512MB available
- Disk Space: 100MB for full installation
- Network: Internet connection for external APIs

**Recommended System Requirements**:
- RAM: 2GB available
- Disk Space: 500MB for development
- Network: Stable internet connection

## Next Steps

After installation:

1. **[Quick Start Guide](quick-start.md)** - Build your first Enhanced Toolkits application
2. **[Configuration](configuration.md)** - Set up environment variables and options
3. **[Core Toolkits](../toolkits/index.md)** - Explore available toolkits

## Getting Help

If you encounter installation issues:

<!-- - 📖 Check our [FAQ](../developer/faq.md) -->
- 🐛 [Report an issue](https://github.com/malvavisc0/enhancedtoolkits/issues)
- 💬 [Join discussions](https://github.com/malvavisc0/enhancedtoolkits/discussions)
