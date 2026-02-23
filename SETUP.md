# APK Decompiler CLI - Setup Guide

This guide will help you set up the APK Decompiler CLI tool with all required dependencies.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Verification](#verification)
4. [OS-Specific Guides](#os-specific-guides)
5. [Troubleshooting](#troubleshooting)
6. [Environment Configuration](#environment-configuration)

---

## Prerequisites

### Minimum Requirements

- **Python**: 3.9 or higher
- **Java**: JDK 8 or higher (required for apktool and jadx)
- **System RAM**: At least 2GB available
- **Disk Space**: At least 500MB for tools and dependencies

### External Tools Required

1. **Java Development Kit (JDK)** - 8+
2. **APKTool** - For decompiling APK files to resources and source
3. **JADX** - For decompiling DEX/APK files to Java source code
4. **AAPT** (Android Asset Packaging Tool) - For parsing Android resources
5. **ADB** (Android Debug Bridge) - For interacting with Android devices
6. **Git** - For version control

---

## Installation

### Quick Setup (Recommended)

The fastest way to set up the entire environment is to use the provided setup command:

```bash
# Clone the repository (if not already done)
git clone <repository-url>
cd apk-decompiler-cli

# Run the complete setup
make setup
```

This command will:
1. Verify Python 3.9+ is installed
2. Create a virtual environment (optional)
3. Install Python dependencies
4. Install external tools
5. Verify all installations

### Step-by-Step Manual Installation

#### Step 1: Clone and Enter the Repository

```bash
git clone <repository-url>
cd apk-decompiler-cli
```

#### Step 2: Create a Virtual Environment (Optional but Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

#### Step 3: Install Python Dependencies

```bash
# Install required packages
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# For development:
pip install -e ".[dev]"
```

#### Step 4: Install External Tools

```bash
# Linux/macOS:
bash scripts/install_tools.sh

# Windows (WSL):
bash scripts/install_tools.sh
```

#### Step 5: Verify Installation

```bash
bash scripts/check_tools.sh
```

---

## Verification

After installation, verify everything is working correctly:

### Quick Check

```bash
# Check all tools
make check-tools

# Check Python version
make check-python
```

### Individual Tool Checks

```bash
# Python
python3 --version  # Should be 3.9+

# Java
java -version     # Should be 8+

# APKTool
apktool --version

# JADX
jadx --version

# ADB
adb version

# AAPT
aapt version
```

---

## OS-Specific Guides

### Linux (Ubuntu/Debian)

#### Prerequisites

```bash
sudo apt-get update
sudo apt-get install -y \
    python3.9 \
    python3.9-venv \
    python3.9-dev \
    git \
    curl \
    unzip \
    build-essential
```

#### Installation

```bash
# Option 1: Automated
make setup

# Option 2: Manual
sudo apt-get install -y \
    default-jre \
    default-jdk \
    apktool \
    android-sdk \
    android-sdk-platform-tools

# Install Python dependencies
pip install -r requirements.txt

# Install JADX (if not available in repositories)
bash scripts/install_tools.sh
```

#### Verify

```bash
bash scripts/check_tools.sh
```

### Linux (Fedora/RHEL)

#### Prerequisites

```bash
sudo dnf install -y \
    python3 \
    python3-devel \
    git \
    curl \
    unzip
```

#### Installation

```bash
# Automated setup
make setup

# Or manual installation
sudo dnf install -y \
    java-latest-openjdk \
    java-latest-openjdk-devel \
    apktool \
    android-tools

# Install Python dependencies
pip install -r requirements.txt
```

#### Verify

```bash
bash scripts/check_tools.sh
```

### macOS

#### Prerequisites

Ensure you have Homebrew installed. If not:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### Installation

```bash
# Update Homebrew
brew update

# Install tools
brew install \
    python@3.9 \
    openjdk \
    apktool \
    jadx \
    android-sdk \
    android-platform-tools

# Create virtual environment
python3.9 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

#### Verify

```bash
bash scripts/check_tools.sh
```

#### Troubleshooting Java on macOS

If Java is installed but not found:

```bash
# Find Java installation
/usr/libexec/java_home

# Add to PATH if needed
export JAVA_HOME=$(/usr/libexec/java_home)
echo 'export JAVA_HOME=$(/usr/libexec/java_home)' >> ~/.zprofile
```

### Windows

**Note**: Native Windows installation is complex. We recommend using Windows Subsystem for Linux (WSL).

#### Using WSL (Recommended)

1. Install WSL2:
   ```bash
   wsl --install
   ```

2. Install Ubuntu from Microsoft Store

3. Follow the Ubuntu/Debian instructions above

#### Native Windows (Alternative)

1. **Install Python 3.9+**
   - Download from https://www.python.org/downloads/
   - Add to PATH during installation

2. **Install Java JDK**
   - Download from https://www.oracle.com/java/technologies/downloads/
   - Set JAVA_HOME environment variable

3. **Install Git**
   - Download from https://git-scm.com/download/win

4. **Install APKTool**
   - Download from https://ibotpeaches.github.io/Apktool/install/
   - Add to PATH

5. **Install JADX**
   - Download from https://github.com/skylot/jadx/releases
   - Add to PATH

6. **Install Android SDK**
   - Download Android Studio from https://developer.android.com/studio
   - Install platform-tools

7. **Install Python Dependencies**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

8. **Verify**
   ```bash
   python scripts\check_tools.py  # Python version if bash not available
   ```

---

## Troubleshooting

### Common Issues and Solutions

#### 1. Python Not Found

**Problem**: `python3: command not found`

**Solution**:
- Linux: `sudo apt-get install python3.9`
- macOS: `brew install python@3.9`
- Windows: Download from https://www.python.org/downloads/

#### 2. Python Version Check Failed

**Problem**: Python installed but version is below 3.9

**Solution**:
```bash
# Check current version
python3 --version

# Update/upgrade Python
# Ubuntu/Debian:
sudo apt-get install python3.9

# macOS:
brew install python@3.9
brew link python@3.9 --force

# Windows:
Download Python 3.9+ from python.org
```

#### 3. Java Not Found

**Problem**: `java: command not found`

**Solution**:
```bash
# Linux:
sudo apt-get install default-jre default-jdk

# macOS:
brew install openjdk

# Windows:
Download JDK from https://www.oracle.com/java/technologies/downloads/
Add JAVA_HOME to environment variables
```

#### 4. APKTool Not Found

**Problem**: `apktool: command not found`

**Solution**:
```bash
# Linux:
sudo apt-get install apktool

# macOS:
brew install apktool

# Manual installation:
# Download from https://ibotpeaches.github.io/Apktool/install/
# Add to PATH
```

#### 5. JADX Not Found

**Problem**: `jadx: command not found`

**Solution**:
```bash
# macOS:
brew install jadx

# Linux/Manual:
# Download from https://github.com/skylot/jadx/releases
mkdir -p ~/.local/bin
unzip jadx-*.zip -d ~/.local/bin/jadx
chmod +x ~/.local/bin/jadx/bin/jadx
export PATH="$HOME/.local/bin/jadx/bin:$PATH"
```

#### 6. Android SDK Tools Not Found

**Problem**: `adb: command not found` or `aapt: command not found`

**Solution**:
```bash
# Install Android SDK
# Option 1: Using package managers
# Linux:
sudo apt-get install android-sdk android-sdk-platform-tools

# macOS:
brew install android-sdk android-platform-tools

# Option 2: Download Android Studio
# https://developer.android.com/studio
# Then add platform-tools to PATH
```

#### 7. Permission Denied on Scripts

**Problem**: `Permission denied: ./scripts/install_tools.sh`

**Solution**:
```bash
chmod +x scripts/*.sh
./scripts/install_tools.sh
```

#### 8. Pip Install Failures

**Problem**: Errors during `pip install -r requirements.txt`

**Solution**:
```bash
# Upgrade pip first
pip install --upgrade pip

# Try again with verbose output
pip install -r requirements.txt -v

# If specific package fails, try individually
pip install click
pip install pydantic
# etc.
```

#### 9. Virtual Environment Issues

**Problem**: Virtual environment not activating properly

**Solution**:
```bash
# Recreate virtual environment
rm -rf venv
python3 -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

#### 10. Virtual Environment in Makefile

**Problem**: Make commands fail due to virtual environment

**Solution**:
```bash
# Always activate venv before running make
source venv/bin/activate  # Linux/macOS
make setup
```

### Getting Help

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section above
2. Review individual tool documentation:
   - APKTool: https://ibotpeaches.github.io/Apktool/
   - JADX: https://github.com/skylot/jadx
   - Android SDK: https://developer.android.com/studio/command-line
3. Open an issue on GitHub with:
   - Your OS and version
   - Python version (`python3 --version`)
   - Output from `bash scripts/check_tools.sh`
   - Relevant error messages

---

## Environment Configuration

### Setup Environment Variables

1. **Copy the example environment file**:
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` with your configuration**:
   ```bash
   # Edit paths if tools are installed in non-standard locations
   export APKTOOL_PATH=/path/to/apktool
   export JADX_PATH=/path/to/jadx
   export ADB_PATH=/path/to/adb
   ```

3. **Load environment variables** (optional, for persistent configuration):
   ```bash
   # Add to ~/.bashrc, ~/.zshrc, or your shell config
   source /path/to/project/.env
   ```

### Configuration Options

See `.env.example` for all available configuration options:

- `OUTPUT_DIR`: Where to save decompiled files (default: `./output`)
- `TEMP_DIR`: Temporary directory for processing (default: `/tmp/apk-decompiler`)
- `LOG_LEVEL`: Logging level (default: `INFO`)
- `DEBUG`: Enable debug mode (default: `False`)
- `MAX_CONCURRENT_PROCESSES`: Number of parallel processes (default: `4`)
- `DECOMPILE_TIMEOUT`: Timeout for decompilation in seconds (default: `600`)

---

## Development Setup

For development work:

```bash
# Install with development dependencies
pip install -e ".[dev]"

# Run tests
make test

# Check code quality
make lint

# Format code
make format

# Build documentation
make docs
```

---

## Verification Checklist

After installation, verify:

- [ ] Python 3.9+ installed: `python3 --version`
- [ ] Java installed: `java -version`
- [ ] APKTool installed: `apktool --version`
- [ ] JADX installed: `jadx --version`
- [ ] ADB installed: `adb version`
- [ ] AAPT installed: `aapt version`
- [ ] Python dependencies installed: `pip list | grep -E "click|pydantic|androguard"`
- [ ] All scripts executable: `ls -l scripts/`

Run the verification script:
```bash
bash scripts/check_tools.sh
```

---

## Next Steps

1. Read the main README.md for usage instructions
2. Check out example usage in the documentation
3. Try the CLI: `python -m apk_decompiler --help`
4. For development, read CONTRIBUTING.md

---

## Support

For issues or questions:
- GitHub Issues: [Project Repository]
- Documentation: [Project Wiki]
- Stack Overflow: Tag with `apk-decompiler-cli`

Happy decompiling! 🚀
