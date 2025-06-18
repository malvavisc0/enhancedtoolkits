# Installation Guide

## Prerequisites

- Python 3.8 or higher
- pip package manager
- Git (for GitHub installation)

## Installation Methods

### 1. Install from GitHub (Recommended)

```bash
# Basic installation with core dependencies
pip install git+https://github.com/malvavisc0/enhancedtoolkits.git

# Install with all optional features
pip install "enhancedtoolkits[full] @ git+https://github.com/malvavisc0/enhancedtoolkits.git"

# Install with specific features
pip install "enhancedtoolkits[youtube] @ git+https://github.com/malvavisc0/enhancedtoolkits.git"
pip install "enhancedtoolkits[content] @ git+https://github.com/malvavisc0/enhancedtoolkits.git"
```

### 2. Development Installation

```bash
# Clone the repository
git clone https://github.com/malvavisc0/enhancedtoolkits.git
cd enhancedtoolkits

# Install in development mode
pip install -e .

# Install with development dependencies
pip install -e ".[dev]"
```

## Optional Dependencies

- **youtube**: Enables YouTube transcript functionality
  - `youtube-transcript-api>=0.6.0`

- **content**: Enables advanced content parsing
  - `markitdown>=0.0.1a2`

- **full**: Includes all optional dependencies

- **dev**: Development tools (testing, linting, formatting)

## Verification

After installation, verify everything works:

```python
from enhancedtoolkits import CalculatorTools, __version__
print(f"Enhanced Toolkits v{__version__} installed successfully!")

# Test basic functionality
calc = CalculatorTools()
result = calc.add(2, 3)
print(f"2 + 3 = {result}")
```

## Troubleshooting

### Common Issues

**Import Errors**: Make sure you have the Agno framework installed:

```bash
pip install agno
```

**Missing Optional Dependencies**: Install the specific extras you need:

```bash
pip install "enhancedtoolkits[youtube,content] @ git+https://github.com/malvavisc0/enhancedtoolkits.git"
```

**Version Conflicts**: Use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install git+https://github.com/malvavisc0/enhancedtoolkits.git
```

## Updating

To update to the latest version:

```bash
pip install --upgrade git+https://github.com/malvavisc0/enhancedtoolkits.git
```

## Uninstalling

```bash
pip uninstall enhancedtoolkits
```
