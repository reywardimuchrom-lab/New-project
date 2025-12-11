#!/bin/bash

# APK Decompiler CLI - Tools Verification Script
# Checks for all required external tools and their versions

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

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Track overall status
all_ok=true

print_header "APK Decompiler CLI - Dependency Check"

# ============================================================================
# Python Check
# ============================================================================
print_header "Python Installation"

if command_exists python3; then
    version=$(python3 --version 2>&1 | awk '{print $2}')
    major=$(echo "$version" | cut -d. -f1)
    minor=$(echo "$version" | cut -d. -f2)
    
    if [ "$major" -gt 3 ] || ([ "$major" -eq 3 ] && [ "$minor" -ge 9 ]); then
        print_success "Python 3.9+ found: $version"
    else
        print_error "Python 3.9+ required, found: $version"
        all_ok=false
    fi
else
    print_error "Python 3 not found"
    all_ok=false
fi

# ============================================================================
# Java Check (Required for apktool and jadx)
# ============================================================================
print_header "Java Installation"

if command_exists java; then
    version=$(java -version 2>&1 | head -1)
    print_success "Java found: $version"
else
    print_error "Java not found (required for apktool and jadx)"
    all_ok=false
fi

# ============================================================================
# APKTool Check
# ============================================================================
print_header "APKTool Installation"

if command_exists apktool; then
    version=$(apktool --version 2>&1 | head -1)
    print_success "apktool found: $version"
else
    print_error "apktool not found"
    print_warning "Install with: sudo apt-get install apktool (Linux) or brew install apktool (macOS)"
    all_ok=false
fi

# ============================================================================
# JADX Check
# ============================================================================
print_header "JADX Installation"

if command_exists jadx; then
    print_success "jadx found in PATH"
    jadx --version 2>/dev/null || echo "  (version info unavailable)"
else
    print_error "jadx not found"
    print_warning "Install from: https://github.com/skylot/jadx"
    all_ok=false
fi

# ============================================================================
# AAPT Check
# ============================================================================
print_header "AAPT Installation"

if command_exists aapt; then
    print_success "aapt found in PATH"
else
    print_warning "aapt not found (optional, part of Android SDK)"
    print_warning "Install from: https://developer.android.com/studio/command-line"
fi

# ============================================================================
# ADB Check
# ============================================================================
print_header "ADB Installation"

if command_exists adb; then
    version=$(adb version 2>&1 | head -1)
    print_success "adb found: $version"
else
    print_warning "adb not found (optional, part of Android SDK)"
    print_warning "Install from: https://developer.android.com/studio/command-line"
fi

# ============================================================================
# Python Dependencies Check
# ============================================================================
print_header "Python Dependencies"

if [ -f "requirements.txt" ]; then
    missing_deps=0
    
    # Check critical dependencies
    python3 -c "import click" 2>/dev/null && print_success "click" || {
        print_error "click"
        missing_deps=$((missing_deps + 1))
    }
    
    python3 -c "import pydantic" 2>/dev/null && print_success "pydantic" || {
        print_error "pydantic"
        missing_deps=$((missing_deps + 1))
    }
    
    python3 -c "import androguard" 2>/dev/null && print_success "androguard" || {
        print_error "androguard"
        missing_deps=$((missing_deps + 1))
    }
    
    if [ $missing_deps -gt 0 ]; then
        print_warning "$missing_deps Python dependencies missing"
        print_warning "Install with: pip install -r requirements.txt"
        all_ok=false
    else
        print_success "All critical Python dependencies installed"
    fi
else
    print_warning "requirements.txt not found"
fi

# ============================================================================
# Summary
# ============================================================================
echo ""
if [ "$all_ok" = true ]; then
    print_success "All critical dependencies are installed!"
    echo ""
    echo "Environment is ready for development."
    exit 0
else
    print_error "Some dependencies are missing or incorrect versions"
    echo ""
    echo "Please follow the installation guide in SETUP.md"
    exit 1
fi
