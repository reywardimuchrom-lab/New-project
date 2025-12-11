#!/bin/bash

# APK Decompiler CLI - External Tools Installation Script
# Supports: Linux, macOS, Windows (WSL)

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Utility functions
print_header() {
    echo -e "\n${BLUE}>>> $1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Detect OS
detect_os() {
    case "$(uname -s)" in
        Linux*)
            if [ -f /etc/os-release ]; then
                . /etc/os-release
                echo "$ID"
            else
                echo "linux"
            fi
            ;;
        Darwin*)
            echo "macos"
            ;;
        MINGW*|MSYS*|CYGWIN*)
            echo "windows"
            ;;
        *)
            echo "unknown"
            ;;
    esac
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

OS=$(detect_os)
print_header "Detected OS: $OS"

# ============================================================================
# Java Installation Check (Required for apktool and jadx)
# ============================================================================
print_header "Checking Java Installation"

if ! command_exists java; then
    print_warning "Java is not installed. Installing..."
    case "$OS" in
        ubuntu|debian)
            sudo apt-get update
            sudo apt-get install -y default-jre default-jdk
            ;;
        fedora|rhel)
            sudo dnf install -y java-latest-openjdk java-latest-openjdk-devel
            ;;
        macos)
            brew install openjdk
            ;;
        alpine)
            apk add openjdk11
            ;;
        *)
            print_error "Please install Java JDK manually for your OS"
            exit 1
            ;;
    esac
    print_success "Java installed"
else
    print_success "Java is already installed"
    java -version
fi

# ============================================================================
# APKTool Installation
# ============================================================================
print_header "Installing APKTool"

if command_exists apktool; then
    print_warning "apktool is already installed"
    apktool --version
else
    case "$OS" in
        ubuntu|debian)
            sudo apt-get update
            sudo apt-get install -y apktool
            print_success "apktool installed via apt"
            ;;
        fedora|rhel)
            sudo dnf install -y apktool
            print_success "apktool installed via dnf"
            ;;
        macos)
            if command_exists brew; then
                brew install apktool
                print_success "apktool installed via brew"
            else
                print_warning "Homebrew not found, downloading apktool manually..."
                mkdir -p ~/.local/bin
                curl -L https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.9.3.jar -o ~/.local/bin/apktool.jar
                cat > ~/.local/bin/apktool << 'EOF'
#!/bin/bash
java -jar ~/.local/bin/apktool.jar "$@"
EOF
                chmod +x ~/.local/bin/apktool
                export PATH="$HOME/.local/bin:$PATH"
                print_success "apktool installed manually"
            fi
            ;;
        alpine)
            apk add apktool
            print_success "apktool installed via apk"
            ;;
        *)
            print_error "Unsupported OS for automated apktool installation. Please install manually."
            exit 1
            ;;
    esac
fi

# ============================================================================
# JADX Installation
# ============================================================================
print_header "Installing JADX"

if command_exists jadx; then
    print_warning "jadx is already installed"
    jadx --version 2>/dev/null || echo "jadx found in PATH"
else
    case "$OS" in
        ubuntu|debian|fedora|rhel)
            print_warning "Installing jadx from source..."
            mkdir -p ~/.local/bin
            JADX_VERSION="1.4.7"
            JADX_URL="https://github.com/skylot/jadx/releases/download/v${JADX_VERSION}/jadx-${JADX_VERSION}.zip"
            
            cd ~/.local/bin
            curl -L "$JADX_URL" -o jadx.zip
            unzip -o jadx.zip
            rm jadx.zip
            chmod +x jadx/bin/jadx
            
            export PATH="$HOME/.local/bin/jadx/bin:$PATH"
            print_success "jadx installed manually"
            ;;
        macos)
            if command_exists brew; then
                brew install jadx
                print_success "jadx installed via brew"
            else
                mkdir -p ~/.local/bin
                JADX_VERSION="1.4.7"
                JADX_URL="https://github.com/skylot/jadx/releases/download/v${JADX_VERSION}/jadx-${JADX_VERSION}.zip"
                
                cd ~/.local/bin
                curl -L "$JADX_URL" -o jadx.zip
                unzip -o jadx.zip
                rm jadx.zip
                chmod +x jadx/bin/jadx
                
                export PATH="$HOME/.local/bin/jadx/bin:$PATH"
                print_success "jadx installed manually"
            fi
            ;;
        alpine)
            apk add jadx
            print_success "jadx installed via apk"
            ;;
        *)
            print_warning "Unsupported OS for automated jadx installation"
            ;;
    esac
fi

# ============================================================================
# Android SDK Tools Installation (aapt, adb)
# ============================================================================
print_header "Installing Android SDK Tools"

if command_exists aapt && command_exists adb; then
    print_warning "Android SDK tools are already installed"
else
    case "$OS" in
        ubuntu|debian)
            sudo apt-get update
            sudo apt-get install -y android-sdk-platform-tools android-sdk
            print_success "Android SDK tools installed via apt"
            ;;
        fedora|rhel)
            sudo dnf install -y android-tools
            print_success "Android tools installed via dnf"
            ;;
        macos)
            if command_exists brew; then
                brew install android-sdk android-platform-tools
                print_success "Android SDK tools installed via brew"
            else
                print_warning "Please install Android SDK manually from https://developer.android.com/studio"
            fi
            ;;
        alpine)
            apk add android-tools
            print_success "Android tools installed via apk"
            ;;
        *)
            print_warning "Unsupported OS for automated Android SDK installation"
            print_warning "Please install from: https://developer.android.com/studio/command-line"
            ;;
    esac
fi

# ============================================================================
# Final verification
# ============================================================================
print_header "Verifying installations"

echo ""
echo "Required tools:"
for tool in java apktool jadx aapt adb; do
    if command_exists "$tool"; then
        print_success "$tool"
    else
        print_warning "$tool (not found in PATH, may need manual installation)"
    fi
done

echo ""
print_success "External tools installation completed!"
echo ""
echo "If any tools are missing, please install them manually:"
echo "  - Java: https://www.oracle.com/java/technologies/downloads/"
echo "  - APKTool: https://ibotpeaches.github.io/Apktool/install/"
echo "  - JADX: https://github.com/skylot/jadx"
echo "  - Android SDK: https://developer.android.com/studio/command-line"
echo ""
