# Quick Start Guide

Get APK Decompiler CLI up and running in minutes.

## TL;DR - One-Line Setup

```bash
# Linux/macOS with all prerequisites pre-installed
make setup
```

## Prerequisites Check

```bash
# Verify you have Python 3.9+
python3 --version

# Check if Java is installed
java -version
```

## 3-Step Setup

### Step 1: Clone and Enter Repository
```bash
git clone <repository-url>
cd apk-decompiler-cli
```

### Step 2: Create Virtual Environment (Recommended)
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Run Setup
```bash
make setup
```

This single command will:
- ✓ Install Python dependencies
- ✓ Install external tools
- ✓ Verify all installations

## Verify Installation

```bash
# Run the verification script
make check-tools

# Or use Python version (works on Windows)
python3 scripts/check_tools.py
```

## First Use

```bash
# Show available commands
python -m apk_decompiler --help

# Decompile an APK (when CLI is fully implemented)
python -m apk_decompiler decompile app.apk --output ./output
```

## Common Issues

### "Python not found"
```bash
# Install Python 3.9+
# Ubuntu/Debian: sudo apt-get install python3.9
# macOS: brew install python@3.9
# Windows: Download from python.org
```

### "Java not found"
```bash
# Install Java JDK
# Ubuntu/Debian: sudo apt-get install default-jre default-jdk
# macOS: brew install openjdk
# Windows: Download from https://www.oracle.com/java/technologies/downloads/
```

### "apktool/jadx not found"
```bash
# The install_tools script will handle this:
bash scripts/install_tools.sh
```

### Virtual Environment Issues
```bash
# Recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
```

## Development

```bash
# Format code
make format

# Run tests
make test

# Check code quality
make lint
```

## Need Help?

- **Setup Issues**: See [SETUP.md](SETUP.md)
- **Development**: See [CONTRIBUTING.md](CONTRIBUTING.md)
- **Full Documentation**: See [README.md](README.md)

## File Structure Reference

```
apk-decompiler-cli/
├── apk_decompiler/     # Main package
├── tests/              # Tests
├── scripts/            # Setup scripts
├── Makefile            # Commands
├── requirements.txt    # Python dependencies
├── pyproject.toml      # Project config
├── setup.py            # Package setup
└── SETUP.md           # Detailed setup guide
```

## System Requirements Summary

| Requirement | Minimum | Recommended |
|---|---|---|
| Python | 3.9 | 3.9+ |
| Java | JDK 8 | JDK 11+ |
| RAM | 2GB | 4GB+ |
| Disk Space | 500MB | 1GB+ |

## Network Requirements

During setup, you'll need internet access to:
- Download Python packages (pip install)
- Download external tools (apktool, jadx)
- Download Android SDK tools

Once installed, the CLI doesn't require internet for normal operation.

---

**Now you're ready! Happy decompiling!** 🚀

See [SETUP.md](SETUP.md) for detailed instructions for your OS.
