#!/bin/bash

# APK Decompiler CLI - External Tools Installation Script
# Installs: apktool, jadx, aapt, adb

set -e

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Log functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Get OS type
detect_os() {
    case "$(uname -s)" in
        Linux*)     echo "Linux";;
        Darwin*)    echo "macOS";;
        CYGWIN*)    echo "Windows";;
        MINGW*)     echo "Windows";;
        MSYS*)      echo "Windows";;
        *)          echo "Unknown";;
    esac
}

# Create tools directory
TOOLS_DIR="$HOME/.local/bin"
if [[ "$OS" == "Windows" ]]; then
    TOOLS_DIR="$APPDATA\\apk-decompiler\\bin"
fi

mkdir -p "$TOOLS_DIR"

log_info "Installing external tools to $TOOLS_DIR"

# Install apktool
install_apktool() {
    log_info "Installing apktool..."
    
    if command_exists apktool; then
        log_warning "apktool already installed"
        return 0
    fi
    
    OS=$(detect_os)
    
    case $OS in
        Linux)
            wget -q https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/linux/apktool -O "$TOOLS_DIR/apktool"
            wget -q https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.8.1.jar -O "$TOOLS_DIR/apktool.jar"
            ;;
        macOS)
            if command_exists brew; then
                brew install apktool
                return 0
            else
                curl -L https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/osx/apktool -o "$TOOLS_DIR/apktool"
                curl -L https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.8.1.jar -O "$TOOLS_DIR/apktool.jar"
            fi
            ;;
        Windows)
            curl -L https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/windows/apktool.bat -o "$TOOLS_DIR/apktool.bat"
            curl -L https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.8.1.jar -O "$TOOLS_DIR/apktool.jar"
            ;;
    esac
    
    chmod +x "$TOOLS_DIR/apktool"
    log_success "apktool installed"
}

# Install jadx
install_jadx() {
    log_info "Installing jadx..."
    
    if command_exists jadx; then
        log_warning "jadx already installed"
        return 0
    fi
    
    # Download latest jadx release
    JADX_VERSION=$(curl -s https://api.github.com/repos/skylot/jadx/releases/latest | grep -o '"tag_name": "v[^"]*"' | cut -d'"' -f4)
    
    if [[ -z "$JADX_VERSION" ]]; then
        log_error "Could not fetch latest jadx version"
        return 1
    fi
    
    OS=$(detect_os)
    
    case $OS in
        Linux)
            wget -q "https://github.com/skylot/jadx/releases/latest/download/jadx-$JADX_VERSION.zip" -O /tmp/jadx.zip
            unzip -q /tmp/jadx.zip -d /tmp/jadx
            mv "/tmp/jadx/bin/jadx" "$TOOLS_DIR/jadx"
            rm -rf /tmp/jadx /tmp/jadx.zip
            ;;
        macOS)
            curl -L "https://github.com/skylot/jadx/releases/latest/download/jadx-$JADX_VERSION.zip" -o /tmp/jadx.zip
            unzip -q /tmp/jadx.zip -d /tmp/jadx
            mv "/tmp/jadx/bin/jadx" "$TOOLS_DIR/jadx"
            rm -rf /tmp/jadx /tmp/jadx.zip
            ;;
        Windows)
            curl -L "https://github.com/skylot/jadx/releases/latest/download/jadx-$JADX_VERSION.zip" -o /tmp/jadx.zip
            unzip -q /tmp/jadx.zip -d /tmp/jadx
            mv "/tmp/jadx/bin/jadx.bat" "$TOOLS_DIR/jadx.bat"
            rm -rf /tmp/jadx /tmp/jadx.zip
            ;;
    esac
    
    chmod +x "$TOOLS_DIR/jadx"
    log_success "jadx installed"
}

# Install Android SDK tools (aapt, adb)
install_android_tools() {
    log_info "Installing Android SDK tools..."
    
    # Check if already installed via Android SDK
    if command_exists aapt && command_exists adb; then
        log_warning "Android SDK tools already installed"
        return 0
    fi
    
    # Check if ANDROID_HOME is set
    if [[ -n "$ANDROID_HOME" ]]; then
        if [[ -f "$ANDROID_HOME/build-tools/*/aapt" ]]; then
            log_info "Found aapt in ANDROID_HOME: $ANDROID_HOME"
            return 0
        fi
    fi
    
    # Install command line tools
    OS=$(detect_os)
    SDK_DIR="$HOME/android-sdk"
    
    if [[ "$OS" == "Windows" ]]; then
        SDK_DIR="$APPDATA\\android-sdk"
    fi
    
    mkdir -p "$SDK_DIR"
    cd "$SDK_DIR"
    
    case $OS in
        Linux)
            wget -q https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip -O cmdline-tools.zip
            unzip -q cmdline-tools.zip
            mkdir -p latest
            mv cmdline-tools/* latest/
            rm cmdline-tools.zip
            ;;
        macOS)
            curl -L https://dl.google.com/android/repository/commandlinetools-mac-9477386_latest.zip -o cmdline-tools.zip
            unzip -q cmdline-tools.zip
            mkdir -p latest
            mv cmdline-tools/* latest/
            rm cmdline-tools.zip
            ;;
        Windows)
            curl -L https://dl.google.com/android/repository/commandlinetools-win-9477386_latest.zip -o cmdline-tools.zip
            unzip -q cmdline-tools.zip
            mkdir -p latest
            mv cmdline-tools/* latest/
            rm cmdline-tools.zip
            ;;
    esac
    
    # Set environment variables
    export ANDROID_HOME="$SDK_DIR"
    export PATH="$PATH:$SDK_DIR/latest/bin:$SDK_DIR/platform-tools"
    
    # Install platform tools
    yes | sdkmanager --sdk_root="$SDK_DIR" "platform-tools" "build-tools;34.0.0"
    
    # Create symlinks
    ln -sf "$SDK_DIR/platform-tools/adb" "$TOOLS_DIR/adb" 2>/dev/null || true
    
    log_success "Android SDK tools installed"
}

# Main installation function
main() {
    log_info "Starting external tools installation..."
    
    # Check prerequisites
    if ! command_exists java; then
        log_error "Java is required but not installed. Please install Java 11 or later."
        exit 1
    fi
    
    if ! command_exists wget && ! command_exists curl; then
        log_error "Either wget or curl is required for downloading tools."
        exit 1
    fi
    
    # Install tools
    install_apktool
    install_jadx
    install_android_tools
    
    # Add to PATH
    if [[ ":$PATH:" != *":$TOOLS_DIR:"* ]]; then
        log_warning "Please add $TOOLS_DIR to your PATH environment variable"
        log_warning "Add this line to your ~/.bashrc, ~/.zshrc, or ~/.profile:"
        echo "export PATH=\"\$PATH:$TOOLS_DIR\""
    fi
    
    log_success "All external tools installed successfully!"
    log_info "Please restart your terminal or run 'source ~/.bashrc' to update PATH"
}

# Run main function
main "$@"