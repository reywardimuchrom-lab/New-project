# APK Decompiler CLI

A comprehensive command-line tool for decompiling, analyzing, and extracting information from Android APK files.

## Features

- 🔧 **Multiple Decompilation Methods**: Support for APKTool and JADX for comprehensive code analysis
- 📦 **APK Analysis**: Extract and analyze APK manifest, resources, and source code
- 🎯 **Resource Extraction**: Access drawable, layout, and other resource files
- 🔍 **Code Decompilation**: Convert DEX files to readable Java source code
- 🛡️ **Security Analysis**: Identify potential security issues and suspicious patterns
- 📊 **Report Generation**: Create detailed analysis reports in JSON, XML, or HTML formats
- ⚡ **Batch Processing**: Decompile multiple APKs efficiently with parallel processing
- 🚀 **CLI Integration**: Easy command-line interface for automation and scripting

## Quick Start

### Installation

See [SETUP.md](SETUP.md) for comprehensive installation instructions for all operating systems.

**Quick setup** (requires Python 3.9+ and system prerequisites):

```bash
# Clone repository
git clone <repository-url>
cd apk-decompiler-cli

# Complete setup (Python + external tools)
make setup

# Or just Python setup
make install
```

### Basic Usage

```bash
# Show help
python -m apk_decompiler --help

# Decompile APK
python -m apk_decompiler decompile <path-to-apk>

# Analyze APK
python -m apk_decompiler analyze <path-to-apk>

# Extract resources
python -m apk_decompiler extract <path-to-apk> --output ./output
```

## Requirements

### System Requirements
- **Python**: 3.9 or higher
- **Java**: JDK 8 or higher
- **RAM**: Minimum 2GB
- **Disk Space**: Minimum 500MB for tools and dependencies
- **OS**: Linux, macOS, or Windows (WSL recommended)

### External Tools
1. **APKTool** - Decompiles APKs to resources and source
2. **JADX** - Decompiles DEX files to Java source code
3. **AAPT** - Android Asset Packaging Tool for manifest parsing
4. **ADB** - Android Debug Bridge (optional, for device integration)

## Project Structure

```
apk-decompiler-cli/
├── apk_decompiler/          # Main package
│   ├── __init__.py
│   ├── cli.py              # CLI entry point
│   ├── core/               # Core functionality
│   ├── tools/              # External tool wrappers
│   ├── models/             # Data models
│   └── utils/              # Utility functions
├── tests/                  # Test suite
├── scripts/                # Setup and utility scripts
│   ├── install_tools.sh    # External tools installation
│   └── check_tools.sh      # Dependency verification
├── Makefile                # Development commands
├── setup.py                # Python package setup
├── pyproject.toml          # Project configuration
├── requirements.txt        # Python dependencies
├── .env.example            # Environment configuration template
├── .gitignore              # Git ignore rules
├── SETUP.md                # Detailed setup guide
├── README.md               # This file
└── CONTRIBUTING.md         # Contribution guidelines
```

## Development

### Setup Development Environment

```bash
# Install development dependencies
make install-dev

# Or manually:
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
make test

# With coverage
make test
```

### Code Quality

```bash
# Run linters
make lint

# Format code
make format

# Check formatting without changes
make format-check
```

### Common Commands

```bash
# Display all available make commands
make help

# Check all dependencies
make check-tools

# Clean build artifacts
make clean

# Full cleanup (including venv)
make clean-all
```

## Configuration

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Edit `.env` to customize:
- Tool paths (if non-standard installation)
- Output directories
- Decompilation timeouts
- Logging levels
- Processing options

## Installation Guides

- **[Linux (Ubuntu/Debian)](SETUP.md#linuxubuntudebian)**
- **[Linux (Fedora/RHEL)](SETUP.md#linuxfedorarhel)**
- **[macOS](SETUP.md#macos)**
- **[Windows (WSL)](SETUP.md#windows)**

See [SETUP.md](SETUP.md) for detailed instructions for each platform, including troubleshooting.

## Documentation

- [SETUP.md](SETUP.md) - Complete setup and installation guide
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
- [API Documentation](docs/) - Full API reference

## Troubleshooting

### Common Issues

**Python not found**
```bash
# Install Python 3.9+
# Ubuntu/Debian: sudo apt-get install python3.9
# macOS: brew install python@3.9
# Windows: Download from https://www.python.org/downloads/
```

**Java not found**
```bash
# Install Java JDK
# Ubuntu/Debian: sudo apt-get install default-jre default-jdk
# macOS: brew install openjdk
# Windows: https://www.oracle.com/java/technologies/downloads/
```

**APKTool/JADX not found**
```bash
# Run the installation script
bash scripts/install_tools.sh

# Or run full setup
make setup
```

For more troubleshooting, see the [Troubleshooting section in SETUP.md](SETUP.md#troubleshooting).

## Performance

Decompilation speed depends on:
- APK file size
- Device performance
- Number of DEX files
- Selected decompilation method

Typical performance:
- Small APKs (<10MB): 10-30 seconds
- Medium APKs (10-50MB): 1-5 minutes
- Large APKs (>50MB): 5-15 minutes

## Supported Formats

### Input
- `.apk` files (Android Package files)
- Signed and unsigned APKs

### Output
- Java source code
- XML resources
- Binary resources
- DEX information
- Manifest details

### Report Formats
- JSON
- XML
- HTML
- Text

## Examples

### Basic Decompilation

```bash
python -m apk_decompiler decompile app.apk --output ./decompiled
```

### With Specific Tool

```bash
# Use only APKTool
python -m apk_decompiler decompile app.apk --tool apktool

# Use only JADX
python -m apk_decompiler decompile app.apk --tool jadx
```

### Analysis Report

```bash
python -m apk_decompiler analyze app.apk --report json --output report.json
```

### Batch Processing

```bash
python -m apk_decompiler batch-decompile ./apks/ --output ./decompiled --parallel 4
```

## Security Considerations

- Always analyze untrusted APKs in isolated environments
- Review decompiled code carefully before execution
- Use with caution when dealing with sensitive applications
- Follow all applicable laws and regulations

## License

See LICENSE file for details.

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Support

- 📖 **Documentation**: Check [SETUP.md](SETUP.md) and API docs
- 🐛 **Issues**: Report bugs on GitHub Issues
- 💬 **Discussions**: Use GitHub Discussions for questions
- 📧 **Email**: See CONTRIBUTING.md for contact information

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and updates.

## Acknowledgments

This tool builds upon and integrates:
- [APKTool](https://ibotpeaches.github.io/Apktool/) - APK decompilation
- [JADX](https://github.com/skylot/jadx) - DEX decompilation
- [Androguard](https://github.com/androguard/androguard) - Android analysis
- Android SDK Tools - Official Android development tools

## Disclaimer

This tool is for educational and authorized security testing purposes only. Users are responsible for ensuring they have proper authorization before analyzing any APK files. Unauthorized reverse engineering may violate laws and terms of service.

---

**Happy decompiling!** 🚀

For questions or issues, please refer to [SETUP.md](SETUP.md) or open an issue on GitHub.
