# APK Decompiler CLI

A comprehensive command-line tool for decompiling APK files using multiple decompilation engines including apktool, jadx, aapt, and adb.

## Features

- **Multiple Decompilers**: Support for apktool, jadx, and aapt
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Easy Setup**: Automated installation scripts for all dependencies
- **Flexible Configuration**: Environment-based configuration
- **Batch Processing**: Process multiple APKs efficiently
- **Clean Output**: Organized decompilation results

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Usage](#usage)
- [Development](#development)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## Prerequisites

### System Requirements

- **Operating System**: Windows 10+, macOS 10.15+, or Linux (Ubuntu 18.04+)
- **Python**: 3.9 or later
- **Java**: 11 or later
- **Memory**: At least 4GB RAM (8GB recommended)
- **Storage**: 2GB free space for tools and outputs

### Required External Tools

1. **apktool** - APK decompilation and reconstruction
2. **jadx** - DEX to Java decompiler
3. **aapt** - Android Asset Packaging Tool
4. **adb** - Android Debug Bridge

## Installation

### Automatic Setup (Recommended)

The fastest way to get started is using our automated setup script:

```bash
git clone <repository-url>
cd apk-decompiler-cli
bash scripts/quick-setup.sh
```

Or if you have Make available:

```bash
make setup
```

### Manual Setup

#### Step 1: Install System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install -y openjdk-11-jdk wget curl unzip git build-essential
```

**CentOS/RHEL/Fedora:**
```bash
sudo yum install -y java-11-openjdk-devel wget curl unzip git gcc
# or for newer versions:
sudo dnf install -y java-11-openjdk wget curl unzip git gcc
```

**macOS:**
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install openjdk@11 wget curl git
```

**Windows:**
1. Install [Python 3.9+](https://www.python.org/downloads/)
2. Install [Java 11+](https://adoptopenjdk.net/) or [Oracle Java](https://www.oracle.com/java/technologies/javase-downloads.html)
3. Install [Git for Windows](https://git-scm.com/download/win)
4. Install [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install) (recommended)

#### Step 2: Install Python Dependencies

```bash
# Create virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# For development setup
pip install -e .[dev]
```

#### Step 3: Install External Tools

```bash
# Using Make
make install-tools

# Or using the installation script
bash scripts/install-tools.sh
```

#### Step 4: Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit configuration as needed
nano .env  # or your preferred editor
```

#### Step 5: Verify Installation

```bash
# Verify all dependencies
make verify-deps

# Or run comprehensive validation
make validate-environment
```

### Docker Setup (Alternative)

```bash
# Build and run with Docker
docker build -t apk-decompiler-cli .
docker run -it -v $(pwd)/output:/app/output apk-decompiler-cli

# Or use docker-compose
docker-compose up --build
```

## Quick Start

### Basic Usage

```bash
# Show help
apk-decompiler --help

# Decompile a single APK
apk-decompiler decompile app.apk

# Decompile with specific tool
apk-decompiler decompile app.apk --tool jadx

# Decompile multiple APKs
apk-decompiler decompile *.apk --output-dir ./output

# Batch process with parallel execution
apk-decompiler batch-process ./apks/ --workers 4
```

### Configuration

Edit the `.env` file to customize behavior:

```bash
# Output configuration
OUTPUT_DIR=./decompiled
TEMP_DIR=./temp
KEEP_TEMP_FILES=false

# Tool configuration
JADX_MAX_MEMORY=4096
JADX_THREADS=4
APKTOOL_USE_FRAMEWORK=
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Enable debug mode | `false` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `OUTPUT_DIR` | Output directory | `./decompiled` |
| `TEMP_DIR` | Temporary files directory | `./temp` |
| `KEEP_TEMP_FILES` | Keep temporary files | `false` |
| `JADX_MAX_MEMORY` | JADX max memory (MB) | `4096` |
| `JADX_THREADS` | JADX parallel threads | `4` |
| `APKTOOL_PATH` | Custom apktool path | (empty) |
| `JADX_PATH` | Custom jadx path | (empty) |
| `AAPT_PATH` | Custom aapt path | (empty) |
| `ADB_PATH` | Custom adb path | (empty) |

### File Structure

```
apk-decompiler-cli/
├── src/                    # Source code
├── tests/                  # Test files
│   ├── unit/              # Unit tests
│   └── integration/       # Integration tests
├── scripts/               # Setup and utility scripts
├── decompiled/            # Decompilation output
├── temp/                  # Temporary files
├── cache/                 # Cache directory
├── logs/                  # Log files
├── requirements.txt       # Python dependencies
├── pyproject.toml         # Project configuration
├── .env.example          # Environment template
├── .gitignore            # Git ignore rules
├── Makefile              # Build and task automation
└── README.md             # This file
```

## Usage

### Command Line Interface

```bash
# Main commands
apk-decompiler decompile [OPTIONS] APK_FILE
apk-decompiler batch-process [OPTIONS] DIRECTORY
apk-decompiler info [OPTIONS] APK_FILE
apk-decompiler tools [OPTIONS]

# Decompile options
--tool {apktool,jadx,aapt}  # Specify decompilation tool
--output-dir PATH            # Output directory
--keep-temp                  # Keep temporary files
--parallel                   # Use parallel processing
--workers COUNT              # Number of worker processes

# Batch processing options
--recursive                  # Process subdirectories
--file-pattern PATTERN       # File pattern to match
--exclude-pattern PATTERN    # Files to exclude
```

### Python API

```python
from apk_decompiler import Decompiler

# Initialize decompiler
decompiler = Decompiler()

# Decompile single APK
result = decompiler.decompile('app.apk', tool='jadx')

# Batch process
results = decompiler.batch_process('./apks/', workers=4)

# Get APK information
info = decompiler.get_apk_info('app.apk')
```

## Development

### Setting up Development Environment

```bash
# Clone repository
git clone <repository-url>
cd apk-decompiler-cli

# Setup development environment
make setup-dev

# Install pre-commit hooks
pre-commit install
```

### Development Commands

```bash
# Run tests
make test
make test-unit
make test-integration

# Code quality
make lint          # Run linting
make format        # Format code
make type-check    # Type checking

# All checks
make check

# Update tools
make update-tools
```

### Project Structure

```
src/
└── apk_decompiler/
    ├── __init__.py
    ├── cli.py          # Command-line interface
    ├── core/           # Core functionality
    ├── tools/          # External tool wrappers
    ├── utils/          # Utility functions
    └── config/         # Configuration management
```

### Testing

```bash
# Run all tests
make test

# Run specific test categories
pytest tests/unit/          # Unit tests
pytest tests/integration/   # Integration tests

# Run with coverage
pytest --cov=apk_decompiler tests/
```

## Troubleshooting

### Common Issues

#### Python Version Issues

**Problem**: "Python 3.9+ required"

**Solution**:
```bash
# Check Python version
python3 --version

# Install Python 3.9+ if needed (Ubuntu/Debian)
sudo apt install python3.9

# Or use deadsnakes PPA for older Ubuntu versions
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.9
```

#### Java Issues

**Problem**: "Java is not installed" or "Java version too old"

**Solution**:
```bash
# Check Java version
java -version

# Ubuntu/Debian
sudo apt install openjdk-11-jdk

# macOS
brew install openjdk@11

# Windows - download from Oracle or use chocolatey
choco install openjdk11
```

#### External Tools Not Found

**Problem**: "apktool not found" or "jadx not found"

**Solution**:
```bash
# Reinstall external tools
make install-tools

# Or manually add to PATH
export PATH="$PATH:$HOME/.local/bin"

# Verify installation
make verify-deps
```

#### Permission Issues

**Problem**: "Permission denied" when running scripts

**Solution**:
```bash
# Make scripts executable
chmod +x scripts/*.sh

# For system-wide installation
sudo make install-tools
```

#### Memory Issues

**Problem**: "Out of memory" during decompilation

**Solution**:
```bash
# Adjust JADX memory limit in .env
JADX_MAX_MEMORY=8192  # Increase to 8GB

# Reduce parallel workers
apk-decompiler batch-process ./apks/ --workers 2
```

#### Network/Firewall Issues

**Problem**: "Failed to download tools" during installation

**Solution**:
```bash
# Use proxy if behind firewall
export HTTP_PROXY=http://proxy:port
export HTTPS_PROXY=http://proxy:port

# Download tools manually
# See scripts/install-tools.sh for download URLs
```

### Diagnostic Commands

```bash
# Generate environment report
make validate-environment

# Check specific tool versions
apktool --version
jadx --help
aapt version
adb --version

# Test Python environment
python3 -c "import yaml, click, tqdm; print('All dependencies OK')"

# Check file permissions
ls -la scripts/*.sh
```

### Getting Help

1. Check the [issues page](https://github.com/example/apk-decompiler-cli/issues)
2. Run `make validate-environment` and include the output
3. Check logs in the `logs/` directory
4. Enable debug mode by setting `DEBUG=true` in `.env`

## Platform-Specific Notes

### Linux

- Most dependencies available via package manager
- Use `apt` (Ubuntu/Debian) or `yum` (CentOS/RHEL)
- Ensure Java is properly configured:
  ```bash
  update-alternatives --config java
  export JAVA_HOME=/path/to/java
  ```

### macOS

- Install [Homebrew](https://brew.sh/) for easy dependency management
- Use `brew install` for most dependencies
- Java can be installed via Homebrew or downloaded from Oracle

### Windows

- Consider using [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/) for easier setup
- Use [Chocolatey](https://chocolatey.org/) for package management:
  ```powershell
  choco install python openjdk11 git
  ```
- Ensure PATH is properly configured for all tools

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Run tests: `make check`
5. Commit changes: `git commit -am 'Add feature'`
6. Push to branch: `git push origin feature-name`
7. Create Pull Request

### Code Style

- Follow PEP 8 for Python code
- Use Black for code formatting: `make format`
- Use type hints where possible
- Write tests for new features
- Update documentation as needed

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [apktool](https://ibotpeaches.github.io/Apktool/) - APK decompilation
- [jadx](https://github.com/skylot/jadx) - DEX to Java decompiler
- Android SDK tools for APK analysis
- Python ecosystem for excellent CLI framework tools